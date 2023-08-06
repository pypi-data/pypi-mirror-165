from osaft import WaveType, doinikov1994compressible, settnes2012
from osaft.tests.basetest import BaseTest


class TestCompareSettnesStanding(BaseTest):

    def setUp(self):
        super().setUp()

        self.wave_type = WaveType.STANDING

        # Viscosity
        self.arf_compare_threshold = 10e-1
        self.small_boundary_layer = False
        self.large_boundary_layer = False

        # Viscosity
        self.eta_s = 1e-3
        self.zeta_s = 0
        self.zeta_f = 0
        self.eta_f = 1e-4
        self.R_0 = 5e-6

        # Frequency
        self.f = 2e6

        # Density
        self.rho_s = 2500

        self.cls = doinikov1994compressible.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s, c_s=self.c_s,
            eta_s=self.eta_s, zeta_s=self.zeta_s,
            rho_f=self.rho_f, c_f=self.c_f,
            eta_f=self.eta_f, zeta_f=self.zeta_f,
            p_0=self.p_0, wave_type=self.wave_type, position=self.position,
        )

        self.compare_cls = settnes2012.ARF(
            f=self.f,
            R_0=self.R_0,
            rho_s=self.rho_s, c_s=self.c_s,
            rho_f=self.rho_f, c_f=self.c_f,
            eta_f=self.eta_f,
            p_0=self.p_0, wave_type=self.wave_type, position=self.position,
        )

        self.list_cls = [self.cls, self.compare_cls]

    def test_comparison_arf(self):
        self.assertAlmostEqual(self.cls.compute_arf(), self.cls.compute_arf())


if __name__ == '__main__':
    pass
