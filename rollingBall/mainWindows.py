import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from Ui_untitled import *
import time


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    def clicked_Start(self):
        self.timer = QTimer()
        self.timer.setInterval(int(1000*1/self.openGLWidget.aBall.fps))
        self.timer.timeout.connect(self.move)
        self.timer.start()

    def clicked_Stop(self):
        self.timer.stop()

    def clicked_Light(self):
        self.openGLWidget.aBall.lighted *= -1

    def slide_Ranks(self):
        iv = self.slider_ranks.value()
        self.openGLWidget.aBall.setRank(iv)
        self.showRanksLabel.setText(
            "当前有\n"+str(len(self.openGLWidget.aBall.faces))+"个面")
        self.openGLWidget.update()

    def slide_RollX(self):
        iv = self.slider_roll_x.value()
        self.openGLWidget.aBall.rollx = iv

    def slide_RollY(self):
        iv = self.slider_roll_y.value()
        self.openGLWidget.aBall.rolly = iv

    def slide_RollZ(self):
        iv = self.slider_roll_z.value()
        self.openGLWidget.aBall.rollz = iv

    def slide_Size(self):
        iv = self.slider_size.value()
        r = iv/100
        self.openGLWidget.aBall.setPhi(r)

    def slide_SpeedX(self):
        iv = self.slider_speed_x.value()
        sx = iv/1000
        if self.openGLWidget.aBall.speedx < 0:
            sign = -1
        else:
            sign = 1
        self.openGLWidget.aBall.setSpeedX(sign * sx)

    def slide_SpeedY(self):
        iv = self.slider_speed_y.value()
        sy = iv/1000
        if self.openGLWidget.aBall.speedy < 0:
            sign = -1
        else:
            sign = 1
        self.openGLWidget.aBall.setSpeedY(sign * sy)

    def move(self):
        self.openGLWidget.aBall.anglex = (
            self.openGLWidget.aBall.anglex+self.openGLWidget.aBall.rollx) % 360
        self.openGLWidget.aBall.angley = (
            self.openGLWidget.aBall.angley+self.openGLWidget.aBall.rolly) % 360
        self.openGLWidget.aBall.anglez = (
            self.openGLWidget.aBall.anglez+self.openGLWidget.aBall.rollz) % 360

        self.openGLWidget.aBall.positionx += self.openGLWidget.aBall.speedx
        self.openGLWidget.aBall.positiony += self.openGLWidget.aBall.speedy

        px = self.openGLWidget.aBall.positionx
        py = self.openGLWidget.aBall.positiony
        sx = self.openGLWidget.aBall.speedx
        sy = self.openGLWidget.aBall.speedy
        phi = self.openGLWidget.aBall.phi
        wdivh = self.openGLWidget.aBall.wdivh
        if self.openGLWidget.aBall.wmod == False:
            if (px + phi >= 1 and sx > 0) or (px - phi <= -1 and sx < 0):
                self.openGLWidget.aBall.speedx *= -1
            if (py*wdivh + phi*wdivh >= 1 and sy > 0) or (py*wdivh - phi*wdivh <= -1 and sy < 0):
                self.openGLWidget.aBall.speedy *= -1
        else:
            if (px/wdivh + phi/wdivh >= 1 and sx > 0) or (px/wdivh - phi/wdivh <= -1 and sx < 0):
                self.openGLWidget.aBall.speedx *= -1
            if (py + phi >= 1 and sy > 0) or (py - phi <= -1 and sy < 0):
                self.openGLWidget.aBall.speedy *= -1
        self.openGLWidget.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
