from typing import Optional, Union

from osaft import ViscousFluid, WaveType
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
    :param p_0: pressure amplitude [Pa]
    :param wave_type: wave type
    :param position: position in the standing wave field [m]
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
    ) -> None:

        # Fluid attribute (note: the frequency will be set in the base class
        # only to make sure all attributes have the same Frequency instance)
        fluid = ViscousFluid(f, rho_f, c_f, eta_f, zeta_f)

        # Init of parent class
        super().__init__(
            f=f, R_0=R_0,
            rho_s=rho_s, E_s=E_s, nu_s=nu_s,
            fluid=fluid,
            p_0=p_0, wave_type=wave_type, position=position,
            N_max=N_max,
        )

    @property
    def eta(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.eta_f`
        """
        return self.fluid.eta_f

    @property
    def zeta(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.zeta_f`
        """
        return self.fluid.zeta_f


if __name__ == '__main__':
    pass
