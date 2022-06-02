#! /usr/bin/env python3

from SandingSim.environment import Environement
import json
from os import path


class WindowSaver(Environement):
    def __init__(self):
        super().__init__()

        base.finalExitCallbacks.append(self.save_size)

    def save_size(self):
        with open(path.join(path.dirname(__file__), "window.json"), "w") as f:
            json.dump(
                (
                    self.win.getXSize(),
                    self.win.getYSize(),
                ),
                f,
            )


app = WindowSaver()
app.run()
