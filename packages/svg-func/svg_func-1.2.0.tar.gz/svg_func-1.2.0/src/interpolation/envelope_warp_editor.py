'''
封套扭曲实现
本次1.0版本初步实现5中arch效果
'''

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import os
# os.chdir("..")
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import time
# st1 = time.time()
# from interpolation.deepsvg.svglib.svg import SVG
# from interpolation.deepsvg.svglib.svg_path import SVGPath
from interpolation.deepsvg.difflib.tensor import SVGTensor
from interpolation.deepsvg.difflib.utils import *
from interpolation.deepsvg.difflib.loss import *
from interpolation.deepsvg.svglib.geom import Bbox,Point

from interpolation.deepsvg.svglib.trans_func import *
from interpolation.deepsvg.svglib.util_cpoint import *
from interpolation.envelope_warp import from_str,getstr_in_svg,simpleget_points_insvg,from_str_deepread
# print('import time:',time.time()-st1)

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import torch
from xml.dom.minidom import parse, parseString
import copy
import urllib
import re



def translateXY_points(p_target,bh_indx,svg_path_hz,svg_path_translate,svg_path_rotate,svg_path_scale,p_n=10, reverse=False):
    new_p_target = []
    need_translate_points = copy.deepcopy(p_target)
    for j in range(len(bh_indx)):
        #左上角为原点（即0，0为原点）先缩放，旋转，再平移
        print(svg_path_translate[j],svg_path_rotate[j],svg_path_scale[j])
        trans_xiao = svg_path_translate[j]
        rotate_xiao = float(svg_path_rotate[j])
        scale_xiao = float(svg_path_scale[j])

        indx_xiao = bh_indx[j]
        hz_xiao = svg_path_hz[j]

        p_zi_nums = (indx_xiao[-1] - (len(indx_xiao) - 1) - sum(hz_xiao)) * (p_n - 1)
        szi_points = need_translate_points[:p_zi_nums,:]  # get one path

        if reverse:
            print('in save: trans first')
            szi_points[:, 0] = szi_points[:, 0] + float(trans_xiao[0])
            szi_points[:, 1] = szi_points[:, 1] + float(trans_xiao[1])

            szi_points[:, 0] = szi_points[:, 0] * scale_xiao
            szi_points[:, 1] = szi_points[:, 1] * scale_xiao

            len_r = np.sqrt(szi_points[:, 0]**2+szi_points[:, 1]**2)
            or_theta = np.arcsin(szi_points[:, 1]/len_r)/math.pi*180
            or_theta = or_theta + rotate_xiao
            szi_points[:, 0] = len_r*np.cos(or_theta/180*math.pi)
            szi_points[:, 1] = len_r * np.sin(or_theta / 180 * math.pi)
        else:
            print(' in read: trans finally',find_bbox(szi_points),scale_xiao)
            szi_points[:,0] = szi_points[:,0]*scale_xiao
            szi_points[:, 1] = szi_points[:, 1] * scale_xiao


            len_r = np.sqrt(szi_points[:, 0]**2+szi_points[:, 1]**2)
            or_theta = np.arcsin(szi_points[:, 1]/len_r)/math.pi*180
            or_theta = or_theta + rotate_xiao
            szi_points[:, 0] = len_r*np.cos(or_theta/180*math.pi)
            szi_points[:, 1] = len_r * np.sin(or_theta / 180 * math.pi)

            szi_points[:, 0] = szi_points[:, 0] + float(trans_xiao[0])
            szi_points[:, 1] = szi_points[:, 1] + float(trans_xiao[1])

        new_p_target.append(szi_points)
        need_translate_points = need_translate_points[p_zi_nums:,:]
    p_target = torch.cat(new_p_target, axis=0)
    return p_target

