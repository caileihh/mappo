# coding=utf-8
# import copy
import copy
import math
import re
from random import Random
from shapely.geometry import Polygon
from Particle1 import Particle, Ports, MyPoint
# import example

global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
global allSumUp, bestSumOverlap, allSum, shellWidth
global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName, ModuleLinkSet


def initialize():
    global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
    global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
    global allSumUp, bestSumOverlap, allSum, shellWidth
    global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
    global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName, ModuleLinkSet
    AreaBoundary = []
    ModuleNum = 50
    fileNumber = "16-12004"
    p = []
    v = []
    pBest = []
    allBest = []
    bestF = float('inf')
    bestOverlap = float('inf')
    eps = 1e-6
    MaxStepLength = 2000
    MinStepLength = 200
    allSumUp = float('inf')
    bestSumOverlap = float('inf')
    allSum = float('inf')
    shellWidth = 7.5
    AreaMaxX = -10000
    AreaMinX = 10000
    AreaMaxY = -10000
    AreaMinY = 10000
    random = Random()
    c1 = 3
    c2 = 1.2
    disRate = 0.01
    overlapRate = 1000
    maxScore = -1
    AreaUtiRate = 0
    LinkSET = []
    ModuleLinkSet = []
    MName = []


def qlearning(maxN):
    global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
    global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
    global allSumUp, bestSumOverlap, allSum, shellWidth
    global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
    global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName
    epsilon = 0
    sumM = 0
    cou = 1
    # randArr = randomCommon(ModuleNum, ModuleNum)
    while maxN > 0:
        maxN -= 1
        for i in range(ModuleNum):
            p[i].Move2(400, 400)
        for j in range(200):
            print(j)
            randArr = randomCommon(ModuleNum, ModuleNum)

            # if j == 100:
            #     shellWidth = 17.5
            #     for i in range(ModuleNum):
            #         p[i].resetOutShell()

            for i in randArr:  # 可改为随机扰动
                isInclined = [False] * 12
                StepLength = MinStepLength * random.random()
                if random.random() < epsilon and j < 30:
                    tempStep = getRandomNumberInRange(0, 11)
                    if 1 <= tempStep <= 4:
                        if random.random() < 0.5:
                            if tempStep == 4:
                                p[i].Move(StepLength, 0)
                            elif tempStep == 3:
                                p[i].Move(-StepLength, 0)
                            elif tempStep == 2:
                                p[i].Move(0, -StepLength)
                            else:
                                p[i].Move(0, StepLength)
                        else:
                            isInclined[tempStep] = True
                            if tempStep == 4:
                                p[i].Move(StepLength, StepLength)
                            elif tempStep == 3:
                                p[i].Move(-StepLength, StepLength)
                            elif tempStep == 2:
                                p[i].Move(-StepLength, -StepLength)
                            else:
                                p[i].Move(StepLength, -StepLength)
                    elif tempStep >= 5:
                        p[i].adjustAngle(tempStep - 4)

                    judgeOutOfBounds(p[i])
                else:
                    bestStep = 0
                    tempSum = float("inf")
                    bestStepLength = StepLength
                    for tempStep in range(12):
                        if j < 300:
                            StepLength = MinStepLength * random.random()
                        else:
                            StepLength = MaxStepLength * random.random()
                        tempParticle = p[i].clone()
                        if 1 <= tempStep <= 4:
                            if random.random() < 0.5:
                                if tempStep == 4:
                                    tempParticle.Move(StepLength, 0)
                                elif tempStep == 3:
                                    tempParticle.Move(-StepLength, 0)
                                elif tempStep == 2:
                                    tempParticle.Move(0, -StepLength)
                                else:
                                    tempParticle.Move(0, StepLength)
                            else:
                                isInclined[tempStep] = True
                                if tempStep == 4:
                                    tempParticle.Move(StepLength, StepLength)
                                elif tempStep == 3:
                                    tempParticle.Move(-StepLength, StepLength)
                                elif tempStep == 2:
                                    tempParticle.Move(-StepLength, -StepLength)
                                else:
                                    tempParticle.Move(StepLength, -StepLength)
                        elif tempStep >= 5:
                            tempParticle.adjustAngle(tempStep - 4)
                        else:
                            tempParticle.adjustAngle(0)

                        judgeOutOfBounds(tempParticle)

                        tempOverlap = 0
                        tempDis = 0
                        AreaOverlap = 0
                        AreaUtlization = 0

                        tempmaxx = -1e10
                        tempmaxy = -1e10
                        tempminx = 1e10
                        tempminy = 1e10
                        for k in range(ModuleNum):
                            if k != i:
                                tempmaxx = max(tempmaxx, p[k].getMaxX())
                                tempmaxy = max(tempmaxy, p[k].getMaxY())
                                tempminx = min(tempminx, p[k].getMinX())
                                tempminy = min(tempminy, p[k].getMinY())
                            else:
                                tempmaxx = max(tempmaxx, tempParticle.getMaxX())
                                tempmaxy = max(tempmaxy, tempParticle.getMaxY())
                                tempminx = min(tempminx, tempParticle.getMinX())
                                tempminy = min(tempminy, tempParticle.getMinY())
                        AreaUtlization = (tempmaxx - tempminx) * (tempmaxy - tempminy)

                        for k in range(ModuleNum):
                            if k == i:
                                continue
                            tempOverlap += calOverlap(tempParticle, p[k])
                        for ports in LinkSET:  # LinkSet可优化，不必每次读取
                            for tempJ in range(len(ports)):
                                if ports[tempJ] in p[i].portsArrayList:
                                    for tempI in range(len(ports)):
                                        if tempI == tempJ:
                                            continue
                                        tempDis += getDist(tempParticle.portsArrayList[p[i].portsArrayList.index(
                                            ports[tempJ])].get_center_point(), ports[tempI].get_center_point())

                        # AreaOverlap = calOverlap3(tempParticle)
                        if tempDis * disRate + tempOverlap * overlapRate - AreaOverlap * overlapRate + AreaUtlization * AreaUtiRate < tempSum:
                            bestStep = tempStep
                            tempSum = tempDis * disRate + tempOverlap * overlapRate - AreaOverlap * overlapRate + AreaUtlization * AreaUtiRate
                            bestStepLength = StepLength
                            # print(tempSum)
                            # print("dis", tempDis)
                            # print('over', tempOverlap)

                    if 1 <= bestStep <= 4:
                        if not isInclined[bestStep]:
                            if bestStep == 4:
                                p[i].Move(bestStepLength, 0)
                            elif bestStep == 3:
                                p[i].Move(-bestStepLength, 0)
                            elif bestStep == 2:
                                p[i].Move(0, -bestStepLength)
                            else:
                                p[i].Move(0, bestStepLength)
                        else:
                            if bestStep == 4:
                                p[i].Move(bestStepLength, bestStepLength)
                            elif bestStep == 3:
                                p[i].Move(-bestStepLength, bestStepLength)
                            elif bestStep == 2:
                                p[i].Move(-bestStepLength, -bestStepLength)
                            else:
                                p[i].Move(bestStepLength, -bestStepLength)
                    else:
                        if bestStep >= 5:
                            p[i].adjustAngle(bestStep - 4)
                        else:
                            p[i].adjustAngle(0)

                    judgeOutOfBounds(p[i])
        for j in range(0):
            print(j)
            randArr = randomCommon(ModuleNum, ModuleNum)
            for i in randArr:
                bestStep = 0
                bestAngle = 0
                StepLength = MinStepLength * 2 / 3 * random.random()
                bestStepLength = StepLength
                # if j <= 50:
                StepLength = MaxStepLength * 2 / 3 * random.random()
                # else:
                #     StepLength = 300 * random.random()

                if random.random() < epsilon:
                    tempStep = getRandomNumberInRange(0, 11)
                    if 1 <= tempStep <= 4:
                        if tempStep == 4:
                            p[i].Move(StepLength, 0)
                        elif tempStep == 3:
                            p[i].Move(-StepLength, 0)
                        elif tempStep == 2:
                            p[i].Move(0, -StepLength)
                        else:
                            p[i].Move(0, StepLength)
                    elif tempStep >= 5:
                        p[i].adjustAngle(tempStep - 4)

                    judgeOutOfBounds(p[i])
                else:
                    tempSum = float("inf")

                    for tempStep in range(12):
                        for angle in range(8):
                            # if j <= 50:
                            StepLength = 300 * random.random()
                            # else:
                            #     StepLength = 700 * random.random()

                            tempParticle = p[i].clone()

                            if 1 <= tempStep:
                                if tempStep == 4:
                                    tempParticle.Move(StepLength, StepLength)
                                elif tempStep == 3:
                                    tempParticle.Move(-StepLength, StepLength)
                                elif tempStep == 2:
                                    tempParticle.Move(-StepLength, -StepLength)
                                else:
                                    tempParticle.Move(StepLength, -StepLength)
                                judgeOutOfBounds(tempParticle)

                            tempParticle.adjustAngle(angle)
                            judgeOutOfBounds(tempParticle)

                            tempOverlap = 0
                            tempDis = 0
                            AreaOverlap = 0
                            AreaUtlization = 0

                            tempmaxx = -1e10
                            tempmaxy = -1e10
                            tempminx = 1e10
                            tempminy = 1e10

                            for k in range(ModuleNum):
                                if k != i:
                                    tempmaxx = max(tempmaxx, p[k].getMaxX())
                                    tempmaxy = max(tempmaxy, p[k].getMaxY())
                                    tempminx = min(tempminx, p[k].getMinX())
                                    tempminy = min(tempminy, p[k].getMinY())
                                else:
                                    tempmaxx = max(tempmaxx, tempParticle.getMaxX())
                                    tempmaxy = max(tempmaxy, tempParticle.getMaxY())
                                    tempminx = min(tempminx, tempParticle.getMinX())
                                    tempminy = min(tempminy, tempParticle.getMinY())

                            AreaUtlization = (tempmaxx - tempminx) * (tempmaxy - tempminy)

                            for k in range(ModuleNum):
                                if k == i:
                                    continue
                                tempOverlap += calOverlap(tempParticle, p[k])

                            for ports in LinkSET:
                                for tempJ in range(len(ports)):
                                    if ports[tempJ] in p[i].portsArrayList:
                                        for tempI in range(len(ports)):
                                            if tempI == tempJ:
                                                continue
                                            tempDis += getDist(tempParticle.portsArrayList[p[i].portsArrayList.index(
                                                ports[tempJ])].get_center_point(), ports[tempI].get_center_point())

                            AreaOverlap = calOverlap3(tempParticle)
                            for k in range(ModuleNum):
                                if k == i:
                                    continue
                                tempDis += getDist(tempParticle.getCenterPoint(), p[k].getCenterPoint())

                            if tempDis * disRate + tempOverlap * overlapRate - AreaOverlap * overlapRate + AreaUtlization * AreaUtiRate < tempSum:
                                bestStep = tempStep
                                bestAngle = angle
                                tempSum = tempDis * disRate + tempOverlap * overlapRate - AreaOverlap * overlapRate + AreaUtlization * AreaUtiRate
                                bestStepLength = StepLength

                    if 1 <= bestStep:
                        if bestStep == 4:
                            p[i].Move(bestStepLength, bestStepLength)
                        elif bestStep == 3:
                            p[i].Move(-bestStepLength, bestStepLength)
                        elif bestStep == 2:
                            p[i].Move(-bestStepLength, -bestStepLength)
                        else:
                            p[i].Move(bestStepLength, -bestStepLength)
                        judgeOutOfBounds(p[i])

                    p[i].adjustAngle(bestAngle)
                    judgeOutOfBounds(p[i])

        for ports in LinkSET:
            for j in range(len(ports)):
                ports[j].set_sum_dis(0)
                for k in range(len(ports)):
                    if k == j:
                        continue
                    ports[j].sumDis += getDist(ports[j].get_center_point(), ports[k].get_center_point())

        tempOverlap = 0
        tempDis = 0
        AreaOverlap = 0
        AreaUtlization = 0

        tempmaxx = -1e10
        tempmaxy = -1e10
        tempminx = 1e10
        tempminy = 1e10
        for k in range(ModuleNum):
            tempmaxx = max(tempmaxx, p[k].getMaxX())
            tempmaxy = max(tempmaxy, p[k].getMaxY())
            tempminx = min(tempminx, p[k].getMinX())
            tempminy = min(tempminy, p[k].getMinY())
        AreaUtlization = (tempmaxx - tempminx) * (tempmaxy - tempminy)

        for k in range(ModuleNum - 1):
            for i in range(k + 1, ModuleNum):
                tempOverlap += calOverlap2(p[i], p[k])

        for i in range(ModuleNum):
            for ports in LinkSET:
                for tempJ in range(len(ports)):
                    if ports[tempJ] in p[i].portsArrayList:
                        for tempI in range(len(ports)):
                            if tempI == tempJ:
                                continue
                            tempDis += getDist(
                                p[i].portsArrayList[p[i].portsArrayList.index(ports[tempJ])].get_center_point(),
                                ports[tempI].get_center_point())

        fitnessFunction()
        tempSum = 0
        for j in range(ModuleNum):  # 更新个体最优
            # if p[j].getSumF() < pBest[j].getSumF():
            #     try:
            #         pBest[j] = p[j].clone()
            #     except CloneNotSupportedException as e:
            #         print(e)
            # judgeOutOfBounds(p[j])
            tempSum += p[j].getSumF()

        # double tempOverlap = 0;

        for k in range(ModuleNum):
            for j in range(ModuleNum):
                if j != k:
                    tempOverlap += calOverlap2(p[k], p[j])

        if tempOverlap != 0:
            maxN += 1
            print("Place " + str(cou) + " times")
            continue

        if bestF > tempSum * disRate + tempOverlap * overlapRate:
            bestF = tempSum * disRate + tempOverlap * overlapRate
            bestOverlap = tempOverlap

        sumM = tempDis * disRate + tempOverlap * overlapRate - AreaOverlap * overlapRate + AreaUtlization * AreaUtiRate

    return sumM


