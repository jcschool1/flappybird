import game

from output import GraphicalOutput
from input_ import KeyboardInput, Input


if __name__ == '__main__':
    user_output = GraphicalOutput()
    user_input = Input()

    flappybird = game.Game(10, user_input, user_output)

    running: bool = True
    while running:
        r = flappybird.run()
        if r == game.GameResult.QUIT:
            running = False