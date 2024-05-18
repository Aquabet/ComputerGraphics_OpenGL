import time
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtOpenGL import QGLWidget
import math as m
from PyQt5 import QtCore
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Ball import *
import random
from PIL import Image


class MyGLWidget(QtWidgets.QOpenGLWidget):

    IS_PERSPECTIVE = True                               # 透视投影
    # 视景体的left/right/bottom/top/near/far六个面
    VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])
    SCALE_K = np.array([1.0, 1.0, 1.0])                 # 模型缩放比例
    EYE = np.array([0.0, 0.0, 2.0])                     # 眼睛的位置（默认z轴的正方向）
    LOOK_AT = np.array([0.0, 0.0, 0.0])                 # 瞄准方向的参考点（默认在坐标原点）
    EYE_UP = np.array([0.0, 1.0, 0.0])                  # 定义对观察者而言的上方（默认y轴的正方向）
    WIN_W, WIN_H = 0, 0                             # 保存窗口宽度和高度的变量
    LEFT_IS_DOWNED = False                              # 鼠标左键被按下
    MOUSE_X, MOUSE_Y = 0, 0                             # 考察鼠标位移量时保存的起始位置
    ballset = []
    lighted = -1
    ctlpoints = None
    fps = 20

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)

    def initializeGL(self):
        version_profile = QtGui.QOpenGLVersionProfile()
        version_profile.setVersion(2, 0)
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()
        glutInit()
        # 设置背景色
        self.gl.glClearColor(0, 0, 0, 1.0)
        # 深度测试
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(GL_TEXTURE_2D)
        self.DIST, self.PHI, self.THETA = self.getposture()  # 眼睛与观察目标之间的距离、仰角、方位角
        self.ctlpoints = np.array([[[-1, -1, -1],
                                    [-1, -1, -1/3],
                                    [-1, -1, 1/3],
                                    [-1, -1, 1]],
                                   [[-1/3, -1, -1],
                                    [-1/3, -1, -1/3],
                                    [-1/3, -1, 1/3],
                                    [-1/3, -1, 1]],
                                   [[1/3, -1, -1],
                                    [1/3, -1, -1/3],
                                    [1/3, -1, 1/3],
                                    [1/3, -1, 1]],
                                   [[1, -1, -1],
                                    [1, -1, -1/3],
                                    [1, -1, 1/3],
                                    [1, -1, 1]]], 'f')

    def paintGL(self):
        self.paintInit()
        # self.paintrbq()
        self.paintLight()
        self.paintFace()
        self.paintSet()

    def resizeGL(self, width, height):
        self.WIN_W, self.WIN_H = width, height

    def mousePressEvent(self, event):
        self.MOUSE_X, self.MOUSE_Y = event.x(), event.y()
        if event.button() == QtCore.Qt.LeftButton:
            pass

    def mouseMoveEvent(self, event):
        dx = self.MOUSE_X - event.pos().x()
        dy = event.pos().y() - self.MOUSE_Y
        self.MOUSE_X, self.MOUSE_Y = event.pos().x(), event.pos().y()

        self.PHI += 2*np.pi*dy/self.WIN_H
        self.PHI %= 2*np.pi
        self.THETA += 2*np.pi*dx/self.WIN_W
        self.THETA %= 2*np.pi
        r = self.DIST*np.cos(self.PHI)

        self.EYE[1] = self.DIST*np.sin(self.PHI)
        self.EYE[0] = r*np.sin(self.THETA)
        self.EYE[2] = r*np.cos(self.THETA)

        if 0.5*np.pi < self.PHI < 1.5*np.pi:
            self.EYE_UP[1] = -1.0
        else:
            self.EYE_UP[1] = 1.0
        self.update()

    def wheelEvent(self, event):
        step = event.angleDelta().y() / 120
        if step == 1.0:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 0.9
            self.DIST, self.PHI, self.THETA = self.getposture()
        else:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 1.1
            self.DIST, self.PHI, self.THETA = self.getposture()
        self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            self.IS_PERSPECTIVE = not self.IS_PERSPECTIVE
        self.update()

    def paintInit(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 清除屏幕及深度缓存
        glMatrixMode(GL_PROJECTION)        # 设置投影（透视投影）
        glLoadIdentity()

        if self.WIN_W > self.WIN_H:
            if self.IS_PERSPECTIVE:
                glFrustum(self.VIEW[0]*self.WIN_W/self.WIN_H, self.VIEW[1]*self.WIN_W /
                          self.WIN_H, self.VIEW[2], self.VIEW[3], self.VIEW[4], self.VIEW[5])
            else:
                glOrtho(self.VIEW[0]*self.WIN_W/self.WIN_H, self.VIEW[1]*self.WIN_W /
                        self.WIN_H, self.VIEW[2], self.VIEW[3], self.VIEW[4], self.VIEW[5])
        else:
            if self.IS_PERSPECTIVE:
                glFrustum(self.VIEW[0], self.VIEW[1], self.VIEW[2]*self.WIN_H/self.WIN_W,
                          self.VIEW[3]*self.WIN_H/self.WIN_W, self.VIEW[4], self.VIEW[5])
            else:
                glOrtho(self.VIEW[0], self.VIEW[1], self.VIEW[2]*self.WIN_H/self.WIN_W,
                        self.VIEW[3]*self.WIN_H/self.WIN_W, self.VIEW[4], self.VIEW[5])

        # 设置模型视图
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 几何变换
        glScale(self.SCALE_K[0], self.SCALE_K[1], self.SCALE_K[2])

        # 设置视点
        gluLookAt(
            self.EYE[0], self.EYE[1], self.EYE[2],
            self.LOOK_AT[0], self.LOOK_AT[1], self.LOOK_AT[2],
            self.EYE_UP[0], self.EYE_UP[1], self.EYE_UP[2]
        )

        # 设置视口
        glViewport(0, 0, self.WIN_W, self.WIN_H)

    def getposture(self):
        dist = np.sqrt(np.power((self.EYE-self.LOOK_AT), 2).sum())
        if dist > 0:
            phi = np.arcsin((self.EYE[1]-self.LOOK_AT[1])/dist)
            theta = np.arcsin((self.EYE[0]-self.LOOK_AT[0])/(dist*np.cos(phi)))
        else:
            phi = 0.0
            theta = 0.0
        return dist, phi, theta

    def paintSet(self):
        for i in range(len(self.ballset)):
            self.paintBall(i)

    def paintFace(self):
        self.loadPic1()
        self.gl.glBegin(self.gl.GL_QUADS)
        self.gl.glNormal3f(1/3, 1/3, 1/3)
        self.gl.glTexCoord2f(0.0, 1.0)
        self.gl.glVertex3f(-3, -1, -3)
        self.gl.glTexCoord2f(0.0, 0.0)
        self.gl.glVertex3f(-3, -1,  3)
        self.gl.glTexCoord2f(1.0, 0.0)
        self.gl.glVertex3f(3, -1,  3)
        self.gl.glTexCoord2f(1.0, 1.0)
        self.gl.glVertex3f(3, -1, -3)
        self.gl.glEnd()
        # knots = np.array((0, 0, 0, 0, 1, 1, 1, 1), 'f')
        # theNurb = gluNewNurbsRenderer()
        # gluBeginSurface(theNurb)
        # gluNurbsSurface(theNurb,
        #                 knots, knots,
        #                 self.ctlpoints,
        #                 GL_MAP2_VERTEX_3)
        # gluNurbsSurface(theNurb,
        #                 knots, knots,
        #                 self.ctlpoints,
        #                 GL_MAP2_NORMAL)
        # gluEndSurface(theNurb)

    def paintBall(self, ptr):
        thetax = (self.ballset[ptr].anglex+self.ballset[ptr].rollx)/180*m.pi
        thetay = (self.ballset[ptr].angley+self.ballset[ptr].rolly)/180*m.pi
        thetaz = (self.ballset[ptr].anglez+self.ballset[ptr].rollz)/180*m.pi
        t0to = [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [self.ballset[ptr].positionx, self.ballset[ptr].positiony, self.ballset[ptr].positionz, 1]]
        t1 = [[self.ballset[ptr].phi, 0, 0, 0],
              [0, self.ballset[ptr].phi, 0, 0],
              [0, 0, self.ballset[ptr].phi, 0],
              [0, 0, 0, 1]]  # 放缩,
        t2x = [[1, 0, 0, 0],
               [0, m.cos(thetax), m.sin(thetax), 0],
               [0, -m.sin(thetax), m.cos(thetax), 0],
               [0, 0, 0, 1]]
        t2y = [[m.cos(thetay), 0, -m.sin(thetay), 0],
               [0, 1, 0, 0],
               [m.sin(thetay), 0, m.cos(thetay), 0],
               [0, 0, 0, 1]]
        t2z = [[m.cos(thetaz), m.sin(thetaz), 0, 0],
               [-m.sin(thetaz), m.cos(thetaz), 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]

        tmpa = np.array(self.ballset[ptr].vertex)
        tmpb = np.append(tmpa, np.ones((np.shape(tmpa)[0], 1)), axis=1)
        tmpb = tmpb.dot(t1).dot(t2x).dot(t2y).dot(t2z).dot(t0to)
        tmpnormal1 = np.array(self.ballset[ptr].normal)
        tmpnormal2 = np.append(tmpnormal1, np.ones(
            (np.shape(tmpnormal1)[0], 1)), axis=1)
        tmpnormal2 = tmpnormal2.dot(t2x).dot(t2y).dot(t2z)

        self.loadPic2()
        for f in range(len(self.ballset[ptr].faces)):
            # self.gl.glBegin(self.gl.GL_LINE_LOOP)
            self.gl.glBegin(self.gl.GL_TRIANGLES)
            self.gl.glNormal3f(tmpnormal2[f][0], 
                               tmpnormal2[f][1], 
                               tmpnormal2[f][2])
            tantheta = [0.0, 0.0, 0.0]
            theta = np.array([0.0, 0.0, 0.0])
            for point in range(3):
                if (tmpb[self.ballset[ptr].faces[f][point]][2] - self.ballset[ptr].positionz) == 0:
                    if tmpb[self.ballset[ptr].faces[f][point]][0] - self.ballset[ptr].positionx > 0:
                        theta[point] = 0.5*m.pi
                    else:
                        theta[point] = 1.5*m.pi
                else:
                    # Here is a bug, when theta -> $+\infty$ or $-\infty$ , tantheta will overflow int, then the value of tantheta will changed to a value between int_min to int_max
                    # so if tantheta greater than int_max or less than int_min, theta will not be the right value approach to 0.5Pi or 1.5Pi but any ohter value of other parts of the pic
                    # there is a right way to calculate it by sin(theta) and cos(theta) and judge the quadrant by its sign. but I am lazy to change it cause it does not affect the result of this project
                    # but if you want to use this code for any other place, such as change a pic of your own, you had better fix the bug :)
                    # -By Jasiah
                    # tantheta[point] = (tmpb[self.ballset[ptr].faces[f][point]][0] - self.ballset[ptr].positionx) / (tmpb[self.ballset[ptr].faces[f][point]][2] - self.ballset[ptr].positionz)
                    theta[point] = np.arctan(
                        (tmpb[self.ballset[ptr].faces[f][point]][0] - self.ballset[ptr].positionx) / (tmpb[self.ballset[ptr].faces[f][point]][2] - self.ballset[ptr].positionz)) + np.pi*0.5
                    if (tmpb[self.ballset[ptr].faces[f][point]][2] - self.ballset[ptr].positionz) < 0:
                        theta[point] += np.pi
            height = np.array([0.0, 0.0, 0.0])
            for point in range(3):
                height[point] = tmpb[self.ballset[ptr].faces[f][point]][1] - self.ballset[ptr].positiony
            height += self.ballset[ptr].phi
            height /= 2*self.ballset[ptr].phi
            # print(height, theta/2/m.pi)
            for point in range(3):
                self.gl.glTexCoord2f(theta[point]/m.pi/2, height[point])
                self.gl.glVertex3f(tmpb[self.ballset[ptr].faces[f][point]][0],
                                   tmpb[self.ballset[ptr].faces[f][point]][1],
                                   tmpb[self.ballset[ptr].faces[f][point]][2])
            # self.gl.glTexCoord2f(1.0, 1.0)
            # self.gl.glVertex3f(tmpb[self.ballset[ptr].faces[f][1]][0],
            #                    tmpb[self.ballset[ptr].faces[f][1]][1],
            #                    tmpb[self.ballset[ptr].faces[f][1]][2])
            # self.gl.glTexCoord2f(0.0, 1.0)
            # self.gl.glVertex3f(tmpb[self.ballset[ptr].faces[f][2]][0],
            #                    tmpb[self.ballset[ptr].faces[f][2]][1],
            #                    tmpb[self.ballset[ptr].faces[f][2]][2])
            self.gl.glEnd()

    def addBall(self):
        # self.ballset.append(Ball(1, 0, 0, 0))

        time1 = time.time()  # 程序计时开始
        while True:
            time2 = time.time()  # 程序计时结束
            if time2 - time1 > 0.5:
                break
            phi = (random.random()/2+0.1)
            posx = random.random()*(2 - 2*phi)+phi-1
            posy = 1
            posz = random.random()*(2 - 2*phi)+phi-1
            ok = True
            for ball in self.ballset:
                if m.sqrt((ball.positionx-posx)**2 + (ball.positionz-posz)**2) < phi + ball.phi:
                    ok = False
            if ok == True:
                self.ballset.append(Ball(phi, posx, posy, posz))
                break

        self.update()

    def clearBall(self):
        self.ballset.clear()
        self.ctlpoints = np.array([[[-1, -1, -1],
                                    [-1, -1, -1/3],
                                    [-1, -1, 1/3],
                                    [-1, -1, 1]],
                                   [[-1/3, -1, -1],
                                    [-1/3, -1, -1/3],
                                    [-1/3, -1, 1/3],
                                    [-1/3, -1, 1]],
                                   [[1/3, -1, -1],
                                    [1/3, -1, -1/3],
                                    [1/3, -1, 1/3],
                                    [1/3, -1, 1]],
                                   [[1, -1, -1],
                                    [1, -1, -1/3],
                                    [1, -1, 1/3],
                                    [1, -1, 1]]], 'f')
        self.update()

    def paintrbq(self):
        glBegin(GL_LINES)                    # 开始绘制线段（世界坐标系）

        # 以红色绘制x轴
        glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
        glVertex3f(-1.0, 0.0, 0.0)           # 设置x轴顶点（x轴负方向）
        glVertex3f(2.0, 0.0, 0.0)            # 设置x轴顶点（x轴正方向）
        glVertex3f(-1.0, -1.0, 0.0)
        glVertex3f(-1.0, 1.0, 0.0)
        # 以绿色绘制y轴
        glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
        glVertex3f(0.0, 0.0, 0.0)           # 设置y轴顶点（y轴负方向）
        glVertex3f(0.0, 2.8, 0.0)            # 设置y轴顶点（y轴正方向）

        # 以蓝色绘制z轴
        glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
        glVertex3f(0.0, 0.0, 0.0)           # 设置z轴顶点（z轴负方向）
        glVertex3f(0.0, 0.0, 2.8)            # 设置z轴顶点（z轴正方向）

        glEnd()                              # 结束绘制线段
        glColor4f(1, 1, 1, 1)

    def paintLight(self):
        mat_ambient = [0.8, 0.8, 0.8, 1.0]
        mat_diffuse = [0.8, 0.8, 0.8, 1.0]
        mat_specular = [0.1, 0.1, 0.1, 1.0]
        mat_shininess = [50.0]

        # light_diffuse = [0.0, 1.0, 0.0, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        # light_position = [1.0, 1.0, 1.0, 0.0]
        light_position = [2.0, 1.0, 1.0, 0]

        self.gl.glMaterialfv(self.gl.GL_FRONT, self.gl.GL_AMBIENT, mat_ambient)
        self.gl.glMaterialfv(self.gl.GL_FRONT, self.gl.GL_DIFFUSE, mat_diffuse)
        self.gl.glMaterialfv(
            self.gl.GL_FRONT, self.gl.GL_SPECULAR, mat_specular)
        self.gl.glMaterialfv(
            self.gl.GL_FRONT, self.gl.GL_SHININESS, mat_shininess)

        self.gl.glLightfv(self.gl.GL_LIGHT0, self.gl.GL_DIFFUSE, light_diffuse)
        self.gl.glLightfv(self.gl.GL_LIGHT0,
                          self.gl.GL_POSITION, light_position)

        if self.lighted == -1:
            self.gl.glDisable(self.gl.GL_LIGHTING)
        else:
            self.gl.glEnable(self.gl.GL_LIGHTING)
            self.gl.glEnable(self.gl.GL_LIGHT0)
            self.gl.glDepthFunc(self.gl.GL_LESS)
            self.gl.glEnable(self.gl.GL_DEPTH_TEST)

    def loadPic1(self):
        image = Image.open("./src/1.jpeg")
        # image = Image.open("4.png")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width,
                     image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def loadPic2(self):
        image = Image.open("./src/3.jpeg")
        # image = Image.open("8.jpg")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width,
                     image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
