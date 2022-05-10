import json
import numpy as np
from os import path


class Classifier:
    def __init__(self, timeconstant=0.05):
        with open(path.join(path.dirname(__file__), "classifier.json")) as f:
            data = json.load(f)
        self.vel = data["vel"]
        self.prob = data["prob"]
        self.lowpass = Lowpass(timeconstant)

    def get_prob(self, vel):
        return np.interp(vel, self.vel, self.prob)

    def classify(self, vel, dt):
        return self.lowpass.filter(self.get_prob(vel), dt) > 0.5


class Lowpass:
    def __init__(self, timeconstant, default=0):
        self.timeconstant = timeconstant
        self.default = default
        self.reset()

    def alpha(self, dt):
        return dt / (self.timeconstant * dt)

    def filter(self, val, dt):
        alpha = self.alpha(dt)
        self.last_val = alpha * val + (1 - alpha) * self.last_val
        return self.last_val

    def reset(self):
        self.last_val = self.default
