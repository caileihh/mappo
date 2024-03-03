# coding=utf-8
# import ParticleTest
shellWidth = 7.5


class Particle:
    # def __init__(self):
    #     self.pointNum = 0
    #     self.portN = 0
    #     self.x = []
    #     self.yuanX = []
    #     self.y = []
    #     self.yuanY = []
    #     self.shellX = []
    #     self.shellY = []
    #     self.maxX = 0.0
    #     self.maxY = 0.0
    #     self.minX = 0.0
    #     self.minY = 0.0
    #     self.Area = 0.0
    #     self.Orient = "R0"
    #     self.name = ""
    #     self.ruleName = ""
    #     self.centerPoint = CenterPoint(self.getCenterX(), self.getCenterY())
    #     self.portsArrayList = []
    #     self.sumF = 0.0

    def clone(self):
        p = Particle(name=self.name, pointNum=self.pointNum, x=self.x, y=self.y, ruleName=self.ruleName)
        p.name = self.name
        p.ruleName = self.ruleName
        p.Orient = self.Orient
        p.pointNum = self.pointNum
        p.x = self.x.copy()
        p.yuanX = self.yuanX.copy()
        p.y = self.y.copy()
        p.yuanY = self.yuanY.copy()
        p.maxX = self.maxX
        p.maxY = self.maxY
        p.minX = self.minX
        p.minY = self.minY
        p.Area = self.Area
        p.shellX = self.shellX.copy()
        p.shellY = self.shellY.copy()
        for pp in self.portsArrayList:
            p.portsArrayList.append(pp.clone())
        p.sumF = self.sumF
        p.centerPoint = self.centerPoint.clone()
        return p

    def getArea(self):
        return (self.getMaxX() - self.getMinX()) * (self.getMaxY() - self.getMinY())

    def getCenterPoint(self):
        return self.centerPoint

    def getShellX(self, i):
        while i >= self.pointNum:
            i -= self.pointNum
        return self.shellX[i]

    def getShellY(self, i):
        while i >= self.pointNum:
            i -= self.pointNum
        return self.shellY[i]

    def GetW(self):
        return self.maxX - self.minX

    def GetH(self):
        return self.maxY - self.minY

    def GETSHELLX(self):
        return self.shellX

    def GETSHELLY(self):
        return self.shellY

    def GETX(self):
        return self.x

    def GETY(self):
        return self.y

    def getX(self, i):
        while i >= self.pointNum:
            i -= self.pointNum
        return self.x[i]

    def getY(self, i):
        while i >= self.pointNum:
            i -= self.pointNum
        return self.y[i]

    def getPointNum(self):
        return self.pointNum

    def setSumF(self, sumF):
        self.sumF = sumF

    def getSumF(self):
        return self.sumF

    def getTotalSumF(self):
        sum_value = 0.0
        for ports in self.portsArrayList:
            sum_value += ports.sumDis
        return sum_value

    def adjustAngle(self, angleFlag):
        if (angleFlag == 0):
            return
        x0 = self.getCenterX()
        y0 = self.getCenterY()
        if self.Orient == "R90":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = y1 + x0 - y0
                self.yuanY[i] = x0 - x1 + y0
        elif self.Orient == "R0":
            self.yuanX = self.x.copy()
            self.yuanY = self.y.copy()
        elif self.Orient == "R180":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 * 2 - x1
                self.yuanY[i] = y0 * 2 - y1
        elif self.Orient == "R270":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 + y0 - y1
                self.yuanY[i] = x1 + y0 - x0
        elif self.Orient == "MX":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 * 2 - x1
                self.yuanY[i] = y1
        elif self.Orient == "MY":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x1
                self.yuanY[i] = y0 * 2 - y1
        elif self.Orient == "MXR90":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = y1 + x0 - y0
                self.yuanY[i] = x1 + y0 - x0
                # self.yuanX[i] = x0 + y0 - y1
                # self.yuanY[i] = y0 + x0 - x1
        elif self.Orient == "MYR90":
            for i in range(self.pointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                # self.yuanX[i] = y1 + x0 - y0
                # self.yuanY[i] = x1 + y0 - x0
                self.yuanX[i] = x0 + y0 - y1
                self.yuanY[i] = y0 + x0 - x1

        yuanOrient = self.Orient
        if angleFlag == 0:
            self.x = self.yuanX.copy()
            self.y = self.yuanY.copy()
            self.resetBoundary()
            self.Orient = "R0"
        elif angleFlag == 1:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = y0 - y1 + x0
                self.shellX[i] = y0 - y1 + x0
                self.y[i] = x1 - x0 + y0
                self.shellY[i] = x1 - x0 + y0
            self.Orient = "R90"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum) #中心应该不会变化
        elif angleFlag == 2:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 - x1 + x0
                self.shellX[i] = x0 - x1 + x0
                self.y[i] = y0 - y1 + y0
                self.shellY[i] = y0 - y1 + y0
            self.Orient = "R180"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum)
        elif angleFlag == 3:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = y1 - y0 + x0
                self.shellX[i] = y1 - y0 + x0
                self.y[i] = x0 - x1 + y0
                self.shellY[i] = x0 - x1 + y0
            self.Orient = "R270"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum)
        elif angleFlag == 4:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 - x1 + x0
                self.shellX[i] = x0 - x1 + x0
                self.y[i] = y1 - y0 + y0
                self.shellY[i] = y1 - y0 + y0
            self.Orient = "MX"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum)
        elif angleFlag == 5:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x1 - x0 + x0
                self.shellX[i] = x1 - x0 + x0
                self.y[i] = y0 - y1 + y0
                self.shellY[i] = y0 - y1 + y0
            self.Orient = "MY"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum)
        elif angleFlag == 6:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 + y1 - y0
                self.shellX[i] = x0 + y1 - y0
                self.y[i] = y0 + x1 - x0
                self.shellY[i] = y0 + x1 - x0
                # self.x[i] = x0 + y0 - y1
                # self.shellX[i] = x0 + y0 - y1
                # self.y[i] = y0 + x0 - x1
                # self.shellY[i] = y0 + x0 - x1
            self.Orient = "MXR90"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum)
        elif angleFlag == 7:
            for i in range(self.pointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 + y0 - y1
                self.shellX[i] = x0 + y0 - y1
                self.y[i] = y0 + x0 - x1
                self.shellY[i] = y0 + x0 - x1
                # self.x[i] = x0 + y1 - y0
                # self.shellX[i] = x0 + y1 - y0
                # self.y[i] = y0 + x1 - x0
                # self.shellY[i] = y0 + x1 - x0
            self.Orient = "MYR90"
            # self.centerPoint = CenterPoint(centreX / self.pointNum, centreY / self.pointNum)
        self.resetBoundary()
        self.centerPoint = CenterPoint(self.getCenterX(), self.getCenterY())
        for ports in self.portsArrayList:
            ports.adjust_angle(self.centerPoint, angleFlag, yuanOrient)
        self.resetOutShell()

    def Move(self, x, y):
        centreX = 0
        centreY = 0
        for i in range(self.pointNum):
            self.x[i] += x
            self.yuanX[i] += x
            self.y[i] += y
            self.yuanY[i] += y
            self.shellX[i] += x
            self.shellY[i] += y

            centreX += self.x[i]
            centreY += self.y[i]

        self.maxX += x
        self.minX += x
        self.maxY += y
        self.minY += y

        self.centerPoint = CenterPoint(self.getCenterX(), self.getCenterY())
        for ports in self.portsArrayList:
            ports.move(x, y)

    def Move2(self, x, y):
        absX = x - self.getCenterX()
        absY = y - self.getCenterY()
        centreX = 0
        centreY = 0
        for i in range(self.pointNum):
            self.x[i] += absX
            self.yuanX[i] += absX
            self.y[i] += absY
            self.yuanY[i] += absY
            self.shellX[i] += absX
            self.shellY[i] += absY

            centreX += self.x[i]
            centreY += self.y[i]

        self.maxX += absX
        self.minX += absX
        self.maxY += absY
        self.minY += absY

        self.centerPoint = CenterPoint(self.getCenterX(), self.getCenterY())
        for ports in self.portsArrayList:
            ports.move(absX, absY)
        # resetOutShell()

    # def __init__(self, pointNum, portN, x, y, name, centerPoint, portsArrayList):
    #     self.pointNum = pointNum
    #     self.portN = portN
    #     self.x = x.copy()
    #     self.y = y.copy()
    #     self.name = name
    #     self.centerPoint = centerPoint
    #     self.portsArrayList = portsArrayList
    #
    #     self.resetBoundary()
    #     self.resetOutShell()

    def __init__(self, name, pointNum, x, y, ruleName):
        self.pointNum = 0
        self.portN = 0
        self.x = []
        self.yuanX = []
        self.y = []
        self.yuanY = []
        self.shellX = []
        self.shellY = []
        self.maxX = 0.0
        self.maxY = 0.0
        self.minX = 0.0
        self.minY = 0.0
        self.Area = 0.0
        self.Orient = "R0"
        self.name = ""
        self.ruleName = ""
        # self.centerPoint = CenterPoint(self.getCenterX(), self.getCenterY())
        self.portsArrayList = []
        self.sumF = 0.0

        self.x = x
        self.y = y
        self.yuanX = x.copy()
        self.yuanY = y.copy()
        self.name = name
        self.ruleName = ruleName
        self.pointNum = pointNum
        self.shellX = [0.0] * pointNum
        self.shellY = [0.0] * pointNum
        self.resetBoundary()
        self.centerPoint = CenterPoint(self.getCenterX(), self.getCenterY())
        self.resetOutShell()

    def resetBoundary(self):
        self.maxX = self.minX = self.x[0]
        self.maxY = self.minY = self.y[0]
        for i in range(self.pointNum):
            if self.maxX < self.x[i]:
                self.maxX = self.x[i]
            if self.minX > self.x[i]:
                self.minX = self.x[i]
            if self.maxY < self.y[i]:
                self.maxY = self.y[i]
            if self.minY > self.y[i]:
                self.minY = self.y[i]

    def resetOutShell(self):
        a = [0, 0, 0, 0]  # 顺时针4顶点，左上为0: 0 1 2 3
        for i in range(self.pointNum):
            if self.x[i] == self.maxX:
                if self.y[i] == self.maxY:
                    a[2] = 1
                elif self.y[i] == self.minY:
                    a[1] = 1
            elif self.x[i] == self.minX:
                if self.y[i] == self.minY:
                    a[0] = 1
                elif self.y[i] == self.maxY:
                    a[3] = 1

        if a[0] * a[1] * a[2] * a[3] == 0:
            for i in range(self.pointNum):
                if self.x[i] == self.maxX:
                    self.shellX[i] = self.x[i] + shellWidth
                    if self.y[i] == self.maxY:
                        self.shellY[i] = self.y[i] + shellWidth
                    elif self.y[i] == self.minY:
                        self.shellY[i] = self.y[i] - shellWidth
                    else:
                        if a[1] == 0:
                            self.shellY[i] = self.y[i] - shellWidth
                        elif a[2] == 0:
                            self.shellY[i] = self.y[i] + shellWidth
                elif self.x[i] == self.minX:
                    self.shellX[i] = self.x[i] - shellWidth
                    if self.y[i] == self.maxY:
                        self.shellY[i] = self.y[i] + shellWidth
                    elif self.y[i] == self.minY:
                        self.shellY[i] = self.y[i] - shellWidth
                    else:
                        if a[0] == 0:
                            self.shellY[i] = self.y[i] - shellWidth
                        elif a[3] == 0:
                            self.shellY[i] = self.y[i] + shellWidth
                else:
                    if self.y[i] == self.maxY:
                        self.shellY[i] = self.y[i] + shellWidth
                        if a[1] == 0 or a[2] == 0:
                            self.shellX[i] = self.x[i] + shellWidth
                        elif a[0] == 0 or a[3] == 0:
                            self.shellX[i] = self.x[i] - shellWidth
                    elif self.y[i] == self.minY:
                        self.shellY[i] = self.y[i] - shellWidth
                        if a[0] == 0 or a[3] == 0:
                            self.shellX[i] = self.x[i] - shellWidth
                        elif a[1] == 0 or a[2] == 0:
                            self.shellX[i] = self.x[i] + shellWidth
                    else:
                        if a[0] == 0:
                            self.shellX[i] = self.x[i] - shellWidth
                            self.shellY[i] = self.y[i] - shellWidth
                        elif a[1] == 0:
                            self.shellX[i] = self.x[i] + shellWidth
                            self.shellY[i] = self.y[i] - shellWidth
                        elif a[2] == 0:
                            self.shellX[i] = self.x[i] + shellWidth
                            self.shellY[i] = self.y[i] + shellWidth
                        else:
                            self.shellX[i] = self.x[i] - shellWidth
                            self.shellY[i] = self.y[i] + shellWidth
        else:
            for i in range(self.pointNum):
                if self.x[i] == self.maxX:
                    self.shellX[i] = self.x[i] + shellWidth
                    if self.y[i] == self.maxY:
                        self.shellY[i] = self.y[i] + shellWidth
                    else:
                        self.shellY[i] = self.y[i] - shellWidth
                elif self.x[i] == self.minX:
                    self.shellX[i] = self.x[i] - shellWidth
                    if self.y[i] == self.minY:
                        self.shellY[i] = self.y[i] - shellWidth
                    else:
                        self.shellY[i] = self.y[i] + shellWidth

    def getCenterX(self):
        return (self.maxX + self.minX) / 2

    def getCenterY(self):
        return (self.maxY + self.minY) / 2

    def getName(self):
        return self.name

    def getRuleName(self):
        return self.ruleName

    def getMaxX(self):
        return self.maxX

    def setMaxX(self, maxX):
        self.maxX = maxX

    def getMaxY(self):
        return self.maxY

    def setMaxY(self, maxY):
        self.maxY = maxY

    def getMinX(self):
        return self.minX

    def setMinX(self, minX):
        self.minX = minX

    def getMinY(self):
        return self.minY

    def setMinY(self, minY):
        self.minY = minY

    def getCost(self):
        return 0


class CenterPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        p = CenterPoint(self.x, self.y)
        return p

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y


class Ports:
    def __init__(self, portPointNum, x, y, ruleName):
        self.portPointNum = portPointNum
        self.ruleName = ruleName
        self.x = x
        self.y = y
        self.yuanX = x[:]
        self.yuanY = y[:]
        centreX = sum(x)
        centreY = sum(y)
        self.centerPoint = CenterPoint(centreX / portPointNum, centreY / portPointNum)
        self.sumDis = 0.0  # You need to initialize this appropriately

    def clone(self):
        p = Ports(self.portPointNum, self.x[:], self.y[:], self.ruleName)
        p.yuanX = self.yuanX[:]
        p.yuanY = self.yuanY[:]
        p.centerPoint = self.centerPoint.clone()
        p.sumDis = self.sumDis
        return p

    def get_rule_name(self):
        return self.ruleName

    def get_port_point_num(self):
        return self.portPointNum

    def get_x(self, i):
        while i >= self.portPointNum:
            i -= self.portPointNum
        return self.x[i]

    def get_y(self, i):
        while i >= self.portPointNum:
            i -= self.portPointNum
        return self.y[i]

    def adjust_angle(self, center, angle_flag, orient):
        x0 = center.getX()
        y0 = center.getY()

        if orient == "R90":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = y1 + x0 - y0
                self.yuanY[i] = x0 - x1 + y0
        elif orient == "R0":
            self.yuanX = self.x[:]
            self.yuanY = self.y[:]
        elif orient == "R180":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 * 2 - x1
                self.yuanY[i] = y0 * 2 - y1
        elif orient == "R270":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 + y0 - y1
                self.yuanY[i] = x1 + y0 - x0
        elif orient == "MX":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 * 2 - x1
                self.yuanY[i] = y1
        elif orient == "MY":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x1
                self.yuanY[i] = y0 * 2 - y1
        elif orient == "MXR90":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = y1 + x0 - y0
                self.yuanY[i] = x1 + y0 - x0
        elif orient == "MYR90":
            for i in range(self.portPointNum):
                x1 = self.x[i]
                y1 = self.y[i]
                self.yuanX[i] = x0 + y0 - y1
                self.yuanY[i] = y0 + x0 - x1
        centreX = 0
        centreY = 0
        if angle_flag == 0:
            self.x = self.yuanX[:]
            self.y = self.yuanY[:]
            centreX = sum(self.x)
            centreY = sum(self.y)
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 1:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = y0 - y1 + x0
                self.y[i] = x1 - x0 + y0
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 2:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 - x1 + x0
                self.y[i] = y0 - y1 + y0
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 3:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = y1 - y0 + x0
                self.y[i] = x0 - x1 + y0
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 4:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 - x1 + x0
                self.y[i] = y1 - y0 + y0
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 5:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x1 - x0 + x0
                self.y[i] = y0 - y1 + y0
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 6:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 + y1 - y0
                self.y[i] = y0 + x1 - x0
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)
        elif angle_flag == 7:
            for i in range(self.portPointNum):
                x1 = self.yuanX[i]
                y1 = self.yuanY[i]
                self.x[i] = x0 + y0 - y1
                self.y[i] = y0 + x0 - x1
                centreX += self.x[i]
                centreY += self.y[i]
            self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)

    def move(self, x, y):
        centreX = 0
        centreY = 0
        for i in range(self.portPointNum):
            self.x[i] += x
            self.y[i] += y

            centreX += self.x[i]
            centreY += self.y[i]
        self.centerPoint = CenterPoint(centreX / self.portPointNum, centreY / self.portPointNum)

    def get_sum_dis(self):
        return self.sumDis

    def set_sum_dis(self, sum_dis):
        self.sumDis = sum_dis

    def get_center_point(self):
        return self.centerPoint

    def get_center_x(self):
        return sum(self.x)

    def get_center_y(self):
        return sum(self.y)


class MyPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.angleFlag = 0  # 0 1 2 3: 0 90 180 270; 4 5 6 7: MX,MY,MXR90,MYR90

    def clone(self):
        p = MyPoint()
        p.x = self.x
        p.y = self.y
        p.angleFlag = self.angleFlag
        return p

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    # def getPointNum(self):
    #     return len(self.x)
