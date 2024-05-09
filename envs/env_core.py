import numpy as np
import math
import random
import ParticleTest_SYM as Par1
import init_module
import ParticleTest as Par2
import init_module_Emprean


class EnvCore(object):
    """
    # 环境中的智能体
    """

    def __init__(self):
        self.Module_sym, self.sum_area, self.p = init_module.main_init()
        # self.agent_num = 2 # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        # self.obs_dim = 14  # 设置智能体的观测维度 # set the observation dimension of agents
        # self.action_dim = 5  # 设置智能体的动作维度，这里假定为一个五个维度的 # set the action dimension of agents, here set to a five-dimensional

        self.agent_num = Par1.ModuleNum  # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        self.obs_dim = len(self.observation(self.p)[0])  # 设置智能体的观测维度 # set the observation dimension of agents
        self.action_dim = 2  # 设置智能体的动作维度，这里假定为一个五个维度的 # set the action dimension of agents, here set to a five-dimensional

    def calculate_sum_module_area(self, p):
        Area = 0
        for i in p:
            Area += i.getArea()
        return Area

    def observation(self, p):
        obs1 = []
        for n, i in enumerate(p):
            obs = []
            obs += i.GETX()
            obs += i.GETY()
            tempOverlap = 0
            for k in range(self.agent_num):
                if i == k:
                    continue
                temp = Par1.calOverlap2(self.p[n], self.p[k])
                tempOverlap += temp
            sym = math.sqrt(
                pow(i.getCenterPoint().getX() - Par1.sym_center, 2) + pow(i.getCenterPoint().getY() - Par1.sym_center,
                                                                          2))
            obs += [tempOverlap]
            obs += [sym]
            obs += [i.getMinX() - Par1.AreaMinX, i.getMaxX() - Par1.AreaMaxX, i.getMinY() - Par1.AreaMinY,
                    i.getMaxY() - Par1.AreaMaxY]
            obs1.append(np.array(obs))
        return obs1

    def reset(self):
        """
        # self.agent_num设定为2个智能体时，返回值为一个list，每个list里面为一个shape = (self.obs_dim, )的观测数据
        # When self.agent_num is set to 2 agents, the return value is a list, each list contains a shape = (self.obs_dim, ) observation data
        """
        # sub_agent_obs = []
        # for i in range(self.agent_num):
        #     sub_obs = np.random.random(size=(14,))
        #     sub_agent_obs.append(sub_obs)
        # return sub_agent_obs

        for i in range(self.agent_num):
            self.p[i].Move2(Par1.AreaMaxX * random.random(), Par1.AreaMaxY * random.random())
            Par1.judgeOutOfBounds(self.p[i])
        return self.observation(self.p)

    def write_result(self):
        init_module.write_result()

    # count_done = 0
    def step(self, actions):
        """
        # self.agent_num设定为2个智能体时，actions的输入为一个2纬的list，每个list里面为一个shape = (self.action_dim, )的动作数据
        # 默认参数情况下，输入为一个list，里面含有两个元素，因为动作维度为5，所里每个元素shape = (5, )
        # When self.agent_num is set to 2 agents, the input of actions is a 2-dimensional list, each list contains a shape = (self.action_dim, ) action data
        # The default parameter situation is to input a list with two elements, because the action dimension is 5, so each element shape = (5, )
        """
        # sub_agent_obs = []
        # sub_agent_reward = []
        # sub_agent_done = []
        # sub_agent_info = []
        # for i in range(self.agent_num):
        #     sub_agent_obs.append(np.random.random(size=(14,)))
        #     sub_agent_reward.append([np.random.rand()])
        #     sub_agent_done.append(False)
        #     sub_agent_info.append({})
        #
        # return [sub_agent_obs, sub_agent_reward, sub_agent_done, sub_agent_info]

        sub_agent_obs = self.observation(self.p)
        # sub_agent_reward = []
        sub_agent_done = []
        sub_agent_info = []
        reward_list = [[-1] for _ in range(self.agent_num)]
        done_list = [False for _ in range(self.agent_num)]
        # global count_done, done_reward
        reward = 0
        sym = 0
        Step_Length = 50
        sym_list = [-1.1 for _ in range(self.agent_num)]

        action = []
        for i in actions:
            for j in i:
                action.append(j)
        for i in range(0, len(action), 2):
            index_sym = -2
            for module_sym in self.Module_sym:
                if int(i / 2) + 1 in module_sym:
                    temp_index = [index for index in module_sym if index != int(i / 2) + 1]
                    index_sym = temp_index[0]
                if index_sym != -2 and index_sym != -1:
                    if self.p[int(i / 2)].getCenterPoint().getY() != self.p[index_sym - 1].getCenterPoint().getY():
                        self.p[index_sym - 1].Move2(self.p[index_sym - 1].getCenterPoint().getX(),
                                                    self.p[int(i / 2)].getCenterPoint().getY())
                    if self.p[int(i / 2)].getCenterPoint().getX() - Par1.sym_center != self.p[
                        index_sym - 1].getCenterPoint().getX() - Par1.sym_center:
                        self.p[index_sym - 1].Move(
                            2 * Par1.sym_center - self.p[int(i / 2)].getCenterPoint().getX() - self.p[
                                index_sym - 1].getCenterPoint().getX(),
                            0)
                    self.p[int(i / 2)].Move(Step_Length * (action[i]), Step_Length * (action[i + 1]))
                    self.p[index_sym - 1].Move(- Step_Length * (action[i]), Step_Length * (action[i + 1]))
                    if Par1.judgeOutOfBounds(self.p[int(i / 2)]):
                        reward -= 100
                    Par1.judgeOutOfBounds(self.p[index_sym - 1])
                    temp_sym = math.sqrt(pow(self.p[int(i / 2)].getCenterPoint().getX() - Par1.sym_center, 2) + pow(
                        self.p[int(i / 2)].getCenterPoint().getY() - Par1.sym_center, 2))
                    sym += temp_sym
                    sym_list[int(i / 2)] = temp_sym * 0.05
                elif index_sym == -1:
                    self.p[int(i / 2)].Move(0, Step_Length * (action[i + 1] + action[i]))
                    if Par1.judgeOutOfBounds(self.p[int(i / 2)]):
                        reward -= 100
                    temp_sym = math.sqrt(pow(self.p[int(i / 2)].getCenterPoint().getX() - Par1.sym_center, 2) + pow(
                        self.p[int(i / 2)].getCenterPoint().getY() - Par1.sym_center, 2))
                    sym += temp_sym
                    sym_list[int(i / 2)] = temp_sym * 0.05
                else:
                    self.p[int(i / 2)].Move(Step_Length * (action[i]), Step_Length * (action[i + 1]))
                    if Par1.judgeOutOfBounds(self.p[int(i / 2)]):
                        reward -= 100
                    temp_sym = math.sqrt(pow(self.p[int(i / 2)].getCenterPoint().getX() - Par1.sym_center, 2) + pow(
                        self.p[int(i / 2)].getCenterPoint().getY() - Par1.sym_center, 2))
                    sym += temp_sym
                    sym_list[int(i / 2)] = temp_sym * 0.05

        tempOverlap = 0
        over_num = 0

        for k in range(self.agent_num - 1):
            for i in range(k + 1, self.agent_num):
                temp = Par1.calOverlap2(self.p[i], self.p[k])
                tempOverlap += temp
                if temp != 0:
                    over_num += 1
                    reward_list[k][0] -= temp * 0.1
                    reward_list[i][0] -= temp * 0.1

        done = False
        reward -= tempOverlap * 0.01
        reward -= sym * 0.01
        reward += 15 * (self.agent_num - over_num)
        reward += 0.05 * (self.sum_area - tempOverlap)
        # print(over_num)
        # if t > 90 and tempOverlap > 5000:
        #     reward -= 0.1 * tempOverlap
        if tempOverlap < 3000:
            done = True
            reward += 0.1 * (self.sum_area - tempOverlap)
            # for i in range(len(reward_list)):
            #     reward_list[i][0] = 2
        if tempOverlap == 0 or ((over_num) <= 1):
            # count_done += 1
            reward += 100 * pow(2, 5 - over_num)
            if over_num == 0:
                reward += 1000
            # print("low over_num and cound_done:", count_done)
            # print(reward)
            for i in range(len(reward_list)):
                reward_list[i][0] += 2
            # for i in range(len(reward_list)):
            #     done_list[i] = True
            done = True

        if tempOverlap == 0:
            reward += 100 * self.agent_num
            print("0 Overlap!!")
            # print(reward)
            # for i in range(len(reward_list)):
            #     reward_list[i][0] = 300
            for i in range(len(reward_list)):
                done_list[i] = True
            done = True
            Par1.output_result_txt_file(Par1.transition3("./ModuleGDS.txt", self.p), "ModuleResult2.txt")
        for i in range(self.agent_num):
            sub_agent_info.append({})
        # max_x = max_y = -1e10
        # min_x = min_y = 1e10
        # for i in range(self.agent_num):
        #     min_x = min(self.p[i].getMinX(), min_x)
        #     min_y = min(self.p[i].getMinY(), min_y)
        #     max_x = max(self.p[i].getMaxX(), max_x)
        #     max_y = max(self.p[i].getMaxY(), max_y)
        for i in range(len(reward_list)):
            reward_list[i][0] -= sym_list[i]

        tempDis = 0
        for i in range(self.agent_num):
            now_dis = 0
            for ports in Par1.LinkSET:
                for tempJ in range(len(ports)):
                    if ports[tempJ] in self.p[i].portsArrayList:
                        for tempI in range(len(ports)):
                            if tempI == tempJ:
                                continue
                            now_dis += Par1.getDist(
                                self.p[i].portsArrayList[
                                    self.p[i].portsArrayList.index(ports[tempJ])].get_center_point(),
                                ports[tempI].get_center_point())
            tempDis += now_dis
            reward_list[i][0] -= now_dis * 0.3

        return [sub_agent_obs, reward_list, done_list, sub_agent_info]


