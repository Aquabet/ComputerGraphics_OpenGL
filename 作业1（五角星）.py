# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import time
import copy

#我手算的三角函数
point = [[0, 0.8],
        [0.8*math.sin(2/5*math.pi), 0.8*math.cos(2/5*math.pi)], 
        [0.8*math.sin(1/5*math.pi), -0.8*math.cos(1/5*math.pi)], 
        [-0.8*math.sin(1/5*math.pi), -0.8*math.cos(1/5*math.pi)], 
        [-0.8*math.sin(2/5*math.pi), 0.8*math.cos(2/5*math.pi)] ]
point2 = copy.deepcopy(point)

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLineWidth(10)
    glBegin(GL_LINE_LOOP)
    for i in range(5):
        glVertex2f(point[i][0], point[i][1])
    glEnd()
    glFlush()
    # glutSwapBuffers()

#0->0 1->2 2->4 3->1 4->3
def move(timetick):
    point[1][0] = (10 - timetick)/10*point2[1][0] + timetick/10*point2[2][0]
    point[1][1] = (10 - timetick)/10*point2[1][1] + timetick/10*point2[2][1]
    point[2][0] = (10 - timetick)/10*point2[2][0] + timetick/10*point2[4][0]
    point[2][1] = (10 - timetick)/10*point2[2][1] + timetick/10*point2[4][1]
    point[3][0] = (10 - timetick)/10*point2[3][0] + timetick/10*point2[1][0]
    point[3][1] = (10 - timetick)/10*point2[3][1] + timetick/10*point2[1][1]
    point[4][0] = (10 - timetick)/10*point2[4][0] + timetick/10*point2[3][0]
    point[4][1] = (10 - timetick)/10*point2[4][1] + timetick/10*point2[3][1]
    # for i in range(5):
    #     print(point[i][0], point[i][1])
    draw()

if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow('Pentagon-star Transform')
    glutDisplayFunc(draw)
    timetick = 0
    func = True
    while 1:
        if func == True:
            timetick += 1
        else:
            timetick -= 1
        move(timetick)
        # print(timetick, func)
        if timetick == 10 and func == True:
            func = False
        if timetick == 0 and func == False:
            func = True
        time.sleep(0.1)
    glutMainLoop()
