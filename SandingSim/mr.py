from .control import Control
import mr_sim
from matplotlib.colors import LinearSegmentedColormap
from .mr_control import OrbitalDepthControl
from .classifier import Classifier

MR_Sim = mr_sim.create_simulation(
    mr_sim.ConstantCurvature, mr_sim.Round, mr_sim.Orbital, mr_sim.Preston
)


class MR(Control):
    omega_m = 500
    eccentricity = 0.005
    test_article_width = 0.122
    test_article_length = 0.5
    tex_top_lines = 365
    kp = 1e-9
    sander_radius = 0.122 / 2
    pad_stiffness = 70.5e6 / 50
    window_length = 0.18
    window_width = 0.03

    color_over = [185, 154, 100]
    color_start = [150, 150, 81]
    color_over = [100, 154, 185]
    depth_over = 7e-5
    depth_done = 5e-5

    def __init__(self):
        super().__init__()

        self.hbar_max = (
            self.kp
            * self.eccentricity
            * self.omega_m
            * self.max_force
            / (2 * self.sander_radius * self.max_vel)
        )

        self.mr_controller = OrbitalDepthControl(
            kp=self.kp, R=self.sander_radius, E=self.eccentricity, omega_m=self.omega_m
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
            self.window_length,
            self.window_width,
            dx=self.test_article_length / self.tex_x,
            dy=self.test_article_width / (self.tex_y - self.tex_top_lines),
            eccentricity=self.eccentricity,
            kp=self.kp,
            radius=self.sander_radius,
            auto_velocity=True,
            stiffness=self.pad_stiffness,
        )
        self.mr_sim.set_speed(self.omega_m)

        self.classifier = Classifier()

        self.taskMgr.add(self.mr, "MR Task", priority=2)

    def calc_force(self):
        if self.control == "force":
            return self.max_force * self.trigger
        elif self.control == "depth":
            force = self.mr_controller.calculate(
                vl=self.mr_sim.vl_x,
                hbar=self.hbar_max * self.trigger,
                k1=self.test_article_curvature_x,
                k2=self.test_article_curvature_y,
            )[0]
            if self.trigger > 0 and self.classifier.classify(self.mr_sim.vl_x, base.clock.dt):
                force = self.max_force
            return force
        else:
            raise ValueError('control must be either "force" or "depth".')

    def display_mr(self):
        window_x_middle = self.tex_x >> 1
        window_x_start = window_x_middle - int(
            self.window_length / (2 * self.mr_sim.dx)
        )
        window_x_end = window_x_start + self.mr_sim.profile.shape[1]

        window_y_middle = (self.tex_top_lines + self.tex_y) >> 1
        window_y_start = window_y_middle - int(self.window_width / (2 * self.mr_sim.dy))
        window_y_end = window_y_start + self.mr_sim.profile.shape[0]

        self.tex_image[window_y_start:window_y_end, window_x_start:window_x_end, :] = (
            255 * self.cmap(self.mr_sim.profile / self.depth_over)[:, :, :3]
        )

        self.set_texture()

    def mr(self, task):
        self.mr_sim.dt = base.clock.dt
        self.mr_sim.set_location(self.sander_y)

        self.mr_sim.set_force(self.calc_force())
        self.mr_sim.set_curvature(
            self.test_article_curvature_x, self.test_article_curvature_y
        )
        self.mr_sim.step()

        self.display_mr()

        return task.cont

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
        return self.if_curved_flat(8, 20)
