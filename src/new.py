import os
import sys

import pandas as pd
from PIL import Image, ImageOps

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from motion import project, unproject
from movie import movie_save
from objloader import OBJ
from warping import warp_save
from utils import config_load

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
projection = None
modelview = None
viewport = None


def init(cam):
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(cam['fovy'], cam['aspect'], cam['zNear'], cam['zFar'])

    GL.glMatrixMode(GL.GL_MODELVIEW)


def start(size):
    GLUT.glutInit(sys.argv)

    GLUT.glutInitDisplayMode(GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(size, size)
    GLUT.glutInitWindowPosition(0, 0)
    GLUT.glutCreateWindow('Projections')

    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)


def display(obj, x, y, z, rx, ry, rz):
    global projection, modelview, viewport

    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()

    GL.glPushMatrix()

    GL.glTranslate(x, y, z)
    GL.glRotate(rx, 1, 0, 0)
    GL.glRotate(ry, 0, 1, 0)
    GL.glRotate(rz, 0, 0, 1)
    GL.glCallList(obj.gl_list)

    projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)
    modelview = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)
    viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)

    GL.glPopMatrix()

    GL.glFlush()


def captureScreen(file_name, size):
    data = GL.glReadPixels(0, 0, size, size, GL.GL_RGBA,
                           GL.GL_UNSIGNED_BYTE, None)
    image = Image.frombytes('RGBA', (size, size), data)
    image = ImageOps.flip(image)
    image.save(file_name, 'png')


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python {} <config_file>'.format(sys.argv[0]))
        exit(1)
    else:
        config_file = os.path.abspath(sys.argv[1])
        obj_dir = os.path.dirname(config_file)

    configs = config_load(config_file)

    size = configs['size']
    fps = configs['fps']
    zmax = 1 - configs['camera']['zNear']/configs['camera']['zFar']
    start(size)

    init(configs['camera'])

    obj_path = '{0}/data/{1}/{1}.obj'.format(base_dir, configs['obj'])
    obj = OBJ(obj_path, swapyz=False)

    frameset_file = configs['frameset']
    frameset_path = '{}/framesets/{}.csv'.format(base_dir, frameset_file)
    frames = pd.read_csv(frameset_path)
    n = len(frames.index)

    out_dir = '{}/../output/{}'.format(base_dir, config_file)
    img_dir = out_dir + '/img'
    os.system('mkdir -p ' + img_dir)

    for i in range(n):
        display(obj,
                frames['x'][i],
                frames['y'][i],
                frames['z'][i],
                frames['rx'][i],
                frames['ry'][i],
                frames['rz'][i])
        captureScreen('{}/s{:03}.png'.format(img_dir, i), size)
        depths = GL.glReadPixels(
            0, 0, size, size, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
        s2obj = unproject(depths, size, modelview, projection, viewport)
        display(obj,
                frames['x'][i] + frames['dx'][i],
                frames['y'][i] + frames['dy'][i],
                frames['z'][i] + frames['dz'][i],
                frames['rx'][i] + frames['drx'][i],
                frames['ry'][i] + frames['dry'][i],
                frames['rz'][i] + frames['drz'][i])
        captureScreen('{}/u{:03}.png'.format(img_dir, i), size)
        s2u = project(s2obj, size, modelview, projection, viewport, zmax)
        warp_save('{}/u{:03}.png'.format(img_dir, i), s2u,
                  '{}/ws{:03}.png'.format(img_dir, i), size)

    movie_save(['{}/s{:03}.png'.format(img_dir, i) for i in range(n)], fps,
               '{}/s.mp4'.format(out_dir))
    movie_save(['{}/u{:03}.png'.format(img_dir, i) for i in range(n)], fps,
               '{}/u.mp4'.format(out_dir))
    movie_save(['{}/ws{:03}.png'.format(img_dir, i) for i in range(n)], fps,
               '{}/ws.mp4'.format(out_dir))
