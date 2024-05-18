import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from Ui_untitled import *
import time


class mywindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)


    def clicked_Start(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.move)
        self.timer.start()

    def move(self):
        self.openGLWidget.aDiamond.addAngle(100)
        self.openGLWidget.aDiamond.x += self.openGLWidget.aDiamond.xSpeed
        self.openGLWidget.aDiamond.y += self.openGLWidget.aDiamond.ySpeed
        if (self.openGLWidget.aDiamond.x+self.openGLWidget.aDiamond.r >= 1 and self.openGLWidget.aDiamond.xSpeed > 0 ) or (self.openGLWidget.aDiamond.x-self.openGLWidget.aDiamond.r <= -1 and self.openGLWidget.aDiamond.xSpeed < 0):
            self.openGLWidget.aDiamond.xSpeed *= -1
        if (self.openGLWidget.aDiamond.y+self.openGLWidget.aDiamond.r >= 1 and self.openGLWidget.aDiamond.ySpeed > 0 ) or (self.openGLWidget.aDiamond.y-self.openGLWidget.aDiamond.r <= -1 and self.openGLWidget.aDiamond.ySpeed < 0):
            self.openGLWidget.aDiamond.ySpeed *= -1
        self.openGLWidget.update()

    def clicked_Stop(self):
        self.timer.stop()

    def draw(self):
        self.openGLWidget.paintGL()
        self.openGLWidget.grabFramebuffer()

    def slide_Edges(self):
        iv = self.sliderEdges.value()
        self.openGLWidget.aDiamond.setedge(iv)
        self.draw()

    def slide_SpeedX(self):
        iv = self.slider_speedx.value()
        sx = iv/1000
        if self.openGLWidget.aDiamond.xSpeed < 0:
            sign = -1
        else :
            sign = 1
        self.openGLWidget.aDiamond.setxSpeed(sign * sx)
        self.draw()

    def slide_SpeedY(self):
        iv = self.slider_speedy.value()
        sy = iv/1000
        if self.openGLWidget.aDiamond.ySpeed < 0:
            sign = -1
        else :
            sign = 1
        self.openGLWidget.aDiamond.setySpeed(sign * sy)
        self.draw()


    def slide_Size(self):
        iv = self.slider_size.value()
        r = iv/100
        self.openGLWidget.aDiamond.setr(r)
        self.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