def read_file(filepath):
    list_data = []
    try:
        encoding = "UTF-8"
        with open(filepath, 'r', encoding=encoding) as file:
            list_data = file.readlines()
    except IOError:
        print("Can't find file!")
    return list_data


def getRandomNumberInRange(min_val, max_val):
    if min_val >= max_val:
        raise ValueError("max must be greater than min")

    return random.randint(min_val, max_val)


def Init():
    global LinkSET, bestSumOverlap, pBest, allBest, bestF
    for i in range(ModuleNum):
        v[i] = MyPoint(random.random() * 10, random.random() * 10)

    for ports in LinkSET:
        for j in range(len(ports)):
            for k in range(len(ports)):
                if k == j:
                    continue
                ports[j].sumDis += getDist(ports[j].get_center_point(), ports[k].get_center_point())

    fitnessFunction()

    for i in range(ModuleNum):
        for j in range(ModuleNum):
            if j == i:
                continue
            bestSumOverlap += calOverlap(p[i], p[j])

    for i in range(ModuleNum):
        pBest[i] = p[i].clone()
        allBest[i] = p[i].clone()

    bestF = allSumUp * disRate + bestSumOverlap * overlapRate


def fitnessFunction():
    global allSumUp
    global p
    tempSumOverlap = 0
    for i in range(ModuleNum):
        x = p[i].getSumF()
        p[i].setSumF(x)
        allSumUp += x


