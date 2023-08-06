from __future__ import annotations

from abc import ABC

import numpy as np

from osaft import BackgroundField, ViscousFluid
from osaft.core.functions import conj, pi, sin
from osaft.core.geometries import Sphere
from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.solutions.base_arf import BaseARF


class BaseARFLimiting(BaseARF, ABC):
    """Abstract base class for the computation of the acoustic radiation
    in the models by Doinikov in limiting cases.
    """

    # Required attributes of child class
    _small_boundary_layer: PassiveVariable
    _large_boundary_layer: PassiveVariable
    _background_streaming: PassiveVariable
    field: BackgroundField
    fluid: ViscousFluid
    sphere: Sphere

    # Required properties of child class
    abs_pos: float
    delta: float
    k_f: complex
    R_0: float
    rho_f: float
    x: complex
    x_v: complex

    def __init__(self):

        # Dependent variables
        self._norm_delta = ActiveVariable(
            self._compute_norm_delta,
            'normalized boundary layer thickness',
        )
        self._norm_delta.is_computed_by(
            self.fluid._delta, self.sphere._R_0,
        )

    # -------------------------------------------------------------------------
    # Getters and Setters for independent variables
    # -------------------------------------------------------------------------

    @property
    def small_boundary_layer(self) -> bool:
        """Use limiting case of a small viscous boundary layer :math:`\\delta`

        :getter: returns if a small viscous boundary layer case is used
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._small_boundary_layer.value

    @small_boundary_layer.setter
    def small_boundary_layer(self, value):
        self._small_boundary_layer.value = value

    @property
    def large_boundary_layer(self) -> bool:
        """Use limiting case of a large viscous boundary layer :math:`\\delta`

        :getter: returns if a large viscous boundary layer case is used
        :setter: automatically invokes
            :func:`osaft.core.variable.BaseVariable.notify`
        """
        return self._large_boundary_layer.value

    @large_boundary_layer.setter
    def large_boundary_layer(self, value):
        self._large_boundary_layer.value = value

    @property
    def background_streaming(self) -> bool:
        """Background streaming contribution to the ARF

        :getter: returns if background streaming is considered
        :setter: automatically invokes
            :func:`osaft.core.variable.BaseVariable.notify`
        """
        return self._background_streaming.value

    @background_streaming.setter
    def background_streaming(self, value):
        self._background_streaming.value = value

    # -------------------------------------------------------------------------
    # Background Streaming Contribution
    # -------------------------------------------------------------------------

    def _F_2_standing(self) -> float:
        # F2 according to (5.17)
        x_con = self.x.conjugate()

        F2 = self.x - x_con
        F2 *= sin(self.abs_pos * (self.k_f + conj(self.k_f)))
        F2 *= sin(self.x + x_con) / (self.x + x_con)

        tmp = self.x + x_con
        tmp *= sin(self.abs_pos * (self.k_f - conj(self.k_f)))

        # prevent division by zero error
        if self.x.imag > 1e-5:  # pragma: no cover
            tmp *= np.sinh(2 * self.x.imag) / (2 * self.x.imag)

        F2 -= tmp
        F2 *= -self.x * x_con / self.x_v**2
        F2 *= self.rho_f * pi * 0.75 * self.field.abs_A_squared

        return F2.real

    def _F_2_travelling(self) -> float:
        # F2 according to (5.12)
        x_con = self.x.conjugate()
        F2 = -self.x * x_con * (self.x + x_con) * 1j / self.x_v**2
        F2 *= sin(self.x - x_con) / (self.x - x_con)
        F2 *= self.rho_f * pi * 1.5 * self.field.abs_A_squared
        return F2.real


if __name__ == '__main__':
    pass
