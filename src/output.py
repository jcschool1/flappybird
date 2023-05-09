import os
import pygame
from gpiozero import AngularServo

from assets import GameObject


class Output(object):

    def __init__(self, *args):
        pass

    def render(self, bird: GameObject, pipes: list[GameObject], score: int, *args) -> None:
        print(bird.pos)


class GPIOOutput(Output):

    def __init__(self, servo: AngularServo):
        super().__init__()
        self.servo: AngularServo = servo

    def render(self, bird: GameObject, pipes: list[GameObject], score: int, *args) -> None:
        self.servo.angle = -(bird.pos.y - 2) * 5


class GraphicalOutput(Output):

    def __init__(self):
        super().__init__()
        pygame.init()

        pygame.display.set_caption('Flappy Bird')
        self.screen = pygame.display.set_mode((300, 228))
        self.x, self.y = pygame.display.get_surface().get_size()
        self.scale_coefficient = 1
        self.offset = 0

        self.sprite_bird = pygame.transform.scale(
            GraphicalOutput._load_sprite("bird.png"),
            (
                int(self.scale_coefficient * self.y / 12),
                int(self.scale_coefficient * self.y / 12)
            )
        )

        self.sprite_pipe = pygame.transform.scale(
            GraphicalOutput._load_sprite("pipe.png"),
            (
                int(self.scale_coefficient * self.y / 8),
                int(self.scale_coefficient * self.y * 2)
            )
        )

        self.sprite_floor = pygame.transform.scale(
            GraphicalOutput._load_sprite("floor.png"),
            (
                int(self.scale_coefficient * self.y),
                int(self.scale_coefficient * self.y / 4)
            )
        )

        self.sprite_background = pygame.transform.scale(
            GraphicalOutput._load_sprite("background.png"),
            (
                int(self.scale_coefficient * self.y * 0.75),
                int(self.scale_coefficient * self.y)
            )
        )

    @staticmethod
    def _load_sprite(name: str) -> pygame.Surface:
        return pygame.image.load(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'sprites', name)
        ).convert_alpha()

    def _native_to_pygame(self, x: float, y: float) -> (float, float):
        x, y = x * (self.y / 40), y * (self.y / 40)  # scale up to y = y_display_max
        x, y = x, y + self.offset  # apply offset
        x, y = x * self.scale_coefficient, y * self.scale_coefficient  # apply user specified scale
        x, y = x + (self.x / 2), y + (self.y / 2)  # object to display
        x, y = x, self.y - y  # display to pygame

        return self._max((x, y))

    def _max(self, coords: (float, float)) -> (float, float):
        x, y = coords

        if x < 0:
            x = 0
        if x > self.x:
            x = self.x
        if y < 0:
            y = 0
        if y > self.y:
            y = self.y

        return x, y

    def render(self, bird: GameObject, pipes: list[GameObject], score: int, *args) -> None:
        ...
        # background
        self.screen.fill((0, 0, 0))
        sprite_background_x, sprite_background_y = self._native_to_pygame(0, 0)
        self.screen.blit(self.sprite_background, (sprite_background_x - self.sprite_background.get_size()[0] / 2,
                                                  sprite_background_y - self.sprite_background.get_size()[1] / 2))

        # pipes
        for pipe in pipes:
            sprite_pipe_x, sprite_pipe_y = self._native_to_pygame(pipe.pos.x, pipe.pos.y)
            self.screen.blit(
                self.sprite_pipe,
                (
                    sprite_pipe_x - self.sprite_pipe.get_size()[0] / 2,
                    sprite_pipe_y - self.sprite_pipe.get_size()[1] / 2
                )
            )

        # floor
        if len(pipes) > 0:
            sprite_floor_x, sprite_floor_y = self._native_to_pygame(pipes[0].pos.x % 5, -20)
            self.screen.blit(
                self.sprite_floor,
                (
                    sprite_floor_x - self.sprite_floor.get_size()[0] / 2,
                    sprite_floor_y - self.sprite_floor.get_size()[1] / 2
                )
            )

        # bird
        sprite_bird_x, sprite_bird_y = self._native_to_pygame(bird.pos.x, bird.pos.y)
        self.screen.blit(
            self.sprite_bird,
            (
                sprite_bird_x - self.sprite_bird.get_size()[0] / 2,
                sprite_bird_y - self.sprite_bird.get_size()[1] / 2
            )
        )

        # score
        score_font = pygame.font.SysFont(None, int(self.scale_coefficient * 48))
        font_outer = score_font.render(str(score), True, (0, 0, 0))

        self.screen.blit(font_outer, self._native_to_pygame(0, 15))

        # black bars
        blackbar_x = 0.5 * (self.x - self.y * 0.75) \
                     + (1 - self.scale_coefficient) * (3 / 8) * self.y
        blackbar_y = (self.y / 2) * (1 - self.scale_coefficient)

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (0, 0, blackbar_x, self.y)
        )
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (blackbar_x + self.y * (3 / 4) * self.scale_coefficient, 0, blackbar_x, self.y)
        )
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (0, 0, self.x, blackbar_y)
        )
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (0, blackbar_y + self.y * self.scale_coefficient, self.x, blackbar_y)
        )

        pygame.display.flip()


class GeneralOutput(Output):

    def __init__(self, servo_gpio: int):
        super().__init__()
        servo = AngularServo(servo_gpio, frame_width=0.02)
        self.gpio = GPIOOutput(servo)
        self.graphical = GraphicalOutput()

    def render(self, bird: GameObject, pipes: list[GameObject], score: int, *args) -> None:
        self.gpio.render(bird, pipes, score)
        self.graphical.render(bird, pipes, score)