def getDist(p1, p2):
    return math.hypot(p1.getX() - p2.getX(), p1.getY() - p2.getY())


def read_and_init(filepath):
    try:
        list_data = read_file(filepath)
        if not list_data:
            return

        num = sum(1 for s in list_data if re.match(r"Module:(.*)", s))
        print(num)
        global ModuleNum
        ModuleNum = num

        global p, v, pBest, allBest, AreaBoundary
        global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY
        p = [None] * ModuleNum
        v = [None] * ModuleNum
        pBest = [None] * ModuleNum
        allBest = [None] * ModuleNum
        i = 0
        while i < (len(list_data)):

            temp = list_data[i].strip()
            if re.match(r"Area:(.*)", temp):
                # area_parts = re.findall(r"\((-?\d+\.\d+), (-?\d+\.\d+)\)", temp)
                area_parts = re.findall(r"\((-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)\)", temp)
                AreaBoundary = [MyPoint(float(x), float(y)) for x, y in area_parts]

                AreaMaxX = max(p.x for p in AreaBoundary)
                AreaMinX = min(p.x for p in AreaBoundary)
                AreaMaxY = max(p.y for p in AreaBoundary)
                AreaMinY = min(p.y for p in AreaBoundary)
                i += 1

            elif re.match(r"Module:(.*)", temp):
                moduleNUm = re.findall(r":M(\d+)", temp)
                # ModuleX, strName, ruleNa = map(str.strip, part)
                ModuleX = int(moduleNUm[0])
                strName = 'M' + moduleNUm[0]
                MName.append(strName)
                i += 1
                temp = list_data[i]
                boundary_parts = re.findall(r"\((-?\d+\.\d+), (-?\d+\.\d+)\)", temp)
                x, y = zip(*boundary_parts)
                x = [float(val) for val in x]
                y = [float(val) for val in y]
                ruleNa = re.split(';', temp.strip())
                temp_particle = Particle(strName, len(x), x, y, ruleNa[1])
                p[ModuleX - 1] = temp_particle

                i += 1
                if i < len(list_data):
                    while re.match(r"Port:", list_data[i]):
                        temp = list_data[i]
                        port_parts = re.findall(r"\((-?\d+\.\d+), (-?\d+\.\d+)\)", temp)
                        x, y = zip(*port_parts)
                        x = [float(val) for val in x]
                        y = [float(val) for val in y]
                        ruleNa = re.split(';', temp.strip())
                        temp_port = Ports(len(x), x, y, ruleNa[1])
                        p[ModuleX - 1].portsArrayList.append(temp_port)
                        i += 1
                        if i == len(list_data):
                            break
            else:
                i += 1
            # i += 1
    except ValueError:
        import traceback
        traceback.print_exc()


