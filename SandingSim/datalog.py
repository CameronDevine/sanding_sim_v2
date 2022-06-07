from .mr import MR
import json
from uuid import uuid4 as uuid
from datetime import datetime
import boto3
from botocore import UNSIGNED
from botocore.client import Config


class Data:
    keys = ["pos", "force", "time"]

    def __init__(self):
        self.data = dict(data=[], questions=[])

    def next_experiment(self):
        self.data["data"].append(
            dict(zip(self.keys, [list() for i in range(len(self.keys))]))
        )

    def log(self, **kwargs):
        for key, val in kwargs.items():
            self.data["data"][-1][key].append(val)

    def __setitem__(self, name, value):
        self.data[name] = value

    def answers(self, data):
        self.data["questions"].append(data)


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
            )
        return task.cont

    def log_next_experiment(self):
        self.data.next_experiment()

    def save_answers(self, data):
        self.data.answers(data)

    def init_data(self):
        self.data = Data()
        self.data["order"] = self.order
        self.data["start"] = str(datetime.now())

    def upload_data(self):
        self.data["end"] = str(datetime.now())
        self.s3_client.put_object(
            Bucket=self.bucket, Body=json.dumps(self.data.data), Key=str(uuid())
        )
