import os
import sys
import functools

import numpy as np

import pygame
import pygame.constants as pygc

import OpenGL.GL as GL

from objloader import OBJ
from gl import init
from utils import config_load

d2r = np.pi/180


def roll(rx):
    return np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])


def pitch(ry):
    return np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])


def yaw(rz):
    return np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])


def pointing(rx, ry, rz, vec):
    return yaw(rz*d2r).dot(pitch(ry*d2r).dot(roll(rx*d2r).dot(vec)))


icap = functools.partial(pointing, vec=[1, 0, 0])
jcap = functools.partial(pointing, vec=[0, 1, 0])
kcap = functools.partial(pointing, vec=[0, 0, 1])

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python {} <config_file>'.format(sys.argv[0]))
        exit(1)
    else:
        config_file = os.path.abspath(sys.argv[1])
        obj_dir = os.path.dirname(config_file)

    configs = config_load(config_file)

    pygame.init()
    size = configs['size']
    pygame.display.set_mode((size, size), pygc.OPENGL | pygc.DOUBLEBUF)

    init(configs['camera'])

    obj_path = '{}/{}'.format(obj_dir, configs['obj'])
    obj = OBJ(obj_path, swapyz=False)

    loc = configs['initialize']
    rx, ry, rz = loc['rx'], loc['ry'], loc['rz']
    pos = [loc['x'], loc['y'], loc['z']]
    rotate, move = False, False

    bgcolor = configs['bgcolor']

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygc.QUIT:
                sys.exit()
            elif event.type == pygc.KEYDOWN:
                if event.key == pygc.K_ESCAPE:
                    sys.exit()
                elif event.key == pygc.K_LEFT:
                    rz += 1
                elif event.key == pygc.K_RIGHT:
                    rz -= 1
                elif event.key == pygc.K_a:
                    ry -= 1
                elif event.key == pygc.K_d:
                    ry += 1
                elif event.key == pygc.K_w:
                    rx -= 1
                elif event.key == pygc.K_s:
                    rx += 1
            elif event.type == pygc.MOUSEBUTTONDOWN:
                if event.button == 4:
                    pos += kcap(-rx, -ry, -rz)
                elif event.button == 5:
                    pos -= kcap(-rx, -ry, -rz)
                elif event.button == 1:
                    rotate = True
                elif event.button == 3:
                    move = True
            elif event.type == pygc.MOUSEBUTTONUP:
                if event.button == 1:
                    rotate = False
                elif event.button == 3:
                    move = False
            elif event.type == pygc.MOUSEMOTION:
                i, j = event.rel
                if rotate:
                    ry += i
                    rx += j
                elif move:
                    pos += (i / 20.) * icap(-rx, -ry, -rz)
                    pos -= (j / 20.) * jcap(-rx, -ry, -rz)
        pos = np.around(pos, 3)

        GL.glClearColor(*bgcolor)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()

        GL.glPushMatrix()
        GL.glRotate(rx, 1, 0, 0)
        GL.glRotate(ry, 0, 1, 0)
        GL.glRotate(rz, 0, 0, 1)
        GL.glTranslate(*pos)
        GL.glCallList(obj.gl_list)
        GL.glPopMatrix()

        pygame.display.flip()
        print(*pos, rx, ry, rz, sep=',', flush=True)
