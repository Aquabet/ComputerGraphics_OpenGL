class Diamond():
    n = 80
    edges = 20
    r = 0.8
    fps = 10
    x = 0
    y = 0
    xSpeed = 0.1
    ySpeed = 0.1
    startAngle = 0


    def setedge(self, value):
        self.edges = value

    def setxSpeed(self, value):
        self.xSpeed = value

    def setySpeed(self, value):
        self.ySpeed = value

    def setn(self, value):
        self.n = value

    def setr(self, value):
        self.r = value

    def setfps(self, value):
        self.fps = value

    def setx(self, value):
        self.x = value

    def sety(self, value):
        self.y = value

    def addAngle(self, angle):
        self.startAngle = (self.startAngle+angle) % 360