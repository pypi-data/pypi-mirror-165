from collections.abc import Callable
from typing import Optional, Union

import numpy as np

from osaft import log
from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.functions import clebsch_gordan_coefficient as cg
from osaft.core.functions import conj, full_range, integrate, sqrt
from osaft.core.geometries import Sphere
from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.solutions.doinikov2021viscous.scattering import ScatteringField


class StreamingField(ScatteringField):
    """Streaming field class for Doinikov (viscous fluid-elastic sphere; 2021)

    :param f: frequency [Hz]
    :param R_0: radius [m]
    :param rho_s: density of the particle [kg/m^3]
    :param E_s: Young's modulus of the particle [Pa]
    :param nu_s: Poisson's ratio of the particle [-]
    :param rho_f: density of the fluid [kg/m^3]
    :param c_f: speed of sound in the fluid [m/s]
    :param eta_f: fluid component shear viscosity [Pa s]
    :param zeta_f: fluid component bulk viscosity [Pa s]
    :param p_0: pressure amplitude [Pa]
    :param wave_type: wave type
    :param position: position in the standing wave field [m]
    :param N_max: truncation of the summation index (highest order mode)
    :param inf_factor: see :attr:`.inf_factor`
    :param inf_type: see :attr:`.inf_type`
    :param integration_rel_eps:  relative eps for adaptive integration
    """

    def __init__(
            self, f: Union[Frequency, float],
            R_0: Union[Sphere, float],
            rho_s: float, E_s: float, nu_s: float,
            rho_f: float, c_f: float,
            eta_f: float, zeta_f: float,
            p_0: float, wave_type: WaveType,
            position: Optional[float] = None,
            N_max: int = 5,
            inf_factor: float = 60.0,
            inf_type: Optional[str] = None,
            integration_rel_eps: float = 1e-3,
    ) -> None:
        """Initialize class
        """

        # __init__ parent class
        ScatteringField.__init__(
            self,
            f=f, R_0=R_0,
            rho_s=rho_s, E_s=E_s, nu_s=nu_s,
            rho_f=rho_f, c_f=c_f,
            eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position,
            N_max=N_max,
        )

        # Independent variables
        self._inf_factor = PassiveVariable(inf_factor, 'infinity factor')
        self._inf_type = PassiveVariable(
            inf_type,
            'infinity type',
        )

        self._integration_rel_eps = PassiveVariable(
            integration_rel_eps,
            'estimated integration error goal',
        )

        # Dependent variables
        self._C_0 = ActiveVariable(
            self._compute_C_0,
            'integration constants C_0',
        )

        self._inf = ActiveVariable(self._compute_inf, 'infinity')

        # Dependencies
        self._C_0.is_computed_by(
            self._inf_factor,
            self._inf_type,
            self._integration_rel_eps,
            self.fluid._rho_f,
            self.fluid._eta_f,
            self.fluid._zeta_f,
            self.fluid._k_f,
        )

        self._inf.is_computed_by(
            self._inf_type, self._inf_factor,
            self.sphere._R_0, self.fluid._delta,
        )

    # -------------------------------------------------------------------------
    # Getters and Setters for Independent Variables
    # -------------------------------------------------------------------------

    @property
    def inf_factor(self) -> float:
        """Infinity factor

        Factor that is multiplied with the length given through
        :attr:`.inf_type` to get the upper limit for integration to the
        far-field.

        :getter: returns the infinity factor
        :rtype: float
        :setter: automatically invokes
            :func:`osaft.core.variable.BaseVariable.notify`
        :type: float
        """

        return self._inf_factor.value

    @inf_factor.setter
    def inf_factor(self, value: float) -> None:
        self._inf_factor.value = value

    @property
    def inf_type(self) -> str:
        """Infinity type

        the upper limit of the integration to the far-field is defined as a
        multiple of either radius, boundary layer thickness, acoustic
        wavelength, viscous wavelength, or a user-defined value.
        The options are
        - `'delta'`
        - `'radius'`
        - `'1'` or 1
        - `None`

        The multiplier is set through
        :attr:`.inf_value`

        :getter: returns the infinity type
        :rtype: str
        :setter: automatically invokes
            :func:`osaft.core.variable.BaseVariable.notify`
        """
        return self._inf_type.value

    @inf_type.setter
    def inf_type(self, value: str) -> None:
        self._inf_type.value = value

    @property
    def integration_rel_eps(self) -> float:
        """ Relative integration error goal for adaptive integration

        Relative error goal for the computation of :attr:`.C_integral`

        :getter: returns the relative integration error
        :rtype: float
        :setter: automatically invokes
            :func:`osaft.core.variable.BaseVariable.notify`
        :type: float
        """
        return self._integration_rel_eps.value

    @integration_rel_eps.setter
    def integration_rel_eps(self, value: float) -> None:
        self._integration_rel_eps.value = value

    # -------------------------------------------------------------------------
    # Getters for dependent Variables
    # -------------------------------------------------------------------------

    @property
    def C_0(self) -> np.ndarray:
        """Container for integrals and errors :math:`C_{ml0}`

        (Eq. E5 - E7)

        Stores the integrals and the estimated errors for the integral
        :math:`C_{ml0}`
        """
        return self._C_0.value['integral']

    @property
    def C_0_error(self) -> np.ndarray:
        """Container for integrals and errors :math:`C_{ml0}`

        (Eq. E5 - E7)

        Stores the integrals and the estimated errors for the integral
        :math:`C_{ml0}`
        """
        return self._C_0.value['error']

    @property
    def inf(self):
        """Upper limit for the integration to the far-field (to infinity) [m]
        """
        return self._inf.value

    # -------------------------------------------------------------------------
    # Dependent Variables Methods
    # -------------------------------------------------------------------------

    def _integrate_C_ml0(
        self, kernel: Callable[[float], float],
    ) -> (float, float):
        return integrate(
            kernel, self.R_0, self.inf, rel_eps=self.integration_rel_eps,
        )

    @staticmethod
    def _compute_C_210(l: int, integral: float) -> float:
        return - 1 / (2 * l + 1) * integral

    def _compute_C_210_error(self, l: int, error: float) -> float:
        return self._compute_C_210(l, error)

    def _compute_C_3l0(
            self, l: int, C_2l0: float, C_5l0: float, C_6l0: float,
    ) -> float:
        term_1 = self.V_S_r(l, self.R_0, ac=False) / (l + 1)
        term_1 += self.V_S_theta(l, self.R_0, ac=False)
        term_1 *= self.R_0 ** l

        term_2 = C_2l0 / (l + 1) - C_5l0
        term_2 *= (2 * l + 1) * self.R_0 ** (2 * l - 1)

        term_3 = (2 * l + 3) * self.R_0 ** (2 * l + 1) * C_6l0

        return 0.5 * (term_1 + term_2 - term_3)

    def _compute_C_3l0_error(
            self, l: int, error_2l0: float, error_5l0: float, error_6l0: float,
    ) -> float:
        term_1 = error_2l0 / (l + 1) - error_5l0
        term_1 *= (2 * l + 1) * self.R_0 ** (2 * l - 1)
        term_2 = - (2 * l + 3) * self.R_0 ** (2 * l + 1) * error_6l0
        return 0.5 * term_1 - term_2

    def _compute_C_4l0(
            self, l: int, C_2l0: float, C_5l0: float, C_6l0: float,
    ) -> float:
        term_1 = (2 - l) * self.V_S_r(l, self.R_0, False) / (l * (l + 1))
        term_1 -= self.V_S_theta(l, self.R_0, ac=False)
        term_1 *= self.R_0 ** (l + 2)

        term_2 = C_2l0 / (l + 1) - C_5l0
        term_2 *= (2 * l - 1) * self.R_0 ** (2 * l + 1)

        term_3 = + (2 * l + 1) * self.R_0 ** (2 * l + 3) * C_6l0

        return 0.5 * (term_1 - term_2 + term_3)

    def _compute_C4l0_error(
            self, l: int, error_2l0: float, error_5l0: float,
            error_6l0: float,
    ) -> float:
        term_1 = (2 * l - 1) * self.R_0 ** (2 * l + 1)
        term_1 *= error_2l0 / (l + 1) - error_5l0

        term_2 = (2 * l + 1) * self.R_0 ** (2 * l + 3) * error_6l0

        return 0.5 * (-term_1 + term_2)

    @staticmethod
    def _compute_C_5l0(l: int, integral: float) -> float:
        return 1 / (2 * (2 * l - 1) * (2 * l + 1)) * integral

    def _compute_C_5l0_error(self, l: int, error: float) -> float:
        return self._compute_C_5l0(l, error)

    @staticmethod
    def _compute_C_6l0(l: int, integral: float) -> float:
        return - 1 / (2 * (2 * l + 1) * (2 * l + 3)) * integral

    def _compute_C_6l0_error(self, l: int, error: float) -> float:
        return self._compute_C_6l0(l, error)

    def _compute_C_0(self, L_max: Optional[int] = None) -> dict:
        """Computes the integrals :math:`C_{ml0}` for :math:`l` up to `L_max`

        :param L_max: max index of summation
        :return: dictionary with integrals and errors
        """
        if L_max is None:
            l_range = self.range_1_N_max
        else:
            l_range = full_range(1, L_max)

        integrals = np.zeros((6 + 1, self.N_max + 1))
        errors = np.zeros((6 + 1, self.N_max + 1))

        log.info(
            'Integration to compute C_ml0 is performed. This might take '
            'a while.',
        )

        for l in l_range:

            def kernel_C_2l0(s: float) -> float:
                alpha = self.alpha(l, s, ac=False)
                alpha_incident = self.alpha(l, s, ac=True)
                return s ** (1 - l) * (alpha - alpha_incident)

            def kernel_C_5l0(s: float) -> float:
                E = self.E(l, s, ac=False)
                E_incident = self.E(l, s, ac=True)
                return s ** (3 - l) * (E - E_incident)

            def kernel_C_6l0(s: float) -> float:
                E = self.E(l, s, ac=False)
                E_incident = self.E(l, s, ac=True)
                return s ** (1 - l) * (E - E_incident)

            # C_1l0
            integrals[1, l] = 0
            errors[1, l] = 0

            # C_2l0
            integral_C_2l0, error_C_2l0 = self._integrate_C_ml0(kernel_C_2l0)
            integrals[2, l] = self._compute_C_210(l, integral_C_2l0)
            errors[2, l] = self._compute_C_210_error(l, error_C_2l0)

            # C_5l0
            integral_C_5l0, error_C_5l0 = self._integrate_C_ml0(kernel_C_5l0)
            integrals[5, l] = self._compute_C_5l0(l, integral_C_5l0)
            errors[5, l] = self._compute_C_5l0_error(l, error_C_5l0)

            # C_6l0
            integral_C_6l0, error_C_6l0 = self._integrate_C_ml0(kernel_C_6l0)
            integrals[6, l] = self._compute_C_6l0(l, integral_C_6l0)
            errors[6, l] = self._compute_C_6l0_error(l, error_C_6l0)

            # C_3l0
            integrals[3, l] = self._compute_C_3l0(
                l, integrals[2, l], integrals[5, l], integrals[6, l],
            )
            errors[3, l] = self._compute_C_3l0_error(
                l, error_C_2l0, error_C_5l0, error_C_6l0,
            )

            # C_4l0
            integrals[4, l] = self._compute_C_4l0(
                l, integrals[2, l], integrals[5, l], integrals[6, l],
            )
            errors[4, l] = self._compute_C4l0_error(
                l, error_C_2l0, error_C_5l0, error_C_6l0,
            )

        return {'integral': integrals, 'error': errors}

    def _compute_inf(self) -> float:
        if self.inf_type is None:
            if self.R_0 > self.delta:
                return self.inf_factor * self.R_0
            else:
                return self.inf_factor * self.delta
        elif self.inf_type == 'delta':
            return self.inf_factor * self.delta
        elif self.inf_type == 1 or self.inf_type == '1':
            return self.inf_factor
        elif self.inf_type == 'radius':
            return self.inf_factor * self.R_0
        else:
            raise ValueError(
                f"inf_type needs to be 'boundary layer', '1', "
                f"'radius'"
                f'\n '
                f'got: {self.inf_type}',
            )

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def E(self, l: int, r: float, ac: bool) -> float:
        """:math:`E_l(r)`

        (Eq. C17)

        :param l: index l
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        :return: E(l, r)
        """
        gamma = self.gamma(l, r, ac)
        d_gamma = self.d_gamma(l, r, ac)
        beta = self.beta(l, r, ac)
        return - self.rho_f / (self.eta_f * r) * (gamma + r * d_gamma - beta)

    def F(self, n: int, m: int, r: float, ac: bool) -> complex:
        """:math:`F_{mn}(r)`

        (Eq. B5)

        :param n: index n
        :param m: index m
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        :return: F(n, m, r)
        """
        sc = not ac
        factor = 1j * conj(self.k_f ** 2) / r
        term_1 = 2 * self.phi(n, r, sc, True).conjugate()
        term_1 += r * self.d_phi(n, r, sc, True).conjugate()
        term_1 *= self.V_r(m, r, sc, True)
        term_2 = r * self.phi(n, r, sc, True).conjugate()
        term_2 *= self.d_V_r(m, r, sc, True)

        return factor * (term_1 + term_2)

    def G(self, n: int, m: int, r: float, ac: bool) -> complex:
        """:math:`G_{mn}(r)`

        (Eq. B6)

        :param n: index n
        :param m: index m
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        :return: G(m, n, r)
        """
        sc = not ac
        factor = 1j * conj(self.k_f ** 2) / r
        phi = self.phi(n, r, sc, True)
        v_theta = self.V_theta(m, r, sc, True)

        return factor * phi.conjugate() * v_theta

    def V_S_r(self, l: int, r: float, ac: bool) -> float:
        """:math:`V_{Srl}(r)`

        (Eq. F8)

        :param l: index l
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        """

        def first_inner_term(i: int, j: int) -> complex:
            cg_1 = cg(l, 0, j, 0, i, 0)
            if not cg_1:
                return 0
            return cg_1 ** 2 / (2 * i + 1) * conj(self.d_V_r(i, r, sc, True))

        def second_inner_term(i: int, j: int, h: int) -> complex:
            cg_coef = cg(l, 0, j - 2 * i + 1, 0, h, 0)
            if not cg_coef:
                return 0
            factor_1 = (2 * j - 4 * i + 3) * cg_coef ** 2 / (2 * h + 1)
            factor_2 = self.V_theta(j, r, sc, True) / r
            term_1 = (h + 1) * (h + 2) / (2 * h + 3)
            term_1 *= self.V_r(h + 1, r, sc, True).conjugate()
            if h <= 1:
                return factor_1 * factor_2 * term_1
            term_2 = h * (h - 1) / (2 * h - 1)
            term_2 *= self.V_r(h - 1, r, sc, True).conjugate()
            return factor_1 * factor_2 * (term_1 - term_2)

        sc = not ac

        # First Sum
        first_sum = complex(0)
        for n in self.range_N_max:
            first_inner_sum = complex(0)
            for m in full_range(abs(l - n), l + n):
                first_inner_sum += first_inner_term(m, n)
            first_sum += self.V_r(n, r, sc, True) * first_inner_sum

        # Second Sum
        second_sum = complex(0)
        for n in self.range_1_N_max:
            for m in full_range(1, int((n + 1) / 2)):
                for k in full_range(
                        abs(l - (n - 2 * m + 1)), l + n - 2 * m + 1,
                ):
                    second_sum += second_inner_term(m, n, k)
        return (
            (2 * l + 1) / (2 * self.omega)
            * (1j * (first_sum + second_sum)).real
        )

    def V_S_theta(
            self, l: int, r: float, ac: bool,
    ) -> float:
        """:math:`V_{S \\theta l}(r)`

        :param l: index l
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        """

        def first_inner_term(i: int, j: int) -> complex:
            cg_1 = cg(j, 0, l, 0, i, 0)
            cg_2 = cg(j, 0, l, 1, i, 1)
            if not cg_1 or not cg_2:
                return 0
            factor = sqrt(i * (i + 1)) * cg_1 * cg_2 / (2 * i + 1)
            term_1 = self.V_r(j, r, sc, True)
            term_1 *= self.d_V_theta(i, r, sc, True).conjugate()

            term_2 = self.V_r(j, r, sc, True)
            term_2 -= j ** 2 * self.V_theta(j, r, sc, True)

            term_2 = self.V_theta(i, r, sc, True) * term_2.conjugate() / r

            return factor * (term_1 + term_2)

        # Early return
        if l == 0:
            return 0

        sc = not ac

        # First Sum
        first_sum = complex(0)
        for n in self.range_N_max:
            for m in full_range(abs(n - l), n + l):
                if m >= 1:
                    first_sum += first_inner_term(m, n)
        second_sum = self._V_S_theta_second_sum(l, r, ac)
        return (
            (2 * l + 1) / (2 * self.omega * sqrt(l * (l + 1)))
            * (1j * (first_sum + second_sum)).real
        )

    def _V_S_theta_second_sum(self, l: int, r: float, ac: bool) -> complex:

        def second_inner_term(i: int, j: int, h: int) -> complex:
            cg_1 = cg(j - 2 * i, 0, l, 0, h, 0)
            cg_2 = cg(j - 2 * i, 0, l, 1, h, 1)
            if not (h >= 1 and cg_1 and cg_2):
                return 0
            else:
                factor_1 = (2 * j - 4 * i + 1)
                factor_2 = sqrt(h * (h + 1)) * cg_1 * cg_2 / (2 * h + 1)
                V_theta = self.V_theta(h, r, sc, True)
                return factor_1 * factor_2 * V_theta
        # Early return
        if l == 0:
            return 0

        sc = not ac

        # Second Sum
        second_sum = complex(0)
        for n in self.range_2_N_max:
            second_inner_sum = complex(0)
            for m in full_range(1, int(n / 2)):
                for k in full_range(abs(n - 2 * m - l), n - 2 * m + l):
                    second_inner_sum += second_inner_term(m, n, k)
            second_sum += (
                conj(self.V_theta(n, r, sc, True)) / r * second_inner_sum
            )
        return second_sum

    def alpha(self, l: int, r: float, ac: bool) -> float:
        """:math:`\\alpha_l(r)`

        (Eq. B9)

        :param l: index l
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        :return: alpha(l, r)
        """

        def first_term(i: int, j: int) -> complex:
            cg_1 = cg(l, 0, j, 0, i, 0)
            if not cg_1:
                return 0
            factor = cg_1 ** 2 / (2 * i + 1)
            F = self.F(j, i, r, ac)
            G = self.G(j, i, r, ac)
            return factor * (F - i * (i + 1) * G)

        def second_term(i: int, j: int, h: int):
            cg_1 = cg(l, 0, j - 2 * i + 1, 0, h, 0)
            if not cg_1:
                return 0
            factor = (2 * j - 4 * i + 3) * cg_1 ** 2 / (2 * h + 1)
            term_1 = (h + 1) * (h + 2) / (2 * h + 3)
            term_1 *= self.G(j, h + 1, r, ac)
            if h <= 1:
                return factor * term_1
            term_2 = h * (h - 1) / (2 * h - 1)
            term_2 *= self.G(j, h - 1, r, ac)
            return factor * (term_1 - term_2)

        # First Sum
        first_sum = complex(0)
        for n in self.range_N_max:
            for m in full_range(abs(l - n), n + l):
                first_sum += first_term(m, n)

        # Second Sum
        second_sum = complex(0)
        for n in self.range_1_N_max:
            for m in full_range(1, int((n + 1) / 2)):
                for k in full_range(
                        abs(l - (n - 2 * m + 1)),
                        l + n - 2 * m + 1,
                ):
                    second_sum += second_term(m, n, k)

        return (2 * l + 1) / (2 * self.omega) * (first_sum + second_sum).real

    def beta(self, l: int, r: float, ac: bool) -> float:
        """:math:`\\beta_l(r)`

        (Eq. C5)

        :param l: index l
        :param r: radial coordinate r
        :param ac: if True only the contribution from the
        :return: beta(l, r)
        """

        def first_term(i: int, j: int) -> float:
            cg_1 = cg(l, 0, j, 0, i, 0)
            if not cg_1:
                return 0
            factor = cg_1 ** 2 / (2 * i + 1) * self.V_r(j, r, sc, True)
            d_V_r = self.d_V_r(i, r, sc, True)
            phi = self.phi(i, r, sc, True)
            return (factor * (d_V_r - self.k_f ** 2 * phi).conjugate()).real

        def second_term(i: int, j: int, h: int) -> complex:
            cg_1 = cg(l, 0, j - 2 * i + 1, 0, h, 0)
            if not cg_1:
                return 0
            factor = cg_1 ** 2 / (2 * h + 1)
            term_1 = self.V_r(h + 1, r, sc, True)
            term_1 -= self.V_theta(h + 1, r, sc, True)
            term_1 = (h + 1) * (h + 2) / (2 * h + 3) * term_1.conjugate()
            if h <= 1:
                return factor * term_1
            term_2 = self.V_r(h - 1, r, sc, True)
            term_2 -= self.V_theta(h - 1, r, sc, True)
            term_2 = h * (h - 1) / (2 * h - 1) * term_2.conjugate()

            return factor * (term_1 - term_2)

        sc = not ac

        # First Sum
        first_sum = 0
        for n in self.range_N_max:
            first_inner_sum = 0
            for m in full_range(abs(l - n), l + n):
                first_inner_sum += first_term(m, n)
            first_sum += first_inner_sum

        # Second Sum
        second_sum = 0
        for n in self.range_1_N_max:
            for m in full_range(1, int((n + 1) / 2)):
                second_inner_sum = complex(0)
                for k in full_range(
                        abs(l - (n - 2 * m + 1)),
                        l + n - 2 * m + 1,
                ):
                    second_inner_sum += second_term(m, n, k)
                second_inner_sum *= (2 * n - 4 * m + 3)
                second_inner_sum *= self.V_theta(n, r, sc, True) / r
                second_sum += second_inner_sum.real
        return (2 * l + 1) / 2 * (first_sum + second_sum)

    def gamma(self, l: int, r: float, ac: bool) -> float:
        """:math:`\\gamma_l(l, r)`

        (Eq. C9)

        :param l: index l
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        :return: gamma(l, r)
        """

        def first_term(i: int, j: int) -> complex:
            cg_1 = cg(j, 0, l, 0, i, 0)
            cg_2 = cg(j, 0, l, 1, i, 1)
            if not cg_1 or not cg_2:
                return 0

            factor = sqrt(i * (i + 1)) * cg_1 * cg_2 / (2 * i + 1)

            term_1 = self.V_r(j, r, sc, True)
            term_1 *= self.d_V_theta(i, r, sc, True).conjugate()

            term_2 = self.V_r(j, r, sc, True) / r
            term_2 -= j ** 2 * self.V_theta(j, r, sc, True) / r
            term_2 -= self.k_f ** 2 * self.phi(j, r, sc, True)
            term_2 = self.V_theta(i, r, sc, True) * term_2.conjugate()

            return factor * (term_1 + term_2).real

        if l == 0:
            raise ValueError('gamma for n=0 is not defined')

        sc = not ac

        # First Sum
        first_sum = 0
        for n in self.range_N_max:
            for m in full_range(abs(n - l), n + l):
                if m >= 1:
                    first_sum += first_term(m, n)
        second_sum = self._V_S_theta_second_sum(l, r, ac).real
        return (
            (2 * l + 1) / (2 * sqrt(l * (l + 1)))
            * (first_sum + second_sum)
        )

    def d_gamma(self, l: int, r: float, ac: bool) -> float:
        """:math:`\\partial_r \\gamma_l(r)`

        (Eq. C9)

        :param l: index l
        :param r: radial coordinate [m]
        :param ac: if True only the incident field contribution
        :return: d_gamma(l, r)
        """

        def first_term(i: int, j: int) -> float:
            cg_1 = cg(j, 0, l, 0, i, 0)
            cg_2 = cg(j, 0, l, 1, i, 1)
            if not cg_1 or not cg_2:
                return 0
            factor = sqrt(i * (i + 1)) * cg_1 * cg_2 / (2 * i + 1)
            term_1 = self.d_V_r(j, r, sc, True)
            term_1 *= self.d_V_theta(i, r, sc, True).conjugate()

            term_2 = self.V_r(j, r, sc, True)
            term_2 *= self.d2_V_theta(i, r, sc, True).conjugate()

            term_3 = self.V_r(j, r, sc, True) / r
            term_3 -= j ** 2 * self.V_theta(j, r, sc, True) / r
            term_3 -= self.k_f ** 2 * self.phi(j, r, sc, True)
            term_3 = self.d_V_theta(i, r, sc, True) * term_3.conjugate()

            term_4 = self.d_V_r(j, r, sc, True) / r
            term_4 -= j ** 2 * self.d_V_theta(j, r, sc, True) / r
            term_4 -= self.V_r(j, r, sc, True) / r ** 2
            term_4 += j ** 2 * self.V_theta(j, r, sc, True) / r ** 2
            term_4 -= self.k_f ** 2 * self.d_phi(j, r, sc, True)
            term_4 = self.V_theta(i, r, sc, True) * term_4.conjugate()

            return (factor * (term_1 + term_2 + term_3 + term_4)).real

        def second_term(i: int, j: int, h: int) -> float:
            cg_1 = cg(j - 2 * i, 0, l, 0, h, 0)
            cg_2 = cg(j - 2 * i, 0, l, 1, h, 1)
            if not cg_1 or not cg_2:
                return 0
            factor = sqrt(h * (h + 1)) * cg_1 * cg_2 / (2 * h + 1)
            term_1 = self.d_V_theta(j, r, sc, True).conjugate()
            term_1 *= self.V_theta(h, r, sc, True) / r

            term_2 = self.V_theta(j, r, sc, True).conjugate()
            term_2 *= self.d_V_theta(h, r, sc, True) / r

            term_3 = self.V_theta(j, r, sc, True).conjugate()
            term_3 *= self.V_theta(h, r, sc, True) / r ** 2

            return (factor * (term_1 + term_2 - term_3)).real

        if l == 0:
            raise ValueError('d_gamma for n=0 is not defined')

        sc = not ac

        # First Sum
        first_sum = 0
        for n in self.range_N_max:
            for m in full_range(abs(n - l), n + l):
                if m >= 1:
                    first_sum += first_term(m, n)

        # Second Sum
        second_sum = 0
        for n in self.range_2_N_max:
            for m in full_range(1, int(n / 2)):
                second_inner_sum = 0
                for k in full_range(abs(n - 2 * m - l), n - 2 * m + l):
                    if k >= 1:
                        second_inner_sum += second_term(m, n, k)
                second_sum += (2 * n - 4 * m + 1) * second_inner_sum

        return ((2 * l + 1) / (2 * sqrt(l * (l + 1)))
                * (first_sum + second_sum))


if __name__ == '__main__':
    pass
