import numpy as np
import math
import random
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import cv2
import ParticleTest_SYM as Par
import init_module

class EnvCore(object):
    """
    # 环境中的智能体
    """

    def __init__(self):
        self.Module_sym, self.sum_area = init_module.main_init()
        # self.agent_num = 2 # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        # self.obs_dim = 14  # 设置智能体的观测维度 # set the observation dimension of agents
        # self.action_dim = 5  # 设置智能体的动作维度，这里假定为一个五个维度的 # set the action dimension of agents, here set to a five-dimensional

        self.agent_num = Par.ModuleNum  # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        self.obs_dim = len(self.observation(Par.p)[0]) # 设置智能体的观测维度 # set the observation dimension of agents
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
            for k in range(Par.ModuleNum):
                if i == k:
                    continue
                temp = Par.calOverlap2(Par.p[n], Par.p[k])
                tempOverlap += temp
            sym = math.sqrt(
                pow(i.getCenterPoint().getX() - Par.sym_center, 2) + pow(i.getCenterPoint().getY() - Par.sym_center, 2))
            obs += [tempOverlap]
            obs += [sym]
            obs += [i.getMinX() - Par.AreaMinX, i.getMaxX() - Par.AreaMaxX, i.getMinY() - Par.AreaMinY,
                    i.getMaxY() - Par.AreaMaxY]
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

        for i in range(Par.ModuleNum):
            Par.p[i].Move2(Par.AreaMaxX * random.random(), Par.AreaMaxY * random.random())
            Par.judgeOutOfBounds(Par.p[i])
        return self.observation(Par.p)

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

        sub_agent_obs = self.observation(Par.p)
        sub_agent_reward = []
        sub_agent_done = []
        sub_agent_info = []

        done_list = [False for _ in range(Par.ModuleNum)]
        # global count_done, done_reward
        reward = 0
        sym = 0
        Step_Length = 50

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
                    if Par.p[int(i / 2)].getCenterPoint().getY() != Par.p[index_sym - 1].getCenterPoint().getY():
                        Par.p[index_sym - 1].Move2(Par.p[index_sym - 1].getCenterPoint().getX(),
                                                   Par.p[int(i / 2)].getCenterPoint().getY())
                    if Par.p[int(i / 2)].getCenterPoint().getX() - Par.sym_center != Par.p[
                        index_sym - 1].getCenterPoint().getX() - Par.sym_center:
                        Par.p[index_sym - 1].Move(
                            2 * Par.sym_center - Par.p[int(i / 2)].getCenterPoint().getX() - Par.p[
                                index_sym - 1].getCenterPoint().getX(),
                            0)
                    Par.p[int(i / 2)].Move(Step_Length * (action[i]), Step_Length * (action[i + 1]))
                    Par.p[index_sym - 1].Move(- Step_Length * (action[i]), Step_Length * (action[i + 1]))
                    if Par.judgeOutOfBounds(Par.p[int(i / 2)]):
                        reward -= 100
                    Par.judgeOutOfBounds(Par.p[index_sym - 1])
                    sym += math.sqrt(pow(Par.p[int(i / 2)].getCenterPoint().getX() - Par.sym_center, 2) + pow(
                        Par.p[int(i / 2)].getCenterPoint().getY() - Par.sym_center, 2))
                elif index_sym == -1:
                    Par.p[int(i / 2)].Move(0, Step_Length * (action[i + 1] + action[i]))
                    if Par.judgeOutOfBounds(Par.p[int(i / 2)]):
                        reward -= 100
                    sym += math.sqrt(pow(Par.p[int(i / 2)].getCenterPoint().getX() - Par.sym_center, 2) + pow(
                        Par.p[int(i / 2)].getCenterPoint().getY() - Par.sym_center, 2))
                else:
                    Par.p[int(i / 2)].Move(Step_Length * (action[i]), Step_Length * (action[i + 1]))
                    if Par.judgeOutOfBounds(Par.p[int(i / 2)]):
                        reward -= 100
                    sym += math.sqrt(pow(Par.p[int(i / 2)].getCenterPoint().getX() - Par.sym_center, 2) + pow(
                        Par.p[int(i / 2)].getCenterPoint().getY() - Par.sym_center, 2))

        tempDis = 0
        for i in range(Par.ModuleNum):
            for ports in Par.LinkSET:
                for tempJ in range(len(ports)):
                    if ports[tempJ] in Par.p[i].portsArrayList:
                        for tempI in range(len(ports)):
                            if tempI == tempJ:
                                continue
                            tempDis += Par.getDist(
                                Par.p[i].portsArrayList[Par.p[i].portsArrayList.index(ports[tempJ])].get_center_point(),
                                ports[tempI].get_center_point())
        tempOverlap = 0
        over_num = 0
        reward_list = [[-1] for _ in range(Par.ModuleNum)]
        for k in range(Par.ModuleNum - 1):
            for i in range(k + 1, Par.ModuleNum):
                temp = Par.calOverlap2(Par.p[i], Par.p[k])
                tempOverlap += temp
                if temp != 0:
                    over_num += 1
        done = False
        reward -= tempOverlap * 0.01
        reward -= sym * 0.01
        reward += 15 * (Par.ModuleNum - over_num)
        reward += 0.05 * (self.sum_area - tempOverlap)
        # print(over_num)
        # if t > 90 and tempOverlap > 5000:
        #     reward -= 0.1 * tempOverlap
        if tempOverlap < 3000:
            done = True
            reward += 0.1 * (self.sum_area - tempOverlap)
            for i in range(len(reward_list)):
                reward_list[i][0] = 2
        if tempOverlap == 0 or ((over_num) <= 1):
            # count_done += 1
            reward += 100 * pow(2, 5 - over_num)
            if over_num == 0:
                reward += 1000
            # print("low over_num and cound_done:", count_done)
            # print(reward)
            for i in range(len(reward_list)):
                reward_list[i][0] = 300
            for i in range(len(reward_list)):
                done_list[i] = True
            done = True
            Par.output_result_txt_file(Par.transition("./ModuleGDS.txt"), "ModuleResult2.txt")
        if tempOverlap == 0:
            reward += 100 * Par.ModuleNum
            # print("0 Overlap!!")
            # print(reward)
            for i in range(len(reward_list)):
                reward_list[i][0] = 300
            for i in range(len(reward_list)):
                done_list[i] = True
            done = True
        for i in range(Par.ModuleNum):
            sub_agent_info.append({})

        return [sub_agent_obs, reward_list, done_list, sub_agent_info]


