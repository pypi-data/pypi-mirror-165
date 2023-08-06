'''
生成两个单路径图形之间的10个混合图形svg，
+ 以pred和target点对之间的距离分段直接移动，b样条平滑
+ 不默认两个图形的相对位置。由用户输入混合图形变换参数，lr也自由设定（0.05-0.15）。输入60x60，resize到
'''
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# os.chdir("/home/xiemengni/LogoMaker/logomaker/lib/interpolation")
from interpolation.deepsvg.svglib.geom import Point, Bbox
from interpolation.deepsvg.svglib.svg import SVG
from lib.interpolation.deepsvg.svglib.svg_path import SVGPath
from lib.interpolation.deepsvg.svglib.utils import to_gif

from lib.interpolation.deepsvg.difflib.tensor import SVGTensor
from lib.interpolation.deepsvg.difflib.utils import *
from lib.interpolation.deepsvg.difflib.loss import *
from lib.interpolation.deepsvg.svglib.geom import Bbox,Point

import torch.optim as optim
import IPython.display as ipd
from moviepy.editor import ImageClip, concatenate_videoclips, ipython_display

import shutil
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import random
import argparse
import math
import copy


def find_bbox(points):
    return [points[:, 0].min(), points[:, 0].max(), points[:, 1].min(), points[:, 1].max()]


def max_innercircle_cp(tensors):
    # Calculate the distances to the contour
    contours = np.array(tensors.unsqueeze(1)).astype(np.int)
    print(contours.shape)
    raw_dist = np.empty(
        [int(tensors[:, 0].max() - tensors[:, 0].min()), int(tensors[:, 1].max() - tensors[:, 1].min())],
        dtype=np.float32)
    for i in range(int(tensors[:, 0].max() - tensors[:, 0].min())):
        for j in range(int(tensors[:, 1].max() - tensors[:, 1].min())):
            raw_dist[i, j] = cv2.pointPolygonTest(contours, (j, i), True)
    minVal, maxVal, _, maxDistPt = cv2.minMaxLoc(raw_dist)
    return maxDistPt


def find_center(points, mode='bbox'):
    '''
    mode in ['bbox','outercircle','innercircle']
    '''
    if mode == 'bbox':
        bbox = find_bbox(points)
        return [(bbox[1] + bbox[0]) / 2, (bbox[2] + bbox[3]) / 2]
    elif mode == 'innercircle':
        center = max_innercircle_cp(points)
        # center = [center[0] + points[:, 0].min(), center[1] + points[:, 1].min()]
        return center
    elif mode == 'outercircle':
        (x, y), radius = cv2.minEnclosingCircle(np.array(points.unsqueeze(1)).astype(np.int))
        return [x, y]
    else:
        raise ValueError("mode must in ['bbox','outercircle','innercircle']")

def sample_points(commands,control1,control2,end_pos, n=10, mode=None):
    device =commands.device

    z = torch.linspace(0, 1, n, device=device)
    Z = torch.stack([torch.ones_like(z), z, z.pow(2), z.pow(3)], dim=1)

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

    start_pos = torch.cat([
            end_pos[:-1].new_zeros(1, 2),
            end_pos[:-1]
        ])
#     print(control1.shape)
    pos = torch.cat([start_pos.unsqueeze(1),control1.unsqueeze(1),control2.unsqueeze(1),end_pos.unsqueeze(1)],dim=1)
    commands = commands.reshape(-1).long()
    inds = (commands == 1) | (commands == 2)
    commands, pos = commands[inds], pos[inds]

#     print(commands.shape,Q[commands].shape,pos.shape)
    Z_coeffs = torch.matmul(Q[commands], pos)

    # Last point being first point of next command, we drop last point except the one from the last command
    sample_points = torch.matmul(Z, Z_coeffs)
    sample_points = torch.cat([sample_points[:, :-1].reshape(-1, 2), sample_points[-1, -1].unsqueeze(0)])

    if mode=='demo':
        return sample_points, inds
    return sample_points



def spline_smooth(conts):
    CPointX = conts[:,0]
    CPointY = conts[:,1]
    n = len(CPointX)
    knotType = True
    knot = list(np.arange(n+3+1))
    for i in range(0,4):
        knot[i] = 0.0
        knot[n+i] = 1.0


    if knotType:
        L = list(np.arange(n-1))
        S = 0
        for i in range(n-1):
            L[i] = np.sqrt(pow(CPointX[i+1]- CPointX[i],2) + pow(CPointY[i+1]- CPointY[i],2))
            S = S + L[i]

        tmp = L[0]
        for i in range(4,n):
            tmp = tmp + L[i-3]
            knot[i] = tmp / S
    else:
        tmp = 1 / (n-3)
        tmpS = tmp
        for i in range(4,n):
            knot[i] = tmpS
            tmpS = tmpS + tmp
