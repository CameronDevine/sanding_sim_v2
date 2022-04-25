from .control import Control
import mr_sim
from matplotlib.colors import LinearSegmentedColormap
from .mr_control import OrbitalDepthControl

MR_Sim = mr_sim.create_simulation(
    mr_sim.Flat, mr_sim.Round, mr_sim.Orbital, mr_sim.Preston
)


class MR(Control):
    omega_m = 500
    eccentricity = 0.005
    max_force = 20
    test_article_width = 0.1
    test_article_length = 0.25
    tex_top_lines = 309
    kp = 1e-9
    sander_radius = 0.122 / 2
    window_length = 0.08
    window_width = 0.02

    color_over = [185, 154, 100]
    color_start = [150, 150, 81]
    color_over = [100, 154, 185]
    depth_over = 7e-5
    depth_done = 5e-5

    def __init__(self):
        super().__init__()

        self.hbar_max = self.kp * self.eccentricity * self.omega_m * self.max_force / (2 * self.sander_radius * self.max_vel)

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

        self.profile_dx = self.test_article_length / self.tex_x
        self.profile_dy = self.test_article_width / (self.tex_y - self.tex_top_lines)

        self.mr_sim = MR_Sim(
            self.window_length,
            self.window_width,
            dx=self.profile_dx,
            dy=self.profile_dy,
            eccentricity=self.eccentricity,
            kp=self.kp,
            radius=self.sander_radius,
            auto_velocity=True,
        )
        self.mr_sim.set_speed(self.omega_m)

        self.taskMgr.add(self.mr, "MR Task", priority=2)

    def mr(self, task):
        self.mr_sim.dt = base.clock.dt
        self.mr_sim.set_location(-self.sander_y)
        # self.mr_sim.set_force(self.max_force * self.trigger)
        self.mr_sim.set_force(
            self.mr_controller.calculate(
                vl=self.mr_sim.vl_x, hbar=self.hbar_max * self.trigger
            )[0]
        )
        self.mr_sim.step()

        window_x_middle = self.tex_x >> 1
        window_x_start = window_x_middle - int(
            self.window_length / (2 * self.profile_dx)
        )
        window_x_end = window_x_start + self.mr_sim.profile.shape[1]

        window_y_middle = (self.tex_top_lines + self.tex_y) >> 1
        window_y_start = window_y_middle - int(
            self.window_width / (2 * self.profile_dy)
        )
        window_y_end = window_y_start + self.mr_sim.profile.shape[0]

        self.tex_image[window_y_start:window_y_end, window_x_start:window_x_end, :] = (
            255 * self.cmap(self.mr_sim.profile / self.depth_over)[:, :, :3]
        )

        self.set_texture()

        return task.cont
