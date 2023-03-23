import random

from dataclasses import dataclass


@dataclass()
class Vector:
    x: float
    y: float


class GameObject(object):

    def __init__(self, pos: Vector = Vector(0, 0), vel: Vector = Vector(0, 0), acc: Vector = Vector(0, 0)):
        self.pos: Vector = pos
        self.vel: Vector = vel
        self.acc: Vector = acc

    def update_position(self, delta: float) -> None:
        self.vel.x += self.acc.x * delta
        self.vel.y += self.acc.y * delta
        self.pos.x += self.vel.x * delta
        self.pos.y += self.vel.y * delta

    def max(self, x: (int, int), y: (int, int)) -> None:
        if self.pos.x < x[0]:
            self.pos.x = x[0]
        if self.pos.x > x[1]:
            self.pos.x = x[1]

        if self.pos.y < y[0]:
            self.pos.y = y[0]
        if self.pos.y > y[1]:
            self.pos.y = y[1]

class Bird(GameObject):

    def __init__(self, acc_y: float):
        super(Bird, self).__init__(pos=Vector(-5, 0), acc=Vector(0, acc_y))

    def jump(self) -> None:
        self.vel.y = self.acc.y * -0.5


class Pipe(GameObject):

    def __init__(self, speed_coefficient: float = 1.0):
        vel = Vector(-5*speed_coefficient, 0)
        pos = Vector(20, random.randint(1, 7)*2-7)
        super(Pipe, self).__init__(pos=pos, vel=vel)
        self.passed = False

    def pass_(self) -> None:
        self.passed = True
