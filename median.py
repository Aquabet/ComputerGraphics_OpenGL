from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math as m
import time

xleft = -0.5
xright = 0.5
ybottom = -0.5
ytop = 0.5

p1 = [-0.7, -0.7]
p2 = [0.4, 0.2]


def init():
    glBegin(GL_LINE_LOOP)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(-0.7, -0.7)
    glVertex2f(0.4, 0.2)
    glEnd()


def checkPosition(p):
    num = 0
    if p[0] < xleft:
        num += 1
    if p[0] > xright:
        num += 2
    if p[1] < ybottom:
        num += 4
    if p[1] > ytop:
        num += 8
    return num


def drawP(p):
    # glBegin(GL_LINES)
    # glVertex2f(p[0]-0.01, p[1]-0.01)
    # glVertex2f(p[0]+0.01, p[1]+0.01)
    # glEnd()
    glBegin(GL_QUADS)
    glVertex2f(p[0]-0.02, p[1]-0.02)
    glVertex2f(p[0]+0.02, p[1]-0.02)
    glVertex2f(p[0]+0.02, p[1]+0.02)
    glVertex2f(p[0]-0.02, p[1]+0.02)

    glEnd()
    glFlush()
    time.sleep(0.5)

def display():
    glColor(1, 1, 1)
    glLineWidth(10)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init()
    glFlush()
    glColor(0, 0, 1)

    pc1 = p1
    pc2 = p2

    if checkPosition(pc2) == 0:  # find p2 final
        pass
    elif (checkPosition(pc1) & checkPosition(pc2)) != 0:
        pc2 = pc1
    else:
        pm = [0, 0]
        while not (((abs(pm[0]-xleft) < 0.001 or abs(pm[0]-xright) < 0.001) and (pm[1] > ybottom and pm[1] < ytop)) or
                   (abs(pm[1]-ybottom) < 0.001 or abs(pm[1]-ytop) < 0.001) and (pm[0] > xleft and pm[0] < xright)):
            pm = [(pc1[0]+pc2[0])/2, (pc1[1]+pc2[1])/2]

            drawP(pm)
            
            if (checkPosition(pm) & checkPosition(pc2)) != 0 and checkPosition(pm) != 0:
                pc2 = pm
            else:
                pc1 = pm
        pc2 = pm
    pfinal2 = pc2

    pc1 = p1
    pc2 = p2

    if checkPosition(pc1) == 0:  # find p1 final
        pass
    elif (checkPosition(pc1) & checkPosition(pc2)) != 0:
        pc2 = pc1
    else:
        pm = [0, 0]
        while not (((abs(pm[0]-xleft) < 0.001 or abs(pm[0]-xright) < 0.001) and (pm[1] > ybottom and pm[1] < ytop)) or
                   (abs(pm[1]-ybottom) < 0.001 or abs(pm[1]-ytop) < 0.001) and (pm[0] > xleft and pm[0] < xright)):
            pm = [(pc1[0]+pc2[0])/2, (pc1[1]+pc2[1])/2]

            drawP(pm)

            if (checkPosition(pm) & checkPosition(pc1)) != 0 and checkPosition(pm) != 0:
                pc1 = pm
            else:
                pc2 = pm
        pc1 = pm
    pfinal1 = pc1

    glColor(1, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(pfinal1[0], pfinal1[1])
    glVertex2f(pfinal2[0], pfinal2[1])
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow("median")
    glEnable(GL_DEPTH_TEST) #开启遮挡关系
    glDepthFunc(GL_LEQUAL)
    glutDisplayFunc(display)
    glutMainLoop()
