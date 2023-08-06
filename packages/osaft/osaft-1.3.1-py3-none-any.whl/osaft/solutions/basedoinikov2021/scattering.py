from abc import ABC
from collections.abc import Iterable, Sequence
from typing import Optional, Union

import numpy as np

from osaft import ViscoelasticFluid, ViscousFluid, WaveType, log
from osaft.core.frequency import Frequency
from osaft.core.functions import BesselFunctions as Bf
from osaft.core.functions import full_range
from osaft.core.geometries import Sphere
from osaft.core.helper import InputHandler
from osaft.core.variable import ActiveListVariable, ActiveVariable
from osaft.solutions.base_scattering import BaseScattering
from osaft.solutions.basedoinikov2021.coefficientmatrix import (
    CoefficientMatrix,
)


class BaseScatteringDoinikov2021(CoefficientMatrix, BaseScattering, ABC):
    """Scattering field class for Doinikov (viscous fluid-elastic sphere; 2021)

    :param f: frequency [Hz]
    :param R_0: radius [m]
    :param rho_s: density of the particle [kg/m^3]
    :param E_s: Young's modulus of the particle [Pa]
    :param nu_s: Poisson's ratio of the particle [-]
    :param fluid: Fluid instance of the model
    :param p_0: pressure amplitude [Pa]
    :param wave_type: wave type
    :param position: position in the standing wave field [m]
    """

    def __init__(
            self, f: Union[Frequency, float],
            R_0: Union[Sphere, float],
            rho_s: float, E_s: float, nu_s: float,
            fluid: Union[ViscousFluid, ViscoelasticFluid],
            p_0: float, wave_type: WaveType,
            position: Optional[float] = None,
            N_max: int = 5,
    ) -> None:
        """Constructor method
        """

        BaseScattering.__init__(self, N_max=N_max)

        CoefficientMatrix.__init__(
            self, f=f, R_0=R_0,
            rho_s=rho_s, E_s=E_s, nu_s=nu_s,
            fluid=fluid,
            p_0=p_0, wave_type=wave_type, position=position,
        )

        log.info('Create ScatteringField')

        # Dependent variables - Coefficients
        self._a = ActiveListVariable(
            self._compute_a,
            'radial fluid coefficients a_n',
        )
        self._a.is_computed_by(self._list_matrix_M_n, self._list_vector_n)
        self._a_hat = ActiveListVariable(
            self._compute_a_hat,
            'radial particle coefficients a_hat_n',
        )
        self._a_hat.is_computed_by(self._list_matrix_M_n, self._list_vector_n)
        self._b = ActiveListVariable(
            self._compute_b,
            'tangential fluid coefficients b_n',
        )
        self._b.is_computed_by(self._list_matrix_M_n, self._list_vector_n)
        self._b_hat = ActiveListVariable(
            self._compute_b_hat,
            'tangential particle coefficients '
            'b_hat_n',
        )
        self._b_hat.is_computed_by(self._list_matrix_M_n, self._list_vector_n)

        # Dependent Variables - Ranges
        self._range_N_max = ActiveVariable(self._compute_range_N_max)
        self._range_1_N_max = ActiveVariable(self._compute_range_1_N_max)
        self._range_2_N_max = ActiveVariable(self._compute_range_2_N_max)

    def __repr__(self):
        return (
            f'ScatteringField({self.f}, {self.R_0}, {self.rho_s}, '
            f'{self.E_s}), {self.nu_s}. {self.rho_f}, {self.c_f}, '
            f'{self.eta_f}, {self.zeta_f}, {self.p_0}, {self.wave_type}, '
            f'{self.field.position}, {self.N_max})'
        )

    # -------------------------------------------------------------------------
    # User-facing methods
    # -------------------------------------------------------------------------

    def radial_particle_displacement(
        self,
        r: Union[float, Sequence],
        theta: Union[float, Sequence],
        t: Union[float, Sequence],
        mode: Optional[int] = None,
    ) -> Union[complex, np.ndarray]:
        """First-order radial particle displacements [m]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: mode
        :return: first-order radial particle displacement
        """

        def coefficients(
            l: int, x: Union[complex, np.ndarray],
        ) -> Union[complex, np.ndarray]:
            term1 = self.k_l * self.a_hat(l) * Bf.d1_besselj(l, self.k_l * x)
            term2 = (l + 1) * l * self.b_hat(l) * Bf.besselj(l, self.k_t * x)
            term2 /= x
            return term1 - term2

        r, theta, t = InputHandler.handle_input(
            r, theta, t, self.R_0,
            inside_sphere=True,
        )

        return self.radial_mode_superposition(coefficients, r, theta, t, mode)

    def radial_particle_velocity(
        self,
        r: Union[float, Sequence],
        theta: Union[float, Sequence],
        t: Union[float, Sequence],
        mode: Optional[int] = None,
    ) -> Union[complex, np.ndarray]:
        """ First-order radial particle velocity [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: mode
        """

        displacement = self.radial_particle_displacement(r, theta, t, mode)
        return -1j * self.frequency.omega * displacement

    def tangential_particle_displacement(
        self,
        r: Union[float, Sequence],
        theta: Union[float, Sequence],
        t: Union[float, Sequence],
        mode: Optional[int] = None,
    ) -> Union[complex, np.ndarray]:
        """ First-order tangential particle displacements [m]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: mode
        :return: first-order tangential particle displacements
        """

        def coefficients(
            l: int, x: Union[complex, np.ndarray],
        ) -> Union[complex, np.ndarray]:
            term1 = self.a_hat(l) * Bf.besselj(l, self.k_l * x)
            term2 = Bf.besselj(l, self.k_t * x)
            term2 += self.k_t * x * Bf.d1_besselj(l, self.k_t * x)
            term2 *= self.b_hat(l)
            return (term1 - term2) / x

        r, theta, t = InputHandler.handle_input(
            r, theta, t, self.R_0,
            inside_sphere=True,
        )

        return self.tangential_mode_superposition(
            coefficients, r, theta, t,
            mode,
        )

    def tangential_particle_velocity(
        self,
        r: Union[float, Sequence],
        theta: Union[float, Sequence],
        t: Union[float, Sequence],
        mode: Optional[int] = None,
    ) -> Union[complex, np.ndarray]:
        """ First-order tangential particle displacements [m]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: mode
        :return: first-order tangential particle displacements
        """

        displacement = self.tangential_particle_displacement(r, theta, t, mode)
        return -1j * self.frequency.omega * displacement

    def potential_coefficient(self, n: int) -> complex:
        return self.a(n)

    # -------------------------------------------------------------------------
    # Coefficients
    # -------------------------------------------------------------------------

    def _compute_a(self, n: int) -> complex:
        if n == 0:
            return self.a_0()
        else:
            return self.det_M_n(n, 0) / self.det_M_n(n)

    def _compute_a_hat(self, n: int) -> complex:
        if n == 0:
            return self.a_hat_0()
        else:
            return self.det_M_n(n, 2) / self.det_M_n(n)

    def _compute_b(self, n: int) -> complex:
        if n == 0:
            return 0
        else:
            return self.det_M_n(n, 1) / self.det_M_n(n)

    def _compute_b_hat(self, n: int) -> complex:
        if n == 0:
            return 0
        else:
            return self.det_M_n(n, 3) / self.det_M_n(n)

    def a(self, n: int) -> complex:
        """Coefficient :math:`a_n` [m^2/s]

        (Eq. A18)

        :param n: mode
        :return: coefficient a_n
        """
        return self._a.item(n)

    def a_hat(self, n: int) -> complex:
        """Coefficient :math:`\\hat{a}_n` [m^2/s]

        (Eq. A18)

        :param n: mode
        :return: coefficient a_hat_n
        """
        return self._a_hat.item(n)

    def b(self, n: int) -> complex:
        """Coefficient :math:`b_n` [m^2/s]

        (Eq. A18)

        :param n: mode
        """
        return self._b.item(n)

    def b_hat(self, n: int) -> complex:
        """Coefficient :math:`\\hat{b}_n` [m^2/s]

        (Eq. A18)

        :param n: mode
        """
        return self._b_hat.item(n)

    # -------------------------------------------------------------------------
    # Ranges
    # -------------------------------------------------------------------------

    @property
    def range_N_max(self) -> Iterable:
        """Returns ``range(0, N_max + 1)``
        """
        return self._range_N_max.value

    @property
    def range_1_N_max(self) -> Iterable:
        """Returns ``range(1, N_max + 1)``
        """
        return self._range_1_N_max.value

    @property
    def range_2_N_max(self) -> Iterable:
        """Returns ``range(2, N_max + 1)``
        """
        return self._range_2_N_max.value

    def _compute_range_N_max(self) -> Iterable:
        return full_range(self.N_max)

    def _compute_range_1_N_max(self) -> Iterable:
        return full_range(1, self.N_max)

    def _compute_range_2_N_max(self) -> Iterable:
        return full_range(2, self.N_max)

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def V_r_sc(self, n: int, r: float) -> complex:
        """Scattering contribution to :math:`V_{rn}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        """
        inviscid = self.a(n) * self.k_f * Bf.d1_hankelh1(n, self.k_f * r)
        viscous = n * (n + 1) * self.b(n) * Bf.hankelh1(n, self.k_v * r) / r
        return inviscid - viscous

    def d_V_r(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        """:math:`\\partial_r V_{rn}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: scattered field
        :param incident: incident field
        """
        if incident and not scattered:
            return self.d_V_r_i(n, r)
        elif incident and scattered:
            return self.d_V_r_sc(n, r) + self.d_V_r_i(n, r)
        elif not incident and scattered:
            return self.d_V_r_sc(n, r)
        else:
            raise ValueError(
                'Neither scattered nor incident field has '
                'been has been selected. Velocity field is zero.', )

    def d_V_r_sc(self, n: int, r: float) -> complex:
        """:math:`\\partial_r V_{rn}^{sc}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        """
        viscous = self.k_v * Bf.d1_hankelh1(n, self.k_v * r) * r
        viscous -= Bf.hankelh1(n, self.k_v * r)
        viscous *= n * (n + 1) * self.b(n) / r**2
        inviscid = self.k_f ** 2 * self.a(n) * Bf.d2_hankelh1(n, self.k_f * r)
        return inviscid - viscous

    def d_V_r_i(self, n: int, r: float) -> complex:
        """:math:`\\partial_r V_{rn}^{i}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.k_f ** 2 * self.A_in(n) * Bf.d2_besselj(n, self.k_f * r)

    def d2_V_r(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        """:math:`\\partial^2_r V_{rn}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: scattered field
        :param incident: incident field
        """
        if incident and not scattered:
            return self.d2_V_r_i(n, r)
        elif incident and scattered:
            return self.d2_V_r_sc(n, r) + self.d2_V_r_i(n, r)
        elif not incident and scattered:
            return self.d2_V_r_sc(n, r)
        else:
            raise ValueError(
                'Neither scattered nor incident field has '
                'been has been selected. Velocity field is zero.', )

    def d2_V_r_i(self, n: int, r: float) -> complex:
        """:math:`\\partial^2_r V_{rn}^{i}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.k_f ** 3 * self.A_in(n) * Bf.d3_besselj(n, self.k_f * r)

    def d2_V_r_sc(self, n: int, r: float) -> complex:
        """:math:`\\partial^2_r V_{rn}^{sc}(r)` [m/s]

        (Eq. 35)

        :param n: mode
        :param r: radial coordinate [m]
        """
        inviscid = self.k_f ** 3 * self.a(n) * Bf.d3_hankelh1(n, self.k_f * r)
        viscous = 2 * Bf.hankelh1(n, self.k_v * r) / r ** 3
        viscous -= 2 * self.k_v * Bf.d1_hankelh1(n, self.k_v * r) / r ** 2
        viscous += self.k_v ** 2 * Bf.d2_hankelh1(n, self.k_v * r) / r
        viscous *= n * (n + 1) * self.b(n)
        return inviscid - viscous

    def V_theta_sc(self, n: int, r: float) -> complex:
        """Scattering contribution to :math:`V_{\\theta n}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        """
        inviscid = self.a(n) * Bf.hankelh1(n, self.k_f * r)
        viscous = Bf.hankelh1(n, self.k_v * r)
        viscous += self.k_v * r * Bf.d1_hankelh1(n, self.k_v * r)
        viscous *= self.b(n)
        return (inviscid - viscous) / r

    def d_V_theta(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        """:math:`\\partial_r V_{\\theta n}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: scattered field
        :param incident: incident field
        """
        if incident and scattered:
            if n == 0:
                return 0
            return self.d_V_theta_sc(n, r) + self.d_V_theta_i(n, r)
        elif incident and not scattered:
            return self.d_V_theta_i(n, r)
        elif not incident and scattered:
            return self.d_V_theta_sc(n, r)
        else:
            raise ValueError(
                'Neither scattered nor incident field has '
                'been has been selected. Velocity field is zero.', )

    def d_V_theta_sc(
        self, n: int, r: float,
    ) -> complex:
        """:math:`\\partial_r V_{\\theta n}^{sc}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        """
        nominator_div_r = self.V_theta_sc(n, r)
        inviscid = self.k_f * self.a(n) * Bf.d1_hankelh1(n, self.k_f * r)
        viscous = 2 * Bf.d1_hankelh1(n, self.k_v * r)
        viscous += self.k_v * r * Bf.d2_hankelh1(n, self.k_v * r)
        viscous *= self.b(n) * self.k_v
        d_nominator = inviscid - viscous
        return (d_nominator - nominator_div_r) / r

    def d_V_theta_i(self, n: int, r: float) -> complex:
        """:math:`\\partial_r V_{\\theta n}^{i}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        """
        nominator_div_r = self.V_theta_i(n, r)
        d_nominator = self.k_f * self.A_in(n) * Bf.d1_besselj(n, self.k_f * r)
        return (d_nominator - nominator_div_r) / r

    def d2_V_theta(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        """:math:`\\partial^2_r V_{\\theta n}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: scattered field
        :param incident: incident field
        """
        if incident and scattered:
            if n == 0:
                return 0
            return self.d2_V_theta_sc(n, r) + self.d2_V_theta_i(n, r)
        elif incident and not scattered:
            return self.d2_V_theta_i(n, r)
        elif not incident and scattered:
            return self.d2_V_theta_sc(n, r)
        else:
            raise ValueError(
                'Neither scattered nor incident field has '
                'been has been selected. Velocity field is zero.', )

    def d2_V_theta_sc(self, n: int, r: float) -> complex:
        """:math:`\\partial^2_r V_{\\theta n}^{sc}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        """
        inviscid = self.k_f ** 2 * self.a(n) * Bf.d2_hankelh1(n, self.k_f * r)
        viscous = 3 * Bf.d2_hankelh1(n, self.k_v * r)
        viscous += self.k_v * r * Bf.d3_hankelh1(n, self.k_v * r)
        viscous *= self.b(n) * self.k_v ** 2
        dd_nominator = (inviscid - viscous)
        return (dd_nominator - 2 * self.d_V_theta_sc(n, r)) / r

    def d2_V_theta_i(self, n: int, r: float) -> complex:
        """:math:`\\partial^2_r V_{\\theta n}^{i}(r)` [m/s]

        (Eq. 36)

        :param n: mode
        :param r: radial coordinate [m]
        """
        dd_nominator = self.A_in(n) * Bf.d2_besselj(n, self.k_f * r)
        dd_nominator *= self.k_f ** 2
        return (dd_nominator - 2 * self.d_V_theta_i(n, r)) / r

    def phi(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        """:math:`\\varphi_n(r)`

        (Eq. 28, 30)

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: scattered field
        :param incident: incident field
        """
        if incident and not scattered:
            return self.phi_i(n, r)
        elif incident and scattered:
            return self.phi_i(n, r) + self.phi_sc(n, r)
        elif not incident and scattered:
            return self.phi_sc(n, r)
        else:
            raise ValueError(
                'Neither scattered nor incident field has '
                'been has been selected. Velocity field is zero.', )

    def phi_sc(self, n: int, r: float) -> complex:
        """:math:`\\varphi_n^{sc}(r)`

        (Eq. 28, 30)

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.a(n) * Bf.hankelh1(n, self.k_f * r)

    def phi_i(self, n: int, r: float) -> complex:
        """:math:`\\varphi_n^i(r)`

        (Eq. 28, 30)

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.A_in(n) * Bf.besselj(n, self.k_f * r)

    def d_phi(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        """:math:`\\partial_r \\varphi_n(r)`

        (Eq. 28, 30)

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: scattered field
        :param incident: incident field
        """
        if incident and not scattered:
            return self.d_phi_i(n, r)
        elif incident and scattered:
            return self.d_phi_i(n, r) + self.d_phi_sc(n, r)
        elif not incident and scattered:
            return self.d_phi_sc(n, r)
        else:
            raise ValueError(
                'Neither scattered nor incident field has '
                'been has been selected. Velocity field is zero.', )

    def d_phi_sc(self, n: int, r: float) -> complex:
        """:math:`\\partial_r \\varphi_n^{sc}(r)`

        (Eq. 28, 30)

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.a(n) * self.k_f * Bf.d1_hankelh1(n, self.k_f * r)

    def d_phi_i(self, n: int, r: float) -> complex:
        """:math:`\\partial_r \\varphi_n^{i}(r)`

        (Eq. 28, 30)

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.A_in(n) * self.k_f * Bf.d1_besselj(n, self.k_f * r)


if __name__ == '__main__':
    pass
