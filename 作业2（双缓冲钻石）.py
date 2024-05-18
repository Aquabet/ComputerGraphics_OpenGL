from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math as m
import time


class diamond:
    n = 80
    edges = 20
    r = 0.8
    startAngle = 0
    fps = 10

    def addAngle(self, angle):
        self.startAngle = (self.startAngle+angle) % 360


def draw(obj):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glBegin(GL_LINE_LOOP)
    # for i in range(obj.n):
    #     glVertex2f(obj.r*m.cos(2*m.pi*i/obj.n),
    #                obj.r*m.sin(2*m.pi*i/obj.n))
    # glEnd()
    point = []
    for i in range(obj.edges):
        point.append([obj.r*m.cos((i/obj.edges+obj.startAngle/360)*2*m.pi),
                      obj.r*m.sin((i/obj.edges+obj.startAngle/360)*2*m.pi)])
    glBegin(GL_LINES)
    for i in range(obj.edges):
        for j in range(i, obj.edges):
            glVertex2f(point[i][0], point[i][1])
            glVertex2f(point[j][0], point[j][1])
    glEnd()


def display():
    glLineWidth(2)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    aDiamond = diamond()
    while 1:
        draw(aDiamond)
        glutSwapBuffers()
        aDiamond.addAngle(20)
        time.sleep(1/aDiamond.fps)


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(600, 600)
    glutCreateWindow("Diamond")
    glutDisplayFunc(display)
    glutMainLoop()