def ReadConnectFile(filepath):
    global p
    global LinkSET
    list = read_file(filepath)
    if not list:
        return
    LinkSET.clear()
    line = 0
    while line < len(list):
        temp = list[line]
        if "Link" in temp:
            line += 1
            ModuleList = list[line].split(" ")
            line += 1
            PortList = list[line].split(" ")
            linkArr = []
            ModuleArr = []
            for i in range(len(ModuleList)):
                ModuleN = int(ModuleList[i][ModuleList[i].index("M") + 1:].strip())
                PortN = int(PortList[i].strip())
                linkArr.append(p[ModuleN - 1].portsArrayList[PortN - 1])
                ModuleArr.append(ModuleN - 1)
            LinkSET.append(linkArr)
            ModuleLinkSet.append(ModuleArr)
            print(len(LinkSET))
        line += 1


def ReadConnectFile2(filepath, particle):
    # global p
    LinkSET = []
    list = read_file(filepath)
    if not list:
        return
    LinkSET.clear()
    line = 0
    while line < len(list):
        temp = list[line]
        if "Link" in temp:
            line += 1
            ModuleList = list[line].split(" ")
            line += 1
            PortList = list[line].split(" ")
            linkArr = []
            ModuleArr = []
            for i in range(len(ModuleList)):
                ModuleN = int(ModuleList[i][ModuleList[i].index("M") + 1:].strip())
                PortN = int(PortList[i].strip())
                linkArr.append(particle[ModuleN - 1].portsArrayList[PortN - 1])
                ModuleArr.append(ModuleN - 1)
            LinkSET.append(linkArr)
            ModuleLinkSet.append(ModuleArr)
            print(len(LinkSET))
        line += 1
    return LinkSET


