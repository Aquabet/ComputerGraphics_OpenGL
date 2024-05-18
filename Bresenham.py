from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math as m
import time

myR = 8

def drawPixel(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x/10, y/10)
    glVertex2f(x/10+0.1, y/10)
    glVertex2f(x/10+0.1, y/10+0.1)
    glVertex2f(x/10, y/10+0.1)
    glEnd()

def init():
    glColor(1,0,0)
    glBegin(GL_LINE_LOOP)
    n = 80
    R = 0.8
    for i in range(n+1):
        glVertex3f(R*m.cos(2*m.pi*i/n)+0.05, R*m.sin(2*m.pi*i/n)+0.05, -1)
    glEnd()
    glColor(1,1,0)
    glBegin(GL_LINES)
    glVertex3f(-1,0.05,-1)
    glVertex3f(1,0.05,-1)
    glVertex3f(0.05,-1,-1)
    glVertex3f(0.05,1,-1)
    glEnd()
    glColor(1,1,1)
    for i in np.arange(-1, 1.1, 0.1):
        glBegin(GL_LINES)
        glVertex2f(-1, i)
        glVertex2f(1, i)
        glVertex2f(i, -1)
        glVertex2f(i, 1)
        glEnd()
#增量法推\deltaD
def to_H(x, y, delta):
    x+=1
    delta += 2*x+1
    return x, y, delta

def to_D(x, y, delta):
    x+=1
    y-=1
    delta += 2*(x-y+1)
    return x, y, delta

def to_V(x, y, delta):
    y-=1
    delta += (-2*y+1)
    return x, y, delta

def display():
    glLineWidth(5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init()
    glFlush()

    x = 0
    y = myR
    delta = 2*(1-y)
    while y >= 0:
        drawPixel(x, y)
        # drawPixel(-x, y)
        # drawPixel(x, -y)
        # drawPixel(-x, -y)
        glFlush()
        time.sleep(1)
        # 若deltaD>0，若deltaHD<=0 取D，否则取V
        # 若deltaD<0，若deltaDV<=0 取H，否则取D
        if delta < 0:
            delta1 = 2*(delta+y) - 1
            if delta1 <= 0:
                x, y, delta = to_H(x, y, delta)
            else:
                x, y, delta = to_D(x, y, delta)
        elif delta > 0:
            delta2 = 2*(delta-x) - 1
            if(delta2 <= 0):
                x, y, delta = to_D(x, y, delta)
            else:
                x, y, delta = to_V(x, y, delta)
        else:
            x, y, delta = to_D(x, y, delta)

if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow("Bresenham_Algorithm")
    glEnable(GL_DEPTH_TEST) #开启遮挡关系
    glDepthFunc(GL_LEQUAL)
    glutDisplayFunc(display)
    glutMainLoop()