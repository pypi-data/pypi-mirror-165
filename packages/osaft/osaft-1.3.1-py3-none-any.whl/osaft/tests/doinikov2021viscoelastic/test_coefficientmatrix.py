import unittest
from typing import Optional

import numpy as np
from basetest import BaseTest

import osaft.solutions.doinikov2021viscoelastic
from osaft.core.functions import BesselFunctions as Bf


class TestCoefficientMatrix(BaseTest):

    def setUp(self) -> None:
        super().setUp()

        self.cls = osaft.solutions.doinikov2021viscoelastic.ScatteringField(
            f=self.f, R_0=self.R_0,
            rho_s=self.rho_s, E_s=self.E_s, nu_s=self.nu_s,
            rho_f=self.rho_f, c_f=self.c_f,
            eta_f=self.eta_f, zeta_f=self.zeta_f,
            eta_p=self.eta_p, zeta_p=self.zeta_p,
            lambda_M=self.lambda_M,
            p_0=self.p_0, wave_type=self.wave_type,
            position=self.position,
        )

        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # generic tests
    # -------------------------------------------------------------------------

    def test_viscosity_term(self) -> None:
        self.do_testing(self.cls.viscosity_term, self.viscosity_term)

    def test_D_0(self) -> None:
        self.do_testing(self.cls.D_0, self.D_0)

    def test_a_0(self) -> None:
        self.do_testing(self.cls.a_0, self.a_0)

    def test_a_hat_0(self) -> None:
        self.do_testing(self.cls.a_hat_0, self.a_hat_0)

    def test_matrix_M(self) -> None:
        def element_test_matrix(m: int, i: int, j: int) -> complex:
            return self.cls.matrix_M(m)[i, j]

        def element_matrix(m: int, i: int, j: int) -> complex:
            return self.matrix_M(m)[i, j]

        for ix, iy in np.ndindex(self.cls.matrix_M(0).shape):
            for n in range(0, 3):
                with self.subTest(f'Matrix element {ix}, {iy}, mode {n}'):
                    self.do_testing(
                        element_test_matrix, element_matrix,
                        args_1=(n, ix, iy), args_2=(n, ix, iy),
                        threshold=1e-5,
                    )

    def test_vector_N(self):
        def element_test_vector(m: int, i: int) -> complex:
            return self.vector_N(m)[i]

        def element_vector(m: int, i: int) -> complex:
            return self.cls.vector_n(m)[i]

        for n in range(3):
            for index in range(4):
                with self.subTest(msg=f'coefficient = {n}'):
                    self.do_testing(
                        element_test_vector, element_vector,
                        args_1=(n, index), args_2=(n, index),
                    )

    def test_properties(self) -> None:
        properties = ['x_l', 'x_t', 'x_f', 'x_v']
        self._test_properties(properties)

    def test_methods_n(self) -> None:
        methods = {}
        methods['a'] = None
        methods['b'] = None
        methods['a_hat'] = None
        methods['b_hat'] = None
        self._test_methods_n(methods, n_end=6)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def omega(self):
        return 2 * np.pi * self.f

    @property
    def x_l(self):
        return self.cls.k_l * self.cls.R_0

    @property
    def x_t(self):
        return self.cls.k_t * self.cls.R_0

    @property
    def x_f(self):
        return self.cls.k_f * self.R_0

    @property
    def x_v(self):
        return self.cls.k_v * self.R_0

    @property
    def eta_c(self):
        return self.cls.fluid.eta_c

    @property
    def zeta_c(self):
        return self.cls.fluid.zeta_c

    def viscosity_term(self):
        return (
            1j * self.rho_f * self.c_f ** 2 / self.omega
            + self.zeta_c - 2 * self.eta_c / 3
        )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    def D_0(self):
        prefactor1 = self.E_s * self.cls.k_f * self.cls.x_l ** 2
        prefactor1 *= Bf.hankelh1(1, self.x_f) / (1 + self.nu_s)

        term1 = self.nu_s * Bf.besselj(0, self.x_l) / (1 - 2 * self.nu_s)
        term1 -= Bf.d2_besselj(0, self.x_l)

        prefactor2 = 1j * self.omega * self.cls.k_l * self.x_f ** 2
        prefactor2 *= Bf.besselj(1, self.x_l)

        term2 = Bf.hankelh1(0, self.x_f) * self.viscosity_term()
        term2 -= 2 * self.eta_c * Bf.d2_hankelh1(0, self.x_f)

        return prefactor1 * term1 + prefactor2 * term2

    def a_0(self):

        term1 = Bf.d2_besselj(0, self.x_l)
        term1 -= self.nu_s * Bf.besselj(0, self.x_l) / (1 - 2 * self.nu_s)
        term1 *= self.E_s * self.cls.k_f * self.x_l ** 2
        term1 *= Bf.besselj(1, self.x_f) / (1 + self.nu_s)

        term2 = 2 * self.eta_c * Bf.d2_besselj(0, self.x_f)
        term2 -= Bf.besselj(0, self.x_f) * self.viscosity_term()
        term2 *= 1j * self.omega * self.cls.k_l * self.x_f ** 2
        term2 *= Bf.besselj(1, self.x_l)

        return (term1 + term2) * self.cls.A_in(0) / self.D_0()

    def a_hat_0(self):
        return (
            self.cls.A_in(0) * self.cls.k_f * self.x_f ** 2 / self.D_0()
            * (
                Bf.hankelh1(1, self.x_f)
                * (
                    Bf.besselj(0, self.x_f) * self.viscosity_term()
                    - 2 * self.eta_c * Bf.d2_besselj(0, self.x_f)
                )
                + Bf.besselj(1, self.x_f)
                * (
                    2 * self.eta_c * Bf.d2_hankelh1(0, self.x_f)
                    - Bf.hankelh1(0, self.x_f) * self.viscosity_term()
                )
            )
        )

    def matrix_M(self, l: int) -> np.ndarray:
        M = np.zeros((4, 4), dtype=complex)

        M[0, 0] = self.x_f * Bf.d1_hankelh1(l, self.x_f)
        M[0, 1] = -l * (l + 1) * Bf.hankelh1(l, self.x_v)
        M[0, 2] = 1j * self.omega * self.x_l * Bf.d1_besselj(l, self.x_l)
        M[0, 3] = - 1j * self.omega * l * (l + 1) * Bf.besselj(l, self.x_t)
        M[1, 0] = Bf.hankelh1(l, self.x_f)
        M[1, 1] = (
            - Bf.hankelh1(l, self.x_v)
            - self.x_v * Bf.d1_hankelh1(l, self.x_v)
        )
        M[1, 2] = 1j * self.omega * Bf.besselj(l, self.x_l)
        M[1, 3] = - 1j * self.omega * (
            Bf.besselj(l, self.x_t)
            + self.x_t * Bf.d1_besselj(l, self.x_t)
        )
        M[2, 0] = self.x_f ** 2 * (
            2 * self.eta_c * Bf.d2_hankelh1(l, self.x_f)
            - self.viscosity_term()
            * Bf.hankelh1(l, self.x_f)
        )
        M[2, 1] = (
            2 * l * (l + 1) * self.eta_c
            * (
                Bf.hankelh1(l, self.x_v)
                - self.x_v * Bf.d1_hankelh1(l, self.x_v)
            )
        )
        M[2, 2] = (
            self.E_s * self.x_l ** 2 / (1 + self.nu_s)
            * (
                -Bf.d2_besselj(l, self.x_l)
                + self.nu_s
                * Bf.besselj(l, self.x_l) / (1 - 2 * self.nu_s)
            )
        )
        M[2, 3] = (
            l * (l + 1) * self.E_s / (1 + self.nu_s)
            * (
                self.x_t * Bf.d1_besselj(l, self.x_t)
                - Bf.besselj(l, self.x_t)
            )
        )
        M[3, 0] = 2 * self.eta_c * (
            self.x_f * Bf.d1_hankelh1(l, self.x_f)
            - Bf.hankelh1(l, self.x_f)
        )
        M[3, 1] = self.eta_c * ((2 - l ** 2 - l) * Bf.hankelh1(l, self.x_v)
                                - self.x_v ** 2 * Bf.d2_hankelh1(l, self.x_v))
        M[3, 2] = (
            self.E_s / (1 + self.nu_s)
            * (
                Bf.besselj(l, self.x_l)
                - self.x_l * Bf.d1_besselj(l, self.x_l)
            )
        )
        M[3, 3] = (
            self.E_s / (2 * (1 + self.nu_s))
            * (
                self.x_t ** 2 * Bf.d2_besselj(l, self.x_t)
                - (2 - l ** 2 - l) * Bf.besselj(l, self.x_t)
            )
        )
        return M

    def vector_N(self, l: int) -> np.ndarray:
        vec_n = np.zeros(4, dtype=complex)

        vec_n[0] = - self.cls.A_in(l) * self.x_f * Bf.d1_besselj(l, self.x_f)
        vec_n[1] = - self.cls.A_in(l) * Bf.besselj(l, self.x_f)
        vec_n[2] = (
            self.cls.A_in(l) * self.x_f ** 2
            * (
                self.viscosity_term() * Bf.besselj(l, self.x_f)
                - 2 * self.eta_c * Bf.d2_besselj(l, self.x_f)
            )
        )
        vec_n[3] = (
            2 * self.cls.A_in(l) * self.eta_c
            * (
                Bf.besselj(l, self.x_f)
                - self.x_f * Bf.d1_besselj(l, self.x_f)
            )
        )

        return vec_n

    def det_matrix(self, n: int, column: Optional[int] = None) -> complex:
        matrix = self.matrix_M(n).copy()
        vector = self.vector_N(n)
        if column is not None:
            matrix[:, column] = vector
        return np.linalg.det(matrix)

    def a(self, n: int) -> complex:
        if n == 0:
            return self.a_0()
        else:
            return self.det_matrix(n, 0) / self.det_matrix(n)

    def b(self, n: int) -> complex:
        if n == 0:
            return 0
        else:
            return self.det_matrix(n, 1) / self.det_matrix(n)

    def a_hat(self, n: int) -> complex:
        if n == 0:
            return self.a_hat_0()
        else:
            return self.det_matrix(n, 2) / self.det_matrix(n)

    def b_hat(self, n: int) -> complex:
        if n == 0:
            return 0
        else:
            return self.det_matrix(n, 3) / self.det_matrix(n)


if __name__ == '__main__':
    unittest.main()
