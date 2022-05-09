from direct.gui.DirectGui import *

class Questionnaire:
    def __init__(self):
        self.frame = DirectFrame(frameColor=(1, 1, 1, 1), frameSize=(-1, 1, -1, 1))
        OnscreenText(parent=self.frame, text="This is a test")
        DirectButton(parent=self.frame, text="Next", pressEffect=1, command=self.hide)
        DirectRadioButton(parent=self.frame)

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()

    def destroy(self):
        self.frame.destroy()
