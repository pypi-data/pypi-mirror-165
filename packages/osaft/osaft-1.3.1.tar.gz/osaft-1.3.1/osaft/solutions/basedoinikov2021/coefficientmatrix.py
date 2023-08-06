from abc import ABC
from typing import Optional, Union

import numpy as np

from osaft import ViscoelasticFluid, ViscousFluid, WaveType
from osaft.core.frequency import Frequency
from osaft.core.functions import BesselFunctions as Bf
from osaft.core.geometries import Sphere
from osaft.core.variable import ActiveListVariable
from osaft.solutions.basedoinikov2021.base import BaseDoinikov


class CoefficientMatrix(BaseDoinikov, ABC):
    """Coefficient matrix class for scattering field class for Doinikov
    (viscous fluid-elastic sphere; 2021)

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

    def __init__(
            self,
            f: Union[Frequency, float],
            R_0: Union[Sphere, float],
            rho_s: float, E_s: float, nu_s: float,
            fluid: Union[ViscousFluid, ViscoelasticFluid],
            p_0: float, wave_type: WaveType,
            position: Optional[float] = None,
    ) -> None:
        """Constructor method
        """

        super().__init__(
            f=f, R_0=R_0,
            rho_s=rho_s, E_s=E_s, nu_s=nu_s,
            fluid=fluid,
            p_0=p_0, wave_type=wave_type, position=position,
        )
        self._list_matrix_M_n = ActiveListVariable(
            self._compute_matrix_M,
            'Matrices M(n)',
        )

        self._list_matrix_M_n.is_computed_by(
            self._x_f, self._x_v, self._x_l, self._x_t,
        )

        self._list_vector_n = ActiveListVariable(
            self._compute_vector_n,
            'Vectors N(n)',
        )
        self._list_vector_n.is_computed_by(
            self._x_f, self.field._A_in,
        )

    def det_M_n(self, n: int, column: Optional[int] = None) -> complex:
        """Determinant of the matrix `M` for the mode `n`

        :param n: mode
        :param column: the `l`th coefficient is replaced with the vector `N`
        """
        matrix = self.matrix_M(n).copy()
        vector = self.vector_n(n)
        if column is not None:
            matrix[:, column] = vector
        return np.linalg.det(matrix)

    def matrix_M(self, n: int) -> np.ndarray:
        """Matrix :math:`M_l`

        (Eq. A19 - A 22)

        :param n: mode
        """
        return self._list_matrix_M_n.item(n)

    def vector_n(self, n: int) -> np.ndarray:
        """Vector :math:`n_l`

        (Eq. A19 - A 22)

        :param n: mode
        """
        return self._list_vector_n.item(n)

    def _compute_matrix_M(self, l: int) -> np.ndarray:
        """Matrix :math:`M_l`

        (Eq. A19 - A 22)

        :param l: mode
        :return: matrix M_l
        """
        M = np.zeros((4, 4), dtype=complex)

        # First Row
        M[0, 0] = self.x_f * Bf.d1_hankelh1(l, self.x_f)
        M[0, 1] = -l * (l + 1) * Bf.hankelh1(l, self.x_v)
        M[0, 2] = 1j * self.omega * self.x_l * Bf.d1_besselj(l, self.x_l)
        M[0, 3] = - 1j * self.omega * l * (l + 1) * Bf.besselj(l, self.x_t)
        M[1, 0] = Bf.hankelh1(l, self.x_f)
        M[1, 1] = - Bf.hankelh1(l, self.x_v)
        M[1, 1] -= self.x_v * Bf.d1_hankelh1(l, self.x_v)
        M[1, 2] = 1j * self.omega * Bf.besselj(l, self.x_l)
        M[1, 3] = Bf.besselj(l, self.x_t)
        M[1, 3] += self.x_t * Bf.d1_besselj(l, self.x_t)
        M[1, 3] *= - 1j * self.omega

        # Second Column
        M[2, 0] = 2 * self.eta * Bf.d2_hankelh1(l, self.x_f)
        M[2, 0] -= self.viscosity_term() * Bf.hankelh1(l, self.x_f)
        M[2, 0] *= self.x_f ** 2
        M[2, 1] = Bf.hankelh1(l, self.x_v)
        M[2, 1] -= self.x_v * Bf.d1_hankelh1(l, self.x_v)
        M[2, 1] *= 2 * l * (l + 1) * self.eta
        M[2, 2] = -Bf.d2_besselj(l, self.x_l)
        M[2, 2] += self.nu_s * Bf.besselj(l, self.x_l) / (1 - 2 * self.nu_s)
        M[2, 2] *= self.E_s * self.x_l ** 2 / (1 + self.nu_s)
        M[2, 3] = self.x_t * Bf.d1_besselj(l, self.x_t)
        M[2, 3] -= Bf.besselj(l, self.x_t)
        M[2, 3] *= l * (l + 1) * self.E_s / (1 + self.nu_s)

        # Third Column
        M[3, 0] = self.x_f * Bf.d1_hankelh1(l, self.x_f)
        M[3, 0] -= Bf.hankelh1(l, self.x_f)
        M[3, 0] *= 2 * self.eta
        M[3, 1] = (2 - l ** 2 - l) * Bf.hankelh1(l, self.x_v)
        M[3, 1] -= self.x_v ** 2 * Bf.d2_hankelh1(l, self.x_v)
        M[3, 1] *= self.eta
        M[3, 2] = Bf.besselj(l, self.x_l)
        M[3, 2] -= self.x_l * Bf.d1_besselj(l, self.x_l)
        M[3, 2] *= self.E_s / (1 + self.nu_s)
        M[3, 3] = self.x_t ** 2 * Bf.d2_besselj(l, self.x_t)
        M[3, 3] -= (2 - l ** 2 - l) * Bf.besselj(l, self.x_t)
        M[3, 3] *= self.E_s / (2 * (1 + self.nu_s))
        return M

    def _compute_vector_n(self, l: int) -> np.array:
        """Vector :math:`n_l`

        (Eq. A19 - A 22)

        :param l: mode
        :return: matrix M_l
        """
        vec_n = np.zeros(4, dtype=complex)

        vec_n[0] = - self.A_in(l) * self.x_f * Bf.d1_besselj(l, self.x_f)
        vec_n[1] = - self.A_in(l) * Bf.besselj(l, self.x_f)
        vec_n[2] = self.viscosity_term() * Bf.besselj(l, self.x_f)
        vec_n[2] -= 2 * self.eta * Bf.d2_besselj(l, self.x_f)
        vec_n[2] *= self.A_in(l) * self.x_f ** 2
        vec_n[3] = Bf.besselj(l, self.x_f)
        vec_n[3] -= self.x_f * Bf.d1_besselj(l, self.x_f)
        vec_n[3] *= 2 * self.A_in(l) * self.eta

        return vec_n

    def viscosity_term(self) -> complex:
        """ Often used function of fluids shear and bulk viscosity
        """
        return (
            1j * self.rho_f * self.c_f ** 2 / self.omega
            + self.zeta - 2 * self.eta / 3
        )

    def a_0(self):
        """Coefficient :math:`a_0` [m^2/s]

        (Eq. A15)

        :return: coefficient a_0
        """
        term1 = Bf.d2_besselj(0, self.x_l)
        term1 -= self.nu_s * Bf.besselj(0, self.x_l) / (1 - 2 * self.nu_s)
        term1 *= self.E_s * self.k_f * self.x_l ** 2
        term1 *= Bf.besselj(1, self.x_f) / (1 + self.nu_s)

        term2 = 2 * self.eta * Bf.d2_besselj(0, self.x_f)
        term2 -= Bf.besselj(0, self.x_f) * self.viscosity_term()
        term2 *= 1j * self.omega * self.k_l * self.x_f ** 2
        term2 *= Bf.besselj(1, self.x_l)

        return (term1 + term2) * self.A_in(0) / self.D_0()

    def a_hat_0(self):
        """Coefficient :math:`\\hat{a}_0` [m^2/s]

        (Eq. A15)

        :return: coefficient a_0
        """
        prefactor = self.A_in(0) * self.k_f * self.x_f ** 2 / self.D_0()

        term1 = Bf.besselj(0, self.x_f) * self.viscosity_term()
        term1 -= 2 * self.eta * Bf.d2_besselj(0, self.x_f)
        term1 *= Bf.hankelh1(1, self.x_f)

        term2 = 2 * self.eta * Bf.d2_hankelh1(0, self.x_f)
        term2 -= Bf.hankelh1(0, self.x_f) * self.viscosity_term()
        term2 *= Bf.besselj(1, self.x_f)

        return prefactor * (term1 + term2)

    def D_0(self):
        """Coefficient :math:`D_0`

        (Eq. A17)

        :return: coefficient D_0
        """
        prefactor1 = self.E_s * self.k_f * self.x_l ** 2
        prefactor1 *= Bf.hankelh1(1, self.x_f) / (1 + self.nu_s)

        term1 = self.nu_s * Bf.besselj(0, self.x_l) / (1 - 2 * self.nu_s)
        term1 -= Bf.d2_besselj(0, self.x_l)

        prefactor2 = 1j * self.omega * self.k_l * self.x_f ** 2
        prefactor2 *= Bf.besselj(1, self.x_l)

        term2 = Bf.hankelh1(0, self.x_f) * self.viscosity_term()
        term2 -= 2 * self.eta * Bf.d2_hankelh1(0, self.x_f)

        return prefactor1 * term1 + prefactor2 * term2

    if __name__ == '__main__':
        pass
