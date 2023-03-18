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
        self.servo = servo

    def render(self, bird: GameObject, pipes: list[GameObject], *args) -> None:
        self.servo.angle = bird.pos.y * 9


#TODO: Ausgabe Rechnungen
class GraphicalOutput(Output):

    def __init__(self):
        super().__init__()
        pygame.init()
        self.x = 800
        self.y = 800
        self.screen = pygame.display.set_mode((self.x, self.y))

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
    ...