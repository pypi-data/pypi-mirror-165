from abc import ABC
from typing import Optional, Union

from osaft import WaveType
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.solutions.basedoinikov1994.arf_general import BaseGeneralARF
from osaft.solutions.doinikov1994compressible.arf_limiting import ARFLimiting


class ARFArbitraryRadius(ARFLimiting, BaseGeneralARF, ABC):
    """Base class for Doinikov (viscous fluid-viscous sphere; 1994)

    .. note::
        This class implements all attributes and methods to compute the ARF
        for the case of an arbitrary particle radius.
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
        rho_s: float,
        c_s: float,
        eta_s: float,
        zeta_s: float,
        rho_f: float,
        c_f: float,
        eta_f: float,
        zeta_f: float,
        p_0: float,
        wave_type: WaveType,
        position: Optional[float],
        small_boundary_layer: bool,
        large_boundary_layer: bool,
        background_streaming: bool,
        N_max: int,
    ) -> None:

        # Call to init method of parent class
        ARFLimiting.__init__(
            self,
            f=f, R_0=R_0,
            rho_s=rho_s, c_s=c_s, eta_s=eta_s, zeta_s=zeta_s,
            rho_f=rho_f, c_f=c_f, eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position,
            N_max=N_max,
            small_boundary_layer=small_boundary_layer,
            large_boundary_layer=large_boundary_layer,
            background_streaming=background_streaming,
        )
        BaseGeneralARF.__init__(self)
