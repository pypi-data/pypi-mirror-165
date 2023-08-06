import unittest

from osaft.core.functions import pi, sin, xexpexp1
from osaft.tests.basetest_arf import HelperStandingARF, HelperTravelingARF
from osaft.tests.doinikov1994rigid.setup_test_arf import BaseTestARF


class TestARFArbitraryBL(BaseTestARF):

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

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
    # D_n
    # -------------------------------------------------------------------------

    def D_n_limit(self, n: int) -> complex:
        if n == 0:
            return self.D_0
        elif n == 1:
            return self.D_1
        else:
            raise ValueError('D_n in the limit is only defined for n = 0, 1')

    @property
    def D_0(self):
        out = self.G_1
        out += self.x_v ** 3 * (12 + self.x_v ** 2) * self.function(self.x_v)
        out *= -self.x ** 3 * self.G_0
        out += 2 * self.x ** 3 / 9
        out += self.x ** 3 / (3 * self.x_v ** 2)
        return out

    @property
    def D_1(self):
        out = - 2 * (1 + 1j) * (9 + self.x_v ** 2)
        out *= self.function(self.x_v - 1j * self.x_v)
        out += 2 * self.G_3 * self.function(self.x_v)
        out += 1j * self.G_4 * self.function(-1j * self.x_v)
        out *= - self.x_v ** 3
        out += self.G_2
        out *= self.cls.x ** 3 * self.G_0.conjugate() / (1 + self.x_v)
        out += self.cls.x ** 3 / (3 * self.x_v ** 2)
        return out

    @staticmethod
    def function(z):
        return xexpexp1(z)

    # -------------------------------------------------------------------------
    # G_n
    # -------------------------------------------------------------------------

    @property
    def G_0(self) -> complex:
        denominator = 72 * (
            9 * self.rho_t + 9 * self.rho_t * self.x_v
            + (2 + self.rho_t) * self.x_v ** 2
        )
        numerator = (1 - self.rho_t)
        return numerator / denominator

    @property
    def G_1(self) -> complex:
        out = 48 - 96 * self.x_v + 2 * self.x_v ** 2 - 14 * self.x_v ** 3
        out += self.x_v ** 4 - self.x_v ** 5
        return out

    @property
    def G_2(self):
        out = 48 + (48 + 192 * 1j / 5) * self.x_v
        out += (122 + 192 * 1j) * self.x_v ** 2 / 5
        out += 42 * (1 - 1j) * self.x_v ** 3 / 5
        out += (49 + 36 * 1j) * self.x_v ** 4 / 10
        out -= (31 - 17 * 1j) * self.x_v ** 5 / 10
        out += (6 + 31 * 1j) * self.x_v ** 6 / 30
        out += (1 + 6 * 1j) * self.x_v ** 7 / 30
        out += 1j * self.x_v ** 8 / 30
        return out

    @property
    def G_3(self):
        return 3 - 3 * 1j * self.x_v - self.x_v ** 2

    @property
    def G_4(self):
        out = 9 + 9 * self.x_v + 41 * self.x_v ** 2 / 10
        out += 11 * self.x_v ** 3 / 10
        out += self.x_v ** 4 / 5 + self.x_v ** 5 / 30
        return out

    # -------------------------------------------------------------------------
    # F2 (Streaming contribution)
    # -------------------------------------------------------------------------

    def F_2_standing(self):
        k = self.cls.k_f
        x = self.x
        x_v = self.x_v
        d = self.cls.abs_pos
        first = sin(k * d + k.conjugate() * d) * sin(x + x.conjugate())
        first *= (x - x.conjugate()) / (x + x.conjugate())
        second = sin(k * d - k.conjugate() * d) * sin(x - x.conjugate())
        second *= (x + x.conjugate()) / (x - x.conjugate())
        out = first - second
        out *= - 3 / 4 * pi * self.rho_f * self.cls.field.abs_A_squared
        out *= x * x.conjugate()
        out /= x_v**2
        return out

    def F_2_travelling(self):
        x = self.x
        x_v = self.x_v

        out = sin(x - x.conjugate()) / (x - x.conjugate()) * 1j / x_v**2
        out *= x * x.conjugate() * (x + x.conjugate())
        out *= - 3 / 2 * pi * self.rho_f * self.cls.field.abs_A_squared
        return out

    def test_F_2_standing(self):
        self.do_testing(
            self.cls._F_2_standing, self.F_2_standing,
            threshold=1e-8,
        )

    def test_F_2_travelling(self):
        self.do_testing(
            self.cls._F_2_travelling, self.F_2_travelling,
            threshold=1e-8,
        )

    def test_methods_n(self):

        dict_methods = dict()
        dict_methods['D_n_limit'] = None
        self.background_streaming = True
        self.assign_parameters()
        self._test_methods_n(dict_methods, n_end=1, threshold=1e-8)

    def test_properties(self):
        dict_properties = dict()
        dict_properties['G_0'] = None
        dict_properties['G_1'] = None
        dict_properties['G_2'] = None
        dict_properties['G_4'] = None
        dict_properties['D_0'] = None
        dict_properties['D_1'] = None
        self.background_streaming = True
        self.assign_parameters()
        self._test_properties(dict_properties, threshold=1e-6)

    def test_D_n_error(self):
        self.assertRaises(ValueError, self.cls.D_n_limit, 2)


# |x| << 1  |x| << |x_v|
class TestSmallParticleTravelling(BaseTestARF, HelperTravelingARF):

    def setUp(self):
        super().setUp()
        self._threshold = 1e-3
        self.long_wavelength = True
        self.fastened_sphere = False
        self.large_boundary_layer = False
        self.small_boundary_layer = False
        self.background_streaming = True
        self.assign_parameters()

    def compute_arf(self):
        D_0 = self.cls.D_0
        D_1 = self.cls.D_1
        F1 = D_0 - D_0.conjugate()
        F1 += 2 * (D_1 - D_1.conjugate())
        F1 *= 3 / 2 * 1j * pi * self.rho_f * self.cls.field.abs_A_squared
        F2 = self.cls._F_2_travelling() if self.background_streaming else 0
        S_9 = 0 if self.background_streaming else self.cls.S_9n_contribution()
        return (F1 + F2 - S_9).real


class TestSmallParticleStanding(BaseTestARF, HelperStandingARF):

    def setUp(self):
        super().setUp()
        self._threshold = 1e-3
        self.long_wavelength = True
        self.fastened_sphere = False
        self.large_boundary_layer = False
        self.small_boundary_layer = False
        self.background_streaming = True
        self.assign_parameters()

    def compute_arf(self):
        D_0 = self.cls.D_0
        D_1 = self.cls.D_1
        sine = sin(2 * self.cls.k_f * self.cls.abs_pos)
        sine_conj = sin(2 * self.cls.k_f.conjugate() * self.cls.abs_pos)
        F1 = D_0 * sine + D_0.conjugate() * sine_conj
        F1 -= 2 * (D_1 * sine + D_1.conjugate() * sine_conj)
        F1 *= 3 / 4 * pi * self.rho_f * self.cls.field.abs_A_squared
        F2 = self.cls._F_2_standing() if self.background_streaming else 0
        S_9 = 0 if self.background_streaming else self.cls.S_9n_contribution()
        return (F1 + F2 - S_9).real


if __name__ == '__main__':
    unittest.main()
