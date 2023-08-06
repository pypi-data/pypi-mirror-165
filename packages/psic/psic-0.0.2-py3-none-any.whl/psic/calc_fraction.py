# -*- coding: utf-8 -*-
"""
计算球体在立方体中的体积分数
"""

import numpy as np


def is_in_rectangle(point, xmin, xmax, ymin, ymax):  # 判断点位置在矩形内外
    x = point[0]
    y = point[1]
    if xmin <= x <= xmax and ymin <= y <= ymax:
        return True
    else:
        return False


def cross_num(center, r, xmin, xmax, ymin, ymax):  # 判断圆与直线相交数量
    x = center[0]
    y = center[1]
    num = 0
    if x-r <= xmin <= x+r or x-r <= xmax <= x+r:
        num += 1
    if y-r <= ymin <= y+r or y-r <= ymax <= y+r:
        num += 1
    return num


def calc_axisX_cross_point(center, r, Y):
    x0 = center[0]
    y0 = center[1]
    a = -2*x0
    b = -2*y0
    c = x0**2 + y0**2 - r**2
    e = Y**2 + b*Y + c
    if a**2 - 4*e < 0:
        return []
    delta = np.sqrt(a**2 - 4*e)
    root1 = (-a + delta)/2.0
    root2 = (-a - delta)/2.0
    return [[root1, Y], [root2, Y]]


def calc_axisY_cross_point(center, r, X):
    x0 = center[0]
    y0 = center[1]
    a = -2*x0
    b = -2*y0
    c = x0**2 + y0**2 - r**2
    e = X**2 + a*X + c
    if b**2 - 4*e < 0:
        return []
    delta = np.sqrt(b**2 - 4*e)
    root1 = (-b + delta)/2.0
    root2 = (-b - delta)/2.0
    return [[X, root1], [X, root2]]


def calc_cross_points(center, r, xmin, xmax, ymin, ymax):
    p1 = calc_axisY_cross_point(center, r, xmin)
    p2 = calc_axisY_cross_point(center, r, xmax)
    p3 = calc_axisX_cross_point(center, r, ymin)
    p4 = calc_axisX_cross_point(center, r, ymax)
    return p1+p2+p3+p4


def calc_minor_area(chrod_length, r):
    half_angle = np.arcsin(0.5*chrod_length/r)
    minor_area = r**2*half_angle - 0.5*chrod_length*r*np.cos(half_angle)
    return minor_area


def calc_area_fraction(centers, radiuses, xmin, xmax, ymin, ymax):
    circles_area = 0
    for i in range(len(centers)):
        center = centers[i]
        r = radiuses[i][0]
        num_int = cross_num(center, r, xmin, xmax, ymin, ymax)
        chrod_length = 0
        if num_int > 0:
            points = calc_cross_points(center, r, xmin, xmax, ymin, ymax)
            cross_points = []
            for point in points:
                if is_in_rectangle(point, xmin, xmax, ymin, ymax):
                    cross_points.append(point)
            if len(cross_points) > 0:
                chrod_length = np.sqrt((cross_points[0][0]-cross_points[1][0])**2+(cross_points[0][1]-cross_points[1][1])**2)
        
        area = 0
        if is_in_rectangle(center, xmin, xmax, ymin, ymax) and num_int == 0:
            area = np.pi*r**2
        elif is_in_rectangle(center, xmin, xmax, ymin, ymax) and num_int == 1 and len(cross_points) > 0:
            area = np.pi*r**2 - calc_minor_area(chrod_length, r)
        elif is_in_rectangle(center, xmin, xmax, ymin, ymax) == False and num_int == 1 and len(cross_points) > 0:
            area = calc_minor_area(chrod_length, r)
        elif num_int == 2 and len(cross_points) > 0:
            area = calc_minor_area(chrod_length, r) + np.absolute(0.5*(cross_points[0][0]-cross_points[1][0])*(cross_points[0][1]-cross_points[1][1]))
        circles_area += area
                
    fraction = circles_area/(xmax-xmin)/(ymax-ymin)
    return fraction


def calc_volume_fraction(centers, radiuses, size):
    volume = 1.0
    for s in size:
        volume *= (s[1] - s[0])
    return np.sum(4.0/3.0*np.pi*radiuses**3)/volume
    
    
if __name__ == "__main__":
    centers = [[0.67903757, 0.37195601], [0.36737042, -0.01959854], [-0.01426161, 0.2907907, ], [0.46292355, 1.01283521], [0.29917023, 1.02242966], [1.0233473, -0.02120813],
               [0.80638937, 0.70588318], [-0.03138388, 0.90409142], [1.01879076, 0.83622931], [0.37065488, 0.66405636], [0.84560447, 1.01858671], [0.64792281, 0.80065118], [0.2646079, 0.50382419]]

    radiuses = [[0.21479203], [0.26824568], [0.1926382], [0.0552244], [0.10880974], [0.18590287],
                [0.0876847], [0.10656674], [0.07639095], [0.07590341], [0.09191926], [0.07027798], [0.08319493]]

    xmin, xmax = 0, 1
    ymin, ymax = 0, 1
    
    print('圆形面积占比', calc_area_fraction(np.array(centers), np.array(radiuses), xmin, xmax, ymin, ymax))
