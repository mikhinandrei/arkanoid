from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
import time
import math

#Размеры поля

M = 20
N = 20

SCALE = 20

WIDTH = SCALE * (M+1)
HEIGHT = SCALE * (N+1)
SPEED = 0.07

epsilon = 0.00001


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


class Ball():
    global epsilon
    global SPEED

    def __init__(self):
        self.dead = 0
        self.direction = "down"
        self.x = M//2
        self.y = N//2
        self.traectory_x = 0
        self.traectory_y = -1
        self.radius = N/40
        self.draw_circle()
        self.move_circle()


    def draw_circle(self):
        amount_segments = 50
        glPushMatrix()
        glBegin(GL_LINE_LOOP)
        for i in range(amount_segments):
            angle = (2.0 * math.pi * i)/amount_segments
            dx = self.radius * math.cos(angle) * SCALE
            dy = self.radius * math.sin(angle) * SCALE
            glVertex2f(self.x * SCALE + dx, self.y * SCALE + dy)
        glEnd()
        glPopMatrix()

    def move_circle(self):
        if self.dead == 0:
            if self.y - 0.8 <= epsilon:
                print("You die")
                self.dead = 1
            else:
                self.x += self.traectory_x * SPEED
                self.y += self.traectory_y * SPEED
            if (M + 1 - self.radius) - self.y <= epsilon:
                self.traectory_y = -1



class Platform():
    global M
    global N
    global SCALE
    global epsilon

    def __init__(self):
        self.x = M/2
        self.length = 5
        self.borders = [int(self.x - self.length // 2), int(self.x + self.length // 2)]
        self.ball = Ball()

    def move(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            if self.borders[0] > 0:
                self.x -= 1
                self.borders[0] -= 1
                self.borders[1] -= 1
        if key == GLUT_KEY_RIGHT:
            if self.borders[1] <= M:
                self.x += 1
                self.borders[0] += 1
                self.borders[1] += 1
        glutPostRedisplay()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        for x in range(self.borders[0], self.borders[1]):
            glColor3ub(220, 220, 220)
            glRectf(x * SCALE, SCALE, (x + 1) * SCALE, 0)
        self.ball.draw_circle()
        self.ball.move_circle()
        if self.ball.y - (1 + self.ball.radius) <= epsilon:
            if self.borders[0] <= self.ball.x <= self.borders[1]:
                self.reflect_ball()
        if (self.ball.x - self.ball.radius <= epsilon) or (M - (self.ball.x + self.ball.radius - 1) <= epsilon):
            self.reflect_ball_from_the_wall()
        time.sleep(0.01)
        if self.ball.dead == 0:
            glFlush()
            glutPostRedisplay()

    def reflect_ball(self):
        point1 = [self.x, 0]
        point2 = [self.ball.x, self.ball.y]
        line_vector = [point2[0] - point1[0], point2[1] - point1[1]]
        self.ball.traectory_x = line_vector[0]
        self.ball.traectory_y = line_vector[1]
        print(line_vector)

    def reflect_ball_from_the_wall(self):
        self.ball.traectory_x *= -1


if __name__ == '__main__':
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Arkanoid")

    game = Platform()

    glClearColor(0, 0, 0, 0)

    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glutDisplayFunc(game.draw)
    glutSpecialFunc(game.move)

    glutMainLoop()