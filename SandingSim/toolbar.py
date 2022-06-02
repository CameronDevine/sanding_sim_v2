from direct.gui.DirectGui import *
from .gui import GUI


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

    def set_buttons(self, buttons):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for button, func in buttons.items():
            self.buttons.append(self.button(text=button, command=func))
        num_buttons = len(self.buttons)
        spacing = self.spacing_ratio * self.window_height
        width = spacing * (num_buttons - 1)
        for i, button in enumerate(self.frame.children):
            self.place_center(
                button,
                (
                    -width / 2 + i * spacing,
                    0,
                    self.window_bottom + 0.05 * self.window_height,
                ),
            )

    def disable(self):
        for button in self.buttons:
            button["state"] = DGG.DISABLED

    def enable(self):
        for button in self.buttons:
            button["state"] = DGG.NORMAL
