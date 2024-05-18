import time
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from Ball import *
import math as m


class MyGLWidget(QtWidgets.QOpenGLWidget):

    aBall = Ball()

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)

    def initializeGL(self):
        version_profile = QtGui.QOpenGLVersionProfile()
        version_profile.setVersion(2, 0)
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()

        # 设置背景色
        self.gl.glClearColor(0, 0, 0, 1.0)
        # 深度测试
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)

    def paintGL(self):
        thetax = (self.aBall.anglex+self.aBall.rollx)/180*m.pi
        thetay = (self.aBall.angley+self.aBall.rolly)/180*m.pi
        thetaz = (self.aBall.anglez+self.aBall.rollz)/180*m.pi

        t0to = [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [self.aBall.positionx, self.aBall.positiony, 0, 1]]
        t1 = [[self.aBall.phi, 0, 0, 0],
              [0, self.aBall.phi, 0, 0],
              [0, 0, self.aBall.phi, 0],
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

        tmpa = np.array(self.aBall.vertex)
        tmpb = np.append(tmpa, np.ones((np.shape(tmpa)[0], 1)), axis=1)
        tmpb = tmpb.dot(t1).dot(t2x).dot(t2y).dot(t2z).dot(t0to)
        tmpnormal1 = np.array(self.aBall.normal)
        tmpnormal2 = np.append(tmpnormal1, np.ones((np.shape(tmpnormal1)[0], 1)), axis=1)
        tmpnormal2 = tmpnormal2.dot(t2x).dot(t2y).dot(t2z)
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT |
                        self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glShadeModel(self.gl.GL_SMOOTH)

        mat_ambient = [0.8, 0.8, 0.8, 1.0]
        mat_diffuse = [0.8, 0.8, 0.8, 1.0]
        mat_specular = [0.1, 0.1, 0.1, 1.0]
        mat_shininess = [50.0]

        light_diffuse = [0.0, 1.0, 0.0, 1.0]
        light_position = [1.0, 1.0, 1.0, 0.0]

        self.gl.glMaterialfv(self.gl.GL_FRONT, self.gl.GL_AMBIENT, mat_ambient)
        self.gl.glMaterialfv(self.gl.GL_FRONT, self.gl.GL_DIFFUSE, mat_diffuse)
        self.gl.glMaterialfv(
            self.gl.GL_FRONT, self.gl.GL_SPECULAR, mat_specular)
        self.gl.glMaterialfv(
            self.gl.GL_FRONT, self.gl.GL_SHININESS, mat_shininess)

        self.gl.glLightfv(self.gl.GL_LIGHT0, self.gl.GL_DIFFUSE, light_diffuse)
        self.gl.glLightfv(self.gl.GL_LIGHT0,
                          self.gl.GL_POSITION, light_position)

        if self.aBall.lighted == -1:
            self.gl.glDisable(self.gl.GL_LIGHTING)
        else:
            self.gl.glEnable(self.gl.GL_LIGHTING)
            self.gl.glEnable(self.gl.GL_LIGHT0)
            self.gl.glDepthFunc(self.gl.GL_LESS)
            self.gl.glEnable(self.gl.GL_DEPTH_TEST)

        for f in range(len(self.aBall.faces)):
            self.gl.glBegin(self.gl.GL_LINE_LOOP)
            self.gl.glNormal3f(
                tmpnormal2[f][0], tmpnormal2[f][1], tmpnormal2[f][2])
            for i in range(3):
                self.gl.glVertex3f(np.array(tmpb[self.aBall.faces[f][i]][0]),
                                   np.array(tmpb[self.aBall.faces[f][i]][1]),
                                   np.array(tmpb[self.aBall.faces[f][i]][2]))
            self.gl.glEnd()

    def resizeGL(self, width, height):
        self.aBall.wdivh = width/height
        self.gl.glViewport(0, 0, width, height)

        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()

        if width <= height:
            self.aBall.wmod = False
            self.gl.glOrtho(-1, 1, -1*height/width,
                            1*height/width, -1, 1)
        else:
            self.aBall.wmod = True
            self.gl.glOrtho(-1*width/height, 1*width / height,
                            -1, 1, -1, 1)

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        self.gl.glLoadIdentity()
