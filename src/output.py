import pygame
from gpiozero import AngularServo

from assets import GameObject


class Output(object):

    def __init__(self, *args):
        pass

    def render(self, bird: GameObject, pipes: list[GameObject], *args) -> None:
        print(bird.pos)


class GPIOOutput(Output):

    def __init__(self, servo: AngularServo):
        super().__init__()
        self.servo: AngularServo = servo

    def render(self, bird: GameObject, pipes: list[GameObject], *args) -> None:
        self.servo.angle = bird.pos.y * 9


#TODO: Ausgabe Rechnungen
class GraphicalOutput(Output):

    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode()
        self.x, self.y = pygame.display.get_surface().get_size()
        self.scale_coefficient = 1
        self.offset = 0

    def _object_to_display(self, x: float, y: float) -> (float, float):
        return x + (self.x/2), y + (self.y/2)

    def _display_to_pygame(self, x: float, y: float) -> (float, float):
        return x, self.y - y

    def _native_to_pygame(self, x: float, y: float) -> (float, float):
        x, y = x * (self.y/40), y * (self.y/40)                         # scale up to y = y_display_max
        x, y = x, y + self.offset                                       # apply offset
        x, y = x * self.scale_coefficient, y * self.scale_coefficient   # apply user specified scale
        x, y = self._object_to_display(x, y)                            # object to display
        x, y = self._display_to_pygame(x, y)                            # display to pygame

        return x, y

    def render(self, bird: GameObject, pipes: list[GameObject], *args) -> None:
        dx_game = self.y * 3/4
        dy_game = self.y

        dx_black_bar = (self.x - dx_game)/2
        dy_black_bar = self.y

        x_game_start = (self.x - dx_game)/2
        x_game_end = x_game_start + dx_game

        x_offset = dx_game/4
        output_coefficient = 0.8 * self.y/20

        x_bird = (self.x/2) - x_offset
        y_bird = -bird.pos.y * output_coefficient

        self.screen.fill((222, 222, 222))

        pygame.draw.circle(self.screen, (255, 0, 0), (int(bird.pos.x*40)+400, -int(bird.pos.y*40)+400), 20)

        for pipe in pipes:
            x_pipe = pipe.pos.x * output_coefficient - x_offset
            y_pipe = -pipe.pos.y * output_coefficient

            pygame.draw.circle(self.screen, (0, 0, 255), (int(pipe.pos.x*40)+400, -int(pipe.pos.y*40)+400), 50)

        pygame.display.flip()


class GeneralOutput(Output):
    
    def __init__(self):
        super().__init__()
        pygame.init()

