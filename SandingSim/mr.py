from .control import Control
import mr_sim
from matplotlib.colors import LinearSegmentedColormap
from .mr_control import OrbitalDepthControl
from .classifier import Classifier
import numpy as np

MR_Sim = mr_sim.create_simulation(
    mr_sim.ConstantCurvature, mr_sim.Round, mr_sim.Orbital, mr_sim.Preston
)


class MR(Control):
    omega_m = 500
    eccentricity = 0.005
    test_article_width = 0.122
    test_article_length = 0.425
    tex_top_lines = 365
    kp = 1e-9
    sander_radius = 0.122 / 2
    pad_stiffness = 70.5e6 / 50
    window_length = 0.18
    window_width = 0.02

    max_force_curved = 8
    max_force_flat = 20

    average_speed = 0.0948

    color_over = [185, 154, 100]
    color_start = [150, 150, 81]
    color_over = [100, 154, 185]
    depth_over = 7e-5
    depth_done = 5e-5

    def __init__(self):
        super().__init__()

        self.hbar_max_flat = (
            self.kp
            * self.eccentricity
            * self.omega_m
            * self.max_force_flat
            / (2 * self.sander_radius * self.average_speed)
        )

        self.mr_controller = OrbitalDepthControl(
            kp=self.kp,
            R=self.sander_radius,
            E=self.eccentricity,
            omega_m=self.omega_m,
            stiffness=self.pad_stiffness,
        )
        k1 = np.mean([self.curved_curvature_start, self.curved_curvature_end])
        k2 = self.curved_curvature_x
        ws = 2 * np.sqrt(
            2
            * (
                np.sin(self.mr_controller.phi) ** 2 / k1
                + np.cos(self.mr_controller.phi) ** 2 / k2
            )
        )
        d = np.sqrt(
            self.max_force_curved * np.sqrt(k1 * k2) / (np.pi * self.pad_stiffness)
        )
        self.hbar_max_curved = (
            self.kp
            * self.eccentricity
            * self.omega_m
            * self.pad_stiffness
            * np.pi
            * d ** (3 / 2)
            / (self.average_speed * ws * np.sqrt(k1 * k2))
        )

        self.color_done = self.tex_image[0, 0, :]
        self.cmap = LinearSegmentedColormap(
            "sim",
            {
                "red": [
                    [0, self.color_start[0] / 255, self.color_start[0] / 255],
                    [
                        self.depth_done / self.depth_over,
                        self.color_done[0] / 255,
                        self.color_done[0] / 255,
                    ],
                    [1, self.color_over[0] / 255, self.color_over[0] / 255],
                ],
                "green": [
                    [0, self.color_start[1] / 255, self.color_start[1] / 255],
                    [
                        self.depth_done / self.depth_over,
                        self.color_done[1] / 255,
                        self.color_done[1] / 255,
                    ],
                    [1, self.color_over[1] / 255, self.color_over[1] / 255],
                ],
                "blue": [
                    [0, self.color_start[2] / 255, self.color_start[2] / 255],
                    [
                        self.depth_done / self.depth_over,
                        self.color_done[2] / 255,
                        self.color_done[2] / 255,
                    ],
                    [1, self.color_over[2] / 255, self.color_over[2] / 255],
                ],
            },
        )

        self.mr_sim = MR_Sim(
            self.test_article_length,
            self.test_article_width,
            dx=self.test_article_length / self.tex_x,
            dy=self.test_article_width / (self.tex_y - self.tex_top_lines),
            eccentricity=self.eccentricity,
            kp=self.kp,
            radius=self.sander_radius,
            auto_velocity=True,
            stiffness=self.pad_stiffness,
        )
        self.mr_sim.set_speed(self.omega_m)

        self.classifier = Classifier(timeconstant=0.075)

        self.taskMgr.add(self.mr, "MR Task", priority=2)

    def calc_force(self):
        if self.control == "force":
            return self.max_force * self.trigger
        elif self.control == "depth":
            kx = self.test_article_curvature_x
            ky = self.test_article_curvature_y
            force, self.case = self.mr_controller.calculate(
                vl=self.mr_sim.vl_x,
                hbar=self.hbar_max * self.trigger,
                k1=max(kx, ky),
                k2=min(kx, ky),
                phi=0 if kx < ky else np.pi / 2,
            )
            if self.trigger > 0 and self.classifier.classify(self.mr_sim.vl_x, self.dt):
                force = self.max_force
            return force
        else:
            raise ValueError('control must be either "force" or "depth".')

    def display_mr(self):
        window_size_x = int(self.window_length / self.mr_sim.dx)
        window_size_y = int(self.window_width / self.mr_sim.dy)

        window_x_middle = self.tex_x >> 1
        window_x_start = window_x_middle - (window_size_x >> 1)
        window_x_end = window_x_start + window_size_x

        window_y_middle = (self.tex_top_lines + self.tex_y) >> 1
        window_y_start = window_y_middle - (window_size_y >> 1)
        window_y_end = window_y_start + window_size_y

        profile_x_middle = self.mr_sim.profile.shape[1] >> 1
        profile_x_start = profile_x_middle - (window_size_x >> 1)
        profile_x_end = profile_x_start + window_size_x

        profile_y_middle = self.mr_sim.profile.shape[0] >> 1
        profile_y_start = profile_y_middle - (window_size_y >> 1)
        profile_y_end = profile_y_start + window_size_y

        profile = self.mr_sim.profile[
            profile_y_start:profile_y_end, profile_x_start:profile_x_end
        ]

        self.tex_image[window_y_start:window_y_end, window_x_start:window_x_end, :] = (
            255 * self.cmap(profile / self.depth_over)[:, :, :3]
        )

        self.set_texture()

    def mr(self, task):
        self.mr_sim.dt = self.dt
        self.mr_sim.set_location(self.sander_y)

        self.mr_sim.set_force(self.calc_force())
        self.mr_sim.set_curvature(
            self.test_article_curvature_x, self.test_article_curvature_y
        )
        self.mr_sim.step()

        self.display_mr()

        return task.cont

    def reset(self):
        self.tex_image = self.tex_image_orig
        self.mr_sim.profile = 0
        self.set_texture()

    @property
    def test_article_curvature_y(self):
        curvature_slope = (
            self.test_article_curvature_end - self.test_article_curvature_start
        ) / self.test_article_curvature_length
        curvature_mean = (
            self.test_article_curvature_start + self.test_article_curvature_end
        ) / 2
        return curvature_slope * -self.sander_y + curvature_mean

    @property
    def max_force(self):
        return self.if_curved_flat(self.max_force_curved, self.max_force_flat)

    @property
    def hbar_max(self):
        return self.if_curved_flat(self.hbar_max_curved, self.hbar_max_flat)
