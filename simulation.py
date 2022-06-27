from SandingSim.mr import MR
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


class Simulation(MR):
    def __init__(self, control, test_article):
        self.control = control
        self.test_article = test_article
        self.stick_value = -1
        super().__init__()
        self.is_simulation = True
        self.controller = True
        self.sander_y = self.amp

    @property
    def trigger(self):
        return 1

    @property
    def stick(self):
        return self.stick_value

    @property
    def dt(self):
        return 0.001


class FakeTask:
    cont = None
    done = None


task = FakeTask()

methods = ("force", "depth")

for test_article in ("flat", "curved"):
    force = ([], [])
    profile = [None, None]
    case = ([], [])
    for i, control in enumerate(methods):
        print(test_article, control)
        vl_x = []
        x = []
        sim = Simulation(control, test_article)
        while True:
            # print(sim.sander_y, sim.stick)
            sim.move(task)
            sim.mr(task)
            if sim.sander_y <= -sim.amp:
                sim.stick_value = 1
                # break
            elif sim.sander_y >= sim.amp and sim.stick == 1:
                break
            force[i].append(sim.mr_sim.force)
            vl_x.append(sim.mr_sim.vl_x)
            x.append(sim.sander_y)
            if test_article == "curved":
                k1 = sim.test_article_curvature_x
                k2 = sim.test_article_curvature_y
                d1 = np.sqrt(
                    sim.mr_sim.force * np.sqrt(k1 * k2) / (np.pi * sim.pad_stiffness)
                )
                d2 = (
                    sim.mr_sim.force / (np.pi * sim.pad_stiffness)
                    + sim.sander_radius ** 4 * (k1 + k2) / 8
                ) / sim.sander_radius ** 2
                if sim.sander_radius >= np.sqrt(d1 / k2):
                    case[i].append(1)
                elif sim.sander_radius <= np.sqrt(d2 / k1):
                    case[i].append(2)
                else:
                    case[i].append(3)
        window_size_x = int(sim.window_length / sim.mr_sim.dx)
        window_size_y = int(sim.window_width / sim.mr_sim.dy)
        profile_x_middle = sim.mr_sim.profile.shape[1] >> 1
        profile_x_start = profile_x_middle - (window_size_x >> 1)
        profile_x_end = profile_x_start + window_size_x
        profile_y_middle = sim.mr_sim.profile.shape[0] >> 1
        profile_y_start = profile_y_middle - (window_size_y >> 1)
        profile_y_end = profile_y_start + window_size_y
        profile[i] = sim.mr_sim.profile[
            profile_y_start:profile_y_end, profile_x_start:profile_x_end
        ]
        X = sim.mr_sim.X[profile_y_start:profile_y_end, profile_x_start:profile_x_end]
        Y = sim.mr_sim.Y[profile_y_start:profile_y_end, profile_x_start:profile_x_end]
        sim.destroy()

        if test_article == "curved":
            half = len(force[i]) >> 1
            plt.figure()
            plt.subplot(2, 1, 1)
            plt.plot(x[:half], force[i][:half])
            plt.subplot(2, 1, 2)
            plt.plot(x[:half], case[i][:half])

    plt.figure()
    for i, control in enumerate(methods):
        plt.subplot(2, 1, i + 1)
        plt.imshow(
            profile[i],
            aspect="equal",
            origin="lower",
            extent=(X.min(), X.max(), Y.min(), Y.max()),
            vmin=min(prof.min() for prof in profile),
            vmax=max(prof.max() for prof in profile),
        )
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title(
            "{} test article using the {} control method".format(test_article, control)
        )

    plt.figure()
    for i, control in enumerate(methods):
        plt.plot(
            X[profile[i].shape[0] >> 1, :],
            profile[i][profile[i].shape[0] >> 1, :],
            label=control,
        )
    plt.ylabel("Material Removed (m)")
    plt.xlabel("x (m)")
    plt.legend()

    plt.figure()
    for i, control in enumerate(methods):
        plt.plot(force[i], label=control)
    plt.ylabel("force (N)")
    plt.xlabel("loop index")
    plt.legend()

plt.figure()
plt.plot(vl_x)
plt.xlabel("loop index")
plt.ylabel("velocity (m/s)")
plt.text(4000, -0.15, "Average Speed {}m/s".format(np.mean(np.abs(vl_x))))

with PdfPages("simulation.pdf") as pdf:
    for fig in plt.get_fignums():
        pdf.savefig(fig)
