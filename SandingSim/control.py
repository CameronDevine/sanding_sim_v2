from .environment import Environement
from panda3d.core import InputDevice
import numpy as np


class Control(Environement):
    deadband = 0.05
    amp = 0.15
    max_vel = 0.18
    max_accel = 0.12
    vel = 0
    hover_distance = 0.03
    end = 0

    def __init__(self):
        super().__init__()

        self.taskMgr.add(self.move, "Move Task", priority=1)
        self.sander_origin = self.sander.getZ()

        self.controller = None
        self.find_controller()

        self.accept("connect-device", self.connect)
        self.accept("disconnect-device", self.disconnect)

    def find_controller(self):
        devices = self.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if devices:
            self.connect(devices[0])

    def connect(self, device):
        if (
            device.device_class == InputDevice.DeviceClass.gamepad
            and not self.controller
        ):
            print('Controller "{}" connected'.format(device))
            self.controller = device
            self.attachInputDevice(device, prefix="controller")

    def disconnect(self, device):
        if self.controller != device:
            return

        print('Controller "{}" disconnected'.format(device))

        self.detachInputDevice(device)
        self.controller = None

        self.find_controller()

    @property
    def stick(self):
        return self.controller.findAxis(InputDevice.Axis.left_x).value

    @property
    def trigger(self):
        if not self.controller:
            return 0
        return self.controller.findAxis(InputDevice.Axis.left_trigger).value

    def move(self, task):
        if not self.controller:
            return task.cont
        self.move_y()
        self.move_z()
        return task.cont

    def move_y(self):
        dt = base.clock.dt
        stick = self.stick
        if abs(stick) < self.deadband:
            stick = 0
        vel = self.max_vel * stick
        accel = (vel - self.vel) / dt
        if abs(accel) > self.max_accel:
            accel = np.sign(accel) * self.max_accel
        if abs(accel) > 0:
            stop_pos = self.vel ** 2 / (2 * accel) + self.sander_y
        elif self.vel != 0:
            stop_pos = (
                self.vel ** 2 / (2 * np.sign(self.vel) * self.max_accel) + self.sander_y
            )
        else:
            stop_pos = self.sander_y
        if abs(stop_pos) >= self.amp and stop_pos * vel > 0:
            accel = self.vel ** 2 / (2 * (self.sander_y - np.sign(stop_pos) * self.amp))
        self.vel += dt * accel
        old_y = self.sander_y
        self.sander_y += dt * self.vel
        if abs(self.sander_y) > self.amp:
            self.sander_y = np.sign(self.sander_y) * self.amp
            self.vel = (self.sander_y - old_y) / dt

    def move_z(self):
        theta = 0
        if self.test_article_radius:
            theta = np.arctan2(self.sander_y, self.test_article_radius)
        self.sander_z = self.sander_origin + self.test_article_thickness
        self.sander_z += self.test_article_radius * (np.cos(theta) - 1)
        if self.trigger == 0:
            self.sander_z += self.hover_distance
        self.sander_angle = -theta
