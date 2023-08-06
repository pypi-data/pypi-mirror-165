import unittest

from osaft import Doinikov1994Rigid
from osaft.tests.basedoinikov1994.test_base import TestBaseDoinikov1994


class BaseTestARF(TestBaseDoinikov1994):

    def setUp(self) -> None:

        super().setUp()

        self.long_wavelength = False
        self.small_boundary_layer = False
        self.large_boundary_layer = False
        self.background_streaming = True
        self.fastened_sphere = False
        self.N_max = 5

        self._eta_f.low = 1e-5
        self._eta_f.high = 1e-3
        self._f.low = 1e6
        self._f.high = 10e6
        self._R_0.low = 1e-6

        self.cls = Doinikov1994Rigid.ARF(
            f=self.f, R_0=self.R_0,
            rho_s=self.rho_s, rho_f=self.rho_f,
            c_f=self.c_f, eta_f=self.eta_f, zeta_f=self.zeta_f,
            p_0=self.p_0, wave_type=self.wave_type,
            position=self.position,
            long_wavelength=self.long_wavelength,
            small_boundary_layer=self.small_boundary_layer,
            large_boundary_layer=self.large_boundary_layer,
            fastened_sphere=self.fastened_sphere,
            N_max=self.N_max,
        )

        self.list_cls = [self.cls]

    def assign_parameters(self) -> None:
        super().assign_parameters()

        self.cls.fastened_sphere = self.fastened_sphere
        self.cls.small_boundary_layer = self.small_boundary_layer
        self.cls.large_boundary_layer = self.large_boundary_layer
        self.cls.long_wavelength = self.long_wavelength
        self.cls.background_streaming = self.background_streaming
        self.cls.N_max = self.N_max


if __name__ == '__main__':
    unittest.main()