def judgeOutOfBounds(par):
    vx, vy = 0, 0  # 出界判断
    if par.getMaxX() > AreaMaxX - shellWidth:
        vx = AreaMaxX - par.getMaxX() - shellWidth
    elif par.getMinX() < AreaMinX + shellWidth:
        vx = AreaMinX - par.getMinX() + shellWidth
    if par.getMaxY() > AreaMaxY - shellWidth:
        vy = AreaMaxY - par.getMaxY() - shellWidth
    elif par.getMinY() < AreaMinY + shellWidth:
        vy = AreaMinY - par.getMinY() + shellWidth
    par.Move(vx, vy)


def randomCommon(max_val, n):
    if max_val < 0 or n <= 0:
        return [0]  # Returning a single element list with 0
    result = []
    flag = [0] * n
    for i in range(n):
        x = random.randint(0, n - 1)
        while flag[x] == 1:
            x = random.randint(0, n - 1)
        result.append(x)
        flag[x] = 1
    return result


def dcmp(x):
    global eps
    if x > eps:
        return 1
    return -1 if x < -eps else 0


def cross(a, b, c):
    return (a.x - c.x) * (b.y - c.y) - (b.x - c.x) * (a.y - c.y)


def intersection(a, b, c, d):
    p = MyPoint(a.x, a.y)
    t = float(((a.x - c.x) * (c.y - d.y) - (a.y - c.y) * (c.x - d.x)) / (
            (a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)))
    p.x += (b.x - a.x) * t
    p.y += (b.y - a.y) * t
    return p


