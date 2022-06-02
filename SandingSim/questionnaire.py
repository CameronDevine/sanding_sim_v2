from direct.gui.DirectGui import *
from .gui import GUI
from panda3d.core import TextNode


class Questionnaire(GUI):
    likert_labels = [
        "Strongly\nagree",
        "Agree",
        "Somewhat\nagree",
        "Neutral",
        "Somewhat\ndisagree",
        "Disagree",
        "Strongly\ndisagree",
    ]
    likert_values = range(3, -4, -1)
    likert_spacing_ratio = 0.13

    def __init__(self, statements):
        super().__init__((self.left, self.right, self.bottom, self.top))
        self.text(
            text="Please indicate your agreement with the following statements.",
            pos=(0, 0, self.top - 0.1 * self.height),
            scale=0.06,
        )
        self.responses = [[None] for i in range(len(statements))]
        for i, statement in enumerate(statements):
            self.question(
                self.responses[i], statement, self.top - (i * 0.15 + 0.2) * self.height
            )

    def question(self, variable, statement, pos):
        self.text(
            text=statement,
            pos=(self.left + 0.05 * self.width, 0, pos),
            scale=0.04,
            text_align=TextNode.ALeft,
        )
        self.likert(variable, pos - 0.07 * self.height)

    def likert(self, variable, zpos):
        num_buttons = len(self.likert_labels)
        spacing = self.likert_spacing_ratio * self.width
        width = spacing * (num_buttons - 1)
        buttons = num_buttons * [None]
        for i, (label, value) in enumerate(zip(self.likert_labels, self.likert_values)):
            xpos = -width / 2 + i * spacing
            buttons[i] = self.radio_button(
                variable=variable, value=[value], text=label, pos=(xpos, 0, zpos)
            )
            self.center_horizontal(self.frame.find(buttons[i].name), xpos)
        for button in buttons:
            button.setOthers(buttons)

    def complete(self):
        for (response,) in self.responses:
            if response is None:
                return False
        return True

    @property
    def top(self):
        return self.window_top - 0.05 * self.window_height

    @property
    def bottom(self):
        return self.window_bottom + 0.15 * self.window_height

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
