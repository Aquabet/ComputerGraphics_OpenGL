# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import time

class ListNode:
    def __init__(self, ymax=0, x=0, deltax=0, next=None):
        self.x = x
        self.deltax = deltax
        self.ymax = ymax
        self.next = next

edge = np.zeros((20, 20), dtype=np.int)
edge -= 1

def init():
    glColor(1,0,0)
    drawline(2, 2, 2, 7, 5)
    drawline(2, 7, 5, 5, 4)
    drawline(5, 5, 11, 8, 3)
    drawline(11, 8, 11, 3, 2)
    drawline(11, 3, 5, 1, 1)
    drawline(5, 1, 2, 2, 0)
    edge[2, 2] = -1
    edge[2, 7] = -1
    edge[5, 5] = -1
    edge[11, 8] = -1
    edge[11, 3] = -1
    edge[5, 1] = -1
    glColor(1,1,1)
    for i in np.arange(-1, 1.1, 0.1):
        glBegin(GL_LINES)
        glVertex3f(-1, i, -0.9)
        glVertex3f(1, i, -0.9)
        glVertex3f(i, -1, -0.9)
        glVertex3f(i, 1, -0.9)
        glEnd()

def drawline(x1, y1, x2, y2, line):
    if x2 != x1:
        k = (y2-y1)/(x2-x1)
        if abs(k) <= 1:
            if x1 > x2:
                yNow = y2
            else:
                yNow = y1
            for xNow in range(min(x1, x2), max(x1, x2)+1):
                if line != -1:
                    drawPixel(xNow, round(yNow), -1)
                    edge[xNow, int(yNow)] = line
                else:
                    drawPixel(xNow, round(yNow))
                yNow = yNow + k
        else:
            if y1 > y2:
                xNow = x2
            else:
                xNow = x1
            for yNow in range(min(y1, y2), max(y1, y2)+1):
                if line != -1:
                    drawPixel(int(xNow+0.5), yNow, -1)
                    edge[int(xNow), yNow] = line
                else:
                    drawPixel(int(xNow+0.5), yNow)
                xNow = xNow + 1/k
    else:
        for i in range(min(y1, y2), max(y1, y2)+1):
            if line != -1:
                drawPixel(x1, i, -1)
                edge[x1, i] = line
            else:
                drawPixel(x1, i)

    glFlush()


# [-1, 1]->[0, 20]
def drawPixel(x, y, height=0):
        glBegin(GL_QUADS)
        glVertex3f((x-10)/10, (y-10)/10, height)
        glVertex3f((x-10)/10+0.1, (y-10)/10, height)
        glVertex3f((x-10)/10+0.1, (y-10)/10+0.1, height)
        glVertex3f((x-10)/10, (y-10)/10+0.1, height)
        glEnd()

def display():
    glLineWidth(5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init()
    glFlush()
    et = []
    et.append(ListNode(2, 5, -3))
    et.append(ListNode(3, 5, 3))
    et.append(ListNode(8, 11, 0))
    et.append(ListNode(8, 5, 2))
    et.append(ListNode(7, 5, -3/2))
    et.append(ListNode(7, 2, 0))

    AET = []
    for i in range(9):
        AET.append(ListNode(0, 0, 0))
    for i in range(9):
        for j in range(12):
            if edge[j, i] != -1:
                # print("edge"+str(i)+" "+str(j) +str(edge[j, i]) )
                node = AET[i]
                while node.next != None:
                    node = node.next
                node.next = ListNode(et[edge[j, i]].ymax, j, et[edge[j, i]].deltax)
    drawline(2, 2, 7, 2, -1)
    drawline(6, 4, 11, 4, -1)
    glColor(1,0,0)
    drawline(3, 1, 7, 1, 6)
    glColor(0,0,0)
    drawPixel(5, 6, -0.5)
    glColor(1,1,1)
    for i in range(9):
        node = AET[i]
        # print(str(i)+" begin")
        while node.next != None:
            # print(node.next.x)
            node = node.next

    todraw = False
    for i in range(9):
        node = AET[i]
        while node.next != None:
            if todraw == False:
                begin = node.next
                todraw = True
            else:
                end = node.next
                todraw = False
                drawline(begin.x, i, end.x, i, -1)
            node = node.next


if __name__ == "__main__":
    
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow("polyfill")
    glEnable(GL_DEPTH_TEST) #开启遮挡关系
    glDepthFunc(GL_LEQUAL)
    glutDisplayFunc(display)
    glutMainLoop()