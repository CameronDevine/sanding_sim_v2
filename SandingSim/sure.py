from direct.gui.DirectGui import *
from .gui import GUI
from panda3d.core import TextNode


class Sure(GUI):
    def __init__(self, next):
        self.next = next
        super().__init__((self.left, self.right, self.bottom, self.top))
        self.button(text="No", command=self.no)
        self.button(text="Yes", command=self.yes)
        for button, pos in zip(self.frame.children, (-self.width / 4, self.width / 4)):
            self.place_center(button, (pos, 0, self.top - 2 * self.height / 3))
        self.text(
            text="Are you sure?",
            pos=(0, 0, self.top - self.height / 3),
            scale=0.06,
        )
        self.hide()

    def yes(self):
        self.hide()
        self.next()

    def no(self):
        self.hide()

    @property
    def top(self):
        return self.height / 2

    @property
    def bottom(self):
        return -self.height / 2

    @property
    def left(self):
        return -self.width / 2

    @property
    def right(self):
        return self.width / 2

    @property
    def width(self):
        return 1.8 * self.height

    @property
    def height(self):
        return 0.3 * self.window_height
