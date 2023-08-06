from typing import Optional, Union

from osaft import ViscoelasticFluid, WaveType
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.solutions.basedoinikov2021.scattering import (
    BaseScatteringDoinikov2021,
)


class ScatteringField(BaseScatteringDoinikov2021):
    """Scattering field class for Doinikov (viscous fluid-elastic sphere; 2021)

    :param f: frequency [Hz]
    :param R_0: radius [m]
    :param rho_s: density of the particle [kg/m^3]
    :param E_s: Young's modulus of the particle [Pa]
    :param nu_s: Poisson's ratio of the particle [-]
    :param rho_f: density of the fluid [kg/m^3]
    :param c_f: speed of sound in the fluid [m/s]
    :param eta_f: fluid component shear viscosity [Pa s]
    :param zeta_f: fluid component bulk viscosity [Pa s]
    :param eta_p: shear viscosity of polymer component [Pa s]
    :param zeta_p: bulk viscosity of polymer component [Pa s]
    :param lambda_M: relaxation time of fluid [s]
    :param p_0: pressure amplitude [Pa]
    :param wave_type: wave type
    :param position: position in the standing wave field [m]
    """

    def __init__(
            self,
            f: Union[Frequency, float], R_0: Union[Sphere, float],
            rho_s: float, E_s: float, nu_s: float,
            rho_f: float, c_f: float,
            eta_f: float, zeta_f: float,
            eta_p: float, zeta_p: float,
            lambda_M: float,
            p_0: float, wave_type: WaveType,
            position: Optional[float] = None,
            N_max: int = 5,
    ) -> None:

        # Fluid attribute (note: the frequency will be set in the base class
        # only to make sure all attributes have the same Frequency instance)
        fluid = ViscoelasticFluid(
            frequency=f, rho=rho_f, c=c_f, eta_f=eta_f, zeta_f=zeta_f,
            eta_p=eta_p, zeta_p=zeta_p, lambda_M=lambda_M,
        )

        # Init of parent class
        super().__init__(
            f=f, R_0=R_0,
            rho_s=rho_s, E_s=E_s, nu_s=nu_s,
            fluid=fluid,
            p_0=p_0, wave_type=wave_type, position=position,
            N_max=N_max,
        )

    # -------------------------------------------------------------------------
    # Required Methods
    # -------------------------------------------------------------------------

    @property
    def eta(self) -> complex:
        """ Wraps to :attr:`osaft.core.fluids.ViscoelasticFluid.eta_c`
        """
        return self.fluid.eta_c

    @property
    def zeta(self) -> complex:
        """ Wraps to :attr:`osaft.core.fluids.ViscoelasticFluid.zeta_c`
        """
        return self.fluid.zeta_c

    # -------------------------------------------------------------------------
    # Wrappers specific to viscoelastic model
    # -------------------------------------------------------------------------

    @property
    def eta_p(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscoelasticFluid.eta_p`
        """
        return self.fluid.eta_p

    @eta_p.setter
    def eta_p(self, value) -> None:
        self.fluid.eta_p = value

    @property
    def zeta_p(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscoelasticFluid.zeta_p`
        """
        return self.fluid.zeta_p

    @zeta_p.setter
    def zeta_p(self, value) -> None:
        self.fluid.zeta_p = value

    @property
    def lambda_M(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscoelasticFluid.lambda_M`
        """
        return self.fluid.lambda_M

    @lambda_M.setter
    def lambda_M(self, value) -> None:
        self.fluid.lambda_M = value


if __name__ == '__main__':
    pass
