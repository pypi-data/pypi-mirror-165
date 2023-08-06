import unittest

import numpy as np
from basetest import BaseTest
from basetest_arf import HelperStandingARF, HelperTravelingARF

import osaft

conj = osaft.core.functions.conj


class TestARF(BaseTest):

    def setUp(self) -> None:
        super().setUp()

        self._v_boundary_conditions = 1e-3
        self.runs = 5
        self.rng = np.random.default_rng(seed=self.seed)

        self.cls = osaft.doinikov2021viscous.ARF(
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

    def V_r(self, n: int) -> complex:
        return self.cls.V_r(n, self.cls.R_0, True, True)

    def V_theta(self, n: int) -> complex:
        return self.cls.V_theta(n, self.cls.R_0, True, True)

    # -------------------------------------------------------------------------
    # ARF
    # -------------------------------------------------------------------------

    def compute_arf(self) -> float:
        first_sum = (
            4 * self.eta_f / self.R_0 ** 2
            * self.cls.C_0[3, 1]
            + 2 / 3 * self.R_0 * self.rho_f
            * self.cls.gamma(1, self.R_0, False)
        )

        second_sum = complex(0)
        for n in self.cls.range_N_max:
            if n == 0:
                term_1 = 0
            else:
                term_1 = (
                    n * conj(self.V_r(n - 1))
                    * (self.V_r(n) + (n + 1) * self.V_theta(n))
                    / ((2 * n - 1) * (2 * n + 1))
                )
            term_2 = ((n + 1) * conj(self.V_r(n + 1))
                      * (self.V_r(n) - n * self.V_theta(n))
                      / ((2 * n + 1) * (2 * n + 3)))
            second_sum += term_1 + term_2
        return 2 * osaft.pi * self.R_0 ** 2 * (
            first_sum - self.rho_f *
            second_sum.real
        )


class TestARFStanding(TestARF, HelperStandingARF):

    def setUp(self) -> None:
        super().setUp()


class TestARFTravelling(TestARF, HelperTravelingARF):

    def setUp(self) -> None:
        super().setUp()


class TestARFErrorEstimation(TestARF):

    def setUp(self) -> None:
        super().setUp()

    def test_error_estimation(self):
        arf, error = self.cls.compute_arf(True)
        self.assertTrue(abs(arf) > 100 * abs(error))


if __name__ == '__main__':
    unittest.main()
