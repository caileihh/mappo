import copy
import math
import random
import ParticleTest_SYM as Par
import numpy as np


def over(p, ModuleNum):
    tempOverlap = 0
    for k in range(ModuleNum):
        for j in range(ModuleNum):
            if j != k:
                tempOverlap += Par.calOverlap2(p[k], p[j])
    return tempOverlap

def legalization2(p, ModuleNum):
    sum_overlap = over(p, ModuleNum)
    now_overlap = sum_overlap
    count = 0
    i = 0
    while sum_overlap != 0:
        p = push_component(p)

        now_overlap = over(p, ModuleNum)
        if now_overlap != sum_overlap:
            sum_overlap = now_overlap
            print(sum_overlap, count)
        else:
            break
        count += 1
        i += 1
        if count >= 1000:
            count = 0
    return p


def reverse_vector_if_angle_greater_than_90(a, b):
    # 计算向量 a 和 b 的点积
    dot_product = np.dot(a, b)

    # 如果点积为负，表示夹角大于90度，将向量 a 取反
    if dot_product < 0:
        a = -a

    return a

def ray_intersects_segment(ray_origin, ray_direction, segment_start, segment_end):
    # 射线起点
    ray_origin = np.array(ray_origin)
    # 射线方向向量（单位向量）
    ray_direction = np.array(ray_direction) / np.linalg.norm(ray_direction)
    # 线段起点和终点
    segment_start = np.array(segment_start)
    segment_end = np.array(segment_end)

    # 检查射线和线段是否平行
    cross_product = np.cross(ray_direction, segment_end - segment_start)
    if np.abs(cross_product) < 1e-9:
        return False  # 平行，不相交

    # 计算射线与线段的交点
    t = np.cross(segment_start - ray_origin, segment_end - segment_start) / cross_product
    u = np.dot((ray_origin + t * ray_direction) - segment_start, (segment_end - segment_start)) / np.dot(
        segment_end - segment_start, segment_end - segment_start)

    # 如果 t 大于 0 且 u 在 [0, 1] 之间，则射线与线段相交
    if t >= 0 and 0 <= u <= 1:
        return True
    else:
        return False


def vector_projection(a, b):
    # 计算点积
    dot_product = np.dot(a, b)
    # 计算向量 b 的模长的平方
    b_length_squared = np.dot(b, b)
    # 计算投影向量
    projection = (dot_product / b_length_squared) * b
    return projection

def push_component(p):
    gamma = 0.6
    for i, t1 in enumerate(p):
        for j, t2 in enumerate(p):
            temp_overlap = Par.calOverlap2(t1, t2)
            if i != j and temp_overlap != 0:
                direction_x = t1.centerPoint.getX() - t2.centerPoint.getX()
                direction_y = t1.centerPoint.getY() - t2.centerPoint.getY()
                if direction_x == 0 and direction_y == 0:
                    direction_x += random.choice([-4, 4])
                    direction_y += random.choice([-4, 4])
                vector_to_other = (direction_x, direction_y)
                # direction_x *= 2
                # direction_y *= 2
                direction = np.array([direction_x, direction_y])
                while_flag = True
                while while_flag:
                    t1_after = copy.deepcopy(t1)
                    # offset_vector = (vector_to_other / 20) * math.sqrt(temp_overlap) * random.random()
                    # offset_x = ((math.sqrt(temp_overlap) * direction_x) / 150) * random.random()
                    # offset_y = ((math.sqrt(temp_overlap) * direction_y) / 150) * random.random()
                    offset_x = direction[0] / (math.sqrt(pow(direction[0], 2) + pow(direction[0], 2)) + 1e-7)*random.random()
                    offset_y = direction[1] / (math.sqrt(pow(direction[0], 2) + pow(direction[0], 2)) + 1e-7)*random.random()
                    t1_after[1] += offset_x
                    t1_after[2] += offset_y

                    Par.judgeOutOfBounds(t1_after)
                    t1 = t1_after
                    while_flag = False
    return p