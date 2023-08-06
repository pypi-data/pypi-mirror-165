import unittest

from osaft.solutions.basedoinikov1994.base import BaseDoinikov1994
from osaft.tests.basetest import BaseTest


class BaseTestDoinikov1994(BaseTest):

    def setUp(self) -> None:

        super().setUp()
        self.cls = BaseDoinikov1994(
            self.f, self.R_0,
            self.rho_f, self.c_f,
            self.eta_f, self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
        )

    @property
    def x_0(self) -> complex:
        return self.cls.field.k_f.real * self.R_0

    @property
    def x(self) -> complex:
        return self.cls.field.k_f * self.R_0

    @property
    def x_v(self) -> complex:
        return self.cls.field.k_v * self.R_0

    @property
    def norm_delta(self) -> complex:
        return self.cls.fluid.delta / self.R_0

    @property
    def rho_t(self):
        return self.rho_f / self.rho_s


class TestBaseDoinikov1994(BaseTestDoinikov1994):

    def test_properties(self) -> None:
        properties = ['x', 'x_0', 'x_v', 'norm_delta']
        self._test_properties(properties)


if __name__ == '__main__':
    unittest.main()