def PolygonArea(p, n):
    if n < 3:
        return 0.0
    s = float(p[0].y * (p[n - 1].x - p[1].x))
    for i in range(1, n - 1):
        s += p[i].y * (p[i - 1].x - p[i + 1].x)
    s += p[n - 1].y * (p[n - 2].x - p[0].x)
    return abs(s * 0.5)


tmp = [MyPoint() for _ in range(20)]
poly = [MyPoint() for _ in range(20)]


def CPIA(a, b, na, nb):
    # p = b.copy()
    # ploy = [MyPoint(b[i].x, b[i].y) for i in range(len(b))]
    for i in range(len(b)):
        poly[i].x = b[i].x
        poly[i].y = b[i].y
    # p = copy.deepcopy(b)
    if nb < 3:
        return 0.0
    else:
        tn, sflag, eflag = 0, 0, 0
        for i in range(na):
            if i == na - 1:
                sflag = dcmp(cross(a[0], poly[0], a[i]))
            else:
                sflag = dcmp(cross(a[i + 1], poly[0], a[i]))

            tn = 0
            for j in range(nb):

                if sflag >= 0:
                    tmp[tn] = MyPoint(poly[j].x, poly[j].y)
                    tn += 1

                if i == na - 1:
                    if j == nb - 1:
                        eflag = dcmp(cross(a[0], poly[0], a[i]))
                    else:
                        eflag = dcmp(cross(a[0], poly[j + 1], a[i]))
                else:
                    if j == nb - 1:
                        eflag = dcmp(cross(a[i + 1], poly[0], a[i]))
                    else:
                        eflag = dcmp(cross(a[i + 1], poly[j + 1], a[i]))

                if (sflag ^ eflag) == -2:
                    if i == na - 1:
                        if j == nb - 1:
                            tmp[tn] = intersection(a[i], a[0], poly[j], poly[0])
                        else:
                            tmp[tn] = intersection(a[i], a[0], poly[j], poly[j + 1])
                    else:
                        if j == nb - 1:
                            tmp[tn] = intersection(a[i], a[i + 1], poly[j], poly[0])
                        else:
                            tmp[tn] = intersection(a[i], a[i + 1], poly[j], poly[j + 1])
                    tn += 1
                sflag = eflag
            # p = copy.deepcopy(tmp)
            # p = [MyPoint(tmp[i].x, tmp[i].y) for i in range(len(tmp))]
            for i in range(len(tmp)):
                if i < len(poly):
                    poly[i].x = tmp[i].x
                    poly[i].y = tmp[i].y
                else:
                    poly.append(tmp[i])
            nb = tn
            poly[nb] = MyPoint(poly[0].x, poly[0].y)

    return PolygonArea(poly, nb)


def SPIA(a, b, na, nb):
    t1 = [MyPoint() for _ in range(na)]
    t2 = [MyPoint() for _ in range(nb)]
    res = 0.0

    t1[0] = MyPoint(a[0].x, a[0].y)
    # print(b)
    t2[0] = MyPoint(b[0].x, b[0].y)

    for i in range(2, na):
        t1[1] = MyPoint(a[i - 1].x, a[i - 1].y)
        t1[2] = MyPoint(a[i].x, a[i].y)

        num1 = dcmp(cross(t1[1], t1[2], t1[0]))

        if num1 < 0:
            t1[1], t1[2] = t1[2], t1[1]

        for j in range(2, nb):
            t2[1] = MyPoint(b[j - 1].x, b[j - 1].y)
            t2[2] = MyPoint(b[j].x, b[j].y)

            num2 = dcmp(cross(t2[1], t2[2], t2[0]))

            if num2 < 0:
                t2[1], t2[2] = t2[2], t2[1]
            res += CPIA(t1, t2, 3, 3) * num1 * num2

    return res