#读取svg并取轮廓点，只对单张svg操作
def get_points_color_insvg(svg_path,p_n=10,filetype='url',apply='editor'):
    svg_str = getstr_in_svg(svg_path,filetype=filetype)
    # st=time.time()

    domTree, svg_path_indx, svg_path_fillcolor, svg_path_tensor, svg_path_translate, svg_path_rotate, svg_path_scale, svg_path_hz = from_str_deepread(
        svg_str, apply)

    #
    # print('read in svg time:', time.time() - st)
    bh_indx = svg_path_indx
    # print(bh_indx, svg_path_fillcolor)
    bh_color = svg_path_fillcolor

    svg_tensor = torch.cat(svg_path_tensor, axis=0)
    # print('svg_tensor shape', svg_tensor.shape)
    svg_target = SVGTensor.from_data(svg_tensor)
    p_target = svg_target.sample_points(n=p_n)


    #####if apply=='editor', points must translate to target ord
    # print('apply:',apply,svg_path_translate)
    if 'editor' in apply and (len(svg_path_translate)>0 or len(svg_path_rotate)>0 or len(svg_path_scale)>0):
        p_target = translateXY_points(p_target,bh_indx,svg_path_hz,svg_path_translate,svg_path_rotate,svg_path_scale,p_n=p_n)
    word_bbox = find_bbox(p_target)
    return p_target, bh_indx, bh_color, svg_path_hz, svg_path_translate, svg_path_rotate, svg_path_scale, word_bbox, domTree



