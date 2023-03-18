import keyboard

from gpiozero import Button


class Input(object):
    def __init__(self, *args):
        pass

    def jump(self) -> bool:
        return False

    def quit(self) -> bool:
        return False


class GPIOInput(Input):

    def __init__(self, button: Button):
        super(GPIOInput, self).__init__()
        self.button = button

    def jump(self) -> bool:
        return bool(self.button.value)


class KeyboardInput(Input):

    def __init__(self):
        super(KeyboardInput, self).__init__()

    def jump(self) -> bool:
        return keyboard.is_pressed("space")


class GeneralInput(Input):
    ...