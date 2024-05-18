# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import time
x1 = 0
y1 = 0
x2 = 0
y2 = 0

def init():
    glColor(1,0,0)
    glBegin(GL_LINES)
    glVertex3f((x1-10)/10+0.05, (y1-10)/10+0.05,-1)
    glVertex3f((x2-10)/10+0.05, (y2-10)/10+0.05,-1)
    glEnd()
    glColor(1,1,1)
    for i in np.arange(-1, 1.1, 0.1):
        glBegin(GL_LINES)
        glVertex2f(-1, i)
        glVertex2f(1, i)
        glVertex2f(i, -1)
        glVertex2f(i, 1)
        glEnd()

# [-1, 1]->[0, 20]
def drawPixel(x, y):
    glBegin(GL_QUADS)
    glVertex2f((x-10)/10, (y-10)/10)
    glVertex2f((x-10)/10+0.1, (y-10)/10)
    glVertex2f((x-10)/10+0.1, (y-10)/10+0.1)
    glVertex2f((x-10)/10, (y-10)/10+0.1)
    glEnd()

def display():
    glLineWidth(5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init()
    glFlush()

    k = (y2-y1)/(x2-x1)
    if abs(k) <= 1:
        yNow = y1
        for xNow in range(x1, x2+1):
            drawPixel(xNow, round(yNow))
            glFlush()
            yNow = yNow + k
            time.sleep(0.5)
    else:
        xNow = x1
        for yNow in range(y1, y2+1):
            drawPixel(int(xNow+0.5), yNow)
            glFlush()
            xNow = xNow + 1/k
            time.sleep(0.5)



if __name__ == "__main__":
    x1 = int(input("请输入第一个点的x坐标:"))
    y1 = int(input("请输入第一个点的y坐标:"))
    x2 = int(input("请输入第二个点的x坐标:"))
    y2 = int(input("请输入第二个点的y坐标:"))
    
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow("DDA_Algorithm")
    glEnable(GL_DEPTH_TEST) #开启遮挡关系
    glDepthFunc(GL_LEQUAL)
    glutDisplayFunc(display)
    glutMainLoop()