def save_l_svg(domTree, transed_points,indx_zi,color_zi, hz_zi, mode='random', apply='editor1', bh_translate=None, bh_rotate=None, bh_scale=None,c_svg=None, file_path=None,n=10):
    '''
    :param domTree:
    :param transed_points: [2,N]
    :param indx_zi: 不同path的间隔indx
    :param color_zi: 不同path的颜色
    :param hz_zi: 每个M的结尾有没有Z
    :param file_path: 存储路径
    :param n: 每个cmd取多少点
    :return:
    '''

    # if 'editor' in apply:
    if True:
        # c_svg = np.array(c_svg)
        # width = max(c_svg[:, 0]) - min(c_svg[:, 0])
        # height = max(c_svg[:, 1]) - min(c_svg[:, 1])

        bh_translate = np.array(bh_translate).astype(np.float)
        pred_bbox = find_bbox(np.around(transed_points, decimals=3).T)
        with_viewbox = str(float(pred_bbox[0])) + ' ' + str(float(pred_bbox[2])) + ' ' + str(
            float(pred_bbox[6])) + ' ' + str(float(pred_bbox[7]))
        if domTree.documentElement.getAttribute("width") != '':
            domTree.documentElement.setAttribute("width", str(max(transed_points[0,:])))
        if domTree.documentElement.getAttribute("height") != '':
            domTree.documentElement.setAttribute("height", str(max(transed_points[1,:])))
            if domTree.documentElement.getAttribute("viewbox") != '':
                domTree.documentElement.setAttribute("viewbox",with_viewbox)
            # print(pred_bbox)

        # modify points trans, back to origin svg
        print(bh_translate)
        bh_translate[:, 0] *= -1
        bh_translate[:, 1] *= -1
        bh_scale = 1/np.array(bh_scale).astype(np.float)
        bh_rotate = -np.array(bh_rotate).astype(np.float)
        transed_points = translateXY_points(torch.tensor(transed_points.T), indx_zi, hz_zi, bh_translate, bh_rotate, bh_scale, p_n=n, reverse=True)
        transed_points =  np.array(transed_points.T)

    names = domTree.documentElement.getElementsByTagName("path")

    transed_points = np.around(transed_points, decimals=3)
    pred_bbox = find_bbox(transed_points.T)
    with_viewbox = str(float(pred_bbox[0])) + ' ' + str(float(pred_bbox[2])) + ' ' + str(
        float(pred_bbox[6])) + ' ' + str(float(pred_bbox[7]))
    if mode=='random':
        domTree.documentElement.setAttribute("viewBox", with_viewbox)


    # fill_attr = f'fill="black" stroke="black"'
    fill_attr = ''
    marker_attr = ''
    path_filling = '1'
    svg = str((
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{with_viewbox}">'
        f'{""}'))
    print(color_zi)

    for j in range(len(indx_zi)):
        indx_xiao = indx_zi[j]
        hz_xiao = hz_zi[j]
        p_str = ''
        print('indx_xiao', indx_xiao, hz_xiao)

        p_zi_nums = (indx_xiao[-1] - (len(indx_xiao) - 1) - sum(hz_xiao)) * (n - 1)
        szi_points = transed_points[:, :p_zi_nums]
        transed_points = transed_points[:, p_zi_nums:]
        color = color_zi[j]
        last_inx = 0
        if len(indx_xiao) > 2:
            for i in range(len(indx_xiao) - 2):  # path里的笔画
                sinx = indx_xiao[i]
                einx = indx_xiao[i + 1]
                gp = 2
                if hz_xiao[i] == 0:
                    gp = 1

                p_num = (einx - sinx - gp) * (n - 1)
                if p_num <= 0:
                    p_pred = szi_points[:, last_inx:last_inx + 1]
                    p_str += "M" + str(p_pred[0, 0]) + " " + str(
                        p_pred[1, 0])
                else:
                    # print(sinx, einx, p_num, last_inx, szi_points.shape)
                    p_pred = szi_points[:, last_inx:last_inx + p_num]
                    p_str += "M" + str(p_pred[0, 0]) + " " + str(
                        p_pred[1, 0]) + " " + " ".join(
                        "L" + str(p_pred[0, a]) + " " + str(
                            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"

                    last_inx = last_inx + p_num

                if i == len(indx_xiao) - 3:
                    # print(last_inx, szi_points.shape)
                    p_pred = szi_points[:, last_inx:]
                    p_str += "M" + str(p_pred[0, 0]) + " " + str(
                        p_pred[1, 0]) + " " + " ".join(
                        "L" + str(p_pred[0, a]) + " " + str(
                            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
        #                     plot_points(p_pred.T, show_color=True)
        #     #                 plt.plot(p_pred[0,:],p_pred[1,:],c='red')
        #                     plt.show()
        else:
            p_pred = szi_points[:, :]
            p_str += "M" + str(p_pred[0, 0]) + " " + str(
                p_pred[1, 0]) + " " + " ".join(
                "L" + str(p_pred[0, a]) + " " + str(
                    p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
        #             plot_points(p_pred.T, show_color=True)
        # #           plt.plot(p_pred[0,:],p_pred[1,:],c='red')
        #             plt.show()

        # print(color)
        if color[0] == "":
            color = ['black']
        path_svg = '<path d="{}" fill="{}"/>'.format(p_str, color[0])
        # print(path_svg)
        svg = svg + str((f'{path_svg}'))
        names[j].setAttribute("d", p_str)

    svg = svg + str(('</svg>'))
    # print(svg)
    if file_path is not None:
        # with open(file_path, 'w',encoding='utf-8') as f:
        #     f.write(svg)
        with open(file_path.replace('.svg', '_changes.svg'), 'w',encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            nsvg=''
            nsvg += str(domTree.toxml('UTF-8'), encoding="utf-8")
            # svg += str(('</svg>'))
            f.write(nsvg)

    # print(domTree.toxml('UTF-8'))
    return svg, str(domTree.toxml('UTF-8'), encoding="utf-8")

def main(svgpath=None,sample_n=10,filetype='path',c_svg=None,csvg_filetype='path',apply='editor',arch_per=0.5,pos='up',fix='top', mode='arch',file_path = None):
    '''
    :param svgpath: 输入svg，可以3种格式，根据 filetype
    :param sample_n: 默认10  svg中每个cmd的取点数，对点做坐标计算。点越多越平滑，
    :param filetype: svgpath的类型，默认path   'url'是文件的url地址，'path'本地svg文件， 'string'是直接字符串输入，
    :param c_svg: 默认None  如果用于四边形封套。需输入文件矩形四个角点的target位置，[4,2]; 如果用于random轮廓，轮廓的输入数据，格式与输入svg一致，可以是
                            ‘url','path','string'。4个角点位置的顺序是
    :param csvg_filetype: c_svg的类型，默认path   'url'是文件的url地址，'path'本地svg文件， 'string'是直接字符串输入，
    :param arch_per: 默认0.3 arch效果拱的程度 1~100%
    :param pos: 默认up 朝哪个方向拱，分别有'up' 'left' 'right' 'down'
    :param fix: 暂时不使用
    :param mode:默认arch  一共有5种 'arch' 'single_arch' 'polygon' 'circle','random' ,
    :param apply: 20220402新增编辑器版本的3种4边形效果 ['editor1','editor2','editor3']
    :param file_path:默认None 结果svg存储路径
    :return: 返回svg的字符串。两种方式做出。第一种是完全自己写， 第二种是只改变d中的数据。 一般只用第二个结果
    '''
    st=time.time()
    read_points, bh_indx, bh_color, bh_hz, bh_translate, bh_rotate, bh_scale, points_bbox, domTree = get_points_color_insvg(svgpath, p_n=sample_n, filetype=filetype, apply=apply)
    rt = time.time()
    print('read time:',rt-st)

    if 'editor' in apply:
        pbbox=copy.deepcopy(points_bbox)
        pbbox = np.array(pbbox)
        olt = [pbbox[0], pbbox[3]]
        old = [pbbox[0], pbbox[2]]
        ord = [pbbox[1], pbbox[2]]
        ort = [pbbox[1], pbbox[3]]
        w = pbbox[6]
        h = pbbox[7]
        nlt = 1
        nld = 1
        nrd = 1
        nrt = 1
        try:
            polytype=int(apply[-1])
            if polytype==1:
                theta_1 = 67.7/180*math.pi
                #平行四边形
                nlt=olt
                nld=[old[0]+h/math.tan(theta_1),old[1]]
                nrd=[ord[0]+h/math.tan(theta_1),ord[1]]
                nrt=ort
            elif polytype == 2:
                theta_1 = 67.7 / 180 * math.pi
                # 梯形
                nlt = olt
                nld = [old[0] + h / math.tan(theta_1), old[1]]
                nrd = [ord[0] - h / math.tan(theta_1), ord[1]]
                nrt = ort
            elif polytype == 3:
                # 透视平行四边形
                nlt = [olt[0], olt[1]+2*h]
                nld = [old[0], old[1]+0.5*h]
                nrd = ord
                nrt = ort
            c_svg = [nlt,nld,nrd,nrt]
            print('new c_svg:',c_svg)
            mode='polygon'
        except:
            print('in other mode:',mode)

    if 'arch' in mode:
        transed_points = trans_points(read_points, points_bbox, n=sample_n, arch_per=arch_per, pos=pos, fix=fix,
                                      mode=mode)
    elif mode == 'polygon':
        #         c_svg = [[10,30],[0,0],[40,0],[30,30]]
        transed_points = trans_points_random4poly(read_points, c_svg, points_bbox, n=sample_n, mode='polygon')
    elif mode == 'circle':
        transed_points = trans_points_circle(read_points, points_bbox)
    elif mode == 'random':
        s_points, target_tensor, p_n = simpleget_points_insvg(c_svg,filetype=csvg_filetype)
        transed_points = trans_points_anycon(read_points, target_tensor, s_points, p_n, scale_sf=1.01)
    else:
        raise ValueError("mode not in 'arch' 'single_arch' 'polygon' 'circle','random'")
    trt = time.time()
    # print('transed time:',trt-rt)
    svg, xml = save_l_svg(domTree,transed_points, bh_indx, bh_color, bh_hz, mode=mode, apply=apply, bh_translate=bh_translate, bh_rotate=bh_rotate, bh_scale=bh_scale,c_svg=c_svg, file_path=file_path,n=sample_n)
    sat = time.time()
    # print('saved time:',sat-trt)
    print('total used time:',sat-st)

    return svg, xml



if __name__ == "__main__":

    # svg,xml = main(svgpath=r"C:\Users\25790\Downloads\0d1dd158-e46a-43a7-aeef-826c6eca32da.svg",c_svg=[[0.0,596.0],[0.0,149.0],[1668.0,0.0],[1668.0,298.0]],
    #                file_path=r'C:\Users\25790\Downloads\result22.svg', filetype='path',csvg_filetype='string',mode='polygon',apply='editor2',pos='up',fix='top')
    # print(time.time()-st1)
    # print(xml)
    # main(r"C:\Users\25790\Downloads\双边拱+喇叭状+汉堡封套_5.13\文字.svg")
    #     main(r"C:\Users\25790\Downloads\整体封套_5.16\文字_竖.svg")
    paths = [r'C:\Users\25790\Downloads\01.svg'
             # r'C:\Users\25790\Downloads\0-2.svg',
             # r'C:\Users\25790\Downloads\0-3.svg',
             # r'C:\Users\25790\Downloads\0-4.svg',
             # r'C:\Users\25790\Downloads\0-5.svg',
             # r'C:\Users\25790\Downloads\0-6.svg'
             ]
    i = 1
    for p in paths:
        for per in [0.2, 0.4, 0.6]:#[0.2, 0.4, 0.6]
            for mode in ['arch', 'single_arch', 'double_arch']:
                for pos in ['up', 'down', 'left', 'right']:
                    if mode != 'arch':
                        for fix in ['positive', 'negative']:
                            main(p, sample_n=10, arch_per=per, pos=pos, fix=fix, mode=mode,
                                 file_path=r'C:\Users\25790\Downloads\fengtao_test\res_%d.svg' % i)
                            i += 1
                    else:
                        main(p, sample_n=10, arch_per=per, pos=pos, fix='positive', mode=mode,
                             file_path=r'C:\Users\25790\Downloads\fengtao_test\res_%d.svg' % i)
                        i += 1







