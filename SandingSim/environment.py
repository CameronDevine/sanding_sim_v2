from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, AmbientLight
import numpy as np
from os import path
from .questionnaire import Questionnaire


class Environement(ShowBase):
    test_article = "curved"

    def __init__(self):
        super().__init__()

        self.disableMouse()

        # self.render.setShaderAuto()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        # for region in self.win.getActiveDisplayRegions():
        #     region.setActive(False)

        self.environment = self.loader.loadModel(
            path.join(path.dirname(__file__), "..", "environment.bam")
        )
        self.environment.reparentTo(self.render)

        # self.questionnaire = Questionnaire()

        # self.region = self.win.makeDisplayRegion()
        # self.region.setCamera(self.environment.find("Camera/Camera"))
        self.win.getActiveDisplayRegions()[0].setCamera(
            self.environment.find("Camera/Camera")
        )

        self.sander = self.environment.find("Sander")

        self.curved_part = self.environment.find("Curved")
        self.tex = self.curved_part.findTexture("*")
        self.tex_image = (
            np.frombuffer(bytes(self.tex.getRamImage()), np.uint8)
            .copy()
            .reshape(self.tex_x, self.tex_y, 3)
        )

        # self.tex_image[365,:,:] = 255

        # alight = AmbientLight('alight')
        # alight.setColor((1, 1, 1, 1))
        # alight_node = self.environment.attachNewNode(alight)
        # self.environment.setLight(alight_node)

        # light = self.environment.find('Light/Light')
        # light.node().setShadowCaster(True, 2048, 2048)
        # self.environment.setLight(light)

        self.set_test_article(self.test_article)

    def set_texture(self):
        self.tex.setRamImage(self.tex_image.tobytes())

    def set_test_article(self, test_article):
        self.test_article = test_article
        path_name_show, path_name_hide = self.if_curved_flat(("Curved", "Flat"), ("Flat", "Curved"))
        self.environment.find(path_name_hide).hide()
        self.environment.find(path_name_show).show()

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

    def if_curved_flat(self, curved, flat):
        if self.test_article == "curved":
            return curved
        elif self.test_article == "flat":
            return flat
        else:
            raise ValueError('test_article must be either "curved" or "flat".')

    @property
    def test_article_thickness(self):
        return self.if_curved_flat(0.0492, 0.03)

    @property
    def test_article_radius(self):
        return self.if_curved_flat(0.8, 0)

    @property
    def test_article_curvature_length(self):
        return self.if_curved_flat(0.6, 1)

    @property
    def test_article_curvature_end(self):
        return self.if_curved_flat(0.667, 0)

    @property
    def test_article_curvature_start(self):
        return self.if_curved_flat(10, 0)

    @property
    def test_article_curvature_x(self):
        return self.if_curved_flat(1.25, 0)
