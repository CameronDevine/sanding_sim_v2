from .mr import MR
import json
from uuid import uuid4 as uuid
from datetime import datetime
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from gzip import compress


class Data:
    def __init__(self):
        self.data = dict(data=[], questions=[], metadata={})

    def next_experiment(self):
        self.data["data"].append(dict())

    def log(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.data["data"][-1]:
                self.data["data"][-1][key].append(val)
            else:
                self.data["data"][-1][key] = [val]

    def log_final(self, **kwargs):
        self.data["data"][-1].update(kwargs)

    def __setitem__(self, name, value):
        self.data[name] = value

    def answers(self, data):
        self.data["questions"].append(data)

    def add_metadata(self, key, val):
        self.data["metadata"][key] = val


class DataLog(MR):
    bucket = "sanding-sim-v2"

    def __init__(self):
        self.log_active = False

        super().__init__()

        self.taskMgr.add(self.log, "Log Task", priority=3)

        self.s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    def log(self, task):
        if self.log_active:
            self.data.log(
                pos=self.mr_sim.y,
                force=self.mr_sim.force,
                time=base.clock.getFrameTime(),
                trigger=self.raw_trigger,
                stick=self.stick,
            )
        return task.cont

    def log_profile(self):
        self.data.log_final(
            profile=self.mr_sim.profile.tolist(),
            X=self.mr_sim.X.tolist(),
            Y=self.mr_sim.Y.tolist(),
        )

    def log_next_experiment(self):
        self.data.next_experiment()

    def save_answers(self, data):
        self.data.answers(data)

    def init_data(self):
        self.data = Data()
        self.data.add_metadata("order", self.order)
        self.data.add_metadata("start", str(datetime.now()))
        self.data.add_metadata("deadband", self.deadband)
        self.data.add_metadata("amp", self.amp)
        self.data.add_metadata("max_vel", self.max_vel)
        self.data.add_metadata("max_accel", self.max_accel)
        self.data.add_metadata("binary_trigger", self.binary_trigger)
        self.data.add_metadata("omega_m", self.omega_m)
        self.data.add_metadata("eccentricity", self.eccentricity)
        self.data.add_metadata("test_article_width", self.test_article_width)
        self.data.add_metadata("test_article_length", self.test_article_length)
        self.data.add_metadata("kp", self.kp)
        self.data.add_metadata("sander_radius", self.sander_radius)
        self.data.add_metadata("pad_stiffness", self.pad_stiffness)
        self.data.add_metadata("window_length", self.window_length)
        self.data.add_metadata("window_width", self.window_width)
        self.data.add_metadata("max_force_curved", self.max_force_curved)
        self.data.add_metadata("max_force_flat", self.max_force_flat)
        self.data.add_metadata("depth_over", self.depth_over)
        self.data.add_metadata("depth_done", self.depth_done)

    def upload_data(self):
        self.data.add_metadata("end", str(datetime.now()))
        self.s3_client.put_object(
            Bucket=self.bucket,
            Body=compress(json.dumps(self.data.data)),
            Key=str(uuid()),
        )
