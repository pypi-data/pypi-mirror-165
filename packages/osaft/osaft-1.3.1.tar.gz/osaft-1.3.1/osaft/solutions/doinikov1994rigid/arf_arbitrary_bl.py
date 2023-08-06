from __future__ import annotations

from abc import ABC
from typing import Optional, Union

import numpy as np

from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.functions import full_range, pi, xexpexp1
from osaft.core.geometries import Sphere
from osaft.core.variable import ActiveVariable
from osaft.solutions.doinikov1994rigid.arf_limiting import ARFLimiting


class ARFArbitraryBL(ARFLimiting, ABC):
    """ARF according to Doinikov's theory (viscous fluid-rigid sphere; 1994)

    .. note::
        This classes implements all attributes and methods to compute the ARF
        for the case where both particle radius and boundary layer thickness
        are small compared to the wavelength
        :math:`|x| \\ll 1`, :math:`1 \\ll |x_v|`.
        This class does not actually implement a method for the ARF. If you
        want to compute the ARF use
        :attr:`~osaft.solutions.doinikov1994rigid.ARF`

    :param f: Frequency [Hz]
    :param R_0: Radius of the sphere [m]
    :param rho_s: Density of the sphere [kg/m^3]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity [Pa s]
    :param zeta_f: bulk viscosity [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param wave_type: Type of wave, travel(l)ing or standing
    :param position: Position in the standing wave field [rad]
    :param long_wavelength: using :math:`x \\ll 1`
    :param small_boundary_layer: :math:`x \\ll x_v \\ll 1`
    :param large_boundary_layer: :math`x \\ll 1 \\ll x_v`
    :param fastened_sphere: use theory of fastened sphere
    :param background_streaming: background streaming contribution
    :param N_max: Highest order mode
    """

    def __init__(
        self, f: Union[Frequency, float, int],
        R_0: Union[Sphere, float, int],
        rho_s: float,
        rho_f: float,
        c_f: float,
        eta_f: float,
        zeta_f: float,
        p_0: float,
        wave_type: WaveType,
        position: Optional[float],
        long_wavelength: bool,
        small_boundary_layer: bool,
        large_boundary_layer: bool,
        fastened_sphere: bool,
        background_streaming: bool,
        N_max: int,
    ) -> None:
        """Constructor method
        """

        # Call to init method of parent class
        super().__init__(
            f, R_0, rho_s, rho_f, c_f, eta_f, zeta_f,
            p_0, wave_type, position, long_wavelength,
            small_boundary_layer,
            large_boundary_layer,
            fastened_sphere, background_streaming, N_max,
        )

        # Coefficients G_n
        self._G_0 = ActiveVariable(self._compute_G_0, 'G_0')
        self._G_1 = ActiveVariable(self._compute_G_1, 'G_1')
        self._G_2 = ActiveVariable(self._compute_G_2, 'G_2')
        self._G_3 = ActiveVariable(self._compute_G_3, 'G_3')
        self._G_4 = ActiveVariable(self._compute_G_4, 'G_4')

        self._G_0.is_computed_by(self._rho_t, self._x_v)
        self._G_1.is_computed_by(self._x_v)
        self._G_2.is_computed_by(self._x_v)
        self._G_3.is_computed_by(self._x_v)
        self._G_4.is_computed_by(self._x_v)

        # Coefficients D_n
        self._D_0 = ActiveVariable(self._compute_D_0, 'D_0')
        self._D_1 = ActiveVariable(self._compute_D_1, 'D_1')

        self._D_0.is_computed_by(self._x, self._x_v, self._rho_t)
        self._D_1.is_computed_by(self._x, self._x_v, self._rho_t)

    def _F_1_limit(self) -> float:
        def term(n: int) -> float:
            A_n = self.A_in(n)
            A_n1 = self.A_in(n + 1)
            out = self.D_n_limit(n) * A_n * A_n1.conjugate()
            out += self.D_n_limit(n).conjugate() * A_n.conjugate() * A_n1
            out *= (n + 1) / (2 * n + 1) / (2 * n + 3)
            return out.real

        arf = np.sum([term(n) for n in full_range(1)])
        return - 3 / 2 * pi * self.rho_f * arf

    # -------------------------------------------------------------------------
    # Small Particle ARF
    # -------------------------------------------------------------------------

    def _arf_small_particle(self) -> float:
        """ Acoustic radiation force for the case where the particle radius
        and the viscous boundary layer are small compared to the wavelength
        """
        if self.wave_type == WaveType.TRAVELLING:
            return self._arf_small_particle_travelling()
        else:
            return self._arf_small_particle_standing()

    def _arf_small_particle_travelling(self) -> float:
        """Eq. (5.10), (5.12), (6.1), (6.2)
        """
        # F1
        F1 = self._F_1_limit()
        # F_2
        F2 = self._F_2_travelling() if self.background_streaming else 0
        # S_9n contribution to background streaming
        S_9n = 0 if self.background_streaming else self.S_9n_contribution()
        return F1 + F2 - S_9n

    def _arf_small_particle_standing(self) -> float:
        """Eq. (5.15), (5.16), (6.1), (6.2)
        """
        # F1
        F1 = self._F_1_limit()
        # F_2
        F2 = self._F_2_standing() if self.background_streaming else 0
        # S_9n contribution to background streaming
        S_9n = 0 if self.background_streaming else self.S_9n_contribution()
        return F1 + F2 - S_9n

    # -------------------------------------------------------------------------
    # Coefficients D_n
    # -------------------------------------------------------------------------

    def D_n_limit(self, n: int) -> complex:
        """Approximation for the coefficient D_0, D_1 from Eq (6.1), (6.2)
        """
        if n == 0:
            return self.D_0
        elif n == 1:
            return self.D_1
        else:
            raise ValueError('D_n in the limit is only defined for n = 0, 1')

    @property
    def D_0(self) -> complex:
        """Approximation for the coefficient D_0 from Eq (6.1)
        """
        return self._D_0.value

    def _compute_D_0(self) -> complex:
        out = self.G_1
        out += self.x_v ** 3 * (12 + self.x_v ** 2) * self._f(self.x_v)
        out *= - self.x ** 3 * self.G_0
        out += 2 * self.x ** 3 / 9
        out += self.x ** 3 / (3 * self.x_v ** 2)
        return out

    @property
    def D_1(self) -> complex:
        """Approximation for the coefficient D_1 from Eq (6.2)
        """
        return self._D_1.value

    def _compute_D_1(self):
        out = - 2 * (1 + 1j) * (9 + self.x_v ** 2)
        out *= self._f(self.x_v - 1j * self.x_v)
        out += 2 * self.G_3 * self._f(self.x_v)
        out += 1j * self.G_4 * self._f(-1j * self.x_v)
        out *= - self.x_v ** 3
        if abs(out.real + self.G_2.real) / abs(self.G_2.real) < 1e-6:
            RuntimeWarning(  # pragma: no cover
                'Possible precision loss detected. '
                'Consider using a limiting case solution.',
            )
        out += self.G_2
        out *= self.x ** 3 * self.G_0.conjugate() / (1 + self.x_v)
        out += self.x ** 3 / (3 * self.x_v ** 2)
        return out

    @staticmethod
    def _f(z):
        return xexpexp1(z)

    # -------------------------------------------------------------------------
    # Coefficients S_9n
    # -------------------------------------------------------------------------

    def S_9n_contribution(self) -> complex:
        """S_9n contribution to the background streaming"""

        # S_90 + #S_91 (background streaming contribution)
        S_9n = 2 * self.x**3 * self.x_v**(-2) / 9

        term_1 = S_9n * self.A_in(0) * self.A_in(1).conjugate()
        term_1 += S_9n.conjugate() * self.A_in(1) * self.A_in(0).conjugate()
        term_2 = S_9n * self.A_in(1) * self.A_in(2).conjugate()
        term_2 += S_9n.conjugate() * self.A_in(2) * self.A_in(1).conjugate()

        return (2 * term_1 / 15 + term_2 / 3).real

    # -------------------------------------------------------------------------
    # Coefficients G_n
    # -------------------------------------------------------------------------

    @property
    def G_0(self) -> complex:
        """Approximation to value G_0 from Eq (6.3)
        """
        return self._G_0.value

    def _compute_G_0(self) -> complex:
        denominator = 9 * self.rho_t + 9 * self.rho_t * self.x_v
        denominator += (2 + self.rho_t) * self.x_v ** 2
        out = (1 - self.rho_t) / (72 * denominator)
        return out

    @property
    def G_1(self) -> complex:
        """Approximation to value G_1 from Eq (6.4)
        """
        return self._G_1.value

    def _compute_G_1(self) -> complex:
        out = 48 - 96 * self.x_v + 2 * self.x_v ** 2 - 14 * self.x_v ** 3
        out += self.x_v ** 4 - self.x_v ** 5
        return out

    @property
    def G_2(self) -> complex:
        """Approximation to value G_2 from Eq (6.5)
        """
        return self._G_2.value

    def _compute_G_2(self) -> complex:
        out = 48 + (48 + 192 * 1j / 5) * self.x_v
        out += (122 + 192 * 1j) * self.x_v ** 2 / 5
        out += 42 * (1 - 1j) * self.x_v ** 3 / 5
        out += (49 + 36 * 1j) * self.x_v ** 4 / 10
        out -= (31 - 17 * 1j) * self.x_v ** 5 / 10
        out += (6 + 31 * 1j) * self.x_v ** 6 / 30
        out += (1 + 6 * 1j) * self.x_v ** 7 / 30
        out += 1j * self.x_v ** 8 / 30
        return out

    @property
    def G_3(self) -> complex:
        """Approximation to value G_3 from Eq (6.6)
        """
        return self._G_3.value

    def _compute_G_3(self) -> complex:
        return 3 - 3 * 1j * self.x_v - self.x_v ** 2

    @property
    def G_4(self) -> complex:
        """Approximation to value G_4 from Eq (6.7)
        """
        return self._G_4.value

    def _compute_G_4(self) -> complex:
        out = 9 + 9 * self.x_v + 41 * self.x_v ** 2 / 10
        out += 11 * self.x_v ** 3 / 10 + self.x_v ** 4 / 5 + self.x_v ** 5 / 30
        return out


if __name__ == '__main__':
    pass
