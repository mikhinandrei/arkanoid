from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
import time
import math

# Constants

M = 30  # Width in squares
N = 20  # Height in squares

SCALE = 20  # Pixels in one square

WIDTH = SCALE * M
HEIGHT = SCALE * N
SPEED = 0.1  # Speed of the ball

epsilon = 0.00001

COLORS = [(51, 237, 57)]


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
    global COLORS
    global SCALE

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 4
        self.type = random.randrange(7)
        self.capsule = Capsule(self.type)
        self.display_brick()

    # Display the brick
    def display_brick(self):
        glColor3ub(COLORS[0][0], COLORS[0][1], COLORS[0][2])
        glRectf((self.x -0.9) * SCALE, (self.y + 0.9) * SCALE, (self.x + 0.9) * SCALE, self.y * SCALE)


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

    # Display the ball
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

    # Move the ball. Calculating velocities on x and y axes
    def move_circle(self):
        if self.dead == 0:
            if self.y - 0.8 <= epsilon:
                print("You die")
                self.dead = 1
            else:
                self.x += self.traectory_x * SPEED
                self.y += self.traectory_y * SPEED
            if (N - self.radius) - self.y <= epsilon:
                self.traectory_y = -1


# Player`s Platform
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
        self.bricks = [Brick(2 * x + 1, 19) for x in range(15)]

    # Move platform
    def move(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            if self.borders[0] > 0:
                self.x -= 1
                self.borders[0] -= 1
                self.borders[1] -= 1
        if key == GLUT_KEY_RIGHT:
            if self.borders[1] < M:
                self.x += 1
                self.borders[0] += 1
                self.borders[1] += 1
        glutPostRedisplay()

    # Display objects
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        for x in range(self.borders[0], self.borders[1]):
            glColor3ub(220, 220, 220)
            glRectf(x * SCALE, SCALE, (x + 1) * SCALE, 0)
        self.ball.draw_circle()
        self.ball.move_circle()
        self.draw_bricks()
        if self.touch():
            self.reflect_ball()
        coord = self.touch_bricks()
        if coord:
            print(coord)
            self.reflect_from_brick(coord)
            # self.reflect_from_brick()
        if (self.ball.x - self.ball.radius <= epsilon) or (M - (self.ball.x + self.ball.radius) <= epsilon):
            self.reflect_ball_from_the_wall()
        time.sleep(0.01)
        if self.ball.dead == 0:
            glFlush()
            glutPostRedisplay()

    # Display brick
    def draw_bricks(self):
        for brick in self.bricks:
            brick.display_brick()

    # Processing of reflections of the ball from the platform
    def reflect_ball(self):
        point1 = [self.x, 0]
        point2 = [self.ball.x, self.ball.y]
        line_vector = [point2[0] - point1[0], point2[1] - point1[1]]
        self.ball.traectory_x = line_vector[0]/(line_vector[0]**2 + line_vector[1]**2)**0.5
        self.ball.traectory_y = line_vector[1]/(line_vector[0]**2 + line_vector[1]**2)**0.5

    def reflect_from_brick(self, coord):
        self.ball.traectory_x *= -1
        self.ball.traectory_y *= -1
        self.bricks[coord].x = -10
        self.bricks[coord].y = -10

    # Reflections from lateral walls
    def reflect_ball_from_the_wall(self):
        self.ball.traectory_x *= -1

    # This function checks if the ball touches the platform
    def touch(self):
        if self.ball.y - (1 + self.ball.radius) > epsilon:
            return 0
        x1 = self.ball.x + (self.ball.radius - (1 - self.ball.y)**2) ** 0.5
        x2 = self.ball.x - (self.ball.radius - (1 - self.ball.y) ** 2) ** 0.5
        if (x2 > self.borders[0]) and (x2 < self.borders[1]):
            return 1
        elif (x1 > self.borders[0]) and (x1 < self.borders[1]):
            return 1
        else:
            return 0

    # This function checks if the ball touches the brick
    def touch_bricks(self):
        coord_1 = int((self.ball.x - self.ball.radius) // 2)
        print(coord_1)
        if 0 <= (self.ball.x + self.ball.radius) // 2 <= len(self.bricks) - 1:
            coord_2 = int((self.ball.x + self.ball.radius) // 2)
        else:
            coord_2 = coord_1
        y1 = int(self.ball.x // 2)
        y2 = int(self.ball.x // 2 + 1)
        brick1 = self.bricks[coord_1]
        brick2 = self.bricks[coord_2]
        if self.ball.radius - (brick1.y - self.ball.y) ** 2 >= 0:
            x1 = self.ball.x + (self.ball.radius - (brick1.y - self.ball.y) ** 2) ** 0.5
            x2 = self.ball.x - (self.ball.radius - (brick1.y - self.ball.y) ** 2) ** 0.5
            if (x2 > brick1.x - 0.9) and (x2 < brick1.x + 0.9):
                return coord_1
            elif (x1 > brick1.x - 0.9) and (x1 < brick1.x + 0.9):
                return coord_1
            elif (x2 > brick2.x - 0.9) and (x2 < brick2.x + 0.9):
                return coord_2
            elif (x1 > brick2.x - 0.9) and (x1 < brick2.x + 0.9):
                return coord_2
            else:
                return 0
        else:
            return 0


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