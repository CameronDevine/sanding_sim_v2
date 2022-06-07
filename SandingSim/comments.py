from direct.gui.DirectGui import *
from .gui import GUI
from panda3d.core import TextNode


class Comments(GUI):
    entry_scale = 0.06

    def __init__(self):
        super().__init__((self.left, self.right, self.bottom, self.top))
        self.text(
            text="If you have any further comments, please leave them below.",
            pos=(0, 0, self.top - 0.15 * self.height),
            scale=0.06,
        )
        self.entry = DirectEntry(
            parent=self.frame,
            width=0.8 * self.width / self.entry_scale,
            numLines=14,
            cursorKeys=1,
            focus=1,
            pos=(-0.4 * self.width, 0, self.top - 0.3 * self.height),
            scale=self.entry_scale,
        )

    def get_answers(self):
        return self.entry.get()

    @property
    def top(self):
        return self.window_top - 0.1 * self.window_height

    @property
    def bottom(self):
        return self.window_bottom + 0.2 * self.window_height

    @property
    def left(self):
        return -self.width / 2

    @property
    def right(self):
        return self.width / 2

    @property
    def width(self):
        return 1.2 * self.window_height

    @property
    def height(self):
        return self.top - self.bottom
