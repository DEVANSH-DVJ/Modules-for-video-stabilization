import os
import sys

import cv2
import numpy as np
import json


sys.path.append('/home/devansh/DDStab')
from GlobalNets.GlobalPWCNets import getGlobalPWCModel

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def writeFlow(flow, filename):

    height, width, nBands = flow.shape
    assert nBands == 2, 'Number of bands = %r != 2' % nBands
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    assert u.shape == v.shape, 'Invalid flow shape'
    height, width = u.shape

    f = open(filename, 'wb')
    np.array(height).astype(np.int32).tofile(f)
    np.array(width).astype(np.int32).tofile(f)
    np.array(nBands).astype(np.int32).tofile(f)
    tmp = np.zeros((height, width * nBands))
    tmp[:, np.arange(width) * 2] = u
    tmp[:, np.arange(width) * 2 + 1] = v
    tmp.astype(np.float32).tofile(f)

    f.close()


def make_colorwheel():
    '''
    Generates a color wheel for optical flow visualization as presented in:
        Baker et al. 'A Database and Evaluation Methodology for Optical Flow' (ICCV, 2007)
        URL: http://vision.middlebury.edu/flow/flowEval-iccv07.pdf

    According to the C++ source code of Daniel Scharstein
    According to the Matlab source code of Deqing Sun
    '''

    RY = 15
    YG = 6
    GC = 4
    CB = 11
    BM = 13
    MR = 6

    ncols = RY + YG + GC + CB + BM + MR
    colorwheel = np.zeros((ncols, 3))
    col = 0

    # RY
    colorwheel[0:RY, 0] = 255
    colorwheel[0:RY, 1] = np.floor(255 * np.arange(0, RY) / RY)
    col = col + RY
    # YG
    colorwheel[col:col + YG, 0] = 255 - np.floor(255 * np.arange(0, YG) / YG)
    colorwheel[col:col + YG, 1] = 255
    col = col + YG
    # GC
    colorwheel[col:col + GC, 1] = 255
    colorwheel[col:col + GC, 2] = np.floor(255 * np.arange(0, GC) / GC)
    col = col + GC
    # CB
    colorwheel[col:col + CB, 1] = 255 - np.floor(255 * np.arange(CB) / CB)
    colorwheel[col:col + CB, 2] = 255
    col = col + CB
    # BM
    colorwheel[col:col + BM, 2] = 255
    colorwheel[col:col + BM, 0] = np.floor(255 * np.arange(0, BM) / BM)
    col = col + BM
    # MR
    colorwheel[col:col + MR, 2] = 255 - np.floor(255 * np.arange(MR) / MR)
    colorwheel[col:col + MR, 0] = 255
    return colorwheel


def flow_compute_color(u, v, convert_to_bgr=False):
    '''
    Applies the flow color wheel to (possibly clipped) flow components u and v.

    According to the C++ source code of Daniel Scharstein
    According to the Matlab source code of Deqing Sun

    :param u: np.ndarray, input horizontal flow
    :param v: np.ndarray, input vertical flow
    :param convert_to_bgr: bool, whether to change ordering and output BGR instead of RGB
    :return:
    '''
    # print(u.shape)
    flow_image = np.zeros((u.shape[0], u.shape[1], 3), np.uint8)

    colorwheel = make_colorwheel()  # shape [55x3]
    ncols = colorwheel.shape[0]

    rad = np.sqrt(np.square(u) + np.square(v))
    a = np.arctan2(-v, -u) / np.pi

    fk = (a + 1) / 2 * (ncols - 1)
    k0 = np.floor(fk).astype(np.int32)
    k1 = k0 + 1
    k1[k1 == ncols] = 0
    f = fk - k0

    for i in range(colorwheel.shape[1]):

        tmp = colorwheel[:, i]
        col0 = tmp[k0] / 255.0
        col1 = tmp[k1] / 255.0
        col = (1 - f) * col0 + f * col1

        idx = (rad <= 1)
        col[idx] = 1 - rad[idx] * (1 - col[idx])
        col[~idx] = col[~idx] * 0.75   # out of range?

        # Note the 2-i => BGR instead of RGB
        ch_idx = 2 - i if convert_to_bgr else i
        flow_image[:, :, ch_idx] = np.floor(255 * col)

    return flow_image


def cvtFlow2Color(flow_uv, clip_flow=None, convert_to_bgr=False):
    '''
    Expects a two dimensional flow image of shape [H,W,2]

    According to the C++ source code of Daniel Scharstein
    According to the Matlab source code of Deqing Sun

    :param flow_uv: np.ndarray of shape [H,W,2]
    :param clip_flow: float, maximum clipping value for flow
    :return:
    '''

    assert flow_uv.ndim == 3, 'input flow must have three dimensions'
    assert flow_uv.shape[2] == 2, 'input flow must have shape [H,W,2]'

    if clip_flow is not None:
        flow_uv = np.clip(flow_uv, 0, clip_flow)

    u = flow_uv[:, :, 0]
    v = flow_uv[:, :, 1]

    rad = np.sqrt(np.square(u) + np.square(v))
    rad_max = np.max(rad)

    epsilon = 1e-5
    u = u / (rad_max + epsilon)
    v = v / (rad_max + epsilon)

    return flow_compute_color(u, v, convert_to_bgr)


def run(net, img1_path, img2_path, save_loc):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    os.system('mkdir -p ' + save_loc)
    os.system('cp ' + img1_path + ' ' + save_loc + '/i1.png')
    os.system('cp ' + img2_path + ' ' + save_loc + '/i2.png')

    flow_HW2 = net.getNumpyFlow(img1, img2)

    cv2.imwrite(save_loc + '/gflow.png', cvtFlow2Color(flow_HW2))

    writeFlow(flow_HW2, save_loc + '/gflow.flo')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} [dir_loc]'.format(sys.argv[0]))
        sys.exit(1)
    else:
        dir_loc = sys.argv[1]

    # dir_loc = 'data/Map_v1/rs/00/'

    img1_path = dir_loc + '/gs.png'
    img2_path = dir_loc + '/rs.png'

    model_tag = 'GLNoWarp4YTBB'
    model_path = '/home/jerin/HDD-1/jerin/CVPR22/GlobalFlownets'
    openfile = open(f'{model_path}/{model_tag}/config.json', 'r')
    config = json.load(openfile)
    config = config['GlobalNetModelParameters']
    net = getGlobalPWCModel(config, f'{model_path}/{model_tag}/-1.pth')

    run(net, dir_loc + '/gs.png', dir_loc + '/rs_0.png', dir_loc + '/gs_rs_0')
    run(net, dir_loc + '/gs.png', dir_loc + '/rs_1.png', dir_loc + '/gs_rs_1')
    run(net, dir_loc + '/gs.png', dir_loc + '/rs_2.png', dir_loc + '/gs_rs_2')
    run(net, dir_loc + '/rs_0.png', dir_loc + '/rs_1.png', dir_loc + '/rs_0_rs_1')
    run(net, dir_loc + '/rs_0.png', dir_loc + '/rs_2.png', dir_loc + '/rs_0_rs_2')
    run(net, dir_loc + '/rs_1.png', dir_loc + '/rs_2.png', dir_loc + '/rs_1_rs_2')
