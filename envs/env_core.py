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
        init_module.main_init()
        # self.agent_num = 2 # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        # self.obs_dim = 14  # 设置智能体的观测维度 # set the observation dimension of agents
        # self.action_dim = 5  # 设置智能体的动作维度，这里假定为一个五个维度的 # set the action dimension of agents, here set to a five-dimensional

        self.agent_num = Par.ModuleNum  # 设置智能体(小飞机)的个数，这里设置为两个 # set the number of agents(aircrafts), here set to two
        self.obs_dim = len(self.observation(Par.p)) # 设置智能体的观测维度 # set the observation dimension of agents
        self.action_dim = 5  # 设置智能体的动作维度，这里假定为一个五个维度的 # set the action dimension of agents, here set to a five-dimensional

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
        sub_agent_obs = []
        for i in range(self.agent_num):
            sub_obs = np.random.random(size=(14,))
            sub_agent_obs.append(sub_obs)
        return sub_agent_obs
        # for i in range(Par.ModuleNum):
        #     Par.p[i].Move2(Par.AreaMaxX * random.random(), Par.AreaMaxY * random.random())
        #     Par.judgeOutOfBounds(Par.p[i])
        # return self.observation(Par.p)

    def step(self, actions):
        """
        # self.agent_num设定为2个智能体时，actions的输入为一个2纬的list，每个list里面为一个shape = (self.action_dim, )的动作数据
        # 默认参数情况下，输入为一个list，里面含有两个元素，因为动作维度为5，所里每个元素shape = (5, )
        # When self.agent_num is set to 2 agents, the input of actions is a 2-dimensional list, each list contains a shape = (self.action_dim, ) action data
        # The default parameter situation is to input a list with two elements, because the action dimension is 5, so each element shape = (5, )
        """
        sub_agent_obs = []
        sub_agent_reward = []
        sub_agent_done = []
        sub_agent_info = []
        for i in range(self.agent_num):
            sub_agent_obs.append(np.random.random(size=(14,)))
            sub_agent_reward.append([np.random.rand()])
            sub_agent_done.append(False)
            sub_agent_info.append({})

        return [sub_agent_obs, sub_agent_reward, sub_agent_done, sub_agent_info]


