from __future__ import annotations

from typing import Optional, Union

import numpy as np

from osaft import log
from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.core.warnings import EPS, raise_assumption_warning
from osaft.solutions.doinikov1994rigid.arf_general import ARFArbitraryRadius


class ARF(ARFArbitraryRadius):
    """ARF according to Doinikov's theory (viscous fluid-rigid sphere; 1994)

    There is a large number of options for the computation of the ARF in
    different limiting cases. For a more detailed explanation see
    :ref:`this example <sphx_glr_examples_tutorial_example_doinikov_1994.py>`.

    :param f: Frequency [Hz]
    :param R_0: Radius of the sphere [m]
    :param rho_s: Density of the sphere [kg/m^3]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity [Pa s]
    :param zeta_f: bulk viscosity [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param wave_type: Type of wave, traveling or standing
    :param position: Position within the standing wave field [m]
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
        position: Optional[float] = None,
        long_wavelength: bool = False,
        small_boundary_layer: bool = False,
        large_boundary_layer: bool = False,
        fastened_sphere: bool = False,
        background_streaming: bool = True,
        N_max: int = 5,
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
    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def compute_arf(self) -> float:
        """Acoustic radiation fore in [N]

        It logs the current values of :attr:`x` and :attr:`x_v`.

        :raises WrongWaveTypeError: if wrong :attr:`wave_type`
        :raises AssumptionWarning: if used solution might not be valid
        """
        # Checking wave_type
        self.check_wave_type()
        # Check Option combination
        self._check_option_combinations()

        log.info(
            'Computing the ARF with Doinikov1994Rigid.\n'
            f'x   = {self.x:+.4e} -> |x|   = {np.absolute(self.x):+.4e}\n'
            f'x_v = {self.x_v:+.4e} -> |x_v| = {np.absolute(self.x_v):+.4e}',
        )

        # Small Particle Solutions
        if not self.long_wavelength:
            return self._general_solution()

        # Checking x_v and x
        abs_x = np.abs(self.x)
        abs_x_v = np.abs(self.x_v)

        # Fastened Sphere Solution
        if self.fastened_sphere:
            if self.large_boundary_layer:
                out = self._arf_fastened_large_delta()
                test_assumption = abs_x < EPS * abs_x_v and EPS * abs_x_v < 1
            else:
                out = self._arf_fastened_small_delta()
                test_assumption = abs_x < EPS and 1 < EPS * abs_x_v
        else:
            # long wavelength and small boundary layer
            if self.small_boundary_layer:
                out = self._arf_small_particle_small_delta()
                test_assumption = abs_x < EPS and 1 < EPS * abs_x_v
            # long wavelength and large boundary layer
            elif self.large_boundary_layer:
                out = self._arf_small_particle_large_delta()
                test_assumption = abs_x < EPS * abs_x_v and EPS * abs_x_v < 1
            # long wavelength solution
            else:
                test_assumption = abs_x < EPS and abs_x < EPS * abs_x_v
                out = self._arf_small_particle()

        raise_assumption_warning(test_assumption)
        return out

    def _check_option_combinations(self):
        """Checks if the combination of options is correct
        """
        allowed_combinations = [
            # General
            (False, False, False, False, False),
            (False, False, False, False, True),
            # Long wavelength, Arbitrary Boundary Layer
            (True, False, False, False, False),
            (True, False, False, False, True),
            # Long wavelength, Small Boundary Layer
            (True, True, False, False, True),
            (True, True, False, True, True),
            # Long wavelength, Large Boundary Layer
            (True, False, True, False, True),
            (True, False, True, True, True),
        ]
        combination = (
            self.long_wavelength, self.small_boundary_layer,
            self.large_boundary_layer, self.fastened_sphere,
            self.background_streaming,
        )
        if combination not in allowed_combinations:
            raise ValueError(
                f'The chosen combination {combination} for long_wavelength,'
                'small_boundary_layer, large_boundary_layer,'
                'fastened_sphere, background streaming is not allowed.'
                f'Allowed options are: {allowed_combinations}',
            )


if __name__ == '__main__':
    pass
