from .mr import MR
import json
from uuid import uuid4 as uuid
from datetime import datetime


class DataLog(MR):
    def __init__(self):
        super().__init__()

        base.finalExitCallbacks.append(self.save)

        self.taskMgr.add(self.log, "Log Task", priority=3)

        self.pos = []
        self.force = []
        self.time = []

    def log(self, task):
        self.pos.append(self.mr_sim.y)
        self.force.append(self.mr_sim.force)
        self.time.append(base.clock.getFrameTime())

        return task.cont

    def save(self):
        with open("{}.json".format(uuid()), "w") as f:
            json.dump(
                dict(
                    date=str(datetime.now()),
                    time=self.time,
                    force=self.force,
                    pos=self.pos,
                    profile=self.mr_sim.profile.tolist(),
                ),
                f,
            )