#     print(knot)
    #节点向量
    #knot = [0,0,0,0,0.25,0.4,0.8,1,1,1,1]

    def de_boor_cal(u,knot,X, Y):
        #判断u在哪个区间
        m = len(knot) #节点个数 且 m = n + k +1
        n = len(X)
        i = 3
        for i in range(3,m-3):
            if u>=knot[i] and u<knot[i+1]:
                break
        # print(i)
        #递归计算
        if knot[i+3] - knot[i] == 0:
            a41 = 0
        else:
            a41 = (u - knot[i]) / (knot[i+3] - knot[i])
        if knot[i-1+3] - knot[i-1] == 0:
            a31 = 0
        else:
            a31 = (u - knot[i-1]) / (knot[i-1+3] - knot[i-1])
        if knot[i-2+3] - knot[i-2] == 0:
            a21 = 0
        else:
            a21 = (u - knot[i-2]) / (knot[i-2+3] - knot[i-2])

        XP40 = X[i]
        YP40 = Y[i]
        XP30 = X[i-1]
        YP30 = Y[i - 1]
        XP20 = X[i-2]
        YP20 = Y[i - 2]
        XP10 = X[i-3]
        YP10 = Y[i - 3]

        XP41 = (1 - a41) * XP30 + a41 * XP40
        YP41 = (1 - a41) * YP30 + a41 * YP40

        XP31 = (1 - a31) * XP20 + a31 * XP30
        YP31 = (1 - a31) * YP20 + a31 * YP30

        XP21 = (1 - a21) * XP10 + a21 * XP20
        YP21 = (1 - a21) * YP10 + a21 * YP20
        if knot[i+3-1] - knot[i] == 0:
            a42 = 0
        else:
            a42 = (u - knot[i]) / (knot[i+3-1] - knot[i])
        if knot[i-1+3-1] - knot[i-1] == 0:
            a32 = 0
        else:
            a32 = (u - knot[i-1]) / (knot[i-1+3-1] - knot[i-1])


        XP42 = (1 - a42) * XP31 + a42 * XP41
        YP42 = (1 - a42) * YP31 + a42 * YP41

        XP32 = (1 - a32) * XP21 + a32 * XP31
        YP32 = (1 - a32) * YP21 + a32 * YP31

        if knot[i+3-2] - knot[i] == 0:
            a43 = 0
        else:
            a43 = (u - knot[i]) / (knot[i+3-2] - knot[i])

        P43 = [(1 - a43) * XP32 + a43 * XP42,(1 - a43) * YP32 + a43 * YP42]
        return P43


    # plt.plot(CPointX,CPointY, '-ob', label="Waypoints")
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")

    Bspline = [[],[]]
    for u in np.arange(0.0,1.0,0.0005):
        P = de_boor_cal(u,knot,CPointX,CPointY)
        Bspline[0].append(P[0])
        Bspline[1].append(P[1])
#     ss=0
#     while ss<len(ll_list):
#         u=ll_list[ss]
#         P = de_boor_cal(u,knot,CPointX,CPointY)
#         Bspline[0].append(P[0])
#         Bspline[1].append(P[1])
#         ss+=1

    Bspline[0].append(CPointX[-1])
    Bspline[1].append(CPointY[-1])
    return Bspline




