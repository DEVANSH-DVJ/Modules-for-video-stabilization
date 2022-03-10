import os
import sys

import numpy as np
import pandas as pd

import OpenGL.GL as GL

from gl import capture, init, start
from objloader import OBJ
from utils import config_load, log, frameset_save, save_image

projection = None
modelview = None
viewport = None


def display(obj, bgcolor, x, y, z, rx, ry, rz):
    global projection, modelview, viewport

    GL.glClearColor(*bgcolor)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()

    GL.glPushMatrix()

    GL.glRotate(rx, 1, 0, 0)
    GL.glRotate(ry, 0, 1, 0)
    GL.glRotate(rz, 0, 0, 1)
    GL.glTranslate(x, y, z)
    GL.glCallList(obj.gl_list)

    projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)
    modelview = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)
    viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)

    GL.glPopMatrix()

    GL.glFlush()


def disturb(sigma, n):
    return np.random.normal(0, sigma, size=(n,))


def smoothen(x, window):
    return np.array(pd.Series(x).rolling(window=window).mean().dropna())


def frameset(setpoint, sigma, n):
    win = int(n / 10)
    np.random.seed(int(setpoint['seed']))
    return {
        'x': setpoint['x'] + smoothen(disturb(sigma['x'], n + win - 1), win),
        'y': setpoint['y'] + smoothen(disturb(sigma['y'], n + win - 1), win),
        'z': setpoint['z'] + smoothen(disturb(sigma['z'], n + win - 1), win),
        'rx': setpoint['rx'] + smoothen(disturb(sigma['rx'], n + win - 1), win),
        'ry': setpoint['ry'] + smoothen(disturb(sigma['ry'], n + win - 1), win),
        'rz': setpoint['rz'] + smoothen(disturb(sigma['rz'], n + win - 1), win)
    }


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python {} <config_file>'.format(sys.argv[0]))
        exit(1)
    else:
        config_file = os.path.abspath(sys.argv[1])
        obj_dir = os.path.dirname(config_file)

    log('Start;')
    log('Loading config file;')
    configs = config_load(config_file)

    log('Starting GL Window;')
    size = configs['size']
    start(size, sys.argv)

    log('Initializing camera;')
    init(configs['camera'])

    obj_path = '{}/{}'.format(obj_dir, configs['obj'])
    obj = OBJ(obj_path, swapyz=configs['swapyz'])

    log('Reading rs_base csv;')
    rs_base_path = '{}/{}'.format(obj_dir, configs['rs_base'])
    rs_base = pd.read_csv(rs_base_path)
    n = len(rs_base.index)

    log('Saving arguments for rendering;')
    sigma = configs['sigma']
    bgcolor = configs['bgcolor']

    for isp, rs_center in rs_base.iterrows():
        out_dir = '{}/rs/{:02}'.format(obj_dir, isp)
        os.system('mkdir -p "{}"'.format(out_dir))
        os.system('rm -rf "{0}/raw"'.format(out_dir))
        os.system('mkdir -p "{0}/raw"'.format(out_dir))

        log('Calculating frames for RS {:02};'.format(isp))
        frames = frameset(rs_center, sigma, size)
        frameset_save(frames, '{}/frames.csv'.format(out_dir),
                      '{}/frames.png'.format(out_dir))

        rs_image = np.ndarray((size, size, 4), dtype=np.uint8)
        log('Starting rendering for RS {:02};'.format(isp))
        for i in range(size):
            display(obj, bgcolor,
                    frames['x'][i],
                    frames['y'][i],
                    frames['z'][i],
                    frames['rx'][i],
                    frames['ry'][i],
                    frames['rz'][i])
            temp = capture(size)

            rs_image[i, :, :] = temp[i, :, :]
            save_image(temp, '{}/raw/{:04}.png'.format(out_dir, i))

        os.system('cp "{}/raw/0000.png" "{}/gs.png"'.format(out_dir, out_dir))
        save_image(rs_image, '{}/rs.png'.format(out_dir))

    log('End;')