class EnvCore_Emprean(object):
    import numpy as np
    import random

    """
    # 环境中的智能体
    """

    def __init__(self):
        self.sum_area, self.p, self.LinkSET = init_module_Emprean.main_init()
        self.agent_num = Par2.ModuleNum  # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        self.obs_dim = len(self.observation(self.p)[0])  # 设置智能体的观测维度 # set the observation dimension of agents
        self.action_dim = 2  # 设置智能体的动作维度，这里假定为一个五个维度的 # set the action dimension of agents, here set to a five-dimensional
        self.cal_wl()

    def calculate_sum_module_area(self, p):
        Area = 0
        for i in p:
            Area += i.getArea()
        return Area

    def legalization(self):
        import legalization2
        legalization2.legalization2(self.p, self.agent_num)

    def observation(self, p):
        obs1 = []
        for n, i in enumerate(p):
            obs = []
            obs += [i.getCenterX()]
            obs += [i.getCenterY()]
            obs += [i.getMaxX() - i.getMinX()]
            obs += [i.getMaxY() - i.getMinY()]
            tempOverlap = 0
            for k in range(self.agent_num):
                if i == k:
                    continue
                temp = Par2.calOverlap2(self.p[n], self.p[k])
                tempOverlap += temp
            obs += [tempOverlap]
            obs += [i.getMinX() - Par2.AreaMinX, i.getMaxX() - Par2.AreaMaxX, i.getMinY() - Par2.AreaMinY,
                    i.getMaxY() - Par2.AreaMaxY]
            obs1.append(np.array(obs))
        return obs1

    def reset(self):
        """
        # self.agent_num设定为2个智能体时，返回值为一个list，每个list里面为一个shape = (self.obs_dim, )的观测数据
        # When self.agent_num is set to 2 agents, the return value is a list, each list contains a shape = (self.obs_dim, ) observation data
        """

        for i in range(self.agent_num):
            self.p[i].Move2(Par2.AreaMinX + (Par2.AreaMaxX - Par2.AreaMinX) * random.random(),
                            Par2.AreaMinY + (Par2.AreaMaxY - Par2.AreaMinY) * random.random())
            Par2.judgeOutOfBounds(self.p[i])
        return self.observation(self.p)

    def write_result(self):
        init_module_Emprean.write_result(self.p)

    def cal_wl(self):
        tempDis = 0
        for i in range(self.agent_num):
            now_dis = 0
            for ports in self.LinkSET:
                for tempJ in range(len(ports)):
                    if ports[tempJ] in self.p[i].portsArrayList:
                        for tempI in range(len(ports)):
                            if tempI == tempJ:
                                continue
                            now_dis += Par2.getDist(
                                self.p[i].portsArrayList[
                                    self.p[i].portsArrayList.index(ports[tempJ])].get_center_point(),
                                ports[tempI].get_center_point())
            tempDis += now_dis
        print("wl:", tempDis)

    # count_done = 0
    def step(self, actions):
        """
        # self.agent_num设定为2个智能体时，actions的输入为一个2纬的list，每个list里面为一个shape = (self.action_dim, )的动作数据
        # 默认参数情况下，输入为一个list，里面含有两个元素，因为动作维度为5，所里每个元素shape = (5, )
        # When self.agent_num is set to 2 agents, the input of actions is a 2-dimensional list, each list contains a shape = (self.action_dim, ) action data
        # The default parameter situation is to input a list with two elements, because the action dimension is 5, so each element shape = (5, )
        """

        sub_agent_obs = self.observation(self.p)
        sub_agent_done = []
        sub_agent_info = []
        reward_list = [[-1] for _ in range(self.agent_num)]
        done_list = [False for _ in range(self.agent_num)]
        # global count_done, done_reward
        reward = 0
        sym = 0
        Step_Length = 50
        sym_list = [-1.1 for _ in range(self.agent_num)]

        action = []
        for i in actions:
            for j in i:
                action.append(j)
        for i in range(0, len(action), 2):
            self.p[int(i / 2)].Move(Step_Length * (action[i]), Step_Length * (action[i + 1]))
            Par2.judgeOutOfBounds(self.p[int(i / 2)])

        tempOverlap = 0
        over_num = 0

        for k in range(self.agent_num - 1):
            for i in range(k + 1, self.agent_num):
                temp = Par2.calOverlap2(self.p[i], self.p[k])
                tempOverlap += temp
                if temp != 0:
                    over_num += 1
                    reward_list[k][0] -= temp * 0.1
                    reward_list[i][0] -= temp * 0.1

        done = False
        reward -= tempOverlap * 0.01
        reward -= sym * 0.01
        reward += 15 * (self.agent_num - over_num)
        reward += 0.05 * (self.sum_area - tempOverlap)
        # print(over_num)
        # if t > 90 and tempOverlap > 5000:
        #     reward -= 0.1 * tempOverlap
        if tempOverlap < 3000:
            reward += 0.1 * (self.sum_area - tempOverlap)

        if tempOverlap == 0 or ((over_num) <= 1):
            # count_done += 1
            reward += 100 * pow(2, 5 - over_num)
            if over_num == 0:
                reward += 1000
            for i in range(len(reward_list)):
                reward_list[i][0] += 2

        if tempOverlap == 0:
            reward += 100 * self.agent_num
            print("0 Overlap!!")
            for i in range(len(reward_list)):
                done_list[i] = True

        tempDis = 0
        for i in range(self.agent_num):
            reward_list[i][0] -= sym_list[i]

            now_dis = 0
            for ports in self.LinkSET:
                for tempJ in range(len(ports)):
                    if ports[tempJ] in self.p[i].portsArrayList:
                        for tempI in range(len(ports)):
                            if tempI == tempJ:
                                continue
                            now_dis += Par2.getDist(
                                self.p[i].portsArrayList[
                                    self.p[i].portsArrayList.index(ports[tempJ])].get_center_point(),
                                ports[tempI].get_center_point())
            tempDis += now_dis
            reward_list[i][0] -= now_dis * 0.1
            sub_agent_info.append({})

        return [sub_agent_obs, reward_list, done_list, sub_agent_info]
