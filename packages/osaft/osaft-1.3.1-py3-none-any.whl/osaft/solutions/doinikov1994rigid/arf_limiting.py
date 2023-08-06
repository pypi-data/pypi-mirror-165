from __future__ import annotations

from abc import ABC
from typing import Optional, Union

from osaft import log
from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.functions import pi, sin
from osaft.core.geometries import Sphere
from osaft.core.helper import StringFormatter as SF
from osaft.core.variable import PassiveVariable
from osaft.solutions.basedoinikov1994.arf_limiting import BaseARFLimiting
from osaft.solutions.doinikov1994rigid.scattering import ScatteringField


class ARFLimiting(ScatteringField, BaseARFLimiting, ABC):
    """Child class for ARF according to Doinikov's theory
    (viscous fluid-rigid sphere; 1994)

    .. note::
        This class implements all attributes and methods to compute the ARF
        in the limiting cases introduces in the article by Doinikov
        :math:`|x| \\ll |x_v| \\ll 1` and :math:`|x| \\ll 1 \\ll |x_v|`.
        This class does not actually implement a method for the ARF. If you
        want to compute the ARF
        use :attr:`~osaft.solutions.doinikov1994rigid.ARF`.

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
        rho_f: float, c_f: float,
        eta_f: float, zeta_f: float,
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

        # init of parent class
        ScatteringField.__init__(
            self,
            f=f, R_0=R_0,
            rho_s=rho_s,
            rho_f=rho_f, c_f=c_f, eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position, N_max=N_max,
        )
        BaseARFLimiting.__init__(self)

        # independent variables
        self._fastened_sphere = PassiveVariable(
            fastened_sphere,
            'fastened sphere limit',
        )

        self._long_wavelength = PassiveVariable(
            long_wavelength,
            'long wavelength limit',
        )
        self._small_boundary_layer = PassiveVariable(
            small_boundary_layer,
            'small viscous boundary layer limit',
        )

        self._large_boundary_layer = PassiveVariable(
            large_boundary_layer,
            'large viscous boundary layer limit',
        )

        self._background_streaming = PassiveVariable(
            background_streaming,
            'background streaming contribution',
        )

        # logging
        log.debug(repr(self))
        log.info(str(self))

    def __repr__(self):
        return (
            f'Donikov1994Rigid.ARF(frequency={self.f}, radius={self.R_0}, '
            f'rho_s={self.rho_s}, rho_f={self.rho_f}, c_f={self.c_f}, '
            f'eta_f={self.eta_f}, zeta_f={self.zeta_f}, '
            f'p_0={self.p_0}, position={self.position}, {self.wave_type}, '
            f'small_viscous_boundary_layer='
            f'{self.small_boundary_layer}, '
            f'large_viscous_boundary_layer='
            f'{self.large_boundary_layer}, '
            f'small_particle_limit={self.long_wavelength}, '
            f'fastened_sphere= {self.fastened_sphere}, '
            f'N_max={self.N_max})'
        )

    def __str__(self):
        out = 'Doinikovs\'s  (1994) model (viscous fluid-rigid sphere) for the'
        out += ' ARF with the following properties: \n'
        out += 'Limit Cases\n'
        out += SF.get_str_text(
            'Small particle limit',
            'small_particle_limit',
            self.long_wavelength, None,
        )
        out += SF.get_str_text(
            'Small delta',
            'small_viscous_boundary_layer',
            self.small_boundary_layer, None,
        )
        out += SF.get_str_text(
            'Fastened Sphere',
            'fastened_sphere',
            self.fastened_sphere, None,
        )
        out += 'Backgroundfield\n'
        out += SF.get_str_text('Frequency', 'f', self.f, 'Hz')
        out += SF.get_str_text('Pressure', 'p_0', self.p_0, 'Pa')
        out += SF.get_str_text('Wavetype', 'wave_type', self.wave_type, None)
        out += SF.get_str_text(
            'Position', 'd',
            self.position, 'rad',
        )
        out += SF.get_str_text(
            'Wavelength', 'lambda',
            self.field.lambda_f, 'm',
        )

        out += 'Fluid\n'
        out += SF.get_str_text(
            'Density', 'rho_f',
            self.rho_f, 'kg/m^3',
        )
        out += SF.get_str_text(
            'Sound Speed', 'c_0',
            self.c_f, 'm/s',
        )
        out += SF.get_str_text(
            'Compressibility', 'kappa_f',
            self.kappa_f, '1/Pa',
        )
        out += SF.get_str_text(
            'Shear viscosity', 'eta_f',
            self.eta_f, '1/Pa',
        )
        out += SF.get_str_text(
            'Bulk viscosity', 'zeta_f',
            self.zeta_f, '1/Pa',
        )

        out += 'Particle\n'
        out += SF.get_str_text(
            'Radius', 'R_0',
            self.R_0, 'm',
        )
        out += SF.get_str_text(
            'Density', 'rho_s',
            self.rho_s, 'kg/m^3',
        )
        return out

    # -------------------------------------------------------------------------
    # Special Expressions for the ARF
    # -------------------------------------------------------------------------

    def _arf_fastened_small_delta(self) -> float:
        # eq. (7.1) for travelling wave and
        # eq. (6.14) w/ \\delta -> 0 for standing
        if self.wave_type == WaveType.TRAVELLING:
            out = 1 - self.norm_delta
            out *= 1.5 * self.norm_delta
        else:
            out = 5 / 6 + 0.75 * self.norm_delta
            out *= self._standing_wave_position_term()
        out *= pi * self.rho_f * self.field.abs_A_squared * self.x_0**3
        return out

    def _arf_fastened_large_delta(self) -> float:
        # eq. (7.5) for travelling wave and eq. (7.6) for standing
        if self.wave_type == WaveType.TRAVELLING:
            out = 1 - 1.2 / self.norm_delta

            out *= -1.5 * self.norm_delta
        else:
            out = 1 + 10 / 27 / self.norm_delta
            out *= 0.9 * self._standing_wave_position_term()
        out *= pi * self.rho_f * self.field.abs_A_squared * self.x_0**3
        out *= self.norm_delta
        return out

    def _arf_small_particle_large_delta(self) -> float:
        # eq. (6.18) for travelling wave and eq. (6.19) for standing
        if self.wave_type == WaveType.TRAVELLING:
            out = (1 - self.rho_t) / self.norm_delta
            out *= -22 / 15
        else:
            out = 11 * (1 - self.rho_t) / 5 / self.norm_delta
            out += 2 * self.rho_t - 1
            out *= self._standing_wave_position_term() / 3
        out *= pi * self.rho_s * self.field.abs_A_squared * self.x_0**3
        return out

    def _arf_small_particle_small_delta(self) -> float:
        # eq. (6.13) for travelling wave and eq. (6.14) for standing
        if self.wave_type == WaveType.TRAVELLING:
            out = 2 + 12 * self.rho_t - 21 * self.rho_t**2 + 7 * self.rho_t**3
            out *= -self.norm_delta / (2 + self.rho_t)
            out += (1 - self.rho_t)**2
            out *= 6 * self.norm_delta
            out /= (2 + self.rho_t)**2
        else:
            out = 3 * (1 - self.rho_t)**2 * self.norm_delta
            out /= (2 + self.rho_t)**2
            out += (5 - 2 * self.rho_t) / (3 * (2 + self.rho_t))
            out *= self._standing_wave_position_term()
        out *= pi * self.rho_f * self.field.abs_A_squared * self.x_0**3
        return out

    def _standing_wave_position_term(self) -> float:
        return sin(2 * self.position)

    # -------------------------------------------------------------------------
    # Getters and Setters for independent variables
    # -------------------------------------------------------------------------

    @property
    def long_wavelength(self) -> bool:
        """Use limiting case for ARF calculation

        :getter: returns if a small particle limit is used
        :setter: automatically invokes
            :func:`src.core.variable.BaseVariable.notify`
        """
        return self._long_wavelength.value

    @long_wavelength.setter
    def long_wavelength(self, value):
        self._long_wavelength.value = value

    @property
    def fastened_sphere(self) -> bool:
        """Use limiting case of fastened sphere

        :getter: returns if fastened sphere limiting case is used
        :setter: automatically invokes
            :func:`src.core.variable.BaseVariable.notify`
        """
        return self._fastened_sphere.value

    @fastened_sphere.setter
    def fastened_sphere(self, value):
        self._fastened_sphere.value = value


if __name__ == '__main__':
    pass
