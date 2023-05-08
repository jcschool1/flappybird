# Datei mit Beispiel Code Beispielen fuer Dokumentation

# # das ist ein Kommentar
# import pygame
#
# a: int = 1
#
# b
# b = 2
#
# if a == 1:
#     print("a ist 1")
#
# # while a == 1:   # wiederholt sich bis a nicht mehr 1 ist
# #     ...
# #
# #     if b == 1:
# #         break   # unterbricht die schleife sofort
#
# for c in ["hi", 5, "banana"]:   # iteriert ueber die Werte der Liste
#     print(c)    # gibt den Wert der Variable c aus
#
# def to_string(arg: int) -> str:
#     return str(arg)
#
# class GraphicalOutput(Output):
#
#     def __init__(self):
#         self.screen: pygame.Surface
#         self.x: int
#         self.y: int
#         self.scale_coefficient: float
#         self.offset: float
#
#         self.sprite_bird: pygame.Surface
#         self.sprite_pipe: pygame.Surface
#         self.sprite_floor: pygame.Surface
#         self.sprite_background: pygame.Surface
#
#     def _object_to_display(self, x: float, y: float) -> (float, float):
#         ...
#     def _display_to_pygame(self, x: float, y: float) -> (float, float):
#         ...
#
#     def _native_to_pygame(self, x: float, y: float) -> (float, float):
#         ...
#
#     def _is_in_bounds(self, coords: (float, float)) -> bool:
#         ...
#
#     def _max(self, coords: (float, float)) -> (float, float):
#         ...
#
#     def render(self, bird: GameObject, pipes: list[GameObject], score: int, *args) -> None:
#         ...
#
# class Game(object):
#
#     def __init__(self, fps: int, input_: Input, output: Output) -> None:
#         self.fps: int = fps
#         self.frame: int = 0
#         self.score: int = 0
#         self.jump_available: bool = True
#         self.bird: Bird = Bird(-70)
#         self.pipes: list[Pipe] = list()
#         self.input_: Input = input_
#         self.output: Output = output
#         self.x_bounds: (int, int) = (-40, 40)
#         self.y_bounds: (int, int) = (-20, 20)
#
#     def _bird_logic(self, delta: float) -> None:
#         ...
#
#     def _pipe_logic(self, delta: float) -> FrameResult:
#         ...
#
#     def every_frame(self, delta: float) -> FrameResult:
#         ...
#
#     def run(self) -> GameResult:
#         ...