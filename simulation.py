from SandingSim.mr import MR
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Simulation(MR):
    def __init__(self, control, test_article):
        self.control = control
        self.test_article = test_article
        self.stick_value = -1
        super().__init__()
        self.is_simulation = True
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

for test_article in ("flat", "curved"):
    for control in ("force", "depth"):
        print(control, test_article)
        force = []
        vl_x = []
        sim = Simulation(control, test_article)
        while True:
            sim.move(task)
            sim.mr(task)
            if sim.sander_y <= -sim.amp:
                sim.stick_value = 1
            elif sim.sander_y >= sim.amp and sim.stick == 1:
                break
            force.append(sim.mr_sim.force)
            vl_x.append(sim.mr_sim.vl_x)
        sim.destroy()

        plt.figure()
        sim.mr_sim.plot()
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("{} test article using the {} control method".format(test_article, control))
        plt.figure()
        plt.plot(sim.mr_sim.X[sim.mr_sim.profile.shape[0] >> 1, :], sim.mr_sim.profile[sim.mr_sim.profile.shape[0] >> 1, :])
        plt.ylabel("Material Removed (m)")
        plt.xlabel("x (m)")
        plt.figure()
        plt.plot(force)
        plt.ylabel("force (N)")
        plt.xlabel("loop index")
        plt.figure()
        plt.plot(vl_x)
        plt.xlabel("loop index")
        plt.ylabel("velocity (m/s)")

with PdfPages("simulation.pdf") as pdf:
    for fig in plt.get_fignums():
        pdf.savefig(fig)
