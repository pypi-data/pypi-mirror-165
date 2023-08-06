import unittest
from functools import cache

import mpmath
from doinikov1994rigid.setup_test_arf import BaseTestARF
from numpy import inf
from scipy.special import factorial

import osaft
from osaft.core.functions import BesselFunctions as Bf
from osaft.core.functions import conj, full_range, integrate, pi


class TestARFGeneral(BaseTestARF):

    def setUp(self) -> None:

        super().setUp()

        self.H_nm_combination_dict = {
            -1: (
                (self.cls.x, self.cls.x_v, ((0, 0),)),
                (self.cls.x_v, self.cls.x, ((0, 0),)),
            ),
            0: (
                (self.cls.x, self.cls.x, ((1, 0), (0, 1))),
                (self.cls.x_v, self.cls.x_v, ((1, 0), (0, 1))),
                (self.cls.x, self.cls.x_v, ((1, 0), (0, 1))),
                (self.cls.x_v, self.cls.x, ((1, 0), (0, 1))),
            ),
            1: (
                (self.cls.x, self.cls.x, ((0, 0),)),
                (self.cls.x, self.cls.x_v, ((0, 0),)),
                (self.cls.x_v, self.cls.x, ((0, 0),)),
            ),
            2: (
                (self.cls.x, self.cls.x, ((1, 0), (0, 1))),
                (self.cls.x_v, self.cls.x_v, ((1, 0), (0, 1))),
                (self.cls.x, self.cls.x_v, ((1, 0), (0, 1))),
                (self.cls.x_v, self.cls.x, ((1, 0), (0, 1))),
            ),
        }

        self.J_nm_combination_dict = {
            -1: (
                (self.cls.x_v, self.cls.x, ((0, 0),)),
            ),
            0: (
                (self.cls.x, self.cls.x, ((1, 0), (0, 1))),
                (self.cls.x_v, self.cls.x, ((1, 0), (0, 1))),
            ),
            1: (
                (self.cls.x, self.cls.x, ((0, 0),)),
                (self.cls.x_v, self.cls.x, ((0, 0),)),
            ),
            2: (
                (self.cls.x, self.cls.x, ((1, 0), (0, 1))),
                (self.cls.x_v, self.cls.x, ((1, 0), (0, 1))),
            ),
        }

    def test_coefficients(self) -> None:
        # test first for l = 1
        method_dict = {}
        method_dict['G_n_l'] = (1, self.cls.x)  # l = 1
        method_dict['L_n_l'] = 1  # l = 1
        method_dict['K_n_l'] = 1  # l = 1

        self._test_methods_n(method_dict)

        # test first for l = 2
        method_dict = {}
        method_dict['G_n_l'] = (1, self.cls.x)  # l = 2
        method_dict['L_n_l'] = 2  # l = 2
        method_dict['K_n_l'] = 2  # l = 2

        self._test_methods_n(method_dict)

    def test_G_sum_1(self):
        for n in range(0, 5):
            first = self.cls.G_sum_1(n)
            second = self.cls.G_sum_1(n)
            self.assertAlmostEqual(abs(first), abs(second))

    def test_G_sum_2(self):
        for n in range(0, 5):
            first = self.cls.G_sum_2(n)
            second = self.cls.G_sum_2(n)
            self.assertAlmostEqual(abs(first), abs(second))

    def test_G_error(self):
        self.assertRaises(ValueError, self.cls.G_n_l, 1, 3, 1)

    def test_L_sum(self):
        for n in range(0, 5):
            first = self.cls.L_sum(n)
            second = self.cls.L_sum(n)
            self.assertAlmostEqual(abs(first), abs(second))

    def test_L_error(self):
        self.assertRaises(ValueError, self.cls.L_n_l, 1, 3)

    def test_K_sum(self):
        for n in range(0, 5):
            first = self.cls.K_sum(n)
            second = self.cls.K_sum(n)
            self.assertAlmostEqual(abs(first), abs(second))

    def test_K_error(self):
        self.assertRaises(ValueError, self.cls.K_n_l, 1, 3)

    @unittest.skip('Test not working due to numerical problems.')
    def test_G_sum_1_compare(self):
        for n in range(0, 5):
            first = self.cls.G_sum_1(n)
            second = (
                self.cls.G_n_l(n, 1, self.cls.x)
                + self.cls.G_n_l(n, 2, self.cls.x)
            ) / 2
            self.assertAlmostEqual(abs(first), abs(second), 1e-3)

    @unittest.skip('Test not working due to numerical problems.')
    def test_G_sum_2_compare(self):
        for n in range(0, 4):
            first = self.cls.G_sum_2(n)
            second = (
                self.cls.G_n_l(n, 1, self.cls.x.conjugate()).conjugate()
                + self.cls.G_n_l(n, 2, self.cls.x)
            ) / 2
            self.assertAlmostEqual(first, second, 1e-5)

    @unittest.skip('Test not working due to numerical problems.')
    def test_L_sum_compare(self):
        for n in range(0, 5):
            first = self.cls.L_sum(n)
            second = (
                self.cls.L_n_l(n, 1)
                + self.cls.L_n_l(n, 2)
            ) / 2
            print(f'{first = }')
            print(f'{second = }')
            self.assertAlmostEqual(abs(first), abs(second), 1e-2)

    @unittest.skip('Test not working due to numerical problems.')
    def test_K_sum_compare(self):
        for n in range(0, 4):
            first = self.cls.K_sum(n)
            second = (
                self.cls.K_n_l(n, 1)
                + self.cls.K_n_l(n, 2)
            ) / 2
            self.assertAlmostEqual(first, second, 1e-3)

    def test_H_nm_j(self):
        # Testing only combinations of j, (n, m), and x, x_v that are used in
        # the paper
        self.run_integration_test(
            self.cls.H_nm_j, self.H_nm_j,
            self.H_nm_combination_dict,
        )

    def test_J_nm_j(self):
        # Testing only combinations of j, (n, m), and x, x_v that are used in
        # the paper
        self.run_integration_test(
            self.cls.J_nm_j, self.J_nm_j,
            self.J_nm_combination_dict,
        )

    # -------------------------------------------------------------------------
    # K_n_l
    # -------------------------------------------------------------------------

    def K_n_l(self, n: int, l: int) -> complex:
        if l == 1:
            return self.K_n_1(n)
        else:
            return self.K_n_2(n)

    def K_n_1(self, n: int) -> complex:
        x_con = self.cls.x.conjugate()

        tmp1 = Bf.d1_hankelh1(n, x_con)
        tmp2 = Bf.d1_hankelh1(n + 1, x_con)

        out = (n + 1) * x_con ** 2 / self.cls.x_v ** 2 * tmp1
        out *= Bf.hankelh1(n, self.cls.x_v)

        out -= x_con * Bf.d1_hankelh1(n + 1, self.cls.x_v) * tmp2
        return out

    def K_n_2(self, n: int) -> complex:
        x_con = self.cls.x.conjugate()

        tmp1 = Bf.d1_hankelh2(n, x_con)
        tmp2 = Bf.d1_hankelh2(n + 1, x_con)

        out = (n + 1) * x_con ** 2 / self.cls.x_v ** 2 * tmp1
        out *= Bf.hankelh1(n, self.cls.x_v)

        out -= x_con * Bf.d1_hankelh1(n + 1, self.cls.x_v) * tmp2
        return out

    def K_sum(self, n: int):
        x_v = self.x_v
        x_con = self.x.conjugate()
        prefactor = (n + 1) * x_con**2 / x_v**2
        term_1 = Bf.hankelh1(n, x_v) * Bf.d1_besselj(n, x_con)
        term_2 = x_con * Bf.d1_hankelh1(n + 1, x_v)
        term_2 *= Bf.d1_besselj(n + 1, x_con)
        return prefactor * term_1 - term_2

    # -------------------------------------------------------------------------
    # L_n_l
    # -------------------------------------------------------------------------

    def L_n_l(self, n: int, l: int) -> complex:
        if l == 1:
            return self.L_n_1(n)
        else:
            return self.L_n_2(n)

    def L_n_1(self, n: int) -> complex:
        x_v_con = self.cls.x_v.conjugate()
        tmp1 = Bf.d1_hankelh1(n, self.cls.x)
        tmp2 = Bf.d1_hankelh1(n + 1, self.cls.x)

        out = -(n + 1) * self.cls.x ** 2 / self.cls.x_v ** 2 * tmp2
        out *= Bf.hankelh2(n + 1, x_v_con)

        out += self.cls.x * Bf.d1_hankelh2(n, x_v_con) * tmp1
        return out

    def L_n_2(self, n: int) -> complex:
        x_v_con = self.cls.x_v.conjugate()
        tmp1 = Bf.d1_hankelh2(n, self.cls.x)
        tmp2 = Bf.d1_hankelh2(n + 1, self.cls.x)

        out = -(n + 1) * self.cls.x ** 2 / self.cls.x_v ** 2 * tmp2
        out *= Bf.hankelh2(n + 1, x_v_con)

        out += self.cls.x * Bf.d1_hankelh2(n, x_v_con) * tmp1
        return out

    def L_sum(self, n: int) -> complex:
        x = self.x
        x_v = self.x_v
        x_v_con = self.x_v.conjugate()
        term_1 = x * Bf.d1_hankelh2(n, x_v_con) * Bf.d1_besselj(n, x)
        term_2 = (n + 1) * x ** 2 / x_v ** 2 * Bf.hankelh2(n + 1, x_v_con)
        term_2 *= Bf.d1_besselj(n + 1, x)
        return term_1 - term_2

    # ------------------------------------------------------------------------
    # G_n_l
    # ------------------------------------------------------------------------

    def G_n_l(self, n: int, l: int, x: complex) -> complex:
        if l == 1:
            return self.G_n_1(n, x)
        else:
            return self.G_n_2(n, x)

    def G_n_1(self, n: int, x: complex) -> complex:
        x_con = x.conjugate()
        tmp1 = Bf.d1_hankelh1(n, x_con)
        tmp2 = Bf.d1_hankelh1(n + 1, x_con)

        out = x_con * Bf.d1_hankelh1(n, x) * tmp1
        out += x * Bf.d1_hankelh1(n + 1, x) * tmp2
        return out

    def G_n_2(self, n: int, x: complex) -> complex:
        x_con = x.conjugate()
        tmp1 = Bf.d1_hankelh2(n, x_con)
        tmp2 = Bf.d1_hankelh2(n + 1, x_con)

        out = x_con * Bf.d1_hankelh1(n, x) * tmp1
        out += x * Bf.d1_hankelh1(n + 1, x) * tmp2
        return out

    def G_sum_1(self, n: int) -> complex:
        x = self.x
        x_con = self.x.conjugate()
        bessel_n = Bf.d1_besselj(n, x_con)
        bessel_n1 = Bf.d1_besselj(n + 1, x_con)
        term_1 = x_con * Bf.d1_hankelh1(n, x) * bessel_n
        term_2 = x * Bf.d1_hankelh1(n + 1, x) * bessel_n1
        return term_1 + term_2

    def G_sum_2(self, n):
        x = self.x
        x_con = self.x.conjugate()
        bessel_n = Bf.d1_besselj(n, x)
        bessel_n1 = Bf.d1_besselj(n + 1, x)
        term_1 = x_con * Bf.d1_hankelh1(n, x_con) * bessel_n
        term_2 = x * Bf.d1_hankelh1(n + 1, x_con) * bessel_n1
        return -(term_1 + term_2)

    # -------------------------------------------------------------------------
    # H_nm_j, J_nm_j, B_qk
    # -------------------------------------------------------------------------

    def H_nm_j(self, x1: complex, x2: complex, n: int, m: int, j: int):

        out = mpmath.mpc(0)
        arg_1 = mpmath.mpc(1j * x2.conjugate() - 1j * x1)
        for k in full_range(n):
            for q in full_range(m):
                M = 2 + k + q + j
                term = mpmath.expint(M, arg_1)
                term *= mpmath.mpc(x1 ** (-(k + 1)))
                term *= mpmath.mpc(x2.conjugate() ** (-(q + 1)))
                term *= self.B_kq(k, q, m, n)
                out += term
        return complex(out)

    @cache
    def J_nm_j(
            self,
            x1: complex,
            x2: complex,
            n: int,
            m: int,
            j: int,
    ) -> complex:
        """Coefficient :math:`J_{nm}^{(j)}`

        :param x1: argument x1
        :param x2: argument x2
        :param n: order n
        :param m: order m
        :param j: exponent
        """
        if 1.01 * abs(x1.real) > abs(x1.imag) > 0.99 * abs(x1.real):
            return self.J_nm_j_quadrature(x1, x2, n, m, j)
        else:
            return self.J_nm_j_sum(x1, x2, n, m, j)

    def J_nm_j_quadrature(
            self, x1: complex, x2: complex,
            n: int, m: int, j: int,
    ):

        def kernel(y: float) -> complex:
            out = y ** (-j) * Bf.hankelh1(n, x1 * y)
            out *= Bf.besselj(m, x2.conjugate() * y)
            return out

        return self.integrate_J_nm_H_nm(kernel)

    def J_nm_j_sum(self, x1: complex, x2: complex, n: int, m: int, j: int):

        arg_1 = mpmath.mpc(1j * x2.conjugate() - 1j * x1)
        arg_2 = mpmath.mpc(- 1j * x2.conjugate() - 1j * x1)
        out = mpmath.mpc(0)
        for k in full_range(n):
            for q in full_range(m):
                M = 2 + k + q + j
                term = mpmath.expint(M, arg_1)
                term -= (- 1) ** (q + m) * mpmath.expint(M, arg_2)
                term *= mpmath.mpc(x1 ** (-(k + 1)))
                term *= mpmath.mpc(x2.conjugate() ** (-(q + 1)))
                term *= self.B_kq(k, q, m, n)
                out += term
        return complex(0.5 * out)

    @staticmethod
    def integrate_J_nm_H_nm(kernel):

        def real_kernel(y: float) -> float:
            return kernel(y).real

        def imag_kernel(y: float) -> float:
            return kernel(y).imag

        real_part, _ = integrate(real_kernel, 1, inf, rel_eps=1e-6)
        imag_part, _ = integrate(imag_kernel, 1, inf, rel_eps=1e-6)

        return real_part + 1j * imag_part

    def run_integration_test(self, fun_1, fun_2, combination_dict):
        range_N_max = full_range(0, 3)
        for j in combination_dict:
            for x1, x2, list_deltas in combination_dict[j]:
                for delta in list_deltas:
                    for n in range_N_max:
                        delta_n, delta_m = delta
                        n, m = n + delta_n, n + delta_m
                        msg = f'{x1 = }, {x2 = }, {j = }, {n = }, {m = }'
                        with self.subTest(msg=msg):
                            self.assertAlmostEqual(
                                fun_1(x1, x2, n, m, j),
                                fun_2(x1, x2, n, m, j),
                                threshold=1e-3,
                            )

    # -------------------------------------------------------------------------
    # B_qk
    # -------------------------------------------------------------------------

    @staticmethod
    def B_kq(k: int, q: int, m: int, n: int) -> complex:
        out = 1j ** (m - n) * (-1) ** k * factorial(n + k) * factorial(
            m + q,
        )
        out /= (2 * 1j) ** (k + q) * factorial(k) * factorial(n - k)
        out /= factorial(q) * factorial(m - q)
        return out

    def test_B_kq(self):

        for m in full_range(4):
            for n in full_range(4):
                for q in full_range(m):
                    for k in full_range(n):
                        self.assertEqual(
                            self.cls.B_kq(k, q, m, n),
                            self.B_kq(k, q, m, n),
                        )

    # -------------------------------------------------------------------------
    # S_1n
    # -------------------------------------------------------------------------

    def S_1n(self, n: int) -> complex:

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v
        H = self.H_nm_j

        first = ((n + 2) * x ** 2 - n * x_conj ** 2) / 2
        first *= H(x, x, n, n + 1, 0) - H(x, x, n, n + 1, 2)
        second = x * x_conj * (H(x, x, n + 1, n, 0) - H(x, x, n + 1, n, 2))
        third = x * x_conj / x_v ** 2 * self.G_n_2(n, x)
        fourth = n * x_conj * H(x, x, n, n, 1)
        fourth += (n + 2) * x * H(x, x, n + 1, n + 1, 1)
        fourth -= x * x_conj * H(x, x, n + 1, n, 0)
        fourth *= (x ** 2 - x_conj ** 2) / x_v ** 2

        return first - second + third + fourth

    def S_2n(self, n: int) -> complex:

        x_v = self.cls.x_v
        x_v_conj = self.cls.x_v.conjugate()
        H = self.H_nm_j

        first = H(x_v, x_v, n + 1, n, 0) - H(x_v, x_v, n + 1, n, 2)
        first *= x_v * x_v_conj
        second = H(x_v, x_v, n, n + 1, 0) - H(x_v, x_v, n, n + 1, 2)
        second *= (n + 1) * x_v ** 2
        third = Bf.hankelh1(n, x_v) * Bf.d1_hankelh2(n, x_v_conj)
        third += Bf.d1_hankelh1(n + 1, x_v) * Bf.hankelh2(n + 1, x_v_conj)
        third *= (n + 1)

        return n * (n + 2) * (first - second - third)

    def S_3n(self, n: int) -> complex:

        x = self.cls.x
        x_v = self.cls.x_v
        x_v_conj = self.cls.x_v.conjugate()
        H = self.H_nm_j

        first = H(x, x_v, n, n + 1, 0) - H(x, x_v, n, n + 1, 2)
        first *= 0.5 * (n * x_v_conj ** 2 - (n + 1) * x ** 2)

        second = H(x, x_v, n + 1, n, 0) - H(x, x_v, n + 1, n, 2)
        second *= x * x_v_conj

        third = H(x, x_v, n, n, -1) - H(x, x_v, n, n, 1)
        third *= 0.5 * x ** 2 * x_v_conj

        fourth = H(x, x_v, n + 1, n + 1, -1) - H(x, x_v, n + 1, n + 1, 1)
        fourth *= 0.5 * x * x_v ** 2

        fifth = n * x_v_conj * H(x, x_v, n, n, 1)
        fifth -= (n + 1) * x * H(x, x_v, n + 1, n + 1, 1)
        fifth *= x ** 2 / x_v ** 2

        sixth = self.cls.L_n_l(n, 1)

        return (n + 2) * (first - second + third + fourth + fifth - sixth)

    def S_4n(self, n: int) -> complex:

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v
        H = self.H_nm_j

        first = H(x_v, x, n, n + 1, 0) - H(x_v, x, n, n + 1, 2)
        first *= ((n + 2) * x_v ** 2 - (n + 1) * x_conj ** 2) / 2

        second = H(x_v, x, n + 1, n, 0) - H(x_v, x, n + 1, n, 2)
        second *= x_conj * x_v

        third = H(x_v, x, n, n, -1) - H(x_v, x, n, n, 1)
        third *= 0.5 * x_conj * x_v ** 2

        fourth = H(x_v, x, n + 1, n + 1, -1) - H(x_v, x, n + 1, n + 1, 1)
        fourth *= x_conj ** 2 * x_v / 2

        fifth = (n + 1) * x_conj * H(x_v, x, n, n, 1)
        fifth -= (n + 2) * x_v * H(x_v, x, n + 1, n + 1, 1)
        fifth *= x_conj ** 2 / x_v ** 2

        sixth = self.cls.K_n_l(n, 2)

        return n * (first + second - third + fourth - fifth + sixth)

    def S_5n(self, n: int) -> complex:

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v
        J = self.cls.J_nm_j

        first = J(x, x, n, n + 1, 0) - J(x, x, n, n + 1, 2)
        first *= 0.5 * ((n + 2) * x ** 2 - n * x_conj ** 2)

        second = J(x, x, n + 1, n, 0) - J(x, x, n + 1, n, 2)
        second *= x * x_conj

        third = self.G_sum_1(n)
        third *= x * x_conj / (x_v ** 2)

        fourth = n * x_conj * J(x, x, n, n, 1)
        fourth += (n + 2) * x * J(x, x, n + 1, n + 1, 1)
        fourth -= x * x_conj * J(x, x, n + 1, n, 0)
        fourth *= (x ** 2 - x_conj ** 2) / x_v ** 2

        return first - second + third + fourth

    def S_6n(self, n: int) -> complex:

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v
        J = self.cls.J_nm_j

        first = (J(x, x, n + 1, n, 0) - J(x, x, n + 1, n, 2)).conjugate()
        first *= 0.5 * ((n + 2) * x ** 2 - n * x_conj ** 2)

        second = (J(x, x, n, n + 1, 0) - J(x, x, n, n + 1, 2)).conjugate()
        second *= x * x_conj

        third = self.G_sum_2(n)
        third *= x * x_conj / (x_v ** 2)

        fourth = n * x * J(x, x, n, n, 1)
        fourth += (n + 2) * x_conj * J(x, x, n + 1, n + 1, 1)
        fourth -= x * x_conj * J(x, x, n, n + 1, 0)
        fourth = (x ** 2 - x_conj ** 2) / x_v ** 2 * fourth.conjugate()

        return first - second + third + fourth

    def S_7n(self, n: int) -> complex:

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v
        J = self.cls.J_nm_j

        first = J(x_v, x, n, n + 1, 0) - J(x_v, x, n, n + 1, 2)
        first *= 0.5 * ((n + 2) * x_v ** 2 - (n + 1) * x_conj ** 2)

        second = J(x_v, x, n + 1, n, 0) - J(x_v, x, n + 1, n, 2)
        second *= x_conj * x_v

        third = J(x_v, x, n, n, -1) - J(x_v, x, n, n, 1)
        third *= 0.5 * x_conj * x_v ** 2

        fourth = J(x_v, x, n + 1, n + 1, -1) - J(x_v, x, n + 1, n + + 1, 1)
        fourth *= 0.5 * x_conj ** 2 * x_v

        fifth = self.K_sum(n)

        sixth = (n + 1) * x_conj * J(x_v, x, n, n, 1)
        sixth -= (n + 2) * x_v * J(x_v, x, n + 1, n + 1, 1)
        sixth *= x_conj ** 2 / x_v ** 2

        return n * (first + second - third + fourth + fifth - sixth)

    def S_8n(self, n: int) -> complex:

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v
        x_v_conj = self.cls.x_v.conjugate()
        J = self.cls.J_nm_j

        first = (J(x_v, x, n + 1, n, 0) - J(x_v, x, n + 1, n, 2)).conjugate()
        first *= 0.5 * (n * x_v_conj ** 2 - (n + 1) * x ** 2)

        second = (J(x_v, x, n, n + 1, 0) - J(x_v, x, n, n + 1, 2)).conjugate()
        second *= x * x_v_conj

        third = (J(x_v, x, n, n, -1) - J(x_v, x, n, n, 1)).conjugate()
        third *= 0.5 * x ** 2 * x_v_conj

        fourth = J(x_v, x, n + 1, n + 1, -1) - J(x_v, x, n + 1, n + 1, 1)
        fourth = x * x_v ** 2 / 2 * fourth.conjugate()

        fifth = self.L_sum(n)

        sixth = n * x_v * J(x_v, x, n, n, 1)
        sixth -= (n + 1) * x_conj * J(x_v, x, n + 1, n + 1, 1)
        sixth = x ** 2 / x_v ** 2 * sixth.conjugate()

        return (n + 2) * (first - second + third + fourth - fifth + sixth)

    def S_9n(self, n: int) -> complex:

        if not self.cls.background_streaming:
            return 0

        x = self.cls.x
        x_conj = self.cls.x.conjugate()
        x_v = self.cls.x_v

        out = x_conj * Bf.d1_besselj(n, x) * Bf.d1_besselj(n, x_conj)
        out += x * Bf.d1_besselj(n + 1, x) * Bf.d1_besselj(n + 1, x_conj)
        out *= x * x_conj / x_v ** 2

        return out

    def test_S_mn(self):
        names = [f'S_{m}n' for m in range(1, 10)]
        for method in names:
            for n in range(0, 3):
                with self.subTest(method='S_1n', arguments=n):
                    self._test_variables(
                        func_1=self.cls.S_1n,
                        func_2=self.S_1n,
                        args_1=n,
                        args_2=n,
                    )

    # -------------------------------------------------------------------------
    # D_n
    # -------------------------------------------------------------------------

    def D_n(self, n) -> complex:

        a_n = self.cls.alpha_n(n)
        b_n = self.cls.beta_n(n)
        a_n1 = self.cls.alpha_n(n + 1)
        b_n1 = self.cls.beta_n(n + 1)

        D_n = a_n * a_n1.conjugate() * self.cls.S_1n(n)
        D_n += b_n * b_n1.conjugate() * self.cls.S_2n(n)
        D_n -= a_n * b_n1.conjugate() * self.cls.S_3n(n)
        D_n -= b_n * a_n1.conjugate() * self.cls.S_4n(n)
        D_n += a_n * self.cls.S_5n(n)
        D_n += a_n1.conjugate() * self.cls.S_6n(n)
        D_n -= b_n * self.cls.S_7n(n)
        D_n -= b_n1.conjugate() * self.cls.S_8n(n)
        D_n += self.cls.S_9n(n) if self.background_streaming else 0

        return D_n

    def test_D_n(self):

        for n in range(1):
            self.do_testing(self.cls.D_n, self.D_n, n, n)

    # -------------------------------------------------------------------------
    # Test ARF
    # -------------------------------------------------------------------------

    def compute_arf(self):

        def term(n: int):
            out = self.D_n(n) * self.cls.A_in(n) * conj(self.cls.A_in(n + 1))
            out += (
                conj(self.D_n(n)) * self.cls.A_in(n + 1)
                * conj(self.cls.A_in(n))
            )
            out *= (n + 1) / (2 * n + 1) / (2 * n + 3)
            return out

        F_1 = sum([term(n) for n in full_range(self.N_max)]).real
        if self.cls.wave_type == osaft.WaveType.STANDING:
            F_2 = self.cls._F_2_standing()
        else:
            F_2 = self.cls._F_2_travelling()
        return -3 / 2 * pi * self.rho_f * F_1 + F_2

    def test_wrong_combination_error(self):
        self.cls.small_boundary_layer = True
        self.cls.large_boundary_layer = True
        self.assertRaises(ValueError, self.cls.compute_arf)

    def test_arf(self):
        self.do_testing(
            self.cls.compute_arf, self.compute_arf,
            threshold=1e-10,
        )


if __name__ == '__main__':

    unittest.main()
