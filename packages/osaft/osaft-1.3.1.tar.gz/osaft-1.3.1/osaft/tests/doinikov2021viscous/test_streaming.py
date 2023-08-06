import unittest
from collections.abc import Iterable

import numpy as np
from basetest import BaseTest

import osaft
from osaft.core.functions import clebsch_gordan_coefficient as cg
from osaft.core.functions import full_range, integrate, sqrt

conj = osaft.core.functions.conj


class TestStreaming(BaseTest):

    def setUp(self) -> None:
        super().setUp()

        self._v_boundary_conditions = 1e-3
        self.runs = 5
        self.rng = np.random.default_rng(seed=self.seed)

        self.cls = osaft.doinikov2021viscous.StreamingField(
            f=self.f, R_0=self.R_0,
            rho_s=self.rho_s, E_s=self.E_s, nu_s=self.nu_s,
            rho_f=self.rho_f, c_f=self.c_f,
            eta_f=self.eta_f, zeta_f=self.zeta_f,
            p_0=self.p_0, wave_type=self.wave_type,
            position=self.position,
        )

        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    @property
    def range_N_max(self) -> Iterable:
        return self.cls.range_N_max

    @property
    def range_1_N_max(self) -> Iterable:
        return self.cls.range_1_N_max

    @property
    def range_2_N_max(self) -> Iterable:
        return self.cls.range_2_N_max

    @property
    def omega(self) -> float:
        return self.cls.omega

    @property
    def k_f(self) -> complex:
        return self.cls.k_f

    @property
    def delta(self):
        return self.cls.delta

    @property
    def k_v(self) -> complex:
        return self.cls.k_v

    def V_r(self, n: int, r: float, ac: bool) -> complex:
        sc = not ac
        return self.cls.V_r(n, r, sc, True)

    def d_V_r(self, n: int, r: float, ac: bool) -> complex:
        sc = not ac
        return self.cls.d_V_r(n, r, sc, True)

    def V_theta(self, n: int, r: float, ac: bool) -> complex:
        sc = not ac
        return self.cls.V_theta(n, r, sc, True)

    def d_V_theta(self, n: int, r: float, ac: bool) -> complex:
        sc = not ac
        return self.cls.d_V_theta(n, r, sc, True)

    def d2_V_theta(self, n: int, r: float, ac: bool):
        sc = not ac
        return self.cls.d2_V_theta(n, r, sc, True)

    def phi(self, n: int, r: float, ac: bool) -> complex:
        sc = not ac
        return self.cls.phi(n, r, sc, True)

    def d_phi(self, n: int, r: float, ac: bool) -> complex:
        sc = not ac
        return self.cls.d_phi(n, r, sc, True)

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def inf(self):
        if self.cls.inf_type is not None:
            raise ValueError
        if self.R_0 > self.delta:
            return self.R_0 * self.cls.inf_factor
        else:
            return self.delta * self.cls.inf_factor

    def alpha(self, l: int, r: float, ac: bool) -> float:
        first_sum = complex(0)
        for n in self.range_N_max:
            for m in full_range(abs(l - n), n + l):
                if cg_coef := cg(l, 0, n, 0, m, 0):
                    first_sum += (
                        cg_coef ** 2 / (2 * m + 1)
                        * (
                            self.F(n, m, r, ac)
                            - m * (m + 1) * self.G(n, m, r, ac)
                        )
                    )
        second_sum = complex(0)
        for n in self.range_1_N_max:
            for m in full_range(1, int((n + 1) / 2)):
                for k in full_range(
                    abs(l - (n - 2 * m + 1)),
                    l + n - 2 * m + 1,
                ):
                    if (cg_coef := cg(l, 0, n - 2 * m + 1, 0, k, 0)):
                        factor = ((2 * n - 4 * m + 3)
                                  * cg_coef ** 2 / (2 * k + 1))
                        first_term = ((k + 1) * (k + 2) / (2 * k + 3)
                                          * self.G(n, k + 1, r, ac))
                        if k <= 1:
                            second_sum += factor * first_term
                            continue
                        second_term = (
                            k * (k - 1) / (2 * k - 1)
                            * self.G(n, k - 1, r, ac)
                        )
                        second_sum += factor * (first_term - second_term)
        return (2 * l + 1) / (2 * self.omega) * (first_sum + second_sum).real

    def beta(self, l: int, r: float, ac: bool) -> float:
        first_sum = 0
        for n in self.range_N_max:
            first_inner_sum = complex(0)
            for m in full_range(abs(l - n), l + n):
                if cg_coef := cg(l, 0, n, 0, m, 0):
                    first_inner_sum += (
                        cg_coef ** 2 / (2 * m + 1)
                        * conj(
                            self.d_V_r(m, r, ac)
                            - self.k_f ** 2 * self.phi(m, r, ac),
                        )
                    )
            first_sum += (self.V_r(n, r, ac) * first_inner_sum).real
        second_sum = 0
        for n in self.range_1_N_max:
            for m in full_range(1, int((n + 1) / 2)):
                second_inner_sum = complex(0)
                for k in full_range(
                    abs(l - (n - 2 * m + 1)),
                    l + n - 2 * m + 1,
                ):
                    if (cg_coef := cg(l, 0, n - 2 * m + 1, 0, k, 0)):
                        factor = cg_coef ** 2 / (2 * k + 1)
                        first_term = ((k + 1) * (k + 2) / (2 * k + 3)
                                      * conj(
                                          self.V_r(k + 1, r, ac)
                                          - self.V_theta(k + 1, r, ac),
                                      ))
                        if k <= 1:
                            second_inner_sum += factor * first_term
                            continue
                        second_term = (
                            k * (k - 1) / (2 * k - 1)
                            * conj(
                                self.V_r(k - 1, r, ac)
                                - self.V_theta(k - 1, r, ac),
                            )
                        )
                        second_inner_sum += factor * (first_term - second_term)
                second_sum += (
                    (2 * n - 4 * m + 3)
                    * self.V_theta(n, r, ac)
                    / r * second_inner_sum
                ).real
        return (2 * l + 1) / 2 * (first_sum + second_sum)

    def gamma(self, l: int, r: float, ac: bool) -> float:
        if l == 0:
            return 0
        first_sum = complex(0)
        for n in self.range_N_max:
            for m in full_range(abs(n - l), n + l):
                cg_coef_1 = cg(n, 0, l, 0, m, 0)
                cg_coef_2 = cg(n, 0, l, 1, m, 1)
                if m >= 1 and cg_coef_1 and cg_coef_2:
                    first_sum += (
                        sqrt(m * (m + 1)) * cg_coef_1 * cg_coef_2 / (2 * m + 1)
                        * (
                            self.V_r(n, r, ac) * conj(self.d_V_theta(m, r, ac))
                            + self.V_theta(m, r, ac)
                            * conj((
                                self.V_r(n, r, ac)
                                - n ** 2 * self.V_theta(n, r, ac)
                            ) / r
                                   - self.k_f ** 2 * self.phi(n, r, ac))
                        )
                    )
        second_sum = self._V_S_theta_second_sum(l, r, ac)
        return (
            (2 * l + 1) / (2 * sqrt(l * (l + 1)))
            * (first_sum + second_sum).real
        )

    def d_gamma(self, l: int, r: float, ac: bool) -> float:
        if l == 0:
            return 0

        first_sum = complex(0)
        for n in self.range_N_max:
            for m in full_range(abs(n - l), n + l):
                cg_coef_1 = cg(n, 0, l, 0, m, 0)
                cg_coef_2 = cg(n, 0, l, 1, m, 1)
                if m >= 1 and cg_coef_1 and cg_coef_2:
                    first_sum += (
                        sqrt(m * (m + 1)) * cg_coef_1 * cg_coef_2 / (2 * m + 1)
                        * (
                            self.d_V_r(n, r, ac)
                            * conj(self.d_V_theta(m, r, ac))
                            + self.V_r(n, r, ac)
                            * conj(self.d2_V_theta(m, r, ac))
                            + self.d_V_theta(m, r, ac)
                            * conj((
                                self.V_r(n, r, ac)
                                - n ** 2 * self.V_theta(n, r, ac)
                            ) / r
                                   - self.k_f ** 2 * self.phi(n, r, ac))
                            + self.V_theta(m, r, ac)
                            * conj((
                                self.d_V_r(n, r, ac)
                                - n ** 2 * self.d_V_theta(n, r, ac)
                            )
                                   / r
                                   - (
                                       self.V_r(n, r, ac)
                                       - n ** 2 * self.V_theta(n, r, ac)
                                   )
                                   / r ** 2
                                   - self.k_f ** 2 * self.d_phi(n, r, ac))
                        )
                    )

        second_sum = complex(0)
        for n in self.range_2_N_max:
            for m in full_range(1, int(n / 2)):
                second_inner_sum = complex(0)
                for k in full_range(abs(n - 2 * m - l), n - 2 * m + l):
                    cg_coef_1 = cg(n - 2 * m, 0, l, 0, k, 0)
                    cg_coef_2 = cg(n - 2 * m, 0, l, 1, k, 1)
                    if k >= 1 and cg_coef_1 and cg_coef_2:
                        second_inner_sum += (
                            sqrt(k * (k + 1))
                            * cg_coef_1 * cg_coef_2 / (2 * k + 1)
                            * (
                                (
                                    conj(self.d_V_theta(n, r, ac))
                                    * self.V_theta(k, r, ac)
                                    + conj(self.V_theta(n, r, ac))
                                    * self.d_V_theta(k, r, ac)
                                ) / r
                                - (
                                    conj(self.V_theta(n, r, ac))
                                    * self.V_theta(k, r, ac)
                                ) / r ** 2
                            )
                        )
                second_sum += (2 * n - 4 * m + 1) * second_inner_sum

        return (
            (2 * l + 1) / (2 * sqrt(l * (l + 1)))
            * (first_sum + second_sum).real
        )

    def E(self, l: int, r: float, ac: bool) -> float:
        return (
            - self.rho_f / (self.eta_f * r)
            * (
                self.gamma(l, r, ac)
                + r * self.d_gamma(l, r, ac) - self.beta(l, r, ac)
            )
        )

    def F(self, n: int, m: int, r: float, ac: bool) -> complex:
        return (
            1j * conj(self.k_f ** 2) / r
            * (
                conj(2 * self.phi(n, r, ac) + r * self.d_phi(n, r, ac))
                * self.V_r(m, r, ac)
                + r * conj(self.phi(n, r, ac)) * self.d_V_r(m, r, ac)
            )
        )

    def G(self, n: int, m: int, r: float, ac: bool) -> complex:
        return (
            1j * conj(self.k_f ** 2) / r * conj(self.phi(n, r, ac)) *
            self.V_theta(m, r, ac)
        )

    # -------------------------------------------------------------------------
    # Integrals
    # -------------------------------------------------------------------------

    def compute_C_0(self) -> np.ndarray:

        l_range = self.range_1_N_max

        C_0 = np.zeros((6 + 1, self.cls.N_max + 1))

        # parameters
        inf = self.cls.inf
        int_eps = self.cls.integration_rel_eps

        for l in l_range:

            # C_1l0
            C_0[1, l] = 0

            # C_2l0
            kernel_C_2l0 = lambda s: s ** (1 - l) * (
                self.alpha(l, s, ac=False) - self.alpha(l, s, ac=True)
            )
            integral_C_2l0, error_C_2l0 = integrate(
                kernel_C_2l0, self.R_0, inf, rel_eps=int_eps,
            )
            C_0[2, l] = - 1 / (2 * l + 1) * integral_C_2l0

            # C_5l0
            kernel_C_5l0 = lambda s: s ** (3 - l) * (
                self.E(l, s, ac=False) - self.E(l, s, ac=True)
            )
            integral_C_5l0, error_C_5l0 = integrate(
                kernel_C_5l0, self.R_0, inf, rel_eps=int_eps,
            )
            C_0[5, l] = (
                1 / (2 * (2 * l - 1) * (2 * l + 1))
                * integral_C_5l0
            )

            # C_6l0
            kernel_C_6l0 = lambda s: s ** (1 - l) * (
                self.E(l, s, ac=False) - self.E(l, s, ac=True)
            )
            integral_C_6l0, error_C_6l0 = integrate(
                kernel_C_6l0, self.R_0, inf, rel_eps=int_eps,
            )
            C_0[6, l] = - 1 / (2 * (2 * l + 1) * (2 * l + 3)) * integral_C_6l0

            # C_3l0
            C_0[3, l] = (
                0.5
                * (
                    self.R_0 ** l
                    * (
                        self.V_S_r(l, self.R_0, ac=False) / (l + 1)
                        + self.V_S_theta(l, self.R_0, ac=False)
                    )
                    + (2 * l + 1) * self.R_0 ** (2 * l - 1)
                    * (
                        C_0[2, l] / (l + 1)
                        - C_0[5, l]
                    )
                    - (2 * l + 3) * self.R_0 ** (2 * l + 1)
                    * C_0[6, l]
                )
            )

            # C_4l0
            C_0[4, l] = (
                0.5
                * (
                    self.R_0 ** (l + 2)
                    * ((2 - l)
                       * self.V_S_r(l, self.R_0, ac=False) / (l * (l + 1))
                       - self.V_S_theta(l, self.R_0, ac=False))
                    - (2 * l - 1) * self.R_0 ** (2 * l + 1)
                    * (
                        C_0[2, l] / (l + 1)
                        - C_0[5, l]
                    )
                    + (2 * l + 1) * self.R_0 ** (2 * l + 3)
                    * C_0[6, l]
                )
            )

        return C_0

    # -------------------------------------------------------------------------
    # Stokes drift velocity
    # -------------------------------------------------------------------------

    def V_S_r(self, l: int, r: float, ac: bool) -> float:
        first_sum = complex(0)
        for n in self.range_N_max:
            first_inner_sum = complex(0)
            for m in full_range(abs(l - n), l + n):
                if cg_coef := cg(l, 0, n, 0, m, 0):
                    first_inner_sum += (
                        cg_coef ** 2 / (2 * m + 1)
                        * conj(self.d_V_r(m, r, ac))
                    )
            first_sum += self.V_r(n, r, ac) * first_inner_sum
        second_sum = complex(0)
        for n in self.range_1_N_max:
            for m in full_range(1, int((n + 1) / 2)):
                second_inner_sum = complex(0)
                for k in full_range(
                    abs(l - (n - 2 * m + 1)),
                    l + n - 2 * m + 1,
                ):
                    cg_coef = cg(l, 0, n - 2 * m + 1, 0, k, 0)
                    if cg_coef:
                        factor = cg_coef ** 2 / (2 * k + 1)
                        term_1 = ((k + 1) * (k + 2) / (2 * k + 3)
                                  * conj(self.V_r(k + 1, r, ac)))
                        if k <= 1:
                            second_inner_sum += factor * term_1
                            continue
                        term_2 = (
                            k * (k - 1) / (2 * k - 1)
                            * conj(self.V_r(k - 1, r, ac))
                        )
                        second_inner_sum += factor * (term_1 - term_2)
                second_sum += (
                    (2 * n - 4 * m + 3)
                    * self.V_theta(n, r, ac) / r
                    * second_inner_sum
                )
        return (
            (2 * l + 1) / (2 * self.omega)
            * (1j * (first_sum + second_sum)).real
        )

    def V_S_theta(self, l: int, r: float, ac: bool) -> float:
        if l == 0:
            return 0

        first_sum = complex(0)
        for n in self.range_N_max:
            for m in full_range(abs(n - l), n + l):
                cg_coef_1 = cg(n, 0, l, 0, m, 0)
                cg_coef_2 = cg(n, 0, l, 1, m, 1)
                if m >= 1 and cg_coef_1 and cg_coef_2:
                    first_sum += (
                        sqrt(m * (m + 1))
                        * cg_coef_1 * cg_coef_2 / (2 * m + 1)
                        * (
                            self.V_r(n, r, ac)
                            * conj(self.d_V_theta(m, r, ac))
                            + self.V_theta(m, r, ac)
                            * conj(
                                self.V_r(n, r, ac)
                                - n ** 2 * self.V_theta(n, r, ac),
                            ) / r
                        )
                    )
        second_sum = self._V_S_theta_second_sum(l, r, ac)
        return ((2 * l + 1) / (2 * self.omega * sqrt(l * (l + 1)))
                * (1j * (first_sum + second_sum))).real

    def _V_S_theta_second_sum(self, l: int, r: float, ac: bool) -> complex:

        second_sum = complex(0)
        for n in self.range_2_N_max:
            second_middle_sum = complex(0)
            for m in full_range(1, int(n / 2)):
                second_inner_sum = complex(0)
                for k in full_range(abs(n - 2 * m - l), n - 2 * m + l):
                    cg_coef_1 = cg(n - 2 * m, 0, l, 0, k, 0)
                    cg_coef_2 = cg(n - 2 * m, 0, l, 1, k, 1)
                    if k >= 1 and cg_coef_1 and cg_coef_2:
                        second_inner_sum += (
                            sqrt(k * (k + 1)) * cg_coef_1 * cg_coef_2
                            * self.V_theta(k, r, ac) / (2 * k + 1)
                        )
                second_middle_sum += (2 * n - 4 * m + 1) * second_inner_sum
            second_sum += conj(self.V_theta(n, r, ac)) / r * second_middle_sum

        return second_sum

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_infinity_not_set(self):
        self.do_testing(self.inf, lambda: self.cls.inf)

    def test_infinity_set(self):
        # inf type
        self.cls.inf_type = 'radius'
        self.do_testing(
            lambda: self.cls.inf_factor * self.R_0,
            lambda: self.cls.inf,
        )
        self.cls.inf_type = 'delta'
        self.cls.inf_factor = 80
        self.do_testing(
            lambda: self.cls.inf_factor * self.delta,
            lambda: self.cls.inf,
        )
        self.cls.inf_type = 1
        self.do_testing(
            lambda: self.cls.inf_factor,
            lambda: self.cls.inf,
        )

    def test_wrong_inf_type(self):
        self.cls.inf_type = 'blabla'
        self.assertRaises(ValueError, lambda: self.cls.inf)

    def test_F_G_dependent(self) -> None:
        self.test_variables.remove(self._R_0)

        for m in range(1, self.runs + 1):
            factor = self.rng.uniform(2, 10)
            dict_methods = dict()
            dict_methods['F'] = (m, factor * self.R_0, True)
            dict_methods['G'] = (m, factor * self.R_0, True)
            self._test_methods_n(dict_methods)

    def test_alpha_beta_gamma(self) -> None:
        radii = self.R_0 * np.linspace(1, 5, self.n_runs)
        for r in radii:
            for n in range(1, 5):
                self.assertAlmostEqual(
                    self.alpha(n, r, False),
                    self.cls.alpha(n, r, False),
                    threshold=1e-8,
                )
                self.assertAlmostEqual(
                    self.beta(n, r, False),
                    self.cls.beta(n, r, False), 1e-6,
                )
                self.assertAlmostEqual(
                    self.gamma(n, r, False),
                    self.cls.gamma(n, r, False),
                    threshold=1e-6,
                )
                self.assertAlmostEqual(
                    self.d_gamma(n, r, False),
                    self.cls.d_gamma(n, r, False),
                    threshold=1e-6,
                )

    def test_gamma_error(self):
        self.assertRaises(ValueError, self.cls.gamma, 0, 1, True)
        self.assertRaises(ValueError, self.cls.d_gamma, 0, 1, True)

    def test_E(self) -> None:
        radii = self.R_0 * np.linspace(1, 5, self.n_runs)
        for r in radii:
            for n in range(1, 5):
                self.assertAlmostEqual(
                    self.E(n, r, False),
                    self.cls.E(n, r, False),
                    threshold=1e-6,
                )

    def test_integrals(self):
        self.cls.N_max = 1
        C_0 = self.compute_C_0()
        for n in range(1, 7):
            for m in self.range_1_N_max:
                with self.subTest(msg=f'C_{n}{m}0'):
                    print(f'{self.cls.C_0[n, m] = }')
                    print(f'{C_0[n, m] = }')
                    self.assertAlmostEqual(self.cls.C_0[n, m], C_0[n, m])

    def test_rel_eps(self):
        self.cls.N_max = 1
        self.cls.integration_rel_eps = 1e-3
        C_first = self.cls.C_0[3, 1]
        self.cls.integration_rel_eps = 1e-9
        C_second = self.cls.C_0[3, 1]
        self.assertAlmostEqual(C_first, C_second)

    def test_stokes_drift_velocity(self) -> None:
        radii = self.R_0 * np.linspace(1, 5, self.n_runs)
        for r in radii:
            for n in range(0, 5):
                first = self._V_S_theta_second_sum(n, r, False)
                second = self.cls._V_S_theta_second_sum(n, r, False)
                if abs(first) > 1e-20 and abs(second) > 1e-20:
                    self.assertAlmostEqual(first, second, threshold=1e-8)
                first = self.V_S_theta(n, r, False)
                second = self.cls.V_S_theta(n, r, False)
                if abs(first) > 1e-20 and abs(second) > 1e-20:
                    self.assertAlmostEqual(first, second, threshold=1e-8)
                first = self.V_S_r(n, r, False)
                second = self.cls.V_S_r(n, r, False)
                if abs(first) > 1e-20 and abs(second) > 1e-20:
                    self.assertAlmostEqual(first, second, threshold=1e-8)


if __name__ == '__main__':
    unittest.main()