def calOverlap(p1, p2):
    # my_point1 = [MyPoint(p1.getShellX(i), p1.getShellY(i)) for i in range(p1.getPointNum())]
    # my_point2 = [MyPoint(p2.getShellX(i), p2.getShellY(i)) for i in range(p2.getPointNum())]
    # return abs(SPIA(my_point1, my_point2, len(my_point1), len(my_point2)))
    poly1 = Polygon((p1.getShellX(i), p1.getShellY(i)) for i in range(p1.getPointNum()))
    poly2 = Polygon((p2.getShellX(i), p2.getShellY(i)) for i in range(p2.getPointNum()))
    return Overlap(poly1, poly2)
    # return abs(example.calcularOverlap(p1.GETSHELLX(), p1.GETSHELLY(), p2.GETSHELLX(), p2.GETSHELLY(), p1.getPointNum(),
    #                                p2.getPointNum()))


def calOverlap2(p1, p2):
    # my_point1 = [MyPoint(p1.getX(i), p1.getY(i)) for i in range(p1.getPointNum())]
    # my_point2 = [MyPoint(p2.getX(i), p2.getY(i)) for i in range(p2.getPointNum())]
    # return abs(SPIA(my_point1, my_point2, len(my_point1), len(my_point2)))
    poly1 = Polygon((p1.getX(i), p1.getY(i)) for i in range(p1.getPointNum()))
    poly2 = Polygon((p2.getX(i), p2.getY(i)) for i in range(p2.getPointNum()))
    return Overlap(poly1, poly2)
    # return abs(example.calcularOverlap(p1.GETX(), p1.GETY(), p2.GETX(), p2.GETY(), p1.getPointNum(), p2.getPointNum()))

def calOverlap3(p1):
    # my_point1 = [MyPoint(p1.getX(i), p1.getY(i)) for i in range(p1.getPointNum())]
    # my_point2 = [MyPoint(AreaBoundary[i].get_x(), AreaBoundary[i].get_y()) for i in range(len(AreaBoundary))]
    # return abs(SPIA(my_point1, my_point2, len(my_point1), len(my_point2)))
    poly1 = Polygon((p1.getX(i), p1.getY(i)) for i in range(p1.getPointNum()))
    poly2 = Polygon((AreaBoundary[i].get_x(), AreaBoundary[i].get_y()) for i in range(len(AreaBoundary)))
    return Overlap(poly1, poly2)
    # x_list = [AreaBoundary[i].get_x() for i in range(len(AreaBoundary))]
    # y_list = [AreaBoundary[i].get_y() for i in range(len(AreaBoundary))]
    # return abs(example.calcularOverlap(p1.GETX(), p1.GETY(), x_list, y_list, p1.getPointNum(), len(AreaBoundary)))


def Overlap(poly1, poly2):
    if poly1.intersects(poly2):
        overlap_poly = poly1.intersection(poly2)
        overlap_area = overlap_poly.area
        # print("Overlap area:", overlap_area)
        return overlap_area
    else:
        # print("Polygons do not intersect.")
        return 0


def transition(ModulePath):
    global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
    global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
    global allSumUp, bestSumOverlap, allSum, shellWidth
    global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
    global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName
    tempList = read_file(ModulePath)
    result_list = []
    for i in range(2):
        result_list.append(tempList[i].strip())
    for i in range(ModuleNum):
        str_builder = "Module:" + p[i].getName()
        result_list.append(str_builder)

        str_builder = "Boundary:"
        for j in range(p[i].getPointNum()):
            str_builder += "(" + format(p[i].getX(j), ".1f") + ", " + format(p[i].getY(j), ".1f") + ")"
        str_builder += ";" + p[i].getRuleName()
        result_list.append(str_builder)

        for j in range(len(p[i].portsArrayList)):
            str_builder = "Port:"
            for k in range(p[i].portsArrayList[j].get_port_point_num()):
                str_builder += "(" + format(p[i].portsArrayList[j].get_x(k), ".1f") + ", " + format(
                    p[i].portsArrayList[j].get_y(k), ".1f") + ")"
            str_builder += ";" + p[i].portsArrayList[j].get_rule_name()
            result_list.append(str_builder)
    return result_list


