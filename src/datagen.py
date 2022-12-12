import os
import sys

import numpy as np
import pandas as pd

import OpenGL.GL as GL

from gl import capture, init, start
from motion import genflow, project, unproject
from movie import movie_save
from objloader import OBJ
from utils import config_load, flag_save, flow_save, log, frameset_save

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


def frameset(setpoint, sigma, n, seed=0):
    return {
        'x': np.linspace(setpoint['x1'], setpoint['x2'], num=n),
        'dx': np.random.normal(0, sigma['x'], size=(n,)),
        'y': np.linspace(setpoint['y1'], setpoint['y2'], num=n),
        'dy': np.random.normal(0, sigma['y'], size=(n,)),
        'z': np.linspace(setpoint['z1'], setpoint['z2'], num=n),
        'dz': np.random.normal(0, sigma['z'], size=(n,)),
        'rx': np.linspace(setpoint['rx1'], setpoint['rx2'], num=n),
        'drx': np.random.normal(0, sigma['rx'], size=(n,)),
        'ry': np.linspace(setpoint['ry1'], setpoint['ry2'], num=n),
        'dry': np.random.normal(0, sigma['ry'], size=(n,)),
        'rz': np.linspace(setpoint['rz1'], setpoint['rz2'], num=n),
        'drz': np.random.normal(0, sigma['rz'], size=(n,))
    }


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python {} <config_file> [-preview]'.format(sys.argv[0]))
        exit(1)
    else:
        config_file = os.path.abspath(sys.argv[1])
        obj_dir = os.path.dirname(config_file)
        if len(sys.argv) > 2 and sys.argv[2] == '-preview':
            preview = True
        else:
            preview = False

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

    log('Reading setpoints csv;')
    setpoints_path = '{}/{}'.format(obj_dir, configs['setpoints'])
    setpoints = pd.read_csv(setpoints_path)
    n = len(setpoints.index)

    log('Saving arguments for rendering;')
    nframes = configs['nframes']
    sigma = configs['sigma']
    fps = configs['fps']
    zmax = 1 - configs['camera']['zNear'] / configs['camera']['zFar']
    bgcolor = configs['bgcolor']
    scale = configs['scale']

    for isp, setpoint in setpoints.iterrows():
        out_dir = '{}/output/{:02}'.format(obj_dir, isp)
        os.system('mkdir -p "{}"'.format(out_dir))
        if not preview:
            os.system('rm -rf "{0}/flow" "{0}/flag"'.format(out_dir))
            os.system('mkdir -p "{0}/flow" "{0}/flag"'.format(out_dir))

        log('Calculating frames for Setpoint {:02};'.format(isp))
        frames = frameset(setpoint, sigma, nframes)
        frameset_save(frames, '{}/frames.csv'.format(out_dir),
                      '{}/frames.png'.format(out_dir))

        video_s = np.empty((nframes, size, size, 4), dtype='uint8')
        video_u = np.empty((nframes, size, size, 4), dtype='uint8')
        log('Starting rendering for Setpoint {:02};'.format(isp))
        for i in range(nframes):
            display(obj, bgcolor,
                    frames['x'][i],
                    frames['y'][i],
                    frames['z'][i],
                    frames['rx'][i],
                    frames['ry'][i],
                    frames['rz'][i])
            video_s[i] = capture(size)
            if not preview:
                depths = GL.glReadPixels(
                    0, 0, size, size, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
                background = np.flipud(depths == 1.0)
                s2obj = unproject(depths, size, modelview, projection, viewport)
            display(obj, bgcolor,
                    frames['x'][i] + frames['dx'][i],
                    frames['y'][i] + frames['dy'][i],
                    frames['z'][i] + frames['dz'][i],
                    frames['rx'][i] + frames['drx'][i],
                    frames['ry'][i] + frames['dry'][i],
                    frames['rz'][i] + frames['drz'][i])
            video_u[i] = capture(size)
            if not preview:
                s2u = project(s2obj, size, modelview, projection, viewport)
                flow, outside = genflow(s2u, size)
                flow_save(flow, '{}/flow/{:06}.flo'.format(out_dir, i))
                flag_save(background, outside, size,
                          '{}/flag/{:06}.png'.format(out_dir, i))

        log('Starting movie conversion for Setpoint {:02};'.format(isp))
        movie_save(video_s, fps, '{}/s.mp4'.format(out_dir))
        movie_save(video_u, fps, '{}/u.mp4'.format(out_dir))

    log('End;')
