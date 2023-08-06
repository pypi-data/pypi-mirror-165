from __future__ import annotations

from abc import ABC
from typing import Optional, Union

from osaft import log
from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.functions import pi, sin, sqrt
from osaft.core.geometries import Sphere
from osaft.core.helper import StringFormatter as SF
from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.solutions.basedoinikov1994.arf_limiting import BaseARFLimiting
from osaft.solutions.doinikov1994compressible.scattering import ScatteringField


class ARFLimiting(ScatteringField, BaseARFLimiting, ABC):
    """Base class for Doinikov 1994 (compressible sphere)

    .. note::
        This class implements all attributes and methods to compute the ARF
        in the limiting cases introduces in the article by Doinikov
        :math:`|x| \\ll |x_v| \\ll 1` and :math:`|x| \\ll 1 \\ll |x_v|`.
        This class does not actually implement a method for the ARF. If you
        want to compute the ARF use
        :attr:`~osaft.solutions.doinikov1994compressible.ARF`

    :param f: Frequency [Hz]
    :param R_0: Radius of the sphere [m]
    :param rho_s: Density of the sphere [kg/m^3]
    :param c_s: Speed of sound of in the sphere [m/s]
    :param eta_s: shear viscosity of in the sphere  [Pa s]
    :param zeta_s: bulk viscosity of in the sphere [Pa s]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity fluid [Pa s]
    :param zeta_f: bulk viscosity fluid [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param wave_type: Type of wave, travel(l)ing or standing
    :param position: Position within the standing wave field [m]
    :param small_boundary_layer: :math:`x \\ll x_v \\ll 1`
    :param large_boundary_layer: :math`x \\ll 1 \\ll x_v`
    :param N_max: Highest order mode
    :param background_streaming: background streaming contribution
    """

    def __init__(
        self, f: Union[Frequency, float, int],
        R_0: Union[Sphere, float, int],
        rho_s: float, c_s: float,
        eta_s: float, zeta_s: float,
        rho_f: float, c_f: float,
        eta_f: float, zeta_f: float,
        p_0: float,
        wave_type: WaveType,
        position: Optional[float],
        small_boundary_layer: bool,
        large_boundary_layer: bool,
        background_streaming: bool,
        N_max: int,
    ) -> None:
        """Constructor method
        """

        # init of parent class
        ScatteringField.__init__(
            self,
            f=f, R_0=R_0,
            rho_s=rho_s, c_s=c_s, eta_s=eta_s, zeta_s=zeta_s,
            rho_f=rho_f, c_f=c_f, eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position, N_max=N_max,
        )
        BaseARFLimiting.__init__(self)

        # independent variables
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

        # Dependent variables
        self._mu = ActiveVariable(
            self._compute_mu,
            '(density * viscosity) ratio',
        )
        self._kappa_t = ActiveVariable(
            self._compute_kappa_t,
            'compressibility ratio',
        )
        self._eta_t = ActiveVariable(
            self._compute_eta_t, 'dynamic viscosity ratio',
        )
        self._zeta_t = ActiveVariable(
            self._compute_zeta_t, 'bulk viscosity ratio',
        )
        self._f1 = ActiveVariable(self._compute_f1, 'f1 ARF factor; B.2.1')
        self._f2 = ActiveVariable(self._compute_f2, 'f2 ARF factor; B.2.1')
        self._f3 = ActiveVariable(self._compute_f3, 'f3 ARF factor; B.2.1')
        self._G = ActiveVariable(self._compute_G, 'G ARF factor; eq. 7.9')
        self._S1 = ActiveVariable(self._compute_S1, 'S1 ARF factor; eq. 7.10')
        self._S2 = ActiveVariable(self._compute_S2, 'S2 ARF factor; eq. 7.11')
        self._S3 = ActiveVariable(self._compute_S3, 'S3 ARF factor; eq. 7.12')
        self._f4 = ActiveVariable(self._compute_f4, 'f4 ARF factor; B.2.1')
        self._g1 = ActiveVariable(self._compute_g1, 'g1 ARF factor; B.2.1')
        self._g2 = ActiveVariable(self._compute_g2, 'g2 ARF factor; B.2.1')
        self._g3 = ActiveVariable(self._compute_g3, 'g3 ARF factor; B.2.1')
        self._g4 = ActiveVariable(self._compute_g4, 'g4 ARF factor; B.2.1')
        self._g5 = ActiveVariable(self._compute_g5, 'g5 ARF factor; B.2.1')
        self._g6 = ActiveVariable(self._compute_g6, 'g6 ARF factor; B.2.1')
        self._g7 = ActiveVariable(self._compute_g7, 'g7 ARF factor; B.2.1')

        # Dependencies
        self._G.is_computed_by(self._S1, self._S2, self._S3)
        self._S1.is_computed_by(
            self._kappa_t, self.fluid._rho_f, self.scatterer._rho_f,
        )
        self._S2.is_computed_by(self._f1, self._f2, self._f4)
        self._S3.is_computed_by(
            self._f1, self._f3, self._f4, self.fluid._rho_f,
            self.scatterer._rho_f, self._kappa_t, self._eta_t,
        )
        self._eta_t.is_computed_by(self.scatterer._eta_f, self.fluid._eta_f)
        self._zeta_t.is_computed_by(self.scatterer._zeta_f, self.fluid._zeta_f)
        self._f1.is_computed_by(self._g1, self._g7)
        self._f2.is_computed_by(self._g1, self._g2, self._g5)
        self._f3.is_computed_by(self._g3, self._g6, self._g7)
        self._f4.is_computed_by(self._g4, self._g6, self._g7)
        self._g1.is_computed_by(self._g5, self._g6)
        self._g2.is_computed_by(self._eta_t, self._zeta_t)
        self._g3.is_computed_by(self._eta_t, self._zeta_t)
        self._g4.is_computed_by(self._eta_t, self._zeta_t)
        self._g5.is_computed_by(self._eta_t)
        self._g6.is_computed_by(self._eta_t)
        self._g7.is_computed_by(self._g6)
        self._norm_delta.is_computed_by(self.fluid._delta, self.sphere._R_0)
        self._kappa_t.is_computed_by(
            self.fluid._rho_f, self.fluid._c_f, self.scatterer._rho_f,
            self.scatterer._c_f,
        )
        self._mu.is_computed_by(
            self.fluid._rho_f, self.fluid._eta_f, self.scatterer._rho_f,
            self.scatterer._eta_f,
        )

        # logging
        log.debug(repr(self))
        log.info(str(self))

    def __repr__(self):
        return (
            f'Donikov1994Rigid.ARF(frequency={self.f}, radius={self.R_0}, '
            f'rho_s={self.rho_s}, c_s={self.c_s}, '
            f'eta_s={self.eta_s}, zeta_s={self.zeta_s}, '
            f'rho_f={self.rho_f}, c_f={self.c_f}, '
            f'eta_f={self.eta_f}, zeta_f={self.zeta_f}, '
            f'p_0={self.p_0}, position={self.position}, {self.wave_type}, '
            f'small_boundary_layer='
            f'{self.small_boundary_layer}, '
            f'large_boundary_layer='
            f'{self.large_boundary_layer}, '
            f'N_max={self.N_max})'
        )

    def __str__(self):
        out = 'Doinikovs\'s  (1994) model (viscous fluid-rigid sphere) for the'
        out += ' ARF with the following properties: \n'
        out += 'Limit Cases\n'
        out += SF.get_str_text(
            'Small particle and small delta',
            'Small particle and small delta',
            self.small_boundary_layer, None,
        )
        out += SF.get_str_text(
            'Small particle and large delta',
            'Small particle and large delta',
            self.large_boundary_layer, None,
        )
        out += 'Backgroundfield\n'
        out += SF.get_str_text('Frequency', 'f', self.f, 'Hz')
        out += SF.get_str_text('Pressure', 'p_0', self.p_0, 'Pa')
        out += SF.get_str_text('Wavetype', 'wave_type', self.wave_type, None)
        out += SF.get_str_text(
            'Position', 'd',
            self.position, '',
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
        out += SF.get_str_text(
            'Sound Speed', 'c_0',
            self.c_s, 'm/s',
        )
        out += SF.get_str_text(
            'Compressibility', 'kappa_s',
            self.kappa_s, '1/Pa',
        )
        out += SF.get_str_text(
            'Shear viscosity', 'eta_s',
            self.eta_s, '1/Pa',
        )
        out += SF.get_str_text(
            'Bulk viscosity', 'zeta_s',
            self.zeta_s, '1/Pa',
        )
        return out

    # -------------------------------------------------------------------------
    # Acoustic radiation force
    # -------------------------------------------------------------------------

    def _arf_small_particle_large_delta(self) -> float:
        """ Eq. 7.1 for WaveType.TRAVELLING; Eq. 7.8 for WaveType.STANDING
        """
        log.info(
            f'kappa_t << 1 : {self.kappa_t:.3e} << 1\n'
            f'rho_f << rho_s : {self.rho_s:.3e} << {self.rho_s:.3e}\n',
        )

        if self.wave_type == WaveType.TRAVELLING:
            out = 5 - 2 * self.kappa_t - 8 * self.f1

            out *= 1 / 6 * self.norm_delta ** 2
        else:
            out = self.G * self._standing_wave_position_term()

        out *= pi * self.field.abs_A_squared * self.rho_f * self.x_0**3
        return out

    def _arf_small_particle_small_delta(self) -> float:
        """ Eq. 6.1 for WaveType.TRAVELLING
        """
        log.info(
            f'kappa_t << 1 : {self.kappa_t:.3e} << 1\n'
            f'mu << 1 : {self.mu:.3e} << 1\n',
        )
        if self.wave_type == WaveType.TRAVELLING:
            out = (self.rho_s - self.rho_f) ** 2
            out /= (2 * self.rho_s + self.rho_f)**2 * (1 + self.mu)

            out *= self.x_0**3 * self.norm_delta

            out *= 6 * pi * self.rho_f * self.field.abs_A_squared
        else:
            raise NotImplementedError(
                'This solution is not implemented because Doinikov says '
                'in 6.1.2 of the publication that this solution is '
                'the same as Yosioka already computed.\n If you are '
                'interested in this value us the Yosioka class.',
            )
        return out

    def _standing_wave_position_term(self) -> float:
        return sin(2 * self.k_f.real * self.position)

    # -------------------------------------------------------------------------
    # Dependent variables
    # -------------------------------------------------------------------------

    @property
    def eta_t(self):
        """By fluid normalized dynamic viscosity
        """
        return self._eta_t.value

    def _compute_eta_t(self):
        return self.scatterer.eta_f / self.fluid.eta_f

    @property
    def zeta_t(self):
        """By fluid normalized bulk viscosity
        """
        return self._zeta_t.value

    def _compute_zeta_t(self):
        return self.scatterer.zeta_f / self.fluid.zeta_f

    @property
    def f1(self):
        """f1 factor of Appendix B
        """
        return self._f1.value

    def _compute_f1(self):
        return self.g1 / self.g7

    @property
    def f2(self):
        """f2 factor of Appendix B
        """
        return self._f2.value

    def _compute_f2(self):
        if self.g1 == 0:  # pragma: no cover
            return 0
        return self.g2 * self.g5 / self.g1 / 2

    @property
    def f3(self):
        """f3 factor of Appendix B
        """
        return self._f3.value

    def _compute_f3(self):
        return self.g3 * self.g6 / self.g7 / 10

    @property
    def f4(self):
        """f4 factor of Appendix B
        """
        return self._f4.value

    def _compute_f4(self):
        return self.g4 * self.g6 / self.g7 / 2

    @property
    def G(self):
        """G factor Eq (7.9)
        """
        return self._G.value

    def _compute_G(self):
        return (self.S1 + self.S2 + self.S3) / 3

    @property
    def S1(self):
        """S_1 factor Eq (7.10)
        """
        return self._S1.value

    def _compute_S1(self):
        return 1 - self.kappa_t + 0.9 * (1 - self.rho_s / self.rho_f)

    @property
    def S2(self):
        """S_2 factor Eq (7.11)
        """
        return self._S2.value

    def _compute_S2(self):
        out = 2 * self.f2 - 1
        out *= 2 * self.f1

        out -= 4 * self.f4
        return out

    @property
    def S3(self):
        """S_3 factor Eq (7.12)
        """
        return self._S3.value

    def _compute_S3(self):
        out = 3 - 1 / self.eta_t
        out *= -120 * (self.f3 - self.f4)

        out += 50 * self.f1 + 43 - 10 * self.kappa_t

        out *= self.rho_s - self.rho_f
        out /= 30 * self.rho_f * (3 + 2 / self.eta_t)

        return out

    @property
    def g1(self):
        """g1 factor of Appendix B
        """
        return self._g1.value

    def _compute_g1(self):
        return self.g5 * self.g6

    @property
    def g2(self):
        """g2 factor of Appendix B
        """
        return self._g2.value

    def _compute_g2(self):
        out = 209 + 148 * self.eta_t + 48 / self.eta_t
        out *= -1 / 9 / self.zeta_t

        out += 19 + 38 * self.eta_t - 12 / self.eta_t
        return out

    @property
    def g3(self):
        """g3 factor of Appendix B
        """
        return self._g3.value

    def _compute_g3(self):
        out = 25 + 370 * self.eta_t - 80 / self.eta_t
        out *= 1 / 9 / self.zeta_t

        out -= (12 + 19 * self.eta_t + 4 / self.eta_t)
        return out

    @property
    def g4(self):
        """g4 factor of Appendix B
        """
        return self._g4.value

    def _compute_g4(self):
        out = 5 + 74 * self.eta_t - 16 / self.eta_t
        out *= 1 / 9 / self.zeta_t

        out -= (3 + 4 / self.eta_t)
        return out

    @property
    def g5(self):
        """g5 factor of Appendix B
        """
        return self._g5.value

    def _compute_g5(self):
        out = (1 - self.eta_t)
        out *= 19 + 16 / self.eta_t
        return out

    @property
    def g6(self):
        """g6 factor of Appendix B
        """
        return self._g6.value

    def _compute_g6(self):
        return 89 + 48 / self.eta_t + 38 * self.eta_t

    @property
    def g7(self):
        """g7 factor of Appendix B
        """
        return self._g7.value

    def _compute_g7(self):
        return self.g6**2

    @property
    def mu(self) -> float:
        """ (density x viscosity) ratio
        :math:`\\tilde{\\mu}=\\frac{\\rho_f\\eta_f}{\\rho_s\\eta_s}`
        """
        return self._mu.value

    def _compute_mu(self):
        out = self.rho_f * self.eta_f
        out /= self.rho_s * self.eta_s
        return sqrt(out)

    @property
    def kappa_t(self) -> float:
        """ compressibility ratio
        :math:`\\tilde{\\kappa}=\\frac{\\kappa_s}{\\kappa_f}`
        """
        return self._kappa_t.value

    def _compute_kappa_t(self):
        return self.kappa_s / self.kappa_f


if __name__ == '__main__':
    pass
