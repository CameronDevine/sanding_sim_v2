from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, AmbientLight
import numpy as np


class Environement(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()

        # self.render.setShaderAuto()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        for region in self.win.getActiveDisplayRegions():
            region.setActive(False)

        self.environment = self.loader.loadModel("environment.bam")
        self.environment.reparentTo(self.render)

        self.region = self.win.makeDisplayRegion()
        self.region.setCamera(self.environment.find("Camera/Camera"))

        self.sander = self.environment.find("Sander")

        self.curved_part = self.environment.find("Curved")
        self.tex = self.curved_part.findTexture("*")
        self.tex_image = (
            np.frombuffer(bytes(self.tex.getRamImage()), np.uint8)
            .copy()
            .reshape(self.tex_x, self.tex_y, 3)
        )

        # alight = AmbientLight('alight')
        # alight.setColor((1, 1, 1, 1))
        # alight_node = self.environment.attachNewNode(alight)
        # self.environment.setLight(alight_node)

        # light = self.environment.find('Light/Light')
        # light.node().setShadowCaster(True, 2048, 2048)
        # self.environment.setLight(light)

    def set_texture(self):
        self.tex.setRamImage(self.tex_image.tobytes())

    @property
    def tex_x(self):
        return self.tex.getXSize()

    @property
    def tex_y(self):
        return self.tex.getYSize()

    @property
    def sander_y(self):
        return self.sander.getY()

    @sander_y.setter
    def sander_y(self, val):
        self.sander.setY(val)

    @property
    def sander_z(self):
        return self.sander.getZ()

    @sander_z.setter
    def sander_z(self, val):
        self.sander.setZ(val)

    @property
    def sander_angle(self):
        return np.deg2rad(self.sander.getP())

    @sander_angle.setter
    def sander_angle(self, val):
        self.sander.setP(np.rad2deg(val))
