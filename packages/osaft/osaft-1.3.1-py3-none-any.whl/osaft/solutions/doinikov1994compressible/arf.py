from __future__ import annotations

from typing import Optional, Union

import numpy as np

from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.core.warnings import EPS, raise_assumption_warning
from osaft.solutions.doinikov1994compressible.arf_general import (
    ARFArbitraryRadius,
)


class ARF(ARFArbitraryRadius):
    """ARF class for Doinikov (viscous fluid-viscous sphere; 1994)

    There is a large number of options for the computation of the ARF in
    different limiting cases. For a more detailed explanation see
    :ref:`this example <sphx_glr_examples_tutorial_example_doinikov_1994.py>`.

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
    :param wave_type: Type of wave, traveling or standing
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
        wave_type: WaveType = WaveType.STANDING,
        position: Optional[float] = None,
        small_boundary_layer: bool = False,
        large_boundary_layer: bool = False,
        background_streaming: bool = True,
        N_max: int = 5,
    ) -> None:
        """Constructor method
        """

        # init of parent class
        super().__init__(
            f=f, R_0=R_0,
            rho_s=rho_s, c_s=c_s, eta_s=eta_s, zeta_s=zeta_s,
            rho_f=rho_f, c_f=c_f, eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position,
            small_boundary_layer=small_boundary_layer,
            large_boundary_layer=large_boundary_layer,
            N_max=N_max, background_streaming=background_streaming,
        )

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def compute_arf(self) -> float:
        """Acoustic radiation fore in [N]

        It logs the current values of :attr:`x` and :attr:`x_v`.

        :raises WrongWaveTypeError: if wrong :attr:`wave_type`
        :raises AssumptionWarning: if used solution might not be valid
        """

        # Checking Wave Type
        self.check_wave_type()

        # Checking x_v and x
        abs_x = np.abs(self.x)
        abs_x_v = np.abs(self.x_v)

        # Cases
        if self.small_boundary_layer and (
            not
            self.large_boundary_layer
        ):
            test = abs_x < EPS and 1 < EPS * abs_x_v
            raise_assumption_warning(test)
            return self._arf_small_particle_small_delta()
        elif (
                not self.small_boundary_layer and
                self.large_boundary_layer
        ):
            test = abs_x < EPS * abs_x_v and abs_x_v < EPS
            raise_assumption_warning(test)
            return self._arf_small_particle_large_delta()
        elif (
                not self.small_boundary_layer and
                not self.large_boundary_layer
        ):
            return self._general_solution()
        else:
            raise ValueError(
                'Small and large viscous boundary layer options cannot'
                'both be True.',
            )


if __name__ == '__main__':
    pass
