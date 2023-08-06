from typing import Optional, Union

from osaft import log
from osaft.core.functions import pi
from osaft.solutions.base_arf import BaseARF
from osaft.solutions.doinikov2021viscous.streaming import StreamingField


class ARF(StreamingField, BaseARF):
    """ARF class for Doinikov (viscous fluid-elastic sphere; 2021)

    :param f: frequency [Hz]
    :param R_0: radius [m]
    :param rho_s: density of the particle [kg/m^3]
    :param E_s: Young's modulus of the particle [Pa]
    :param nu_s: Poisson's ratio of the particle [-]
    :param rho_f: density of the fluid [kg/m^3]
    :param c_f: speed of sound in the fluid [m/s]
    :param eta_f: fluid component shear viscosity [Pa s]
    :param zeta_f: fluid component bulk viscosity [Pa s]
    :param p_0: pressure amplitude [Pa]
    :param wave_type: wave type
    :param position: position in the standing wave field [m]
    :param N_max: truncation of the summation index (highest order mode)
    :param inf_factor: see :attr:`.inf_factor`
    :param inf_type: see :attr:`.inf_type`
    :param integration_rel_eps:  relative eps for adaptive integration
    """

    # -------------------------------------------------------------------------
    # User-facing methods
    # -------------------------------------------------------------------------

    def compute_arf(
            self, return_error: bool = False,
    ) -> Union[float, tuple[float, float]]:

        self.check_wave_type()

        # Integral 1
        integral_1 = self.I_1()
        error_1 = self.I_1_error()

        # Error estimation
        rel_error = error_1 / integral_1

        if abs(rel_error) > 0.01:  # pragma: no cover
            log.warning(
                f'Estimated relative error is {rel_error} > 0.01 \n'
                f'If you want to decrease it try to change the integration '
                f'precision `int_eps` or the integration boundary '
                f'`inf_factor` and `inf_type` \n',
            )
        else:
            log.info(
                f'Estimated relative error is {rel_error} < 0.01 \n',
            )
        if return_error:
            return integral_1, error_1
        else:
            return integral_1

    # -------------------------------------------------------------------------
    # Dependent Variables Methods
    # -------------------------------------------------------------------------

    def _compute_C_0(self, L_max: Optional[int] = 1) -> dict:
        return super()._compute_C_0(L_max=L_max)

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def I_1(self) -> float:
        """Integral :math:`I_1`

        (Eq. 27)
        """
        def term_second_sum(l: int) -> float:

            if l == 0:
                t_1 = 0
            else:
                t_1 = self.V_r(l, self.R_0, True, True)
                t_1 += (l + 1) * self.V_theta(l, self.R_0, True, True)
                t_1 *= self.V_r(l - 1, self.R_0, True, True).conjugate()
                t_1 *= l / ((2 * l - 1) * (2 * l + 1))

            t_2 = self.V_r(l, self.R_0, True, True)
            t_2 -= l * self.V_theta(l, self.R_0, True, True)
            t_2 *= self.V_r(l + 1, self.R_0, True, True).conjugate()
            t_2 *= (l + 1) / ((2 * l + 1) * (2 * l + 3))

            return (t_1 + t_2).real

        term_1 = 4 * self.eta_f / self.R_0 ** 2 * self.C_0[3, 1]
        term_2 = 2 / 3 * self.R_0 * self.rho_f * self.gamma(1, self.R_0, False)
        first_sum = term_1 + term_2

        second_sum = 0
        for n in self.range_N_max:
            second_sum += term_second_sum(n)
        return (
            2 * pi * self.R_0 ** 2
            * (first_sum - self.rho_f * second_sum)
        )

    def I_1_error(self) -> float:
        """Estimated numerical error for integral :math:`I_1`

        (Eq. 27)
        """
        return 8 * self.eta_f * self.C_0_error[3, 1]


if __name__ == '__main__':
    pass
