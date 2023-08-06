import unittest

import numpy as np
from basetest import BaseTest

import osaft
from osaft.core.functions import BesselFunctions as Bf
from osaft.core.functions import LegendreFunctions as Leg
from osaft.core.functions import full_range
from osaft.tests.basetest_scattering import HelperScattering


class TestScattering(BaseTest, HelperScattering):

    def setUp(self) -> None:
        super().setUp()

        self._v_boundary_conditions = 1e-3
        self._v_fluid_threshold = 1e-8
        self.runs = 5
        self.rng = np.random.default_rng(seed=self.seed)

        self.cls = osaft.doinikov2021viscous.ScatteringField(
            f=self.f, R_0=self.R_0,
            rho_s=self.rho_s, E_s=self.E_s, nu_s=self.nu_s,
            rho_f=self.rho_f, c_f=self.c_f,
            eta_f=self.eta_f, zeta_f=self.zeta_f,
            p_0=self.p_0, wave_type=self.wave_type,
            position=self.position,
        )

        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Test V_r, V_theta
    # -------------------------------------------------------------------------

    def test_V(self) -> None:
        combinations = [
            (True, False),
            (False, True), (True, True),
        ]
        threshold = 1e-8
        for factor in np.linspace(1, 5, self.n_runs):
            for n in range(0, 5):
                for scattered, incident in combinations:
                    r = factor * self.R_0
                    self.assertAlmostEqual(
                        self.V_r(n, r, scattered, incident),
                        self.cls.V_r(n, r, scattered, incident),
                        threshold=threshold,
                    )
                    self.assertAlmostEqual(
                        self.d_V_r(n, r, scattered, incident),
                        self.cls.d_V_r(n, r, scattered, incident),
                        threshold=threshold,
                    )
                    self.assertAlmostEqual(
                        self.d2_V_r(n, r, scattered, incident),
                        self.cls.d2_V_r(n, r, scattered, incident),
                        threshold=threshold,
                    )
                    self.assertAlmostEqual(
                        self.V_theta(n, r, scattered, incident),
                        self.cls.V_theta(n, r, scattered, incident),
                    )
                    self.assertAlmostEqual(
                        self.d_V_theta(n, r, scattered, incident),
                        self.cls.d_V_theta(n, r, scattered, incident),
                        threshold=threshold,
                    )
                    self.assertAlmostEqual(
                        self.d2_V_theta(n, r, scattered, incident),
                        self.cls.d2_V_theta(n, r, scattered, incident),
                        threshold=threshold,
                    )
                    self.assertAlmostEqual(
                        self.phi(n, r, scattered, incident),
                        self.cls.phi(n, r, scattered, incident),
                        threshold=threshold,
                    )
                    self.assertAlmostEqual(
                        self.d_phi(n, r, scattered, incident),
                        self.cls.d_phi(n, r, scattered, incident),
                        threshold=threshold,
                    )

    def test_V_error(self):
        self.assertRaises(ValueError, self.cls.V_r, 1, self.R_0, False, False)
        self.assertRaises(
            ValueError, self.cls.d_V_r, 1, self.R_0, False,
            False,
        )
        self.assertRaises(
            ValueError, self.cls.d2_V_r, 1, self.R_0, False,
            False,
        )
        self.assertRaises(
            ValueError, self.cls.V_theta, 1, self.R_0, False,
            False,
        )
        self.assertRaises(
            ValueError, self.cls.d_V_theta, 1, self.R_0, False,
            False,
        )
        self.assertRaises(
            ValueError, self.cls.d2_V_theta, 1, self.R_0, False,
            False,
        )
        self.assertRaises(ValueError, self.cls.phi, 1, self.R_0, False, False)
        self.assertRaises(
            ValueError, self.cls.d_phi, 1, self.R_0, False,
            False,
        )

    # -------------------------------------------------------------------------
    # Velocity Methods
    # -------------------------------------------------------------------------

    def radial_acoustic_fluid_velocity(
            self, r, theta, t, scattered, incident, mode=None,
    ) -> complex:
        def coef(l: int, x: float) -> complex:
            return self.cls.V_r(l, x, scattered, incident)

        out = np.exp(-1j * self.omega * t)
        if mode is not None:
            out *= Leg.cos_monomial(mode, theta, coef(mode, r))
        else:
            out *= Leg.cos_poly(
                theta,
                np.array(
                    [coef(n, r) for n in full_range(0, self.N_max)], ),
            )
        return out

    def tangential_acoustic_fluid_velocity(
            self, r, theta, t, scattered, incident, mode=None,
    ) -> complex:
        def coef(l: int, x: float) -> complex:
            return self.cls.V_theta(l, x, scattered, incident)

        out = np.exp(-1j * self.omega * t)
        if mode is not None:
            out *= Leg.first_cos_monomial(
                mode,
                theta,
                coef(mode, r),
            )
        else:
            out *= Leg.first_cos_poly(
                theta,
                np.array(
                    [coef(n, r) for n in full_range(0, self.N_max)],
                ),
            )
        return out

    def radial_particle_displacement(self, r, theta, t, mode) -> complex:
        def coef(l: int, x: float) -> complex:
            first = self.k_l * self.a_hat(l) * Bf.d1_besselj(l, self.k_l * x)
            second = l * (l + 1) * self.b_hat(l) * Bf.besselj(l, self.k_t * x)
            second /= x
            return first - second

        out = np.exp(-1j * self.omega * t)
        if mode is not None:
            out *= Leg.cos_monomial(mode, theta, coef(mode, r))
        else:
            out *= Leg.cos_poly(
                theta,
                np.array(
                    [coef(n, r) for n in full_range(0, self.N_max)], ),
            )
        return out

    def radial_particle_velocity(self, r, theta, t, mode) -> complex:
        return (-1j * self.omega) * self.radial_particle_displacement(
            r, theta, t, mode,
        )

    def tangential_particle_displacement(self, r, theta, t, mode) -> complex:
        def coef(l: int, x: float) -> complex:
            first = self.a_hat(l) * Bf.besselj(l, self.k_l * x)
            second = Bf.besselj(l, self.k_t * x)
            second += self.k_t * x * Bf.d1_besselj(l, self.k_t * x)
            second *= self.b_hat(l)
            return (first - second) / x

        out = np.exp(-1j * self.omega * t)
        if mode is not None:
            out *= Leg.first_cos_monomial(
                mode,
                theta,
                coef(mode, r),
            )
        else:
            out *= Leg.first_cos_poly(
                theta,
                np.array(
                    [coef(n, r) for n in full_range(1, self.N_max)],
                ),
            )
        return out

    def tangential_particle_velocity(self, r, theta, t, mode) -> complex:
        return (-1j * self.omega) * self.tangential_particle_displacement(
            r, theta, t, mode,
        )
    # -------------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------------

    @property
    def N_max(self) -> int:
        return self.cls.N_max

    @property
    def omega(self) -> float:
        return self.f * 2 * np.pi

    @property
    def k_f(self) -> complex:
        return self.cls.k_f

    @property
    def k_v(self) -> complex:
        return self.cls.k_v

    @property
    def k_l(self) -> complex:
        return self.cls.k_l

    @property
    def k_t(self) -> complex:
        return self.cls.k_t

    def a(self, n: int) -> complex:
        return self.cls.a(n)

    def a_hat(self, n: int) -> complex:
        return self.cls.a_hat(n)

    def b(self, n: int) -> complex:
        return self.cls.b(n)

    def b_hat(self, n: int) -> complex:
        return self.cls.b_hat(n)

    def A_in(self, n: int) -> complex:
        return self.cls.A_in(n)

    # -------------------------------------------------------------------------
    # V_r, V_theta methods
    # ------------------------------------------------------------------------

    def V_r(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            return (
                self.a(n) * self.k_f * Bf.d1_hankelh1(n, self.k_f * r)
                - n * (n + 1) * self.b(n)
                * Bf.hankelh1(n, self.k_v * r) / r
            )
        elif incident and not scattered:
            return (
                self.A_in(n) * self.k_f * Bf.d1_besselj(n, self.k_f * r)
            )
        elif incident and scattered:
            return self.V_r(n, r, True, False) + self.V_r(n, r, False, True)
        else:
            return 0

    def d_V_r(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            return (
                self.k_f ** 2 * self.a(n) * Bf.d2_hankelh1(n, self.k_f * r)
                - n * (n + 1) * self.b(n)
                * (
                    self.k_v * Bf.d1_hankelh1(n, self.k_v * r) * r
                    - Bf.hankelh1(n, self.k_v * r)
                ) / r ** 2
            )
        elif incident and not scattered:
            return (
                self.k_f ** 2 * self.A_in(n) * Bf.d2_besselj(n, self.k_f * r)
            )
        elif incident and scattered:
            return (
                self.d_V_r(n, r, True, False)
                + self.d_V_r(n, r, False, True)
            )
        else:
            return 0

    def d2_V_r(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            return (
                self.k_f ** 3 * self.a(n) * Bf.d3_hankelh1(n, self.k_f * r)
                - n * (n + 1) * self.b(n)
                * (
                    self.k_v ** 2 * Bf.d2_hankelh1(n, self.k_v * r) / r
                    + 2 * (
                        Bf.hankelh1(n, self.k_v * r)
                        - r * self.k_v
                        * Bf.d1_hankelh1(n, self.k_v * r)
                    ) / r ** 3
                )
            )
        elif not scattered and incident:
            return (
                self.k_f ** 3 * self.A_in(n) * Bf.d3_besselj(n, self.k_f * r)
            )
        elif scattered and incident:
            return (
                self.d2_V_r(n, r, True, False)
                + self.d2_V_r(n, r, False, True)
            )
        else:
            return 0

    def V_theta(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            return (
                self.a(n) * Bf.hankelh1(n, self.k_f * r)
                - self.b(n)
                * (
                    Bf.hankelh1(n, self.k_v * r)
                    + self.k_v * r
                    * Bf.d1_hankelh1(n, self.k_v * r)
                )
            ) / r
        elif not scattered and incident:
            return self.A_in(n) * Bf.besselj(n, self.k_f * r) / r
        elif scattered and incident:
            if n == 0:
                return 0
            return (
                self.V_theta(n, r, True, False)
                + self.V_theta(n, r, False, True)
            )
        else:
            return 0

    def d_V_theta(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            nominator_div_r = self.V_theta(n, r, scattered, incident)
            d_nominator = (
                self.k_f * self.a(n) * Bf.d1_hankelh1(n, self.k_f * r)
                - self.b(n) * self.k_v
                * (
                    2 * Bf.d1_hankelh1(n, self.k_v * r)
                    + self.k_v * r
                    * Bf.d2_hankelh1(n, self.k_v * r)
                )
            )
            return (d_nominator - nominator_div_r) / r
        elif incident and not scattered:
            nominator_div_r = self.V_theta(n, r, scattered, incident)
            d_nominator = (
                self.k_f * self.A_in(n)
                * Bf.d1_besselj(n, self.k_f * r)
            )
            return (d_nominator - nominator_div_r) / r
        elif scattered and incident:
            if n == 0:
                return 0
            return (
                self.d_V_theta(n, r, True, False)
                + self.d_V_theta(n, r, False, True)
            )
        else:
            return 0

    def d2_V_theta(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            dd_nominator = (
                self.k_f ** 2 * self.a(n) * Bf.d2_hankelh1(n, self.k_f * r)
                - self.b(n) * self.k_v ** 2
                * (
                    3 * Bf.d2_hankelh1(n, self.k_v * r)
                    + self.k_v * r
                    * Bf.d3_hankelh1(n, self.k_v * r)
                )
            )
            return (
                dd_nominator
                - 2 * self.d_V_theta(n, r, scattered, incident)
            ) / r
        elif incident and not scattered:
            dd_nominator = (
                self.k_f ** 2 * self.A_in(n) * Bf.d2_besselj(n, self.k_f * r)
            )
            return (
                dd_nominator
                - 2 * self.d_V_theta(n, r, scattered, incident)
            ) / r
        elif scattered and incident:
            if n == 0:
                return 0
            return (
                self.d2_V_theta(n, r, True, False)
                + self.d2_V_theta(n, r, False, True)
            )

    def phi(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            return self.a(n) * Bf.hankelh1(n, self.k_f * r)
        elif incident and not scattered:
            return self.A_in(n) * Bf.besselj(n, self.k_f * r)
        elif scattered and incident:
            return self.phi(n, r, True, False) + self.phi(n, r, False, True)
        else:
            return 0

    def d_phi(
        self, n: int, r: float, scattered: bool, incident: bool,
    ) -> complex:
        if scattered and not incident:
            return self.a(n) * self.k_f * Bf.d1_hankelh1(n, self.k_f * r)
        elif not scattered and incident:
            return self.A_in(n) * self.k_f * Bf.d1_besselj(n, self.k_f * r)
        elif scattered and incident:
            return (
                self.d_phi(n, r, True, False)
                + self.d_phi(n, r, False, True)
            )
        else:
            return 0


if __name__ == '__main__':
    unittest.main()
