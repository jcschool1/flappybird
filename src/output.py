import pygame
# import pygame.freetype
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
        self.servo.angle = bird.pos.y * 9


# TODO: Ausgabe Rechnungen
class GraphicalOutput(Output):

    def __init__(self):
        super().__init__()
        pygame.init()
        # pygame.font.init()
        pygame.display.set_caption('Flappy Bird')
        self.screen = pygame.display.set_mode((1000, 500))
        self.x, self.y = pygame.display.get_surface().get_size()
        self.scale_coefficient = 0.5
        self.offset = 0

    def _object_to_display(self, x: float, y: float) -> (float, float):
        return x + (self.x / 2), y + (self.y / 2)

    def _display_to_pygame(self, x: float, y: float) -> (float, float):
        return x, self.y - y

    def _native_to_pygame(self, x: float, y: float) -> (float, float):
        x, y = x * (self.y / 40), y * (self.y / 40)  # scale up to y = y_display_max
        x, y = x, y + self.offset  # apply offset
        x, y = x * self.scale_coefficient, y * self.scale_coefficient  # apply user specified scale
        x, y = self._object_to_display(x, y)  # object to display
        x, y = self._display_to_pygame(x, y)  # display to pygame

        return self._max((x, y))

    def _is_in_bounds(self, coords: (float, float)) -> bool:
        if coords[0] < 0 or self.x < coords[0]:
            return False
        elif coords[1] < 0 or self.y < coords[1]:
            return False

        return True

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
        # background
        self.screen.fill((222, 222, 222))

        # floor

        # pipes
        for pipe in pipes:
            pipe_coords: (float, float) = self._native_to_pygame(pipe.pos.x, pipe.pos.y)

            pygame.draw.circle(self.screen, (0, 0, 255), pipe_coords, 30*self.scale_coefficient)

        # bird
        pygame.draw.circle(self.screen, (0, 255, 0), self._native_to_pygame(bird.pos.x, bird.pos.y), 30*self.scale_coefficient)

        # score
        # font = pygame.freetype.Font("your_font.ttf", 24)
        # font.render_to(self.screen, (0, 0), str(score),(0, 0, 0))

        # black bars
        blackbar_x = (0.5 * (self.x - self.y * 0.75) + (1 - self.scale_coefficient) * (3 / 8) * self.y)
        blackbar_y = (self.y / 2) * (1 - self.scale_coefficient)

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, blackbar_x, self.y))
        pygame.draw.rect(self.screen, (0, 0, 0), (blackbar_x + self.y * (3 / 4) * self.scale_coefficient, 0, blackbar_x, self.y))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.x, blackbar_y))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, blackbar_y + self.y * self.scale_coefficient, self.x, blackbar_y))

        pygame.display.flip()


class GeneralOutput(Output):

    def __init__(self):
        super().__init__()
        pygame.init()
