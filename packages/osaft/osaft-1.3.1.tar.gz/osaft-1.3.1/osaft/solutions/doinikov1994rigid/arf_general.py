from __future__ import annotations

from abc import ABC
from typing import Optional, Union

from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.solutions.basedoinikov1994.arf_general import BaseGeneralARF
from osaft.solutions.doinikov1994rigid.arf_arbitrary_bl import ARFArbitraryBL


class ARFArbitraryRadius(ARFArbitraryBL, BaseGeneralARF, ABC):
    """Child class for ARF according to Doinikov's theory
    (viscous fluid-rigid sphere; 1994)

    .. note::
        This class implements all attributes and methods to compute the ARF
        for the case of an arbitrary particle radius.
        This class does not actually implement a method for the ARF. If you
        want to compute the ARF use
        :attr:`~osaft.solutions.doinikov1994rigid.ARF`

    :param f: Frequency [Hz]
    :param R_0: Radius of the sphere [m]
    :param rho_s: Density of the sphere [kg/m^3]
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
        ARFArbitraryBL.__init__(
            self,
            f=f, R_0=R_0,
            rho_s=rho_s, rho_f=rho_f, c_f=c_f, eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position,
            long_wavelength=long_wavelength,
            small_boundary_layer=small_boundary_layer,
            large_boundary_layer=large_boundary_layer,
            fastened_sphere=fastened_sphere,
            background_streaming=background_streaming,
            N_max=N_max,
        )
        BaseGeneralARF.__init__(self)


if __name__ == '__main__':
    pass
