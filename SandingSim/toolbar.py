from direct.gui.DirectGui import *
from .gui import GUI
from panda3d.core import *


class Toolbar(GUI):
    spacing_ratio = 0.3

    def __init__(self, *args):
        super().__init__(
            (
                self.window_left,
                self.window_right,
                self.window_bottom,
                self.window_bottom + 0.1 * self.window_height,
            )
        )
        self.buttons = []
        self.info = self.text(
            text="",
            pos=(
                self.window_left + 0.025 * self.window_height,
                0,
                self.window_bottom + 0.035 * self.window_height,
            ),
            scale=0.1,
            textMayChange=1,
            text_align=TextNode.ALeft,
        )

    def set_buttons(self, buttons):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for button, func in buttons.items():
            self.buttons.append(self.button(text=button, command=func))
        num_buttons = len(self.buttons)
        spacing = self.spacing_ratio * self.window_height
        width = spacing * (num_buttons - 1)
        i = 0
        for button in self.frame.children:
            if isinstance(button.node(), PGButton):
                self.place_center(
                    button,
                    (
                        -width / 2 + i * spacing,
                        0,
                        self.window_bottom + 0.05 * self.window_height,
                    ),
                )
                i += 1

    def set_info(self, text):
        self.info["text"] = text

    def disable(self):
        for button in self.buttons:
            button["state"] = DGG.DISABLED

    def enable(self):
        for button in self.buttons:
            button["state"] = DGG.NORMAL
