#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Desc: 一些工具
@Time: 2021/11/10
"""


#读取轮廓点边界框属性
def find_bbox(points):
    return[points[:,0].min(),points[:,0].max(),points[:,1].min(),points[:,1].max(), (points[:,0].min()+points[:,0].max())/2,
          (points[:,1].min()+points[:,1].max())/2,
           points[:,0].max()- points[:,0].min(),
          points[:,1].max()- points[:,1].min()]


def write_path_insvg(p_pred,color,svg):
    if not color:
        color='black'
    path_svg = '<path d="{}" fill="{}"/>'.format("M" + str(p_pred[0, 0]) + " " + str(
        p_pred[0, 1]) + " " + " ".join(
        "L" + str(p_pred[0, a]) + " " + str(
            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z", color)

    svg = svg + str((f'{path_svg}'))
    return svg


def gen_svgstr(p_pred):
    p_str = "M" + str(p_pred[0, 0]) + " " + str(
        p_pred[1, 0]) + " " + " ".join(
        "L" + str(p_pred[0, a]) + " " + str(
            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
    return p_str



