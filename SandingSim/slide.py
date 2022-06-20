from direct.gui.DirectGui import *
from .gui import GUI


class SlideBase(GUI):
    def __init__(self):
        super().__init__((self.left, self.right, self.bottom, self.top))

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


class Slide(SlideBase):
    def __init__(self, text, image_filename):
        super().__init__()
        self.text(
            text=text,
            pos=(0, 0, self.top - 0.15 * self.height),
            scale=0.06,
        )
        image = loader.loadTexture(image_filename)
        width = 0.8 * self.width
        height = image.get_orig_file_y_size() * width / image.get_orig_file_x_size()
        DirectFrame(
            parent=self.frame, image=image, image_scale=(1, width / 2, height / 2)
        )


class TextSlide(SlideBase):
    def __init__(self, text):
        super().__init__()
        self.text(
            text=text,
            pos=(0, 0, self.top - 0.45 * self.height),
            scale=0.06,
        )
