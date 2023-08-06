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
from interpolation.deepsvg.svglib.svg import SVG
from interpolation.deepsvg.svglib.svg_path import SVGPath
from interpolation.deepsvg.difflib.tensor import SVGTensor
from interpolation.deepsvg.difflib.utils import *
from interpolation.deepsvg.difflib.loss import *
from interpolation.deepsvg.svglib.geom import Bbox,Point

from interpolation.deepsvg.svglib.trans_func import *
from interpolation.deepsvg.svglib.util_cpoint import *
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

# print('import time:',time.time()-st1)

#读取svg里的path
def from_str(svg_str: str):
    svg_path_groups = []
    SVG_list=[]

    domTree = parseString(svg_str)
    rootNode = domTree.documentElement

    primitives = {
        "path": SVGPath
    }
    for tag, Primitive in primitives.items():
        for x in rootNode.getElementsByTagName(tag):
            svg_path_groups.append(Primitive.from_xml(x))
            SVG_list.append(SVG([Primitive.from_xml(x)]))
        return SVG(svg_path_groups),SVG_list,domTree



def getstr_in_svg(svg_path,filetype='url'):
    if filetype=='url':
        with urllib.request.urlopen(svg_path) as conn:
            svg_str = conn.read()
    elif filetype=='path':
        with open(svg_path, 'r',encoding='utf-8') as file:
            svg_str = file.read()
    else:
        svg_str = svg_path
    return svg_str

def simpleget_points_insvg(svg_path,filetype='url'):
    svg_str = getstr_in_svg(svg_path,filetype=filetype)
    target_svg = SVG.load_svg(svg_str,rb=True).canonicalize()  # .simplify_heuristic()#.normalize().zoom(0.9).canonicalize()#.simplify_heuristic()
    target_tensor = target_svg.to_tensor()
    if target_tensor.shape[0]>=150:
        raise ValueError('c_svg has too many cmd, over 150')
    svg_target = SVGTensor.from_data(target_tensor)
    p_target0 = svg_target.sample_points(n=10)

    p_target = p_target0[:-1].reshape([-1, 9, 2])
    l = np.linalg.norm(p_target[:, 1:, :] - p_target[:, :-1, :], axis=-1).sum(axis=1)#每个cmd周长
    print(p_target.shape, l)
    if min(l) / 10 < 0.8:#特别短
        p_n = l * 20 / (min(l))
    elif min(l) / 0.8 > 50:#特别长
        p_n = l * 50 / (min(l))
    else:
        p_n = l / (0.8)
    # print(l.shape,l,max(l),p_n,np.ceil(p_n).astype(np.int))
    p_n = np.ceil(p_n).astype(np.int)
    s_points = sample_points(svg_target, n_list=p_n)
    s_points = make_clockwise(s_points)
    return s_points,target_tensor,p_n


def translateXY_points(p_target,bh_indx,svg_path_hz,svg_path_translate,p_n=10):
    new_p_target = []
    need_translate_points = copy.deepcopy(p_target)
    for j in range(len(bh_indx)):
        trans_xiao = svg_path_translate[j]

        indx_xiao = bh_indx[j]
        hz_xiao = svg_path_hz[j]

        p_zi_nums = (indx_xiao[-1] - (len(indx_xiao) - 1) - sum(hz_xiao)) * (p_n - 1)
        szi_points = need_translate_points[:p_zi_nums,:]  # get one path
        szi_points[:, 0] = szi_points[:, 0] + trans_xiao[0]
        szi_points[:, 1] = szi_points[:, 1] + trans_xiao[1]
        new_p_target.append(szi_points)
        need_translate_points = need_translate_points[p_zi_nums:,:]
    p_target = torch.cat(new_p_target, axis=0)
    return p_target

