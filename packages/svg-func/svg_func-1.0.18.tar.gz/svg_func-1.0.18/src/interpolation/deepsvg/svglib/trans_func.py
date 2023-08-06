#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Desc: 轮廓坐标变形函数
@Time: 2021/11/10
"""

import numpy as np
import copy
import torch
import math

from .util_cpoint import find_bbox

def trans_points(cont, bbox, n=10, arch_per=0.3, pos=True, fix='top', mode='arch'):
    or_bbox = copy.deepcopy(bbox)
    if pos == 'right' or pos == 'left':
        cont = torch.flip(cont, [1])
        bbox = find_bbox(cont)
    if pos == 'left':
        cont[:, 1] *= (-1)
        bbox = find_bbox(cont)

    cont = np.array(cont)
    bbox = np.array(bbox)
    a = [bbox[0], bbox[2]]
    b = [bbox[1], bbox[2]]
    c = [bbox[0], bbox[3]]
    d = [bbox[1], bbox[3]]
    # 角度百分比（与90度比），圆心左右对称有
    arch_a = math.pi / 2 * arch_per
    center_x = (a[0] + b[0]) / 2
    w = (b[0] - a[0])
    h = c[1] - a[1]
    print(bbox)

    if mode == 'arch':
        # xiahu neg
        if pos == 'up':
            r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
            upper_r = r + h
            circle_c = [center_x, c[1] + r * np.cos(arch_a)]
            # print('r', circle_c, r, arch_a)
            # print((cont[0, 0] - center_x) / (w / 2))
            a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
            r_cont = r + (upper_r - r) * (c[1] - cont[:, 1]) / h  # +
            new_x = circle_c[0] + r_cont * np.sin(a_cont)
            new_y = circle_c[1] - r_cont * np.cos(a_cont)
        #             plt.scatter(new_x, new_y)
        # print(bbox, arch_a)
        else:
            r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
            upper_r = r + h  # *(w/h)
            circle_c = [center_x, a[1] - r * np.cos(arch_a)]
            # print('r', circle_c, r, arch_a)
            a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
            # print((cont[0, 0] - center_x) / (w / 2))
            r_cont = r + (upper_r - r) * (cont[:, 1] - a[1]) / h  # +
            new_x = circle_c[0] + r_cont * np.sin(a_cont)
            new_y = circle_c[1] + r_cont * np.cos(a_cont)
            # plt.scatter(new_x, new_y)
            # print(bbox, arch_a)
    elif mode == 'single_arch':
        if fix=='positive':
            if pos == 'up':
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c = [center_x, a[1] + r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc = circle_c[0] + r * np.sin(a_cont)
                y_arc = circle_c[1] - r * np.abs(np.cos(a_cont))

                y_rate = (c[1] - cont[:, 1]) / h
                new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
                new_y = y_rate * (y_arc - c[1]) + c[1]
            else:
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c = [center_x, c[1] - r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc = circle_c[0] + r * np.sin(a_cont)
                y_arc = circle_c[1] + r * np.abs(np.cos(a_cont))

                y_rate = (cont[:, 1] - a[1]) / h
                new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
                new_y = y_rate * (y_arc - a[1]) + a[1]
        else:
            if pos == 'up':
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c = [center_x, a[1] - r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc = circle_c[0] + r * np.sin(a_cont)
                y_arc = circle_c[1] + r * np.abs(np.cos(a_cont))

                y_rate = (c[1] - cont[:, 1]) / h
                new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
                new_y = y_rate * (y_arc - c[1]) + c[1]
            else:
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c = [center_x, c[1] + r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc = circle_c[0] + r * np.sin(a_cont)
                y_arc = circle_c[1] - r * np.abs(np.cos(a_cont))

                y_rate = (cont[:, 1] - a[1]) / h
                new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
                new_y = y_rate * (y_arc - a[1]) + a[1]
    elif mode == 'double_arch':
        if fix == 'positive':
            if pos == 'up' or pos == 'right':
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c1 = [center_x, a[1] + r * np.cos(arch_a)]  # c[0]
                circle_c2 = [center_x, c[1] + r * np.cos(arch_a)]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc1 = circle_c1[0] + r * np.sin(a_cont)
                y_arc1 = circle_c1[1] - r * np.abs(np.cos(a_cont))
                y_arc2 = circle_c2[1] - r * np.abs(np.cos(a_cont))

            else:
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c1 = [center_x, a[1] + r * np.cos(arch_a)]  # c[0]
                circle_c2 = [center_x, c[1] - r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc1 = circle_c1[0] + r * np.sin(a_cont)
                y_arc1 = circle_c1[1] - r * np.abs(np.cos(a_cont))
                y_arc2 = circle_c2[1] + r * np.abs(np.cos(a_cont))

        else:
            if pos == 'up' or pos == 'right':
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c1 = [center_x, a[1] - r * np.cos(arch_a)]  # c[0]
                circle_c2 = [center_x, c[1] - r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc1 = circle_c1[0] + r * np.sin(a_cont)
                y_arc1 = circle_c1[1] + r * np.abs(np.cos(a_cont))
                y_arc2 = circle_c2[1] + r * np.abs(np.cos(a_cont))

            else:
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c1 = [center_x, a[1] - r * np.cos(arch_a)]  # c[0]
                circle_c2 = [center_x, c[1] + r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc1 = circle_c1[0] + r * np.sin(a_cont)
                y_arc1 = circle_c1[1] + r * np.abs(np.cos(a_cont))
                y_arc2 = circle_c2[1] - r * np.abs(np.cos(a_cont))

        y_rate = (c[1] - cont[:, 1]) / h
        # new_x = y_rate * (x_arc1 - cont[:, 0]) + cont[:, 0]
        new_x = x_arc1
        new_y = y_rate * (y_arc1 - y_arc2) + y_arc2

    transed_points2 = np.array([new_x, new_y])

    if pos == 'right' or pos == 'left':
        if pos == 'left':
            transed_points2[1, :] *= (-1)
        transed_points2 = np.flip(transed_points2, 0)

        w2 = max(transed_points2[0, :]) - min(transed_points2[0, :])
        # print(float((bbox[1] - bbox[0])), float((bbox[3] - bbox[2])), w2, float((or_bbox[3] - or_bbox[2])) / w2)
        cx, cy = (max(transed_points2[0, :]) + min(transed_points2[0, :])) / 2, (
                max(transed_points2[1, :]) + min(transed_points2[1, :])) / 2
        # transed_points2[0, :] = (transed_points2[0, :] - cx) * float((bbox[3] - bbox[2])) / w2 + float(
        #     or_bbox[1] + or_bbox[0]) / 2
        # transed_points2[1, :] = (transed_points2[1, :] - cy) * float((bbox[3] - bbox[2])) / w2 + float(
        #     or_bbox[1] + or_bbox[0]) / 2

    else:
        w2 = max(transed_points2[0, :]) - min(transed_points2[0, :])
        cx, cy = (max(transed_points2[0, :]) + min(transed_points2[0, :])) / 2, (
                max(transed_points2[1, :]) + min(transed_points2[1, :])) / 2
        # transed_points2[0, :] = (transed_points2[0, :] - cx) * float((bbox[1] - bbox[0])) / w2 + float(
        #     bbox[1] + bbox[0]) / 2
        # transed_points2[1, :] = (transed_points2[1, :] - cy) * float(bbox[1] - bbox[0]) / w2 + float(
        #     bbox[3] + bbox[2]) / 2
    transed_points2 = np.around(transed_points2, decimals=3)
    # plt.scatter(transed_points2[0,:],transed_points2[1,:])
    return transed_points2


def trans_points_anycontrolcon(p_target,control_points,new_control_points):
    ###计算
    p_target = np.array(p_target)
    print(p_target.shape)
    v0 = copy.deepcopy(p_target)
    v0 = v0[:,np.newaxis,:].repeat([control_points.shape[0]],axis=1) #8437,4,2
    print('V0.shape',v0.shape)

    vi = copy.deepcopy(control_points)
    vi = vi[np.newaxis,:,:].repeat([v0.shape[0]],axis=0)
    vj = np.concatenate((control_points[1:],[control_points[0]]),axis=0)
    vj = vj[np.newaxis,:,:].repeat([v0.shape[0]],axis=0)
    r0i = np.sqrt(((v0-vi)**2).sum(axis=2))
    r0j = np.sqrt(((v0-vj)**2).sum(axis=2))
    rij = np.sqrt(((vj-vi)**2).sum(axis=2))
    dn = 2*r0i*r0j
    r = (r0i**2+r0j**2-rij**2)/dn
    print('r shape',r.shape)
    r[r>1]=1
    r[r<-1]=-1
    A = np.arccos(r)

    _r = np.sqrt(((v0-vi)**2).sum(axis=2))
    A_i = np.concatenate((A[:,-1][:,np.newaxis],A[:,0:-1]),axis=1)
    print(A.shape,A_i.shape,_r.shape)
    W = (np.tan(A_i/2)+np.tan(A/2))/_r

    W=np.array(W)
    Ws = W.sum(axis=1)
    L = W/Ws[:,np.newaxis].repeat([W.shape[1]],axis=1)
    print('L.shape',L.shape)


    new_control_points = new_control_points[np.newaxis,:,:].repeat([L.shape[0]],axis=0)
    nx_ny = (L[:,:,np.newaxis].repeat([2],axis=2)*new_control_points).sum(axis=1)
    new_p=nx_ny
    new_p = np.array(new_p)
    return new_p


def trans_points_random4poly(p_target, c_svg, word_bbox, n=10, mode='polygon'):
    if mode == 'poly_circle':
        word_bbox = np.array(word_bbox)
        width = word_bbox[6]
        height = word_bbox[7]
        iw = width / n
        ih = height / n
        # print(iw, ih)
        left = list([word_bbox[0], word_bbox[3] - ih * i] for i in range(n))
        bottom = list([word_bbox[0] + iw * i, word_bbox[2]] for i in range(n))
        right = list([word_bbox[1], word_bbox[2] + ih * i] for i in range(n))
        top = list([word_bbox[1] - iw * i, word_bbox[3]] for i in range(n))
        control_points = np.array([left, bottom, right, top]).reshape(-1, 2)
        control_points[:, 0] = (control_points[:, 0] - control_points[:, 0].mean()) * 1.01 + control_points[:, 0].mean()
        control_points[:, 1] = (control_points[:, 1] - control_points[:, 1].mean()) * 1.01 + control_points[:, 1].mean()
        # print(control_points.shape)

        # new_control_points
        r = max(width, height) / 2 * 0.9
        ia = math.pi / (2 * n)
        r_left_a = list([math.pi * (7 / 4) - ia * i for i in range(n)])
        r_left = np.array([r * np.sin(r_left_a), r * np.cos(r_left_a)]).T
        # print(r_left.shape)
        r_bottom_a = list([math.pi * (5 / 4) - ia * i for i in range(n)])
        r_bottom = np.array([r * np.sin(r_bottom_a), r * np.cos(r_bottom_a)]).T

        r_right_a = list([math.pi * (3 / 4) - ia * i for i in range(n)])
        r_right = np.array([r * np.sin(r_right_a), r * np.cos(r_right_a)]).T

        r_top_a = list([math.pi * (9 / 4) - ia * i for i in range(n)])
        r_top = np.array([r * np.sin(r_top_a), r * np.cos(r_top_a)]).T

        new_control_points = np.array([r_left, r_bottom, r_right, r_top]).reshape(-1, 2)
    else:
        c_svg = np.array(c_svg)
        # print(c_svg)

        # 平移缩放无所谓：
        # print(word_bbox)
        word_bbox = np.array(word_bbox)
        control_points = np.array([[word_bbox[0], word_bbox[3]],
                                   [word_bbox[0], word_bbox[2]],
                                   [word_bbox[1], word_bbox[2]],
                                   [word_bbox[1], word_bbox[3]]])
        new_control_points = np.array(c_svg)
        control_points[:, 0] = (control_points[:, 0] - control_points[:, 0].mean()) * 1.01 + control_points[:, 0].mean()
        control_points[:, 1] = (control_points[:, 1] - control_points[:, 1].mean()) * 1.01 + control_points[:, 1].mean()
        # print(control_points)

    new_p = trans_points_anycontrolcon(p_target,control_points,new_control_points)
    return new_p.T

def trans_points_circle(p_target,svg_bbox):
    p_target = np.array(p_target)
    svg_bbox = np.array(svg_bbox)
    # resize到正方形，原点为中心点
    z_l = max(svg_bbox[1] - svg_bbox[0], svg_bbox[3] - svg_bbox[2])
    center = [(svg_bbox[1] + svg_bbox[0]) / 2, (svg_bbox[3] + svg_bbox[2]) / 2]
    p_target[:, 0] = (p_target[:, 0] - center[0]) / (svg_bbox[1] - svg_bbox[0]) * z_l
    p_target[:, 1] = (p_target[:, 1] - center[1]) / (svg_bbox[3] - svg_bbox[2]) * z_l

    copy_p = copy.deepcopy(p_target)
    # x,y 轴上的点不进入计算
    copy_p[:, 0][p_target[:, 0] == 0] = z_l / 4
    copy_p[:, 1][p_target[:, 0] == 0] = z_l / 4
    copy_p[:, 0][p_target[:, 1] == 0] = z_l / 4
    copy_p[:, 1][p_target[:, 1] == 0] = z_l / 4

    # 矩形四周角点不进入计算
    copy_p[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                    z_l / 2 * np.sin(math.pi / 4)]
    copy_p[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == -z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                     -z_l / 2 * np.sin(math.pi / 4)]
    copy_p[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == -z_l / 2)] = [-z_l / 2 * np.sin(math.pi / 4),
                                                                                      -z_l / 2 * np.sin(math.pi / 4)]
    copy_p[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == z_l / 2)] = [-z_l / 2 * np.sin(math.pi / 4),
                                                                                     z_l / 2 * np.sin(math.pi / 4)]

    # 正方形中心点在原点
    # 正方形四周是圆的边缘，中心轴在原位置不变（圆直径径是边长）。平行y连线和平行x连线是越来越大平缓的圆弧。圆弧的夹角从90度逐渐降为0，
    # 边上的两点是圆弧上的点，于x轴或者y轴的夹角从45度降为0。一个矩形里的点，可以画出y连线于x连线的两段弧，计算弧（2个圆）的交点就是在圆内的点。
    # 因为都基于第一象限计算，只取第一象限的交点作为变换后的点位置。四周角点的点和xy轴上的点不纳入计算，直接取得，计算中会出现极值。
    ###思考
    ###这是将原来的直线连线都变为了圆弧，如果是椭圆，或者其他弧线，应该是同理。最大弧线逐渐降级成为直线，需要找方法。本质上是bazier

    incir_copyp = copy.deepcopy(copy_p)
    row_rc_rate = np.abs(incir_copyp[:, 1]) / (z_l / 2)
    row_cir_arch = row_rc_rate * math.pi / 2
    row_qt_arch = row_rc_rate * math.pi / 4
    row_qt_len = z_l * np.cos(row_qt_arch)
    row_cir_r = (row_qt_len / 2) / (np.sin(row_cir_arch / 2))
    row_cir_ceter = np.zeros((row_cir_r.shape[0], 2))
    row_cir_ceter[:, 1] = -row_cir_r * np.cos(row_cir_arch / 2) + z_l * np.sin(row_qt_arch) / 2
    print(row_cir_ceter.shape)

    col_rc_rate = abs(incir_copyp[:, 0]) / (z_l * 0.5)
    col_cir_arch = col_rc_rate * math.pi / 2
    col_qt_arch = col_rc_rate * math.pi / 4
    col_qt_len = z_l * np.cos(col_qt_arch)
    col_cir_r = (col_qt_len / 2) / (np.sin(col_cir_arch / 2))
    col_cir_ceter = np.zeros((col_cir_r.shape[0], 2))
    col_cir_ceter[:, 0] = -col_cir_r * np.cos(col_cir_arch / 2) + z_l * np.sin(col_qt_arch) / 2

    def insec(p1, r1, p2, r2):
        x = p1[:, 0]
        y = p1[:, 1]
        R = r1
        a = p2[:, 0]
        b = p2[:, 1]
        S = r2
        d = np.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
        #     print(np.sort(d-(R+S)),np.sort(d-(np.abs(R-S))),np.sort(d))
        #     print(np.unique((d-(R+S))>0),(d-(np.abs(R-S))).any() < 0,d.any() == 0)
        if np.sort(d - (R + S))[0] > 0 or (d - (np.abs(R - S))).any() < 0:
            # print("Two circles have no intersection")
            return None, None
        elif d.any() == 0:
            # print("Two circles have same center!")
            return None, None
        else:
            A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
            h = np.sqrt(R ** 2 - A ** 2)
            x2 = x + A * (a - x) / d
            y2 = y + A * (b - y) / d
            x3 = np.around(x2 - h * (b - y) / d, 2)
            y3 = np.around(y2 + h * (a - x) / d, 2)
            x4 = np.around(x2 + h * (b - y) / d, 2)
            y4 = np.around(y2 - h * (a - x) / d, 2)
            c1 = np.array([x3, y3])
            c2 = np.array([x4, y4])
            return c1, c2

    c1, c2 = insec(row_cir_ceter, row_cir_r, col_cir_ceter, col_cir_r)
    print(c1.shape, c2.shape)
    c1 = c1.T
    c2 = c2.T
    ###只要第一象限的点
    incir_copyp[np.logical_and(c1[:, 0] > 0, c1[:, 1] > 0)] = c1[np.logical_and(c1[:, 0] > 0, c1[:, 1] > 0)]
    incir_copyp[np.logical_and(c2[:, 0] > 0, c2[:, 1] > 0)] = c2[np.logical_and(c2[:, 0] > 0, c2[:, 1] > 0)]
    incir_copyp = incir_copyp * copy_p / np.abs(copy_p) #正负号赋值

    incir_copyp[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                         z_l / 2 * np.sin(math.pi / 4)]
    incir_copyp[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == -z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                          -z_l / 2 * np.sin(
                                                                                              math.pi / 4)]
    incir_copyp[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == -z_l / 2)] = [
        -z_l / 2 * np.sin(math.pi / 4), -z_l / 2 * np.sin(math.pi / 4)]
    incir_copyp[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == z_l / 2)] = [
        -z_l / 2 * np.sin(math.pi / 4), z_l / 2 * np.sin(math.pi / 4)]

    incir_copyp[:, 0][p_target[:, 0] == 0] = 0
    incir_copyp[:, 1][p_target[:, 0] == 0] = p_target[:, 1][p_target[:, 0] == 0]
    incir_copyp[:, 0][p_target[:, 1] == 0] = p_target[:, 0][p_target[:, 1] == 0]
    incir_copyp[:, 1][p_target[:, 1] == 0] = 0

    return incir_copyp.T



##############################################任意图像封套扭曲
def reshape_points_square(p_pred):
    word_bbox = find_bbox(p_pred)
    z_l = max(word_bbox[6], word_bbox[7])
    p_pred[:, 0] = (p_pred[:, 0] - word_bbox[4]) * z_l / word_bbox[6]
    p_pred[:, 1] = (p_pred[:, 1] - word_bbox[5]) * z_l / word_bbox[7]
    return p_pred


def sample_points(svg_target, n_list=None, mode=None):
    device = svg_target.commands.device

    Q = torch.tensor([
        [[0., 0., 0., 0.],  #  "m"
         [0., 0., 0., 0.],
         [0., 0., 0., 0.],
         [0., 0., 0., 0.]],

        [[1., 0., 0., 0.],  # "l"
         [-1, 0., 0., 1.],
         [0., 0., 0., 0.],
         [0., 0., 0., 0.]],

        [[1., 0., 0., 0.],  #  "c"
         [-3, 3., 0., 0.],
         [3., -6, 3., 0.],
         [-1, 3., -3, 1.]],

        torch.zeros(4, 4),  # "a", no support yet

        torch.zeros(4, 4),  # "EOS"
        torch.zeros(4, 4),  # "SOS"
        torch.zeros(4, 4),  # "z"
    ], device=device)

    commands, pos = svg_target.commands.reshape(-1).long(), svg_target.get_data(svg_target.all_position_keys).reshape(
        -1, 4, 2)
    inds = (commands == svg_target.COMMANDS_SIMPLIFIED.index("l")) | (
                commands == svg_target.COMMANDS_SIMPLIFIED.index("c"))
    commands, pos = commands[inds], pos[inds]

    Z_coeffs = torch.matmul(Q[commands], pos)

    # Last point being first point of next command, we drop last point except the one from the last command
    #     print(Z.shape,Z_coeffs.shape) #10,4  8,4,2
    sample_points = []

    for i, n in enumerate(n_list):
        #         print(n)
        z = torch.linspace(0, 1, int(n), device=device)
        Z = torch.stack([torch.ones_like(z), z, z.pow(2), z.pow(3)], dim=1)
        sample_points_s = torch.matmul(Z, Z_coeffs[i])
        sample_points.append(sample_points_s[:-1].reshape(-1, 2))
    sample_points.append(sample_points_s[-1].unsqueeze(0))
    #     print(sample_points.shape)
    #     sample_points = torch.cat([sample_points[:, :-1].reshape(-1, 2), sample_points[-1, -1].unsqueeze(0)])
    sample_points = torch.cat(sample_points)

    if mode == 'demo':
        return sample_points, inds
    return sample_points


# 算4个点的位置
def cal_jiaoIDX(orjiao_p, ors_points, i=[1, 1]):
    # 象限

    if orjiao_p is not None:
        jiao_p = copy.deepcopy(orjiao_p)
        jiao_p = np.around(np.array(jiao_p), 1)
    else:
        jiao_p = np.array([[0, 0]])
    s_points = copy.deepcopy(ors_points)
    s_points = np.around(np.array(s_points), 1)
    s_bbox = find_bbox(s_points)

    print()
    con_p = None
    idx_1 = None
    # 先判断是否有该象限的点
    if sum(np.logical_and(jiao_p[:, 0] * i[0] > 0, jiao_p[:, 1] * i[1] > 0)) > 0 and orjiao_p is not None:
        print('find in 1 xiangxian')
        l_ori = get_lori(jiao_p)
        sl = l_ori[:, 0] * i[0] + l_ori[:, 1] * i[1]
        arg = np.argsort(sl)
        sort_sl = np.sort(sl)
        nearsort_sl = np.where((sort_sl[-1] - sort_sl) <= 3)
        # 找其中最接近45du的点
        nearsort_arg = arg[nearsort_sl]
        minarg = np.argmin(np.abs(jiao_p[nearsort_arg][:, 0] * i[0] / jiao_p[nearsort_arg][:, 1] * i[1] - 1))
        idx_1 = nearsort_arg[minarg]

        con_p = orjiao_p[idx_1]
    elif sum(np.logical_and(s_points[:, 0] * i[0] > 0, s_points[:, 1] * i[1] > 0)) == 0 and orjiao_p is not None:
        # 象限内没有点，最左上角，第二象限的最左最上
        # print('in most left top', np.where((jiao_p[:, 0] * i[0] <= 0) & (jiao_p[:, 1] * i[1] > 0)))
        ll = np.where((jiao_p[:, 0] * i[0] <= 0) & (jiao_p[:, 1] * i[1] > 0))
        leftmax = np.max(jiao_p[ll][:, 0] * i[0])
        toparg = np.argmax(jiao_p[ll][jiao_p[ll][:, 0] * i[0] == leftmax][:, 1] * i[1])
        idx_1 = ll[0][toparg]
        con_p = orjiao_p[idx_1]
    else:
        # 找45°的坐标
        print('find in 45 du')
        ll = np.where((s_points[:, 0] * i[0] > 0) & (s_points[:, 1] * i[1] > 0))
        #         print('ll',ll)
        if s_points[ll].shape[0] == 0:
            # 第一象限没一点
            ll2 = np.where((s_points[:, 0] * i[0] <= 0) & (s_points[:, 1] * i[1] > 0))
            leftmax = np.max(s_points[ll2][:, 0] * i[0])
            toparg = np.argmax(jiao_p[ll2][jiao_p[ll2][:, 0] * i[0] == leftmax][:, 1] * i[1])
            spoints_idx = ll2[0][toparg]

        else:
            tan1_arg = np.argsort(
                np.abs(s_points[ll][:, 0] * i[0] / (s_points[ll][:, 1] * i[1]) - s_bbox[6] / s_bbox[7]))
            tan1_sort = np.sort(np.abs(s_points[ll][:, 0] * i[0] / (s_points[ll][:, 1] * i[1]) - s_bbox[6] / s_bbox[7]))
            #             print('tan---/',np.abs(s_points[ll][:,0]*i[0]/(s_points[ll][:,1]*i[1])),tan1_arg)
            tan1_nearsort = np.where(tan1_sort <= 0.2)  # 36~52度,再找这个范围内最远的
            choosed_arg = tan1_arg[tan1_nearsort]
            if choosed_arg.shape[0] == 0:
                # 第一象限没有45度点
                choosed_arg = tan1_arg[0]
                spoints_idx = choosed_arg
            else:
                inll_arg = ll[0][choosed_arg]
                # print('choosed_nearsort', tan1_nearsort, choosed_arg, inll_arg, s_points[inll_arg],
                #       s_points[inll_arg].shape)
                #         print('inll_arg',inll_arg,s_points[inll_arg])
                if len(s_points[inll_arg].shape) == 2:
                    # print('s_points[inll_arg]:', s_points[inll_arg])
                    l = np.linalg.norm(s_points[inll_arg], ord=2, axis=1)
                    spoints_idx = inll_arg[np.argmax(l)]
                else:
                    # 符合条件的只有一个点
                    print('###', inll_arg)
                    spoints_idx = inll_arg

        idx_1 = None
        con_p = ors_points[spoints_idx]
    #     print(idx_1)
    return idx_1, con_p


def get_lori(jiao_p):
    # 离远点距离，[N,2]
    jiao_p = np.array(jiao_p)
    # 算多边形角点离中心点距离
    coor1 = jiao_p[np.logical_and(jiao_p[:, 0] > 0, jiao_p[:, 1] > 0)]
    l_ori = np.linalg.norm(jiao_p, ord=1, axis=1)
    #     print('l ori',l_ori)
    l_ori = l_ori[:, np.newaxis].repeat([2], 1)
    re_jiao_p = copy.deepcopy(jiao_p) + 0.001  # 避免为0
    l_ori = l_ori * re_jiao_p / np.abs(re_jiao_p)
    return l_ori


# s_points = sample_points(svg_target,n_list=p_n)
# print(time.time()-st)
# print(s_points.shape)
# plt.show()
# plt.plot(s_points[:,0],s_points[:,1])

def is_clockwise(p):
    start, end = p[:-1], p[1:]
    return torch.stack([start, end], dim=-1).det().sum() > 0


def make_clockwise(p):
    if not is_clockwise(p):
        return p.flip(dims=[0])
    return p


# 点有了
# 判断是否是多边形：
def get_4controlpoints_from_targetcon(target_tensor, s_points,p_n):
    cmds = target_tensor[:, 0]
    nonzm = cmds[np.logical_and(cmds != 0, cmds != 6)]
    whereline = p_n[nonzm == 1]
    if len(whereline)!=len(p_n):
        if sum(whereline)/sum(p_n)<0.5:
            print('not polygons')
            # 计算曲线4个对应角点的位置，对角线交点
            # 中心点为原点
            target_bbox = find_bbox(s_points)
            s_points[:, 0] = s_points[:, 0] - target_bbox[4]
            s_points[:, 1] = s_points[:, 1] - target_bbox[5]
            # 每个点与原点的tan
            idx_1, conp1_sp = cal_jiaoIDX(None, s_points, i=[1, 1])
            idx_2, conp2_sp = cal_jiaoIDX(None, s_points, i=[-1, 1])
            idx_3, conp3_sp = cal_jiaoIDX(None, s_points, i=[-1, -1])
            idx_4, conp4_sp = cal_jiaoIDX(None, s_points, i=[1, -1])
            idx_ss = [idx_2, idx_3, idx_4, idx_1]
            conp_ss = [conp2_sp, conp3_sp, conp4_sp, conp1_sp]
            return idx_ss, conp_ss, s_points, target_bbox
        else:
            # 获得角点坐标
            jiao_p_tensor = list(np.array(target_tensor[cmds == 1]))
            jiao_p = []
            for otensor in jiao_p_tensor:
                otensor = list(otensor)
                if otensor[6:8] not in jiao_p:
                    jiao_p.append(otensor[6:8])
                print(otensor[-2:], jiao_p)
                if otensor[-2:] not in jiao_p:
                    jiao_p.append(otensor[-2:])
            jiao_p = torch.tensor(jiao_p)

    else:
        # 获得角点坐标
        jiao_p = target_tensor[:, -2:]

    print(jiao_p)
    while sum(jiao_p[-1] - jiao_p[0]) == 0:
        jiao_p = jiao_p[:-1]

    # 中心点为原点
    target_bbox = find_bbox(s_points)
    jiao_p[:, 0] = jiao_p[:, 0] - target_bbox[4]
    jiao_p[:, 1] = jiao_p[:, 1] - target_bbox[5]
    s_points[:, 0] = s_points[:, 0] - target_bbox[4]
    s_points[:, 1] = s_points[:, 1] - target_bbox[5]
    print(jiao_p)
    # plt.plot(jiao_p[:, 0], jiao_p[:, 1])
    #     plt.scatter(jiao_p[4,0],jiao_p[4,1])

    # 计算4个角点，
    jiao_p = np.array(jiao_p)
    idx_1, conp1_sp = cal_jiaoIDX(jiao_p, s_points, i=[1, 1])
    idx_2, conp2_sp = cal_jiaoIDX(jiao_p, s_points, i=[-1, 1])
    idx_3, conp3_sp = cal_jiaoIDX(jiao_p, s_points, i=[-1, -1])
    idx_4, conp4_sp = cal_jiaoIDX(jiao_p, s_points, i=[1, -1])
    print(idx_1, idx_2, idx_3, idx_4, 'idxxxxx')
    #     idx_ss = np.array([idx_2,idx_3,idx_4,idx_1])
    idx_ss = [idx_2, idx_3, idx_4, idx_1]
    conp_ss = [conp2_sp, conp3_sp, conp4_sp, conp1_sp]
    return idx_ss, conp_ss, s_points, target_bbox


# control points，原svg
def get_controlp_for_trans(p_pred, s_points, conp_ss, scale=1.01):
    pred_bbox = find_bbox(p_pred)
    width = pred_bbox[6]
    height = pred_bbox[7]

    ##选择2341
    # spoints
    new_control_points = []
    oldpoints_ns = []
    # print(conp_ss,s_points)
    s_points2 = np.around(np.array(s_points), 2)
    conp_ss2 = np.around(conp_ss, 2)
    for i in range(4):
        sp_idxn = np.where(((s_points2[:, 0] - conp_ss2[i][0]) ** 2 < 1) & ((s_points2[:, 1] - conp_ss2[i][1]) ** 2 < 1))[0][0]
        next_i = int((i + 1) % 4)
        next_sp_idxn = np.where(((s_points2[:, 0] - conp_ss2[next_i][0]) ** 2 < 1) & ((s_points2[:, 1] - conp_ss2[next_i][1]) ** 2 < 1))[0][0]
        if next_sp_idxn < sp_idxn:
            points_num = s_points.shape[0] - sp_idxn + next_sp_idxn
            new_control_points.append(s_points[sp_idxn:])
            if next_sp_idxn != 0:
                new_control_points.append(s_points[:next_sp_idxn])
        else:
            points_num = next_sp_idxn - sp_idxn
            new_control_points.append(s_points[sp_idxn:next_sp_idxn])
        oldpoints_ns.append(points_num)
    new_control_points = np.concatenate(new_control_points, axis=0)

    n = oldpoints_ns[0]
    # print('lllll',n,pred_bbox[3],(height/(n)))
    print()
    left = list([pred_bbox[0], pred_bbox[3] - (height / (n)) * i] for i in range(n))
    print('left', len(left))
    n = oldpoints_ns[1]
    bottom = list([pred_bbox[0] + width / n * i, pred_bbox[2]] for i in range(n))
    print(len(bottom))
    n = oldpoints_ns[2]
    right = list([pred_bbox[1], pred_bbox[2] + height / (n) * i] for i in range(n))
    print(len(right))
    n = oldpoints_ns[3]
    top = list([pred_bbox[1] - width / n * i, pred_bbox[3]] for i in range(n))
    print(len(top))
    # print(n,len(left),len(bottom))
    control_points = np.concatenate([left, bottom, right, top]).reshape(-1, 2)
    # print(control_points.shape)
    # 框放大1.01倍
    control_points[:, 0] = (control_points[:, 0] - control_points[:, 0].mean()) * scale + control_points[:, 0].mean()
    control_points[:, 1] = (control_points[:, 1] - control_points[:, 1].mean()) * scale + control_points[:, 1].mean()
    return control_points, new_control_points

def trans_points_anycon(p_pred,target_tensor,s_points,p_n,scale_sf=1.01):
    idx_ss, conp_ss, s_points, target_bbox = get_4controlpoints_from_targetcon(target_tensor, s_points,p_n)
    control_points, new_control_points = get_controlp_for_trans(p_pred, s_points, conp_ss, scale=scale_sf)
    new_p = trans_points_anycontrolcon(p_pred, control_points, new_control_points)
    new_p[:, 0] = new_p[:, 0]*scale_sf + float(target_bbox[4])
    new_p[:, 1] = new_p[:, 1]*scale_sf + float(target_bbox[5])
    return new_p.T