import numpy as np
from scipy.optimize import minimize_scalar


class OrbitalDepthControl:
    def __init__(self, **kwargs):
        self.kp = 1.362e-9
        self.R = 44.5 / 1000
        self.E = 4.8 / 1000
        self.stiffness = 0
        self.hbar = 0
        self.omega_m = 0
        self.k1 = 0
        self.k2 = 0
        self.vl = 0
        self.phi = np.pi / 2

        self.set_vars(kwargs)

    def set_vars(self, args):
        for var, val in args.items():
            setattr(self, var, val)

    def calculate(self, **kwargs):
        self.set_vars(kwargs)
        self.vl = abs(self.vl)

        if self.k1 == 0 and self.k2 == 0:
            return self.calculate_flat(), 0

        if self.k1 > 0 and self.k2 > 0:
            d = self.calculate_case1_d()
            if self.R >= np.sqrt(2 * d / self.k2):
                return self.calculate_case1_f(d), 1

            f = self.calculate_flat()
            d = self.calculate_case2_d(f)
            if self.R <= np.sqrt(2 * d / self.k1):
                return f, 2

            d = self.find_case3_d()
            return self.calculate_case3_f(d), 3

        raise NotImplementedError

    def calculate_flat(self):
        return 2 * self.hbar * self.R * self.vl / (self.E * self.omega_m * self.kp)

    def calculate_ws(self):
        return 2 * np.sqrt(
            2 * (np.sin(self.phi) ** 2 / self.k2 + np.cos(self.phi) ** 2 / self.k1)
        )

    def calculate_case1_d(self):
        return (
            self.hbar
            * self.calculate_ws()
            * self.vl
            * np.sqrt(self.k1 * self.k2)
            / (self.E * self.omega_m * self.stiffness * np.pi * self.kp)
        ) ** (2 / 3)

    def calculate_case1_f(self, d=None):
        if d is None:
            d = self.calculate_case1_d()
        return self.stiffness * np.pi * d ** 2 / np.sqrt(self.k1 * self.k2)

    def calculate_case2_d(self, f=None):
        if f is None:
            f = self.calculate_flat()
        return (
            f / (self.stiffness * np.pi * self.R ** 2)
            + self.R ** 2 * (self.k1 + self.k2) / 8
        )

    def find_case3_d(self):
        res = minimize_scalar(
            self.case3_objective,
            bounds=(self.R ** 2 * self.k2 / 2, self.R ** 2 * self.k1 / 2),
            method="bounded",
            options={"xatol": 1e-6},
        )
        return res.x

    def calculate_case3_theta(self, d):
        return np.arctan(
            np.sqrt((self.R ** 2 * self.k2 - 2 * d) / (2 * d - self.R ** 2 * self.k1))
        )

    def calculate_case3_f(self, d):
        theta = self.calculate_case3_theta(d)
        return (
            4
            * self.stiffness
            * (
                d ** 2
                / (2 * np.sqrt(self.k1 * self.k2))
                * (np.pi / 2 - np.arctan(np.sqrt(self.k1 / self.k2) * np.tan(theta)))
                + d * self.R ** 2 * theta / 2
                - self.R ** 4 / 16 * self.k2 * (theta + np.sin(2 * theta) / 2)
                - self.R ** 4 / 16 * self.k1 * (theta - np.sin(2 * theta) / 2)
            )
        )

    def calculate_case3_hbar(self, d):
        f = self.calculate_case3_f(d)
        w = self.calculate_case3_width(d)
        return self.E * self.omega_m * f * self.kp / (w * self.vl)

    def calculate_case3_width(self, d):
        return min(2 * self.R, np.sqrt(d) * self.calculate_ws())

    def case3_objective(self, d):
        return np.abs(self.hbar - self.calculate_case3_hbar(d))
