import math as m
import numpy as np


class Ball:
    a = 1
    phi = 0.4
    rank = 0
    speedx = 0
    speedy = 0
    rollx = 0
    rolly = 0
    rollz = 0
    positionx = 0
    positiony = 0
    positionz = 0
    anglex = 0
    angley = 0
    anglez = 0
    vertex = []
    faces = []
    normal = []
    solid = False


    def setPhi(self, phi):
        self.phi = phi

    def setRank(self, rank):
        self.rank = rank
        self.vertex, self.faces = self.findball()
        self.findnormal()

    def setSpeedX(self, speedx):
        self.speedx = speedx

    def setSpeedY(self, speedy):
        self.speedy = speedy

    def setRollX(self, rollx):
        self.rollx = rollx

    def setRollY(self, rolly):
        self.rolly = rolly

    def setRollZ(self, rollz):
        self.rollz = rollz

    def setPositionX(self, positionx):
        self.positionx = positionx

    def setPositionY(self, positiony):
        self.positiony = positiony

    def setPositionZ(self, positionz):
        self.positionz = positionz

    def setAngleX(self, anglex):
        self.anglex = anglex

    def setAngleY(self, angley):
        self.angley = angley

    def setAngleZ(self, anglez):
        self.anglez = anglez

    def __init__(self, phi=0.5, posx=0.0, posy=0.0, posz=0.0, rank=2):
        self.setPositionX(posx)
        self.setPositionY(posy)
        self.setPositionZ(posz)
        self.setRank(rank)
        self.setPhi(phi)

    def findball(self, nowrank=-1, vertex=[], faces=[]):
        r = 1
        nowvertex = len(vertex)
        if nowrank == -1:
            X = 0.525731112119133606
            Z = 0.850650808352039932
            vertex = ([[-X, 0.0, Z], [X, 0.0, Z], [-X, 0.0, -Z], [X, 0.0, -Z],
                       [0.0, Z, X], [0.0, Z, -X], [0.0, -Z, X], [0.0, -Z, -X],
                       [Z, X, 0.0], [-Z, X, 0.0], [Z, -X, 0.0], [-Z, -X, 0.0]])
            faces = ([[0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8], [4, 8, 1],
                      [8, 10, 1], [8, 3, 10], [5, 3, 8], [5, 2, 3], [2, 7, 3],
                      [7, 10, 3], [7, 6, 10], [7, 11, 6], [11, 0, 6], [0, 1, 6],
                      [6, 1, 10], [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]])
        else:
            newfaces = []
            for i in faces:
                for j in range(3):
                    for k in range(j+1, 3):
                        newP = np.array(
                            (np.array(vertex[i[j]]) + np.array(vertex[i[k]])) / 2)
                        newP /= np.linalg.norm(newP)
                        newP *= r
                        vertex.append(newP)
                        nowvertex += 1
                newfaces.extend([[i[0], nowvertex-3, nowvertex-2],
                                 [i[1], nowvertex-1, nowvertex-3],
                                 [i[2], nowvertex-2, nowvertex-1],
                                 [nowvertex-1, nowvertex-2, nowvertex-3]])

            faces = newfaces
        nowrank += 1
        if nowrank != self.rank:
            return self.findball(nowrank, vertex, faces)
        else:
            return vertex, faces

    def findnormal(self):
        self.normal = []
        for f in self.faces:
            v12 = []
            v23 = []
            for i in range(3):
                v12.append(self.vertex[f[1]][i] - self.vertex[f[0]][i])
                v23.append(self.vertex[f[2]][i] - self.vertex[f[1]][i])
            normalv = []

            normalv.append(v12[1]*v23[2] - v12[2]*v23[1])
            normalv.append(-(v12[0]*v23[2] - v12[2]*v23[0]))
            normalv.append(v12[0]*v23[1] - v12[1]*v23[0])
            normalv = np.array(normalv)
            normalv /= np.linalg.norm(normalv)
            normalv *= -1
            self.normal.append(normalv)
