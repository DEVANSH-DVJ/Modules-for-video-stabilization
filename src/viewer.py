import os
import sys

import numpy as np
import yaml

import pygame
import pygame.constants as pygc

import OpenGL.GL as GL

from objloader import OBJ
from gl import init


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
    return yaw(rz).dot(pitch(ry).dot(roll(rx).dot(vec)))


pygame.init()
size = 512
pygame.display.set_mode((size, size), pygc.OPENGL | pygc.DOUBLEBUF)

obj = OBJ(sys.argv[1], swapyz=False)

clock = pygame.time.Clock()

init({'fovy': 60, 'aspect': 1, 'zNear': 1.0, 'zFar': 10000.0})

rx, ry, rz = (0., 0., 0.)
pos = [0., 0., -5.]
rotate, move = False, False
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
                pos += pointing(-rx*np.pi/180, -ry*np.pi /
                                180, -rz*np.pi/180, [0, 0, 1])
            elif event.button == 5:
                pos -= pointing(-rx*np.pi/180, -ry*np.pi /
                                180, -rz*np.pi/180, [0, 0, 1])
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
                pos += (i / 20.) * pointing(-rx*np.pi/180,
                                            -ry*np.pi/180,
                                            -rz*np.pi/180,
                                            [1, 0, 0])
                pos -= (j / 20.) * pointing(-rx*np.pi/180,
                                            -ry*np.pi/180,
                                            -rz*np.pi/180,
                                            [0, 1, 0])

    pos = np.around(pos, 3)
    GL.glClearColor(0.0, 1.0, 1.0, 1.0)
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

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python {} <config_file>'.format(sys.argv[0]))
        exit(1)
    else:
        config_file = sys.argv[1]
        obj_dir = os.path.dirname(config_file)

    configs = yaml.load(open(config_file), Loader=yaml.FullLoader)

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
                    pos += pointing(-rx*np.pi/180, -ry*np.pi /
                                    180, -rz*np.pi/180, [0, 0, 1])
                elif event.button == 5:
                    pos -= pointing(-rx*np.pi/180, -ry*np.pi /
                                    180, -rz*np.pi/180, [0, 0, 1])
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
                    pos += (i / 20.) * pointing(-rx*np.pi/180,
                                                -ry*np.pi/180,
                                                -rz*np.pi/180,
                                                [1, 0, 0])
                    pos -= (j / 20.) * pointing(-rx*np.pi/180,
                                                -ry*np.pi/180,
                                                -rz*np.pi/180,
                                                [0, 1, 0])
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
