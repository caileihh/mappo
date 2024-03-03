import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import cv2
import ParticleTest_SYM as Par


def calculate_sum_module_area(p):
    Area = 0
    for i in p:
        Area += i.getArea()
    return Area

def main_init():
    Par.initialize()
    file_number = "16-10005"
    ModuleNum = 16
    ReadList = [
        "./ModuleGDS.txt",
        "./connect.txt",
        "./ModuleResultPPO.txt"
    ]
    ModuleNum = 25
    import gdstkProcess
    import readNetlist

    num_name = gdstkProcess.main()
    sym_list = readNetlist.main()
    Par.read_and_init(ReadList[0])
    Par.ReadConnectFile(ReadList[1])
    Module_sym = Par.Init(num_name=num_name, sym_list=sym_list)

    print("Program is running! Please wait few minutes...")
    input_path = ReadList[0][:ReadList[0].rfind("\\")]
    arg2 = "ModuleResult2.txt"
    sum_area = calculate_sum_module_area(Par.p)
    return Module_sym, sum_area