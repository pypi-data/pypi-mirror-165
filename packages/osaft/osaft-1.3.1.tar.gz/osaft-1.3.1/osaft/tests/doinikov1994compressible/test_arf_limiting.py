import unittest

import numpy as np
from basetest_arf import HelperStandingARF, HelperTravelingARF

from osaft import doinikov1994compressible
from osaft.core.backgroundfields import WaveType
from osaft.core.functions import sqrt
from osaft.tests.basedoinikov1994.test_base import BaseTestDoinikov1994


class TestARFBase(BaseTestDoinikov1994):

    def setUp(self) -> None:

        super().setUp()

        self.small_boundary_layer = False
        self.large_boundary_layer = False

        self.cls = doinikov1994compressible.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s, c_s=self.c_s,
            eta_s=self.eta_s, zeta_s=self.zeta_s,
            rho_f=self.rho_f, c_f=self.c_f,
            eta_f=self.eta_f, zeta_f=self.zeta_f,
            p_0=self.p_0, wave_type=self.wave_type,
            position=self.position,
            small_boundary_layer=self.small_boundary_layer,
            large_boundary_layer=self.large_boundary_layer,
            N_max=self.N_max,
        )

        self.list_cls = [self.cls]

    def assign_parameters(self) -> None:
        super().assign_parameters()

        self.cls.small_boundary_layer = (
            self.small_boundary_layer
        )
        self.cls.large_boundary_layer = (
            self.large_boundary_layer
        )
        self.cls.N_max = self.N_max

    @property
    def kappa_t(self) -> float:
        return self.rho_f * self.c_f**2 / self.rho_s / self.c_s**2

    @property
    def mu(self) -> float:
        return sqrt(self.rho_f * self.eta_f / self.rho_s / self.eta_s)

    @property
    def g1(self):
        return self.g5 * self.g6

    @property
    def g2(self):
        out = 209 + 148 * self.eta_t + 48 / self.eta_t
        out *= - 1 / 9 / self.zeta_t

        out += 19 + 38 * self.eta_t - 12 / self.eta_t

        return out

    @property
    def g3(self):
        out = 25 + 370 * self.eta_t - 80 / self.eta_t
        out *= 1 / 9 / self.zeta_t

        out += -12 - 19 * self.eta_t - 4 / self.eta_t

        return out

    @property
    def g4(self):
        out = 5 + 74 * self.eta_t - 16 / self.eta_t
        out *= 1 / 9 / self.zeta_t

        out += -3 - 4 / self.eta_t

        return out

    @property
    def g5(self):
        out = (1 - self.eta_t)
        out *= (19 + 16 / self.eta_t)
        return out

    @property
    def g6(self):
        return 89 + 48 / self.eta_t + 38 * self.eta_t

    @property
    def g7(self):
        return self.g6**2

    @property
    def G(self):
        return (self.S1 + self.S2 + self.S3) / 3

    @property
    def S1(self):
        return 1 - self.kappa_t + 0.9 * (1 - 1 / self.rho_t)

    @property
    def S2(self):
        out = 2 * self.f2 - 1
        out *= 2 * self.f1

        out -= 4 * self.f4
        return out

    @property
    def S3(self):
        out = 3 - 1 / self.eta_t
        out *= -120 * (self.f3 - self.f4)

        out += 50 * self.f1 + 43 - 10 * self.kappa_t

        out *= self.rho_s - self.rho_f
        out /= 30 * self.rho_f * (3 + 2 / self.eta_t)

        return out

    @property
    def f1(self):
        return self.g1 / self.g7

    @property
    def f2(self):
        if self.g1 == 0:
            return 0
        return self.g2 * self.g5 / 2 / self.g1

    @property
    def f3(self):
        return self.g3 * self.g6 / self.g7 / 10

    @property
    def f4(self):
        return self.g4 * self.g6 / self.g7 / 2

    @property
    def zeta_t(self):
        return self.zeta_s / self.zeta_f

    @property
    def eta_t(self):
        return self.eta_s / self.eta_f


class TestARFMethods(TestARFBase):

    def test_small_particle_small_delta_standing_not_implemented(self) -> None:

        self.cls.small_boundary_layer = True
        self.cls.small_particle_limit = True
        self.cls.wave_type = WaveType.STANDING
        self.assertRaises(
            NotImplementedError,
            self.cls.compute_arf,
        )

    def test_small_viscous_boundary_layer(self) -> None:
        self.assign_parameters()
        self.assertEqual(
            self.small_boundary_layer,
            self.cls.small_boundary_layer,
        )
        self.small_viscous_boundary_layer = True
        self.assign_parameters()
        self.assertEqual(
            self.small_boundary_layer,
            self.cls.small_boundary_layer,
        )

    def test_small_large_BL_ValueError(self):
        self.wave_type = WaveType.STANDING
        self.small_boundary_layer = True
        self.large_boundary_layer = True
        self.assign_parameters()

        self.assertRaises(
            ValueError,
            self.cls.compute_arf,
        )

    def test_properties(self) -> None:
        properties = [
            'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'G',
            'S1', 'S2', 'S3',
            'f1', 'f2', 'f3', 'f4',
            'eta_t', 'zeta_t',
            'rho_t', 'kappa_t', 'mu',
        ]
        self._test_properties(properties)


class TestARFLimit1Traveling(HelperTravelingARF, TestARFBase):

    def setUp(self) -> None:
        TestARFBase.setUp(self)
        self.small_boundary_layer = True
        self.large_boundary_layer = False

    def compute_arf(self):
        out = 6 * np.pi * self.rho_f * self.x_0**3
        out *= self.cls.field.abs_A_squared
        out *= self.norm_delta * (self.rho_s - self.rho_f)**2
        out /= (1 + self.mu) * (2 * self.rho_s + self.rho_f)**2

        return out


# |x| << |x_v| << 1
# |x_s | << | x_v_s | << 1
# kappa_t << 1
# rho_f << rho_s

class TestARFLimit2Traveling(HelperTravelingARF, TestARFBase):

    def setUp(self) -> None:
        TestARFBase.setUp(self)
        self.small_boundary_layer = False
        self.large_boundary_layer = True

    def compute_arf(self):
        out = np.pi / 6 * self.rho_f * self.x_0**3
        out *= self.norm_delta**2 * self.cls.field.abs_A_squared
        out *= 5 - 2 * self.kappa_t - 8 * self.f1

        return out


class TestARFLimit2Standing(HelperStandingARF, TestARFBase):

    def setUp(self) -> None:
        TestARFBase.setUp(self)
        self.small_boundary_layer = False
        self.large_boundary_layer = True

    def compute_arf(self):
        out = np.pi * self.rho_f * self.x_0**3 * self.cls.field.abs_A_squared
        out *= self.G * np.sin(2 * self.position * self.cls.k_f.real)

        return out


if __name__ == '__main__':
    unittest.main()
