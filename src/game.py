import time
from enum import Enum

from assets import Bird, Pipe
from input_ import Input
from output import Output


class GameResult(Enum):
    NONE = 0
    DEAD = 1
    QUIT = 2

class FrameResult(Enum):
    NONE = 0
    DEAD = 1


class Game(object):

    def __init__(self, fps: int, input_: Input, output: Output) -> None:
        self.fps: int = fps
        self.frame: int = 0
        self.score: int = 0
        self.jump_available: bool = True
        self.bird: Bird = Bird(-30)
        self.pipes: list[Pipe] = list()
        self.input_: Input = input_
        self.output: Output = output
        self.x_bounds: (int, int) = (-40, 40)
        self.y_bounds: (int, int) = (-20, 20)


    #TODO: pos begrenzen
    def _bird_logic(self, delta: float) -> None:
        self.bird.update_position(delta)
        self.bird.max(self.x_bounds, self.y_bounds)

        if self.input_.jump() and self.jump_available:
            self.bird.jump()
            self.jump_available = False
        elif self.input_.jump() and not self.jump_available:
            pass
        else:
            self.jump_available = True

    def _pipe_logic(self, delta: float) -> FrameResult:
        if self.frame % int(self.fps * 2.5) == 0:
            self.pipes.append(Pipe())

        for pipe in self.pipes:
            pipe.update_position(delta)

            if not pipe.passed and pipe.pos.x < self.bird.pos.x:
                pipe.pass_()
                self.score += 1

            if pipe.pos.x - 2.5 < self.bird.pos.x < pipe.pos.x + 2.5 and (
                    self.bird.pos.y > pipe.pos.y + 2.5 or pipe.pos.y - 2.5 > self.bird.pos.y):
                return FrameResult.DEAD

        try:
            if self.pipes[0].pos.x < self.x_bounds[0]:
                self.pipes.pop(0)
        except IndexError:
            pass

        return FrameResult.NONE

    def every_frame(self, delta: float) -> FrameResult:
        self._bird_logic(delta)
        result = self._pipe_logic(delta)

        self.output.render(self.bird, self.pipes, self.score)
        print(self.score)

        return result


    def run(self) -> GameResult:
        last_frame: float = time.perf_counter()
        running: bool = True
        result: GameResult = GameResult.NONE
        frame_result: FrameResult = FrameResult.NONE

        while running:
            delta = time.perf_counter() - last_frame

            if delta > 1/self.fps:
                self.frame += 1
                frame_result: FrameResult = self.every_frame(delta)
                last_frame = time.perf_counter()

            if frame_result == FrameResult.DEAD:
                result = GameResult.DEAD
                running = False

            if self.input_.quit():
                result = GameResult.QUIT
                running = False

        return result


