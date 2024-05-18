from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math as m
import time

edges = [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1],
         [10, 1], [11, 1], [12, 1], [13, 1], [14, 1], [
             15, 1], [16, 1], [17, 1], [18, 1],
         [18, 2], [18, 3], [18, 4], [18, 5], [18, 6], [
             18, 7], [18, 8], [17, 8], [16, 8],
         [15, 8], [14, 8], [13, 8], [12, 8], [11, 8], [
             10, 8], [9, 9], [10, 10], [10, 11],
         [10, 12], [10, 13], [10, 14], [10, 15], [
             10, 16], [10, 17], [10, 18], [9, 18], [8, 18],
         [7, 18], [6, 18], [5, 18], [4, 18], [3, 18], [
             2, 18], [1, 18], [1, 17], [1, 16],
         [1, 15], [1, 14], [1, 13], [1, 12], [
             1, 11], [1, 10], [1, 9], [1, 8], [1, 7],
         [1, 6], [1, 5], [1, 4], [1, 3], [1, 2]]


def drawPixel(x, y):
    glBegin(GL_QUADS)
    glVertex2f((x-10)/10, (y-10)/10)
    glVertex2f((x-10)/10+0.1, (y-10)/10)
    glVertex2f((x-10)/10+0.1, (y-10)/10+0.1)
    glVertex2f((x-10)/10, (y-10)/10+0.1)
    glEnd()


def init():
    for i in np.arange(-1, 1.1, 0.1):
        glBegin(GL_LINES)
        glVertex2f(-1, i)
        glVertex2f(1, i)
        glVertex2f(i, -1)
        glVertex2f(i, 1)
        glEnd()
        for i in edges:
            drawPixel(i[0], i[1])


def display():
    glColor(1, 1, 1)
    glLineWidth(5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init()
    glFlush()
    glColor(1, 0, 0)

    readedlist = [[4, 4]]
    stack = [[4, 4]]
    for i in edges:
        readedlist.append(i)

    while len(stack) != 0:
        nowcheck = stack.pop(0)
        drawPixel(nowcheck[0], nowcheck[1])
        glFlush()
        time.sleep(0.05)

        checklist = [[nowcheck[0]-1, nowcheck[1]],
                     [nowcheck[0], nowcheck[1]+1],
                     [nowcheck[0]+1, nowcheck[1]],
                     [nowcheck[0], nowcheck[1]-1]]
        for i in checklist:
            if not (i in readedlist):
                readedlist.append(i)
                stack.append(i)

if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow("Seed_fill")
    glutDisplayFunc(display)
    glutMainLoop()