def interpolate(pred_svgpath,target_svgpath,rb=True,savedir=None,save_svg_dir=None,output_dir=None,
                scale=0.75,rotate=0,trans_x=0,trans_y=0,step_num=10,lr=0.1,loss=False,center=False,save_svg=False):


    result_svgs={}

    def mk_dir(path):
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            shutil.rmtree(path)
            os.mkdir(path)
    if save_svg_dir is not None:
        mk_dir(save_svg_dir)
        mk_dir(output_dir)
        print(pred_svgpath, target_svgpath)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        save_file_path = savedir + os.sep + os.path.split(pred_svgpath)[-1].split(' ')[-1].replace('.svg', '_1.3基础几何' +
                                                                                                   os.path.split(
                                                                                                       target_svgpath)[
                                                                                                       -1].split(' ')[-1])
        save_svg_path = save_svg_dir + os.sep + os.path.split(pred_svgpath)[-1].split(' ')[-1].replace('.svg', '_1.3基础几何' +
                                                                                                       os.path.split(
                                                                                                           target_svgpath)[
                                                                                                           -1].split(' ')[
                                                                                                           -1])

        print(save_file_path)
    svg = SVG.load_svg(pred_svgpath,rb).normalize(Bbox(100)).zoom(0.9).canonicalize().simplify_heuristic()
    svg_pred = SVGTensor.from_data(svg.to_tensor())
    p_pred, inds = svg_pred.sample_points(n=10, mode='demo')

    bbox_pred = find_bbox(p_pred)
    pred_size = max(bbox_pred[1] - bbox_pred[0], bbox_pred[3] - bbox_pred[2])
    size = int(pred_size * (1/scale))
    svg_normsize = Bbox(size)
    svg_rotate = (360-rotate) / 180 * math.pi
    trans_scale = float((0.5*pred_size + 0.5*size) / 60)
    # print(trans_scale,Point(-0.,-0.))
    svg_translate = Point(-trans_x * trans_scale, -trans_y * trans_scale)
    # print(svg_translate)


    tangle = SVG.load_svg(target_svgpath,rb).normalize(svg_normsize).zoom(0.9).canonicalize().simplify_heuristic()
    # print('read tangle',print(tangle.to_tensor().shape))
    svg_target = SVGTensor.from_data(tangle.to_tensor())
    p_target = svg_target.sample_points(n=5)

    # print('read pred target ok')
    pred_c = find_center(p_pred, mode='bbox')
    target_c = find_center(p_target, mode='bbox')

    tangle = tangle.translate(Point(float(pred_c[0] - target_c[0]), float(pred_c[1] - target_c[1]))).rotate(
        svg_rotate,Point(float(pred_c[0]),float(pred_c[1]))).translate(svg_translate).canonicalize().simplify_heuristic()
    svg_target = SVGTensor.from_data(tangle.to_tensor())
    p_target = svg_target.sample_points(n=5)
    # print('center')



    if loss==True:
        l_first, losses = svg_emd_loss(p_pred, p_target, mode='demo')
        print(l_first, losses)
        la = losses[:-1].reshape(-1, 4)
        weight_curve = la.mean(dim=-1)
        weight_curve = (weight_curve - weight_curve.min()) / weight_curve.max() * 5 + 1
        mn = weight_curve.mean()
        # print(weight_curve,len(weight_curve))
        import matplotlib.pyplot as plt
        # plt.plot(list(range(len(weight_curve))),weight_curve)
        pad_ids = np.where(inds == False)
        # print(np.where(inds==False))
        weight_curve = weight_curve.tolist()
        for ids in pad_ids:
            weight_curve.insert(ids[0], mn)

        weight_params = []
        control1 = svg_pred.control1
        control2 = svg_pred.control2
        end_pos = svg_pred.end_pos
        comm = svg_pred.commands
        c1 = []
        c2 = []
        ep = []
        for i in range(len(weight_curve)):
            a = control1[i]
            a.requires_grad_(True)
            b = control2[i]
            b.requires_grad_(True)
            c = end_pos[i]
            c.requires_grad_(True)

            c1.append(a.unsqueeze(0))
            c2.append(b.unsqueeze(0))
            ep.append(c.unsqueeze(0))

            weight_params.append({'params': a, 'lr': weight_curve[i] * lr})
            weight_params.append({'params': b, 'lr': weight_curve[i] * lr})
            weight_params.append({'params': c, 'lr': weight_curve[i] * lr})

        optimizer = optim.Adam(weight_params, lr=lr)

        img_list = []
        # with_viewbox="%d %d %d %d"%(int(-maxsize*0.375),int(-maxsize*0.375),int(maxsize*1.375),int(maxsize*1.375))
        with_viewbox = "0 0 100 100"
        print(with_viewbox)
        best_l = 100
        last_loss = None
        import copy


        for i in range(300):
            optimizer.zero_grad()

            p_pred = sample_points(comm, torch.cat(c1), torch.cat(c2), torch.cat(ep), n=5, mode=None)

            l = svg_emd_loss(p_pred, p_target)
            l.backward()
            optimizer.step()

            if i % 2 == 0:
            # if True:
                #         print(svg_pred.control1.grad) #不一样，就是与距离相关
                # img = svg_pred.draw(with_points=True, do_display=False, return_png=True, with_viewbox=with_viewbox)
                # img_list.append(img)
                # print(l)
                pred_bbox = find_bbox(p_pred)
                bbox_center = Point(float((pred_bbox[0] + pred_bbox[1]) / 2), float((pred_bbox[2] + pred_bbox[3]) / 2))
                svg_pred.save_svg(Bbox(100), save_svg_path.replace('.svg', '_%d.svg' % i), with_viewbox=pred_bbox,
                                  center=bbox_center)
            if best_l - l < 0.001 and i > 10:
                #     if l<(l_first/2):
                break
            if l < best_l:
                best_l = l

        # to_gif(img_list, file_path=save_file_path.replace('.svg', '.gif'))

        svg_list = os.listdir(save_svg_dir)
        svg_nums = len(svg_list)
        print(svg_nums)
        stride = int(svg_nums / 12)
        if stride == 0:
            stride = 1
        for i in range(11):
            if len(glob.glob(save_svg_dir + os.sep + '*_%d.svg' % (stride * (i + 1) * 2))) == 1:
                svgpath = glob.glob(save_svg_dir + os.sep + '*_%d.svg' % (stride * (i + 1) * 2))[0]
                print(svgpath, output_dir)
                shutil.move(svgpath, output_dir)
        # shutil.rmtree(save_svg_dir)
    else:
        def is_clockwise(p):
            start, end = p[:-1], p[1:]
            return torch.stack([start, end], dim=-1).det().sum() > 0

        def make_clockwise(p):
            if not is_clockwise(p):
                return p.flip(dims=[0])
            return p

        def get_length_distribution(p, normalize=True):
            start, end = p[:-1], p[1:]
            length_distr = torch.norm(end - start, dim=-1).cumsum(dim=0)
            length_distr = torch.cat([length_distr.new_zeros(1),
                                      length_distr])

            if normalize:
                length_distr = length_distr / length_distr[-1]

            return length_distr

        # plt.plot(p_pred[:, 0], 30 - p_pred[:, 1])
        # plt.savefig(output_dir + r"\%s.png" % "pred")
        # plt.show()
        n, m = len(p_pred), len(p_target)

        # Make target point lists clockwise
        p_target = make_clockwise(p_target)

        #如果旋转了，重新找左上角：
        if rotate!=0:
            sorts = torch.argsort(p_target[:, 1])
            x_sort = p_target[:, 0][sorts]
            min_x_sort = torch.argmin(x_sort[:3])
            y_sort = sorts[min_x_sort]
            new_p_target = torch.cat([p_target[y_sort:], p_target[:y_sort]])
            p_target = new_p_target

        #x的中心点，如果对称，从上中心点开始顺时针
        ###new find center
        def find_center_index(pred_points, center_x):
            shape_p = pred_points.shape[0]
            shun = True
            sucss = 0
            indx_x = 1
            while sucss == 0:
                if pred_points[:, 0][indx_x] == pred_points[:, 0][-indx_x]:
                    # print('continue find index of x')
                    indx_x += 1
                else:
                    # print('found it !!! index=', indx_x)
                    sucss = 1
            if torch.abs(pred_points[:, 0][indx_x] - center_x) > torch.abs(pred_points[:, 0][-indx_x] - center_x):
                near_pred = pred_points[int(shape_p * 0.75):]
                shun = False
            else:
                near_pred = pred_points[:int(shape_p * 0.25)]
            sorts = torch.argsort(torch.abs(near_pred[:, 0] - center_x))
            # plt.plot(near_pred[:, 0], near_pred[:, 1])
            x_sort = sorts[0]
            if shun == False:
                x_sort = int(shape_p * 0.75) + x_sort
            return x_sort

        if center== True:
            bbox_pred = find_bbox(p_pred)
            xcenter = (bbox_pred[0] + bbox_pred[1]) / 2
            x_sort = find_center_index(p_pred,xcenter)
            new_p_pred = torch.cat([p_pred[x_sort:], p_pred[:x_sort]])
            p_pred = new_p_pred

            bbox_target = find_bbox(p_target)
            xcenter = (bbox_target[0] + bbox_target[1]) / 2
            x_sort = find_center_index(p_target,xcenter)
            new_p_target = torch.cat([p_target[x_sort:], p_target[:x_sort]])
            p_target = new_p_target

        #######################################################################################
        step = 0
        while step < step_num:
            # Compute length distribution
            distr_pred = torch.linspace(0., 1., n).to(p_pred.device)
            distr_target = get_length_distribution(p_target, normalize=True)
            d = torch.cdist(distr_pred.unsqueeze(-1), distr_target.unsqueeze(-1))
            matching = d.argmin(dim=-1)
            p_target_sub = p_target[matching]
            #往target走一步
            l = (p_target_sub - p_pred) / ((step_num + 1) - step) * torch.tensor([[1, 1]], dtype=torch.float).repeat(n,
                                                                                                                     1) + p_pred

            l = np.array(l) #走完一步的轮廓点结果
            import copy
            ll = copy.deepcopy(l)
            ll = spline_smooth(ll) #B样条平滑


            #存png图片
            # import matplotlib.pyplot as plt
            # fig, axe = plt.subplots(1, 1, figsize=(10, 10))
            # #                 axe.plot(l[:,0],30-np.array(l[:,1]),color='black')
            # #                 axe.fill(l[:,0],30-np.array(l[:,1]),color='black')
            # axe.plot(ll[0], 30 - np.array(ll[1]), color='black')
            # axe.fill(ll[0], 30 - np.array(ll[1]), color='black')
            # plt.savefig(output_dir + r"\%d.png" % step)
            # plt.show()

            #存svg
            ll = np.array(ll).T
            p_pred = ll
            pred_bbox = find_bbox(p_pred)
            p_pred[:, 0] = p_pred[:, 0] - (pred_bbox[0] + pred_bbox[1]) / 2
            p_pred[:, 1] = p_pred[:, 1] - (pred_bbox[2] + pred_bbox[3]) / 2
            p_pred = p_pred * (60 / max(pred_bbox[1] - pred_bbox[0], pred_bbox[3] - pred_bbox[2]))
            p_pred = p_pred + 50
            with_viewbox = '0 0 100 100'
            fill_attr = f'fill="black" stroke="black"'
            marker_attr = ''
            path_filling = '1'
            path_svg = '<path {} {} filling="{}" d="{}"></path>'.format(fill_attr, marker_attr, path_filling,
                                                                        "M" + str(p_pred[0, 0]) + " " + str(
                                                                            p_pred[0, 1]) + " " + " ".join(
                                                                            "L" + str(p_pred[i, 0]) + " " + str(
                                                                                p_pred[i, 1]) for i in
                                                                            range(p_pred.shape[0] - 1)) + " Z")
            svg = str((
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{with_viewbox}">'
                f'{""}'
                f'{path_svg}'
                '</svg>')
            )  # height="100px" width="100px"
            if save_svg == True:
                with open(output_dir + os.sep + 'points_%d.svg'%step, 'w') as f:
                    f.write(svg)
            result_svgs[str(step)]=svg

            p_pred = torch.tensor(l)
            print(p_pred.shape, p_target.shape)
            step += 1

        # plt.plot(p_target[:, 0], 30 - p_target[:, 1])
        # plt.savefig(output_dir + r"\%s.png" % "target")
        # plt.show()


        return result_svgs

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="interpolate between two svgs")
    parser.add_argument("--pred_svgpath",default=r'/home/xiemengni/deepsvg-master/dataset/singlepath_svg/3441.svg',help="")
    parser.add_argument("--target_svgpath", default=r'/home/xiemengni/deepsvg-master/dataset/singlepath_svg/2073.svg', help="")
    parser.add_argument("--lr", default=0.1, type=float,help="")
    parser.add_argument("--transfer_x", default=-10, type=float, help="")
    parser.add_argument("--transfer_y", default=-10, type=float, help="")
    parser.add_argument("--rotate", default=90, type=float, help="")
    parser.add_argument("--scale", default=0.7, type=float, help="")
    parser.add_argument("--step_num", default=10, type=int, help="")
    parser.add_argument("--loss", default=False, action='store_true', help="") #点对逼近，为true则迭代
    parser.add_argument("--center", default=False, action='store_true', help="") #中心点对齐，从中心点开始顺时针

    parser.add_argument("--savedir", default='/home/xiemengni/deepsvg-master/dataset/singlepath_svg/interplationOF基础几何与承勋', help="")
    parser.add_argument("--save_svg_dir", default='/home/xiemengni/deepsvg-master/dataset/singlepath_svg/tmp_svg', help="")
    parser.add_argument("--output_dir", default='/home/xiemengni/deepsvg-master/dataset/singlepath_svg/output_3441-3357_svg', help="")
    args = parser.parse_args()

    _=interpolate(args.pred_svgpath, args.target_svgpath, args.savedir, args.save_svg_dir, args.output_dir,scale=args.scale,rotate=args.rotate,
                trans_x=args.transfer_x,trans_y=args.transfer_y,step_num=args.step_num,lr=args.lr,loss=args.loss,center=args.center)



