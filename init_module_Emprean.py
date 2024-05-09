import os

import ParticleTest as Par
import copy


def calculate_sum_module_area(p):
    Area = 0
    for i in p:
        Area += i.getArea()
    return Area

def main_init():
    Par.initialize()
    ReadList = [
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/Module.txt",
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/connect_1.txt",
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/ModuleResultPPO.txt"
    ]

    Par.read_and_init(ReadList[0])
    particle = copy.deepcopy(Par.p)
    linkset = Par.ReadConnectFile2(ReadList[1], particle)
    Par.Init()

    print("Program is running! Please wait few minutes...")
    sum_area = calculate_sum_module_area(Par.p)
    return sum_area, particle, linkset

def write_result(p):
    ReadList = [
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/Module.txt",
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/connect_1.txt",
        os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/ModuleResultPPO.txt"
    ]
    arg2 = os.path.dirname(os.path.abspath(__file__)) + "/dataset/Emprean/ModuleResult2.txt"
    Par.output_result_txt_file(Par.transition3(ReadList[0], p), arg2)