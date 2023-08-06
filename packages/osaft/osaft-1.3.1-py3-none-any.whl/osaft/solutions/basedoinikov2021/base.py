from abc import ABC, abstractmethod
from typing import Optional, Union

from osaft import (
    BackgroundField,
    ElasticSolid,
    ViscoelasticFluid,
    ViscousFluid,
    WaveType,
    log,
)
from osaft.core.basecomposite import BaseSphereFrequencyComposite
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.core.helper import StringFormatter as SF
from osaft.core.variable import ActiveVariable
from osaft.solutions.base_solution import BaseSolution


class BaseDoinikov(BaseSphereFrequencyComposite, BaseSolution, ABC):
    """Base class for Doinikov (viscous fluid-elastic sphere; 2021)

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

    # Supported wave_type for the class
    supported_wavetypes = [WaveType.STANDING, WaveType.TRAVELLING]

    def __init__(
            self, f: Union[Frequency, float],
            R_0: Union[Sphere, float],
            rho_s: float, E_s: float, nu_s: float,
            fluid: Union[ViscousFluid, ViscoelasticFluid],
            p_0: float, wave_type: WaveType,
            position: Optional[float],
    ) -> None:
        """Constructor method
        """

        # Init parent classes
        BaseSphereFrequencyComposite.__init__(self, f, R_0)
        BaseSolution.__init__(self, 'Doinikov2021Viscous')

        # Initializing fluid
        self.fluid = fluid
        # Making sure fluid has the same Frequency instance
        self.fluid.frequency = self.frequency

        # Initialize Components
        self.solid = ElasticSolid(self.frequency, E_s, nu_s, rho_s)
        self.field = BackgroundField(
            self.fluid,
            p_0, wave_type, position,
        )

        # Dependent variables
        self._x_l = ActiveVariable(
            self._compute_x_l,
            'dimensionless wavenumber x_l',
        )
        self._x_t = ActiveVariable(
            self._compute_x_t,
            'dimensionless wavenumber x_t',
        )

        self._x_f = ActiveVariable(
            self._compute_x_f,
            'dimensionless wavenumber x_f',
        )
        self._x_v = ActiveVariable(
            self._compute_x_v,
            'dimensionless wavenumber x_v',
        )

        # Dependencies
        self._x_f.is_computed_by(self.fluid._k_f, self.sphere._R_0)
        self._x_v.is_computed_by(self.fluid._k_v, self.sphere._R_0)
        self._x_l.is_computed_by(self.solid._k_l, self.sphere._R_0)
        self._x_t.is_computed_by(self.solid._k_t, self.sphere._R_0)

        log.debug(repr(self))
        log.info(str(self))

    def __repr__(self):  # pragma: no cover
        return (
            f'BaseDoinikov({self.f}, {self.R_0}, {self.rho_s}, '
            f'{self.E_s}), {self.nu_s}. {self.rho_f}, {self.c_f}, '
            f'{self.eta_f}, {self.zeta_f}'
            f', {self.p_0}, {self.wave_type}, '
            f'{self.field.position})'
        )

    def __str__(self):
        out = 'Doinikov solution with following properties: \n'
        out += SF.get_str_text('Frequency', 'f', self.wave_type, 'Hz')
        out += SF.get_str_text(
            'Wavelength', 'lambda_f',
            self.fluid.lambda_f, 'm',
        )
        out += SF.get_str_text(
            'Boundary Layer Thickness', 'delta',
            self.fluid.delta, 'm',
        )
        out += SF.get_str_text(
            'Viscous wavelength', 'lambda_v',
            self.lambda_v, 'm',
        )
        out += SF.get_str_text('Radius', 'R_0', self.R_0, 'm')
        out += SF.get_str_text(
            'Fluid shear viscosity', 'eta_f', self.eta_f,
            'Pa s',
        )
        out += SF.get_str_text(
            'Fluid bulk viscosity', 'zeta_f', self.zeta_f,
            'Pa s',
        )
        return out

    # -------------------------------------------------------------------------
    # Abstract Methods
    # -------------------------------------------------------------------------

    @property
    @abstractmethod
    def eta(self) -> Union[float, complex]:
        """Fluid shear viscosity. For a
        :class:`osaft.core.fluids.ViscousFluid` returns :math:`\\eta_f`, for a
        :class:`osaft.core.fluids.ViscoelasticFluid` returns :math:`\\eta_c`.
        """
        pass

    @property
    @abstractmethod
    def zeta(self) -> Union[float, complex]:
        """Fluid bulk viscosity. For a
        :class:`osaft.core.fluids.ViscousFluid` returns :math:`\\zeta_f`, for a
        :class:`osaft.core.fluids.ViscoelasticFluid` returns :math:`\\zeta_c`.
        """
        pass

    # -------------------------------------------------------------------------
    # Getters for Dependent Variables
    # -------------------------------------------------------------------------

    @property
    def x_l(self):
        """Dimensionless primary wavenumber in the solid

        :math:`k_l \\cdot R_0`

        """
        return self._x_l.value

    @property
    def x_t(self):
        """Dimensionless secondary wavenumber in the solid

        :math:`k_t \\cdot R_0`

        """
        return self._x_t.value

    @property
    def x_f(self):
        """Dimensionless acoustic wavenumber in the fluid

        :math:`k_f \\cdot R_0`

        """
        return self._x_f.value

    @property
    def x_v(self):
        """Dimensionless viscous wavenumber in the fluid

        :math:`k_v \\cdot R_0`

        """
        return self._x_v.value

    # -------------------------------------------------------------------------
    # Dependent Variables Methods
    # -------------------------------------------------------------------------

    def _compute_x_l(self) -> complex:
        return self.R_0 * self.k_l

    def _compute_x_t(self) -> complex:
        return self.R_0 * self.k_t

    def _compute_x_f(self) -> complex:
        return self.R_0 * self.k_f

    def _compute_x_v(self) -> complex:
        return self.R_0 * self.k_v

    # -------------------------------------------------------------------------
    # Wrappers for Independent Solid Attributes
    # -------------------------------------------------------------------------

    @property
    def rho_s(self) -> float:
        """ Wraps to :attr:`osaft.core.solids.ElasticSolid.rho_s`
        """
        return self.solid.rho_s

    @rho_s.setter
    def rho_s(self, value) -> None:
        self.solid.rho_s = value

    @property
    def E_s(self) -> float:
        """ Wraps to :attr:`osaft.core.solids.ElasticSolid.E_s`
        """
        return self.solid.E_s

    @E_s.setter
    def E_s(self, value) -> None:
        self.solid.E_s = value

    @property
    def nu_s(self) -> float:
        """ Wraps to :attr:`osaft.core.solids.ElasticSolid.nu_s`
        """
        return self.solid.nu_s

    @nu_s.setter
    def nu_s(self, value) -> None:
        self.solid.nu_s = value

    # -------------------------------------------------------------------------
    # Wrappers for Dependent Solid Attributes
    # -------------------------------------------------------------------------

    @property
    def k_l(self) -> float:
        """ Wraps to :attr:`osaft.core.solids.ElasticSolid.k_l`
        """
        return self.solid.k_l

    @property
    def k_t(self) -> float:
        """ Wraps to :attr:`osaft.core.solids.ElasticSolid.k_t`
        """
        return self.solid.k_t

    # -------------------------------------------------------------------------
    # Wrappers for Dependent Fluid Attributes
    # -------------------------------------------------------------------------

    @property
    def rho_f(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.rho_0` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.rho_0`
        """
        return self.fluid.rho_f

    @rho_f.setter
    def rho_f(self, value) -> None:
        self.fluid.rho_f = value

    @property
    def c_f(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.c_f` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.c_f`
        """
        return self.fluid.c_f

    @c_f.setter
    def c_f(self, value) -> None:
        self.fluid.c_f = value

    @property
    def eta_f(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.eta_f` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.eta_f`
        """
        return self.fluid.eta_f

    @eta_f.setter
    def eta_f(self, value) -> None:
        self.fluid.eta_f = value

    @property
    def zeta_f(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.zeta_f` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.zeta_f`
        """
        return self.fluid.zeta_f

    @zeta_f.setter
    def zeta_f(self, value) -> None:
        self.fluid.zeta_f = value

    # -------------------------------------------------------------------------
    # Wrappers for Dependent Fluid Attributes
    # -------------------------------------------------------------------------

    @property
    def k_f(self) -> complex:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.k_f` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.k_f`
        """
        return self.fluid.k_f

    @property
    def k_v(self) -> complex:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.k_v` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.k_v`
        """
        return self.fluid.k_v

    @property
    def delta(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.delta` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.delta`
        """
        return self.fluid.delta

    @property
    def lambda_v(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.lambda_v` or to
        :attr:`osaft.core.fluids.ViscoelasticFluid.lambda_v`
        """
        return self.fluid.lambda_v

    # -------------------------------------------------------------------------
    # Wrappers for Independent Background Field Attributes
    # -------------------------------------------------------------------------

    @property
    def position(self) -> float:
        """Wraps to
        :attr:`osaft.core.backgroundfields.BackgroundField.position`
        """
        return self.field.position

    @position.setter
    def position(self, value: float) -> None:
        self.field.position = value

    @property
    def p_0(self) -> float:
        """Wraps to
        :attr:`osaft.core.backgroundfields.BackgroundField.p_0`
        """
        return self.field.p_0

    @p_0.setter
    def p_0(self, value) -> None:
        self.fluid.p_0 = value

    @property
    def wave_type(self) -> WaveType:
        """Wraps to
        :attr:`osaft.core.backgroundfields.BackgroundField.wave_type`
        """
        return self.field.wave_type

    @wave_type.setter
    def wave_type(self, value) -> None:
        self.field.wave_type = value

    # -------------------------------------------------------------------------
    # Wrappers for Background Field Methods
    # -------------------------------------------------------------------------

    def A_in(self, n):
        """Wraps to
        :attr:`osaft.core.backgroundfields.BackgroundField.A_in`
        """
        return self.field.A_in(n)


if __name__ == '__main__':
    pass
