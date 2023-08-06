import unittest

from osaft.core.backgroundfields import WrongWaveTypeError
from osaft.core.functions import pi, sin
from osaft.tests.basetest_arf import HelperStandingARF, HelperTravelingARF
from osaft.tests.doinikov1994rigid.setup_test_arf import BaseTestARF


class TestARFLimiting(BaseTestARF):

    def test_fastened_sphere(self) -> None:
        self.assign_parameters()
        self.assertEqual(self.fastened_sphere, self.cls.fastened_sphere)
        self.fastened_sphere = True
        self.assign_parameters()
        self.assertEqual(self.fastened_sphere, self.cls.fastened_sphere)

    def test_NotImplemented_solution(self) -> None:
        self.cls.wave_type = 'random'

        self.assertRaises(
            WrongWaveTypeError,
            self.cls.compute_arf,
        )
    # ------------------

    def test_long_wavelength(self) -> None:
        self.long_wavelength = False
        self.assign_parameters()
        self.assertEqual(
            False,
            self.cls.long_wavelength,
        )
        self.long_wavelength = True
        self.assign_parameters()
        self.assertEqual(
            True,
            self.cls.long_wavelength,
        )

    def test_small_boundary_layer(self) -> None:
        self.small_boundary_layer = False
        self.assign_parameters()
        self.assertEqual(
            False,
            self.cls.small_boundary_layer,
        )
        self.small_boundary_layer = True
        self.assign_parameters()
        self.assertEqual(
            True,
            self.cls.small_boundary_layer,
        )

    def test_large_boundary_layer(self) -> None:
        self.large_boundary_layer = False
        self.assign_parameters()
        self.assertEqual(
            False,
            self.cls.large_boundary_layer,
        )
        self.large_boundary_layer = True
        self.assign_parameters()
        self.assertEqual(
            True,
            self.cls.large_boundary_layer,
        )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def rho_t(self) -> float:
        return self.rho_f / self.rho_s

    @property
    def x_0(self) -> complex:
        return self.cls.field.k_f.real * self.R_0

    @property
    def x(self) -> complex:
        return self.cls.x

    @property
    def x_v(self) -> complex:
        return self.cls.x_v

    @property
    def norm_delta(self) -> complex:
        return self.cls.delta / self.R_0

    # -------------------------------------------------------------------------
    # Test Properties
    # -------------------------------------------------------------------------

    def test_properties(self) -> None:
        properties = [
            'x_0', 'norm_delta',
        ]
        self._test_properties(properties, threshold=1e-6)


# |x| << 1 << |x_v|


class TestARFLimit1Standing(BaseTestARF, HelperStandingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = False
        self.large_boundary_layer = False
        self.small_boundary_layer = True
        self.assign_parameters()

    def compute_arf(self):
        out = 3 * (1 - self.rho_t)**2 / (2 + self.rho_t)**2
        out *= self.cls.norm_delta
        out += (5 - 2 * self.rho_t) / (3 * (2 + self.rho_t))

        out *= pi * self.rho_f * self.cls.x_0**3 * self.cls.field.abs_A_squared
        out *= sin(2 * self.position)

        return out


class TestARFLimit1Traveling(BaseTestARF, HelperTravelingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = False
        self.large_boundary_layer = False
        self.small_boundary_layer = True
        self.assign_parameters()

    def compute_arf(self):
        out = 2 + 12 * self.rho_t - 21 * self.rho_t**2 + 7 * self.rho_t**3
        out *= -self.cls.norm_delta / (2 + self.rho_t)

        out += (1 - self.rho_t)**2

        out *= 6 * pi * self.rho_f * self.cls.x_0**3 * self.cls.norm_delta
        out *= self.cls.field.abs_A_squared / (2 + self.rho_t)**2

        return out


# |x| << |x_v| << 1

class TestARFLimit2Standing(BaseTestARF, HelperStandingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = False
        self.large_boundary_layer = True
        self.small_boundary_layer = False
        self.assign_parameters()

    def compute_arf(self):
        out = 11 * (1 - self.rho_t)
        out /= 5 * self.cls.norm_delta

        out += 2 * self.rho_t - 1

        out *= pi / 3 * self.rho_s * self.cls.x_0**3
        out *= self.cls.field.abs_A_squared
        out *= sin(2 * self.position)

        return out


class TestARFLimit2Traveling(BaseTestARF, HelperTravelingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = False
        self.large_boundary_layer = True
        self.small_boundary_layer = False
        self.assign_parameters()

    def compute_arf(self):
        out = -22 / 15 * pi * self.rho_s * self.cls.x_0**3
        out *= self.cls.field.abs_A_squared

        out *= (1 - self.rho_t) / self.cls.norm_delta

        return out


# |x| << 1 << |x_v|

class TestARFLimit3Standing(BaseTestARF, HelperStandingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = True
        self.large_boundary_layer = False
        self.small_boundary_layer = True
        self.assign_parameters()

    def compute_arf(self):
        out = 5 / 6 + 3 / 4 * self.cls.norm_delta

        out *= pi * self.rho_f * self.cls.x_0**3 * self.cls.field.abs_A_squared
        out *= sin(2 * self.position)

        return out


class TestARFLimit3Traveling(BaseTestARF, HelperTravelingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = True
        self.large_boundary_layer = False
        self.small_boundary_layer = True
        self.assign_parameters()

    def compute_arf(self):
        out = 3 / 2 * pi * self.rho_f * self.cls.x_0**3
        out *= self.cls.field.abs_A_squared

        out *= self.cls.norm_delta * (1 - self.cls.norm_delta)

        return out


# |x| << |x_v| << 1

class TestARFLimit4Standing(BaseTestARF, HelperStandingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = True
        self.large_boundary_layer = True
        self.small_boundary_layer = False
        self.assign_parameters()

    def compute_arf(self):
        out = 1 + 10 / 27 / self.cls.norm_delta

        out *= pi * self.rho_f * self.cls.x_0**3 * self.cls.field.abs_A_squared
        out *= 0.9 * sin(2 * self.position)
        out *= self.cls.norm_delta

        return out


class TestARFLimit4Traveling(BaseTestARF, HelperTravelingARF):

    def setUp(self) -> None:
        super().setUp()
        self.long_wavelength = True
        self.fastened_sphere = True
        self.large_boundary_layer = True
        self.small_boundary_layer = False
        self.assign_parameters()

    def compute_arf(self):
        out = -3 / 2 * pi * self.rho_f * self.cls.x_0**3
        out *= self.cls.field.abs_A_squared

        out *= self.cls.norm_delta**2 * (1 - 6 / 5 / self.cls.norm_delta)

        return out


if __name__ == '__main__':
    unittest.main()