#读取svg并取轮廓点，只对单张svg操作
def get_points_color_insvg(svg_path,p_n=10,filetype='url',apply='editor'):
    svg_str = getstr_in_svg(svg_path,filetype=filetype)

    _, svg_list, domTree = from_str(svg_str)
    svg_path_fillcolor = []
    svg_path_indx = []
    svg_path_hz = []
    svg_path_tensor = []

    svg_path_translate=[]
    if 'editor' in apply:
        len_gs = len(domTree.documentElement.getElementsByTagName('g'))
        for i in range(len_gs):
            translate_words=re.split(r'[(,)\s]', domTree.documentElement.getElementsByTagName('g')[i].getAttribute("transform"))
            x_trans=float(translate_words[1])
            y_trans = float(translate_words[3])
            svg_path_translate.append([x_trans,y_trans]) #获取每一个g里的translate向量，与path一一对应

    if 'overlay' in apply:
        len_gs = len(domTree.documentElement.getElementsByTagName('path'))
        for i in range(len_gs):
            translate_words=re.split(r'[(,)\s]', domTree.documentElement.getElementsByTagName('path')[i].getAttribute("transform"))
            print('translate_words',translate_words)
            x_trans=float(translate_words[1])
            y_trans = float(translate_words[2])
            svg_path_translate.append([x_trans,y_trans]) #获取每一个g里的translate向量，与path一一对应

    for svg_sp in svg_list:
        # 每一个path单独处理
        svg_sp = svg_sp.to_path().simplify_arcs()
        svg_path_fillcolor.append(list([svg_sp.svg_path_groups[i].fill for i in range(len(svg_sp.svg_path_groups))]))
        s_indx = list(np.where(svg_sp.to_tensor()[:, 0] == 0)[0]) + \
                 [svg_sp.to_tensor().shape[0]]
        s_hz = []
        # 是否是M开头Z结尾
        if len(s_indx) >= 3:
            for in0 in s_indx[1:-1]:
                if svg_sp.to_tensor()[:, 0][in0 - 1] == 6:
                    s_hz.append(1)
                else:
                    s_hz.append(0)
        if svg_sp.to_tensor()[:, 0][-1] == 6:
            s_hz.append(1)
        else:
            s_hz.append(0)
        svg_path_indx.append(s_indx)
        svg_path_hz.append(s_hz)
        svg_path_tensor.append(svg_sp.to_tensor())
        # print(svg_sp.to_tensor()[:, 0])

    bh_indx = svg_path_indx
    # print(bh_indx, svg_path_fillcolor)
    bh_color = svg_path_fillcolor

    svg_tensor = torch.cat(svg_path_tensor, axis=0)
    # print('svg_tensor shape', svg_tensor.shape)
    svg_target = SVGTensor.from_data(svg_tensor)
    p_target = svg_target.sample_points(n=p_n)

    #####if apply=='editor', points must translate to target ord
    print('apply:',apply,svg_path_translate)
    if ('editor' in apply or 'overlay' in apply)and len(svg_path_translate)>0:
        p_target = translateXY_points(p_target,bh_indx,svg_path_hz,svg_path_translate,p_n=p_n)
    word_bbox = find_bbox(p_target)

    return p_target, bh_indx, bh_color, svg_path_hz, svg_path_translate, word_bbox, domTree



def save_l_svg(domTree, transed_points,indx_zi,color_zi, hz_zi, mode='random', apply='editor1', bh_translate=None, c_svg=None, file_path=None,n=10):
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

    if 'editor' in apply or 'overlay' in apply:
        bh_translate = np.array(bh_translate)
        if 'editor' in apply:
            if domTree.documentElement.getAttribute("width") != '':
                domTree.documentElement.setAttribute("width", str(max(transed_points[0,:])))
            if domTree.documentElement.getAttribute("height") != '':
                domTree.documentElement.setAttribute("height", str(max(transed_points[1,:])))
            # print(pred_bbox)

        # modify points trans, back to origin svg
        bh_translate[:, 0] *= -1
        bh_translate[:, 1] *= -1
        transed_points = translateXY_points(torch.tensor(transed_points.T), indx_zi, hz_zi, bh_translate, p_n=n)
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
        with open(file_path, 'w',encoding='utf-8') as f:
            f.write(svg)
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
    read_points, bh_indx, bh_color, bh_hz, bh_translate, points_bbox, domTree = get_points_color_insvg(svgpath, p_n=sample_n, filetype=filetype, apply=apply)
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
    svg, xml = save_l_svg(domTree,transed_points, bh_indx, bh_color, bh_hz, mode=mode, apply=apply, bh_translate=bh_translate, c_svg=c_svg, file_path=file_path,n=sample_n)
    sat = time.time()
    # print('saved time:',sat-trt)
    print('total used time:',sat-st)

    return svg, xml


if __name__ == "__main__":

    svg,xml = main(svgpath=r"C:\Users\25790\Downloads\00.svg",c_svg=[[0.0,596.0],[0.0,149.0],[1668.0,0.0],[1668.0,298.0]],
                   file_path=r'C:\Users\25790\Downloads\result22.svg', filetype='path',csvg_filetype='string',mode='arch',arch_per=0.5,apply='overlay',pos='up',fix='top')
    # print(time.time()-st1)
    # print(xml)
    # for i in range(34,58):
    #     svg, xml = main(svgpath=r"C:\Users\25790\Downloads\封套测试-2\画板 %d.svg"%i,
    #                     c_svg=r'C:\Users\25790\Downloads\未标题-2-05.svg',
    #                     file_path=r'C:\Users\25790\Downloads\resultss\dresult%d.svg'%i, filetype='path', csvg_filetype='path',
    #                     mode='single_arch', pos='down', fix='negative',arch_per=0.26)






