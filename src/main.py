import os
import sys

import pandas as pd
import yaml
from PIL import Image, ImageOps

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from motion import project, unproject
from movie import movie_save
from objloader import OBJ
from warping import warp_save

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
    size = 512

    start(size)

    config_file = 'config1'
    config_path = '{}/params/configs/{}.yaml'.format(base_dir, config_file)
    configs = yaml.load(open(config_path), Loader=yaml.FullLoader)

    init(configs['camera'])

    obj_path = '{}/data/{}.obj'.format(base_dir, configs['obj'])
    obj = OBJ(obj_path, swapyz=False)

    frameset_file = 'frameset1'
    frameset_path = '{}/params/framesets/{}.csv'.format(base_dir, frameset_file)
    frames = pd.read_csv(frameset_path)
    n = len(frames.index)

    out_dir = '{}/output/{}_{}'.format(base_dir, config_file, frameset_file)
    img_dir = out_dir + '/img'
    os.system('mkdir -p ' + img_dir)

    for i in range(n):
        display(obj,
                frames['x1'][i], frames['y1'][i], frames['z1'][i],
                frames['rx1'][i], frames['ry1'][i], frames['rz1'][i])
        captureScreen('{}/s{:03}.png'.format(img_dir, i), size)
        depths = GL.glReadPixels(
            0, 0, size, size, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
        s2obj = unproject(depths, size, modelview, projection, viewport)
        display(obj,
                frames['x2'][i], frames['y2'][i], frames['z2'][i],
                frames['rx2'][i], frames['ry2'][i], frames['rz2'][i])
        captureScreen('{}/u{:03}.png'.format(img_dir, i), size)
        s2u = project(s2obj, size, modelview, projection, viewport)
        warp_save('{}/u{:03}.png'.format(img_dir, i), s2u,
                  '{}/ws{:03}.png'.format(img_dir, i), size)

    movie_save(['{}/s{:03}.png'.format(img_dir, i) for i in range(n)], 1,
               '{}/s.mp4'.format(out_dir))
    movie_save(['{}/u{:03}.png'.format(img_dir, i) for i in range(n)], 1,
               '{}/u.mp4'.format(out_dir))
    movie_save(['{}/ws{:03}.png'.format(img_dir, i) for i in range(n)], 1,
               '{}/ws.mp4'.format(out_dir))
