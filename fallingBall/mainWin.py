import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from Ui_untitled import *
import time
import math as m


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.setInterval(round(1/self.openGLWidget.fps*1000))
        self.timer.timeout.connect(self.move)
        self.timer.start()

    def clicked_detail(self):
        QMessageBox.about(self, '程序说明', '按键操作：如你所见，主界面上一共三个按钮。\n鼠标操作：拖动可以旋转角度，鼠标滚轮可以靠近、远离。\n键盘操作：按a键可切换是否透视。\n彩蛋：当屏幕上同时存在10个以上球的时候，会触发彩蛋。\n                            Li Jasiah')

    def clicked_addBall(self):
        if len(self.openGLWidget.ballset) > 10:
            QMessageBox.about(self, 'Warning！&&彩蛋', '球有点多，可能会卡\n请不要尝试挑战软件的性能\n球依旧会被添加，但我劝你善良\n            Li Jasiah')
        self.openGLWidget.addBall()
        self.openGLWidget.setFocus()

    def clicked_clear(self):
        self.openGLWidget.clearBall()
        self.openGLWidget.setFocus()

    def move(self):
        for ball in self.openGLWidget.ballset:
            ball.speedy += ball.a*(1/self.openGLWidget.fps)
            ball.positiony -= ball.speedy*(1/self.openGLWidget.fps)

            if ball.positiony + ball.phi >= -1 and ball.positiony - ball.phi <= -1 and ball.speedy > 0:
                ball.speedy *= -0.4
            elif ball.positiony + ball.phi <= -1:
                self.openGLWidget.ballset.remove(ball)
        self.openGLWidget.update()
                # if(ball.speedy <= 0):
                #     ball.speedy = 0
                # else:
                #     x = ball.positionx
                #     y = ball.positiony
                #     z = ball.positionz
                #     for i in range(4):
                #         for j in range(4):
                #             d = m.sqrt((x-self.openGLWidget.ctlpoints[i][j][0])**2 +
                #                        (y-self.openGLWidget.ctlpoints[i][j][1])**2 +
                #                        (z-self.openGLWidget.ctlpoints[i][j][2])**2)
                #             if d < ball.phi:
                #                 # for k in range(3):
                #                 self.openGLWidget.ctlpoints[i][j][0] = self.openGLWidget.ctlpoints[i][j][0]/d*ball.phi
                #                 self.openGLWidget.ctlpoints[i][j][1] = self.openGLWidget.ctlpoints[i][j][1]/d*ball.phi
                #                 self.openGLWidget.ctlpoints[i][j][2] = self.openGLWidget.ctlpoints[i][j][2]/d*ball.phi
                #                 print(self.openGLWidget.ctlpoints)

                #     a = -(2-ball.phi)*ball.a/ball.phi
                #     ball.speedy += a*(1/self.openGLWidget.fps)
                #     ball.positiony -= ball.speedy*(1/self.openGLWidget.fps)
                    # print(self.openGLWidget.ctlpoints)
            #     if ball.solid == False:
            #         ball.solid = True
            #         ball.speedy *= 0.3
            #     g = 0.09/2/ball.phi
            #     ball.speedy -= g*0.1
            #     ball.positiony -= ball.speedy*0.1
            # elif ball.positiony + ball.phi <= -1:
            #     self.openGLWidget.ballset.remove(ball)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.openGLWidget.setFocus()
    myshow.show()
    sys.exit(app.exec_())
