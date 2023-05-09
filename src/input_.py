# import keyboard
import pygame

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
        super().__init__()
        self.button = button

    def jump(self) -> bool:
        return bool(self.button.value)

    def quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False


# class KeyboardInput(Input):
#
#     def __init__(self):
#         super(KeyboardInput, self).__init__()
#
#     def jump(self) -> bool:
#         return keyboard.is_pressed("space")


class PyGameInput(Input):

    def __init__(self):
        super(PyGameInput, self).__init__()

    def jump(self) -> bool:
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "space":
                    return True

    def quit(self) -> bool:
        for event in pygame.event.get(eventtype=pygame.QUIT):
            if event.type == pygame.QUIT:
                return True

        return False


class GeneralInput(Input):
    def __init__(self, button: Button):
        super().__init__()
        self.gpio = GPIOInput(button)


    def jump(self) -> bool:
        return bool(self.button.value)

    def quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False
