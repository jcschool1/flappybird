import game

from output import GeneralOutput
from input_ import PyGameInput


if __name__ == '__main__':
    user_output = GeneralOutput(13)
    user_input = PyGameInput()

    running: bool = True
    while running:
        flappybird = game.Game(30, user_input, user_output)
        r = flappybird.run()

        if r == game.GameResult.QUIT:
            running = False

        if r == game.GameResult.DEAD:
            print("player died")
