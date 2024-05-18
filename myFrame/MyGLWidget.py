from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from Diamond import *
import math as m


class MyGLWidget(QtWidgets.QOpenGLWidget):

    aDiamond = Diamond()

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
        self.gl.glLineWidth(2)
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT |
                        self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()

        self.gl.glBegin(self.gl.GL_LINE_LOOP)
        for i in range(self.aDiamond.n):
            self.gl.glVertex2f(self.aDiamond.r*m.cos(2*m.pi*i/self.aDiamond.n) + self.aDiamond.x,
                               self.aDiamond.r*m.sin(2*m.pi*i/self.aDiamond.n) + self.aDiamond.y)
        self.gl.glEnd()
        point = []
        for i in range(self.aDiamond.edges):
            point.append([self.aDiamond.r*m.cos((i/self.aDiamond.edges+self.aDiamond.startAngle/360)*2*m.pi) + self.aDiamond.x,
                          self.aDiamond.r*m.sin((i/self.aDiamond.edges+self.aDiamond.startAngle/360)*2*m.pi) + self.aDiamond.y])
        self.gl.glBegin(self.gl.GL_LINES)
        for i in range(self.aDiamond.edges):
            for j in range(i, self.aDiamond.edges):
                self.gl.glVertex2f(point[i][0], point[i][1])
                self.gl.glVertex2f(point[j][0], point[j][1])
        self.gl.glEnd()

    def resizeGL(self, width, height):

        side = min(width, height)
        if side < 0:
            return
