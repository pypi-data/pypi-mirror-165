from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cache

import mpmath
import numpy as np
from scipy.special import factorial

from osaft.core.backgroundfields import BackgroundField, WaveType
from osaft.core.functions import BesselFunctions as Bf
from osaft.core.functions import conj, full_range, integrate, pi
from osaft.core.variable import ActiveListVariable, ActiveVariable


class BaseGeneralARF(ABC):
    """Abstract base class for the computation of the acoustic radiation
    force for particle radius and  arbitrary boundary layer thickness
    """

    # Required attributes by child class (Active Variables)
    _x: ActiveVariable
    _x_v: ActiveVariable
    _alpha_n: ActiveVariable
    _beta_n: ActiveVariable
    field: BackgroundField

    # Required properties by child class
    abs_pos: float
    background_streaming: bool
    k_f: complex
    N_max: int
    rho_f: float
    wave_type: WaveType
    x: complex
    x_v: complex

    def __init__(self) -> None:
        """Constructor method
        """

        self._D_n = ActiveListVariable(
            self._compute_D_n,
            'ARF coefficient D_n',
        )

        self._S_1n = ActiveListVariable(
            self._compute_S_1n,
            'ARF coefficient S_{1n}',
        )

        self._S_2n = ActiveListVariable(
            self._compute_S_2n,
            'ARF coefficient S_{2n}',
        )

        self._S_3n = ActiveListVariable(
            self._compute_S_3n,
            'ARF coefficient S_{3n}',
        )

        self._S_4n = ActiveListVariable(
            self._compute_S_4n,
            'ARF coefficient S_{4n}',
        )

        self._S_5n = ActiveListVariable(
            self._compute_S_5n,
            'ARF coefficient S_{5n}',
        )

        self._S_6n = ActiveListVariable(
            self._compute_S_6n,
            'ARF coefficient S_{6n}',
        )

        self._S_7n = ActiveListVariable(
            self._compute_S_7n,
            'ARF coefficient S_{7n}',
        )

        self._S_8n = ActiveListVariable(
            self._compute_S_8n,
            'ARF coefficient S_{8n}',
        )

        self._S_9n = ActiveListVariable(
            self._compute_S_9n,
            'ARF coefficient S_{9n}',
        )

        self._D_n.is_computed_by(
            self._alpha_n, self._beta_n, self._S_1n, self._S_2n,
            self._S_3n, self._S_4n, self._S_5n, self._S_6n, self._S_7n,
            self._S_8n, self._S_9n,
        )
        self._S_1n.is_computed_by(self._x, self._x_v)
        self._S_2n.is_computed_by(self._x, self._x_v)
        self._S_3n.is_computed_by(self._x, self._x_v)
        self._S_4n.is_computed_by(self._x, self._x_v)
        self._S_5n.is_computed_by(self._x, self._x_v)
        self._S_6n.is_computed_by(self._x, self._x_v)
        self._S_7n.is_computed_by(self._x, self._x_v)
        self._S_8n.is_computed_by(self._x, self._x_v)
        self._S_9n.is_computed_by(self._x, self._x_v)

    # -------------------------------------------------------------------------
    # Acoustic radiation force
    # -------------------------------------------------------------------------

    def _general_solution(self) -> float:
        if self.wave_type == WaveType.STANDING:
            return self._standing_general_solution()
        else:
            return self._travelling_general_solution()

    def _F_1(self):
        # F1 according to Eq. (5.15) for the rigid particle
        def term(n: int):
            term_1 = self.D_n(n) * self.field.A_in(n)
            term_1 *= conj(self.field.A_in(n + 1))
            term_2 = conj(self.D_n(n)) * self.field.A_in(n + 1)
            term_2 *= conj(self.field.A_in(n))
            prefactor = (n + 1) / (2 * n + 1) / (2 * n + 3)
            return prefactor * (term_1 + term_2)

        F1 = -3 / 2 * pi * self.rho_f * sum(
            [term(n) for n in full_range(self.N_max)],
        )
        return F1.real

    def _standing_general_solution(self) -> float:
        F1 = self._F_1()
        F2 = self._F_2_standing() if self.background_streaming else 0
        return F1 + F2

    def _travelling_general_solution(self) -> float:
        F1 = self._F_1()
        F2 = self._F_2_travelling() if self.background_streaming else 0
        return F1 + F2

    # -------------------------------------------------------------------------
    # Abstract Methods
    # -------------------------------------------------------------------------

    @abstractmethod
    def alpha_n(self, n: int) -> complex:
        pass

    @abstractmethod
    def beta_n(self, n: int) -> complex:
        pass

    @abstractmethod
    def _F_2_standing(self) -> float:
        pass

    @abstractmethod
    def _F_2_travelling(self) -> float:
        pass

    # -------------------------------------------------------------------------
    # D_n
    # -------------------------------------------------------------------------

    def D_n(self, n: int) -> complex:
        """ coefficient :math:`D_{n}`

        :param n: order
        """
        return self._D_n.item(n)

    def _compute_D_n(self, n: int) -> None:
        # computation according to appendix (5.6)

        n1 = n + 1
        # first term
        out = self.S_1n(n) * self.alpha_n(n) * conj(self.alpha_n(n1))
        out += self.S_2n(n) * self.beta_n(n) * conj(self.beta_n(n1))
        out -= self.S_3n(n) * self.alpha_n(n) * conj(self.beta_n(n1))
        out -= self.S_4n(n) * self.beta_n(n) * conj(self.alpha_n(n1))
        out += self.S_5n(n) * self.alpha_n(n)
        out += self.S_6n(n) * conj(self.alpha_n(n1))
        out -= self.S_7n(n) * self.beta_n(n)
        out -= self.S_8n(n) * conj(self.beta_n(n1))
        out += self.S_9n(n) if self.background_streaming else 0

        return out

    # ------------------------------------------------------------------------
    # G_n_l
    # ------------------------------------------------------------------------

    @staticmethod
    def G_n_l(n: int, l: int, x: complex) -> complex:
        """Coefficient :math:`G_{n}^{(l)}(x)` from the appendix

        :param n: order
        :param l: kind of Hankel function
        """
        x_con = conj(x)
        if l == 1:
            tmp1 = Bf.d1_hankelh1(n, x_con)
            tmp2 = Bf.d1_hankelh1(n + 1, x_con)
        elif l == 2:
            tmp1 = Bf.d1_hankelh2(n, x_con)
            tmp2 = Bf.d1_hankelh2(n + 1, x_con)
        else:
            raise ValueError(f'l can only be 1 or 2 nor {l}')

        out = x_con * Bf.d1_hankelh1(n, x) * tmp1
        out += x * Bf.d1_hankelh1(n + 1, x) * tmp2

        return out

    def G_sum_1(self, n):
        """Numerically stable evaluation of
        :math:`(G_{n}^{(1)}(x) + G_{n}^{(2)}(x)) / 2`

        :param n: order
        """
        x = self.x
        x_con = self.x.conjugate()
        bessel_n = Bf.d1_besselj(n, x_con)
        bessel_n1 = Bf.d1_besselj(n + 1, x_con)
        term_1 = x_con * Bf.d1_hankelh1(n, x) * bessel_n
        term_2 = x * Bf.d1_hankelh1(n + 1, x) * bessel_n1
        return term_1 + term_2

    def G_sum_2(self, n):
        """Numerically stable evaluation of
        :math:`(G_{n}^{(1)*}(x^*) + G_{n}^{(2)}(x)) / 2`

        :param n: order
        """
        x = self.x
        x_con = self.x.conjugate()
        bessel_n = Bf.d1_besselj(n, x)
        bessel_n1 = Bf.d1_besselj(n + 1, x)
        term_1 = x_con * Bf.d1_hankelh1(n, x_con) * bessel_n
        term_2 = x * Bf.d1_hankelh1(n + 1, x_con) * bessel_n1
        return -(term_1 + term_2)

    # ------------------------------------------------------------------------
    # K_n_l
    # ------------------------------------------------------------------------

    def K_n_l(self, n: int, l: int) -> complex:
        """Coefficient :math:`K_{n}^{(l)}(x)` from the appendix

        :param n: order
        :param l: kind of Hankel function
        """
        x_con = self.x.conjugate()
        if l == 1:
            tmp1 = Bf.d1_hankelh1(n, x_con)
            tmp2 = Bf.d1_hankelh1(n + 1, x_con)
        elif l == 2:
            tmp1 = Bf.d1_hankelh2(n, x_con)
            tmp2 = Bf.d1_hankelh2(n + 1, x_con)
        else:
            raise ValueError(f'l can only be 1 or 2 nor {l}')

        out = (n + 1) * x_con**2 / self.x_v**2 * tmp1
        out *= Bf.hankelh1(n, self.x_v)

        out -= x_con * Bf.d1_hankelh1(n + 1, self.x_v) * tmp2
        return out

    def K_sum(self, n: int):
        """Numerically stable evaluation of
        :math:`(K_{n}^{(1)}(x) + K_{n}^{(2)}(x)) / 2`

        :param n: order
        """
        x_v = self.x_v
        x_con = self.x.conjugate()
        prefactor = (n + 1) * x_con**2 / x_v**2
        term_1 = Bf.hankelh1(n, x_v) * Bf.d1_besselj(n, x_con)
        term_2 = x_con * Bf.d1_hankelh1(n + 1, x_v)
        term_2 *= Bf.d1_besselj(n + 1, x_con)
        return prefactor * term_1 - term_2

    # ------------------------------------------------------------------------
    # L_n_l
    # ------------------------------------------------------------------------

    def L_n_l(self, n: int, l: int) -> complex:
        """Numerically stable evaluation of
        :math:`(K_{n}^{(1)}(x) + K_{n}^{(2)}(x)) / 2`

        :param n: order
        :param l: kind of Hankel function
        """
        x_v_con = self.x_v.conjugate()
        if l == 1:
            tmp1 = Bf.d1_hankelh1(n, self.x)
            tmp2 = Bf.d1_hankelh1(n + 1, self.x)
        elif l == 2:
            tmp1 = Bf.d1_hankelh2(n, self.x)
            tmp2 = Bf.d1_hankelh2(n + 1, self.x)
        else:
            raise ValueError(f'l can only be 1 or 2 nor {l}')

        out = - (n + 1) * self.x**2 / self.x_v**2 * tmp2
        out *= Bf.hankelh2(n + 1, x_v_con)

        out += self.x * Bf.d1_hankelh2(n, x_v_con) * tmp1
        return out

    def L_sum(self, n: int) -> complex:
        """Numerically stable evaluation of
        :math:`(L_{n}^{(1)}(x) + L_{n}^{(2)}(x)) / 2`

        :param n: order
        """
        x = self.x
        x_v = self.x_v
        x_v_con = self.x_v.conjugate()
        term_1 = x * Bf.d1_hankelh2(n, x_v_con) * Bf.d1_besselj(n, x)
        term_2 = (n + 1) * x**2 / x_v**2 * Bf.hankelh2(n + 1, x_v_con)
        term_2 *= Bf.d1_besselj(n + 1, x)
        return term_1 - term_2

    # -------------------------------------------------------------------------
    # H_nm, J_nm
    # -------------------------------------------------------------------------

    @staticmethod
    def B_kq(k: int, q: int, m: int, n: int) -> complex:
        """Coefficient :math:`B_{kq}` from the appendix

        :param k: :math:`k`
        :param q: :math:`q`
        :param m: :math:`m`
        :param n: :math:`n`
        """
        numerator = 1j ** (m - n) * (-1) ** k
        numerator *= factorial(n + k) * factorial(m + q)
        denominator = (2 * 1j) ** (k + q) * factorial(k) * factorial(n - k)
        denominator *= factorial(q) * factorial(m - q)
        return numerator / denominator

    @cache
    def J_nm_j(
            self,
            x1: complex,
            x2: complex,
            n: int,
            m: int,
            j: int,
    ) -> complex:
        """Integral :math:`J_{nm}^{(j)}`

        :param x1: :math:`x_1`
        :param x2: :math:`x_2`
        :param n: :math:`n`
        :param m: :math:`m`
        :param j: :math:`j`
        """
        if 1.01 * abs(x1.real) > abs(x1.imag) > 0.99 * abs(x1.real):
            return self._J_nm_j_quadrature(x1, x2, n, m, j)
        else:
            return self._J_nm_j_sum(x1, x2, n, m, j)

    @cache
    def H_nm_j(
            self,
            x1: complex,
            x2: complex,
            n: int,
            m: int,
            j: int,
    ) -> complex:
        """Integral :math:`H_{nm}^{(j)}`

        :param x1: :math:`x_1`
        :param x2: :math:`x_2`
        :param n: :math:`n`
        :param m: :math:`m`
        :param j: :math:`j`
        """
        return self.H_nm_j_sum(x1, x2, n, m, j)

    @cache
    def H_nm_j_sum(
            self,
            x1: complex,
            x2: complex,
            n: int,
            m: int,
            j: int,
    ) -> complex:
        """Coefficient :math:`H_{nm}^{(j)}`

        :param x1: argument x1
        :param x2: argument x2
        :param n: order n
        :param m: order m
        :param j: exponent
        """
        out = mpmath.mpc(0)
        arg_1 = mpmath.mpc(1j * x2.conjugate() - 1j * x1)
        for k in full_range(n):
            for q in full_range(m):
                M = 2 + k + q + j
                term = mpmath.expint(M, arg_1)
                term *= mpmath.mpc(x1 ** (-(k + 1)))
                term *= mpmath.mpc(x2.conjugate() ** (-(q + 1)))
                term *= self.B_kq(k, q, m, n)
                out += term
        return complex(out)

    def _J_nm_j_sum(
            self,
            x1: complex,
            x2: complex,
            n: int,
            m: int,
            j: int,
    ) -> complex:
        """Integrate J_nm using sum of Bessel functions

        :param x1: :math:`x_1`
        :param x2: :math:`x_2`
        :param n: :math:`n`
        :param m: :math:`m`
        :param j: :math:`j`
        """
        arg_1 = mpmath.mpc(- 1j * x1 + 1j * x2.conjugate())
        arg_2 = mpmath.mpc(- 1j * x1 - 1j * x2.conjugate())
        out = mpmath.mpc(0)
        for k in full_range(n):
            for q in full_range(m):
                M = 2 + k + q + j
                term = mpmath.expint(M, arg_1)
                term -= (- 1) ** (q + m) * mpmath.expint(M, arg_2)
                term *= mpmath.mpc(x1 ** (-(k + 1)))
                term *= mpmath.mpc(x2.conjugate() ** (-(q + 1)))
                term *= self.B_kq(k, q, m, n)
                out += term
        return complex(0.5 * out)

    def _J_nm_j_quadrature(
            self,
            x1: complex,
            x2: complex,
            n: int,
            m: int,
            j: int,
    ) -> complex:
        """Integrate J_nm using quadrature

        :param x1: :math:`x_1`
        :param x2: :math:`x_2`
        :param n: :math:`n`
        :param m: :math:`m`
        :param j: :math:`j`
        """
        def kernel(y: float) -> complex:
            out = y ** (-j) * Bf.hankelh1(n, x1 * y)
            out *= Bf.besselj(m, x2.conjugate() * y)
            return out

        return self._integrate_J_nm_H_nm(kernel)

    @staticmethod
    def _integrate_J_nm_H_nm(kernel):
        """Integrate J_nm or H_nm using quadrature

        :param kernel: kernel for integration
        """
        def real_kernel(y: float) -> float:
            return kernel(y).real

        def imag_kernel(y: float) -> float:
            return kernel(y).imag

        real_part, _ = integrate(real_kernel, 1, np.inf)
        imag_part, _ = integrate(imag_kernel, 1, np.inf)

        return real_part + 1j * imag_part

    # ------------------------------------------------------------------------
    # S_in
    # ------------------------------------------------------------------------

    def S_1n(self, n: int) -> complex:
        """ coefficient :math:`S_{1n}`

        :param n: order
        """
        return self._S_1n.item(n)

    def _compute_S_1n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = x.conjugate()
        x_v = self.x_v
        n1 = n + 1
        # first term
        term_1 = self.H_nm_j(x, x, n, n1, 0)
        term_1 -= self.H_nm_j(x, x, n, n1, 2)
        term_1 *= ((n + 2) * x**2 - n * x_con**2) / 2

        # second term
        term_2 = self.H_nm_j(x, x, n1, n, 0)
        term_2 -= self.H_nm_j(x, x, n1, n, 2)
        term_2 *= x * x_con

        # third term
        term_3 = x * x_con / x_v**2 * self.G_n_l(n, 2, x)

        # last term
        term_4 = n * x_con * self.H_nm_j(x, x, n, n, 1)
        term_4 += (n + 2) * x * self.H_nm_j(x, x, n1, n1, 1)
        term_4 -= x_con * x * self.H_nm_j(x, x, n1, n, 0)
        term_4 *= (x**2 - x_con**2) / x_v**2

        return term_1 - term_2 + term_3 + term_4

    def S_2n(self, n: int) -> complex:
        """ coefficient :math:`S_{2n}`

        :param n: order
        """
        return self._S_2n.item(n)

    def _compute_S_2n(self, n: int) -> complex:
        # computation according to appendix A
        x_v = self.x_v
        x_v_con = x_v.conjugate()
        n1 = n + 1
        # first term
        term_1 = self.H_nm_j(x_v, x_v, n1, n, 0)
        term_1 -= self.H_nm_j(x_v, x_v, n1, n, 2)
        term_1 *= x_v * x_v_con
        # second term
        term_2 = self.H_nm_j(x_v, x_v, n, n1, 0)
        term_2 -= self.H_nm_j(x_v, x_v, n, n1, 2)
        term_2 *= n1 * x_v**2

        # third term
        term_3 = Bf.d1_hankelh1(n1, x_v) * Bf.hankelh2(n1, x_v_con)
        term_3 += Bf.hankelh1(n, x_v) * Bf.d1_hankelh2(n, x_v_con)
        term_3 *= n1

        return n * (n + 2) * (term_1 - term_2 - term_3)

    def S_3n(self, n: int) -> complex:
        """ coefficient :math:`S_{3n}`

        :param n: order
        """
        return self._S_3n.item(n)

    def _compute_S_3n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_v = self.x_v
        x_v_con = x_v.conjugate()
        n1 = n + 1

        # first term
        term_1 = self.H_nm_j(x, x_v, n, n1, 0)
        term_1 -= self.H_nm_j(x, x_v, n, n1, 2)
        term_1 *= (n * x_v_con**2 - n1 * x**2) / 2

        # second term
        term_2 = self.H_nm_j(x, x_v, n1, n, 0)
        term_2 -= self.H_nm_j(x, x_v, n1, n, 2)
        term_2 *= x * x_v_con

        # third term
        term_3 = self.H_nm_j(x, x_v, n, n, -1)
        term_3 -= self.H_nm_j(x, x_v, n, n, 1)
        term_3 *= x**2 * x_v_con / 2

        # fourth term
        term_4 = self.H_nm_j(x, x_v, n1, n1, -1)
        term_4 -= self.H_nm_j(x, x_v, n1, n1, 1)
        term_4 *= x * x_v**2 / 2

        # fifth term
        term_5 = n * x_v_con * self.H_nm_j(x, x_v, n, n, 1)
        term_5 -= n1 * x * self.H_nm_j(x, x_v, n1, n1, 1)
        term_5 *= x**2 / x_v**2

        # sixth term
        term_6 = self.L_n_l(n, 1)

        return (n + 2) * (term_1 - term_2 + term_3 + term_4 + term_5 - term_6)

    def S_4n(self, n: int) -> complex:
        """ coefficient :math:`S_{4n}`

        :param n: order
        """
        return self._S_4n.item(n)

    def _compute_S_4n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = x.conjugate()
        x_v = self.x_v
        n1 = n + 1
        # first term
        term_1 = self.H_nm_j(x_v, x, n, n1, 0)
        term_1 -= self.H_nm_j(x_v, x, n, n1, 2)
        term_1 *= ((n + 2) * x_v**2 - n1 * x_con**2) / 2

        # second term
        term_2 = self.H_nm_j(x_v, x, n1, n, 0)
        term_2 -= self.H_nm_j(x_v, x, n1, n, 2)
        term_2 *= x_con * x_v

        # third term
        term_3 = self.H_nm_j(x_v, x, n, n, -1)
        term_3 -= self.H_nm_j(x_v, x, n, n, 1)
        term_3 *= x_con * x_v**2 / 2

        # fourth term
        term_4 = self.H_nm_j(x_v, x, n1, n1, -1)
        term_4 -= self.H_nm_j(x_v, x, n1, n1, 1)
        term_4 *= x_con**2 * x_v / 2

        # fifth term
        term_5 = (n + 2) * x_v * self.H_nm_j(x_v, x, n1, n1, 1)
        term_5 = n1 * x_con * self.H_nm_j(x_v, x, n, n, 1) - term_5
        term_5 *= x_con**2 / x_v**2

        # sixth term
        term_6 = self.K_n_l(n, 2)

        return n * (term_1 + term_2 - term_3 + term_4 - term_5 + term_6)

    def S_5n(self, n: int) -> complex:
        """ coefficient :math:`S_{5n}`

        :param n: order
        """
        return self._S_5n.item(n)

    def _compute_S_5n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = x.conjugate()
        x_v = self.x_v
        n1 = n + 1

        # first term
        term_1 = self.J_nm_j(x, x, n, n1, 0)
        term_1 -= self.J_nm_j(x, x, n, n1, 2)
        term_1 *= 0.5 * ((n + 2) * x**2 - n * x_con**2)

        # second term
        term_2 = self.J_nm_j(x, x, n1, n, 0)
        term_2 -= self.J_nm_j(x, x, n1, n, 2)
        term_2 *= x_con * x

        # third term
        term_3 = self.G_sum_1(n)
        term_3 *= x_con * x / x_v**2

        # fourth term
        term_4 = n * x_con * self.J_nm_j(x, x, n, n, 1)
        term_4 += (n + 2) * x * self.J_nm_j(x, x, n1, n1, 1)
        term_4 -= x_con * x * self.J_nm_j(x, x, n1, n, 0)
        term_4 *= (x**2 - x_con**2) / x_v**2

        return term_1 - term_2 + term_3 + term_4

    def S_6n(self, n: int) -> complex:
        """ coefficient :math:`S_{6n}`

        :param n: order
        """
        self._compute_S_6n(n)
        return self._S_6n.item(n)

    def _compute_S_6n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = x.conjugate()
        x_v = self.x_v
        n1 = n + 1
        # first term
        term_1 = self.J_nm_j(x, x, n1, n, 0)
        term_1 -= self.J_nm_j(x, x, n1, n, 2)
        term_1 = 0.5 * ((n + 2) * x**2 - n * x_con**2) * conj(term_1)

        # second term
        term_2 = self.J_nm_j(x, x, n, n1, 0)
        term_2 -= self.J_nm_j(x, x, n, n1, 2)
        term_2 = x_con * x * conj(term_2)

        # third term
        term_3 = self.G_sum_2(n)
        term_3 *= x_con * x / x_v**2

        # fourth term
        term_4 = n * x * self.J_nm_j(x, x, n, n, 1)
        term_4 += (n + 2) * x_con * self.J_nm_j(x, x, n1, n1, 1)
        term_4 -= x_con * x * self.J_nm_j(x, x, n, n1, 0)
        term_4 = (x**2 - x_con**2) / x_v**2 * conj(term_4)

        return term_1 - term_2 + term_3 + term_4

    def S_7n(self, n: int) -> complex:
        """ coefficient :math:`S_{7n}`

        :param n: order
        """
        return self._S_7n.item(n)

    def _compute_S_7n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = x.conjugate()
        x_v = self.x_v
        n1 = n + 1

        # first term
        term_1 = self.J_nm_j(x_v, x, n, n1, 0)
        term_1 -= self.J_nm_j(x_v, x, n, n1, 2)
        term_1 *= (n + 2) * x_v**2 - n1 * x_con**2
        term_1 *= 0.5

        # second term
        term_2 = self.J_nm_j(x_v, x, n1, n, 0)
        term_2 -= self.J_nm_j(x_v, x, n1, n, 2)
        term_2 *= x_con * x_v

        # third term
        term_3 = self.J_nm_j(x_v, x, n, n, -1)
        term_3 -= self.J_nm_j(x_v, x, n, n, 1)
        term_3 *= 0.5 * x_con * x_v**2

        # fourth term
        term_4 = self.J_nm_j(x_v, x, n1, n1, -1)
        term_4 -= self.J_nm_j(x_v, x, n1, n1, 1)
        term_4 *= 0.5 * x_con**2 * x_v

        # fifth term
        term_5 = self.K_sum(n)

        # sixth term
        term_6 = -(n + 2) * x_v * self.J_nm_j(x_v, x, n1, n1, 1)
        term_6 += n1 * x_con * self.J_nm_j(x_v, x, n, n, 1)
        term_6 *= x_con**2 / x_v**2

        return n * (term_1 + term_2 - term_3 + term_4 + term_5 - term_6)

    def S_8n(self, n: int) -> complex:
        """ coefficient :math:`S_{8n}`

        :param n: order
        """
        return self._S_8n.item(n)

    def _compute_S_8n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = self.x.conjugate()
        x_v = self.x_v
        x_v_con = x_v.conjugate()
        n1 = n + 1
        # first term
        term_1 = self.J_nm_j(x_v, x, n1, n, 0)
        term_1 -= self.J_nm_j(x_v, x, n1, n, 2)
        term_1 = conj(term_1) * (x_v_con**2 * n - n1 * x**2)
        term_1 *= 0.5

        # second term
        term_2 = self.J_nm_j(x_v, x, n, n1, 0)
        term_2 -= self.J_nm_j(x_v, x, n, n1, 2)
        term_2 = x_v_con * x * conj(term_2)

        # third term
        term_3 = self.J_nm_j(x_v, x, n, n, -1)
        term_3 -= self.J_nm_j(x_v, x, n, n, 1)
        term_3 = 0.5 * x_v_con * x**2 * conj(term_3)

        # fourth term
        term_4 = self.J_nm_j(x_v, x, n1, n1, -1)
        term_4 -= self.J_nm_j(x_v, x, n1, n1, 1)
        term_4 = 0.5 * x_v**2 * x * conj(term_4)

        # fifth term
        term_5 = self.L_sum(n)

        # sixth term
        term_6 = n * x_v * self.J_nm_j(x_v, x, n, n, 1)
        term_6 -= n1 * x_con * self.J_nm_j(x_v, x, n1, n1, 1)
        term_6 = x**2 / x_v**2 * conj(term_6)

        # common factor
        return (n + 2) * (term_1 - term_2 + term_3 + term_4 - term_5 + term_6)

    def S_9n(self, n: int) -> complex:
        """ coefficient :math:`S_{9n}`

        :param n: order
        """
        return self._S_9n.item(n)

    def _compute_S_9n(self, n: int) -> complex:
        # computation according to appendix A
        x = self.x
        x_con = x.conjugate()
        x_v = self.x_v
        n1 = n + 1

        out = x * Bf.d1_besselj(n1, x) * Bf.d1_besselj(n1, x_con)
        out += x_con * Bf.d1_besselj(n, x) * Bf.d1_besselj(n, x_con)

        return out * x * x_con / x_v**2


if __name__ == '__main__':
    pass
