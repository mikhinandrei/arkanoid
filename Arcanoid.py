from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
import time

#Размеры поля

M = 20
N = 20

SCALE = 20

WIDTH = SCALE * (M+1)
HEIGHT = SCALE * (N+1)

def disp():
    pass

class Capsule():
    def __init__(self, capsule_type):
        if capsule_type == 0:
            self.feature = "Expand"
        if capsule_type == 1:
            self.feature = "Divide"
        if capsule_type == 2:
            self.feature = "Laser"
        if capsule_type == 3:
            self.feature = "Slow"
        if capsule_type == 4:
            self.feature = "Break"
        if capsule_type == 5:
            self.feature = "Catch"
        if capsule_type == 6:
            self.feature = "Player"

class Brick():
    def __init__(self):
        self.type = random.randrange()

class PrizeBrick():
    def __init__(self):
        self.capsule_type = random.randrange(7)
        self.capsule = Capsule(self.capsule_type)

class Platform():
    global M
    global N
    def __init__(self):
        self.x = M/2
        self.length = 5
        self.borders = [self.x - self.length // 2, self.x + self.length // 2]

    def move(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            if self.borders[0] > 0:
                self.x -= 1
                self.borders[0] -= 1
                self.borders[1] -= 1
        if key == GLUT_KEY_RIGHT:
            if self.borders[0] < M:
                self.x -= 1
                self.borders[0] -= 1
                self.borders[1] -= 1

if __name__ == '__main__':
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Arcanoid")

    glClearColor(0, 0, 0, 0)

    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glutDisplayFunc(disp)

    glutMainLoop()