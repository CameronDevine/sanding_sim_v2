from direct.gui.DirectGui import *
from panda3d.core import LPoint3


class Toolbar:
    spacing_ratio = 0.2

    def __init__(self):
        self.frame = DirectFrame(frameColor=(1, 1, 1, 1), frameSize=(self.left, self.right, self.bottom, self.bottom + 0.1 * self.height))

    def set_buttons(self, buttons):
        for button in self.frame.children:
            button.destroy()
        for button, func in buttons.items():
            DirectButton(parent=self.frame, text=button, pressEffect=1, command=func, scale=0.1, frameColor=(0, 0, 1, 1))
        num_buttons = len(buttons)
        spacing = self.spacing_ratio * self.height
        width = spacing * (num_buttons - 1)
        for i, button in enumerate(self.frame.children):
            pos = LPoint3(-width / 2 + i * spacing, 0, self.bottom + 0.05 * self.height)
            curr = button.getBounds().center
            button.setPos(button.getPos() + pos - curr)

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()

    def destroy(self):
        self.frame.destroy()

    @property
    def top(self):
        return base.aspect2d.find("a2dTopCenter").getZ()

    @property
    def bottom(self):
        return base.aspect2d.find("a2dBottomCenter").getZ()

    @property
    def right(self):
        return base.aspect2d.find("a2dRightCenter").getX()

    @property
    def left(self):
        return base.aspect2d.find("a2dLeftCenter").getX()

    @property
    def height(self):
        return self.top - self.bottom

    @property
    def width(self):
        return self.right - self.left