def transition2(ModulePath):
    global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
    global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
    global allSumUp, bestSumOverlap, allSum, shellWidth
    global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
    global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName
    tempList = read_file(ModulePath)
    result_list = []
    for i in range(2):
        result_list.append(tempList[i].strip())
    for i in range(ModuleNum):
        str_builder = "Module:" + allBest[i].getName()
        result_list.append(str_builder)

        str_builder = "Boundary:"
        for j in range(allBest[i].getPointNum()):
            str_builder += "(" + format(allBest[i].getX(j), ".1f") + ", " + format(allBest[i].getY(j), ".1f") + ")"
        str_builder += ";" + allBest[i].getRuleName()
        result_list.append(str_builder)

        for j in range(len(allBest[i].portsArrayList)):
            str_builder = "Port:"
            for k in range(allBest[i].portsArrayList[j].get_port_point_num()):
                str_builder += "(" + format(allBest[i].portsArrayList[j].get_x(k), ".1f") + ", " + format(
                    allBest[i].portsArrayList[j].get_y(k), ".1f") + ")"
            str_builder += ";" + allBest[i].portsArrayList[j].get_rule_name()
            result_list.append(str_builder)
    return result_list

def transition3(ModulePath, particle):
    global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
    global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
    global allSumUp, bestSumOverlap, allSum, shellWidth
    global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
    global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName
    tempList = read_file(ModulePath)
    result_list = []
    for i in range(2):
        result_list.append(tempList[i].strip())
    for i in range(ModuleNum):
        str_builder = "Module:" + particle[i].getName()
        result_list.append(str_builder)

        str_builder = "Boundary:"
        for j in range(particle[i].getPointNum()):
            str_builder += "(" + format(particle[i].getX(j), ".1f") + ", " + format(particle[i].getY(j), ".1f") + ")"
        str_builder += ";" + particle[i].getRuleName()
        result_list.append(str_builder)

        for j in range(len(particle[i].portsArrayList)):
            str_builder = "Port:"
            for k in range(particle[i].portsArrayList[j].get_port_point_num()):
                str_builder += "(" + format(particle[i].portsArrayList[j].get_x(k), ".1f") + ", " + format(
                    particle[i].portsArrayList[j].get_y(k), ".1f") + ")"
            str_builder += ";" + particle[i].portsArrayList[j].get_rule_name()
            result_list.append(str_builder)
    return result_list


def output_result_txt_file(result_list, filepath):
    try:
        with open(filepath, 'w') as file:
            for s in result_list:
                file.write(s + "\n")
    except Exception as e:
        # TODO: handle exception
        pass


import cProfile
import time

if __name__ == '__main__':
    start_time = time.time()
    global AreaBoundary, ModuleNum, fileNumber, p, v, pBest, allBest
    global bestF, bestOverlap, eps, MaxStepLength, MinStepLength
    global allSumUp, bestSumOverlap, allSum, shellWidth
    global AreaMaxX, AreaMinX, AreaMaxY, AreaMinY, random, c1, c2
    global disRate, overlapRate, maxScore, AreaUtiRate, LinkSET, MName, ModuleLinkSet
    initialize()
    file_number = "50-00001"
    ModuleNum = 50
    ReadList = [
        "D:\\Chrome下载\\sample\\" + str(ModuleNum) + "ModuleCase\\" + file_number + "\\Module.txt",
        "D:\\Chrome下载\\sample\\" + str(ModuleNum) + "ModuleCase\\" + file_number + "\\connect_1.txt",
        "D:\\Chrome下载\\sample\\" + str(ModuleNum) + "ModuleCase\\" + file_number + "\\ModuleResult1.txt"
    ]
    read_and_init(ReadList[0])
    for i in p:
        print(len(i.portsArrayList))
    ReadConnectFile(ReadList[1])
    Init()

    print("Program is running! Please wait few minutes...")
    input_path = ReadList[0][:ReadList[0].rfind("\\")]
    # arg2 = input_path + "\\ModuleResult2.txt"
    arg2 = "./ModuleResult2.txt"
    count = 0
    print(p[0].getX(0))
    p[0].adjustAngle(6)
    print(p[0].getX(0))

    cProfile.run("qlearning(1)", sort="tottime")
    # qlearning(1)
    output_result_txt_file(transition(ReadList[0]), arg2)

    end_time = time.time()
    print("程序运行时间：", end_time - start_time, "秒")
