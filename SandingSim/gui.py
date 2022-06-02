from direct.gui.DirectGui import *
from panda3d.core import LPoint3, PGButton
from os import path
from direct.showbase.Loader import Loader
from direct.showbase.ShowBase import ShowBase

loader = Loader(ShowBase)


class GUI:
    button_maps = loader.loadModel(
        path.join(path.dirname(__file__), "..", "buttons.egg")
    )
    radio_maps = loader.loadModel(path.join(path.dirname(__file__), "..", "radio.egg"))

    def __init__(self, frameSize, frameColor=(1, 1, 1, 1)):
        self.frame = DirectFrame(frameColor=frameColor, frameSize=frameSize)

    def place_center(self, element, pos):
        element.setPos(element.getPos() + pos - element.getBounds().center)

    def center_horizontal(self, element, pos):
        element.setX(element.getX() + pos - element.getBounds().center.x)

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()

    def destroy(self):
        self.frame.destroy()

    def button(self, **kwargs):
        return DirectButton(
            parent=self.frame,
            geom=(
                self.button_maps.find("*/button"),
                self.button_maps.find("*/button_pressed"),
                self.button_maps.find("*/button"),
                self.button_maps.find("*/button_disabled"),
            ),
            geom_pos=(0, 0, 0.3),
            relief=DGG.FLAT,
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.1,
            **kwargs
        )

    def radio_button(self, **kwargs):
        return DirectRadioButton(
            parent=self.frame,
            scale=0.05,
            boxGeom=(
                self.radio_maps.find("*/radio"),
                self.radio_maps.find("*/radio_checked"),
            ),
            frameColor=(0, 0, 0, 0),
            text_scale=0.5,
            boxPlacement="above",
            **kwargs
        )

    def text(self, **kwargs):
        return DirectLabel(parent=self.frame, frameColor=(0, 0, 0, 0), **kwargs)

    @property
    def window_top(self):
        return base.aspect2d.find("a2dTopCenter").getZ()

    @property
    def window_bottom(self):
        return base.aspect2d.find("a2dBottomCenter").getZ()

    @property
    def window_right(self):
        return base.aspect2d.find("a2dRightCenter").getX()

    @property
    def window_left(self):
        return base.aspect2d.find("a2dLeftCenter").getX()

    @property
    def window_height(self):
        return self.window_top - self.window_bottom

    @property
    def window_width(self):
        return self.window_right - self.window_left
