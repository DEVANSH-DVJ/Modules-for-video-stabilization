import os
import sys
from time import sleep

import pandas as pd
import yaml
from PIL import Image, ImageOps

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from objloader import OBJ

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()

    GL.glPushMatrix()

    GL.glTranslate(x, y, z)
    GL.glRotate(rx, 1, 0, 0)
    GL.glRotate(ry, 0, 1, 0)
    GL.glRotate(rz, 0, 0, 1)
    GL.glCallList(obj.gl_list)

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

    config_file = 'config1.yaml'
    config_path = base_dir + '/params/configs/' + config_file
    configs = yaml.load(open(config_path), Loader=yaml.FullLoader)

    init(configs['camera'])

    obj_path = base_dir + '/data/' + configs['obj']
    obj = OBJ(obj_path, swapyz=False)

    frameset_file = 'frameset1.csv'
    frameset_path = base_dir + '/params/framesets/' + frameset_file
    frames = pd.read_csv(frameset_path)
    print(len(frames.index))
    print(frames)

    for i in range(len(frames.index)):
        display(obj,
                frames['x1'][i], frames['y1'][i], frames['z1'][i],
                frames['rx1'][i], frames['ry1'][i], frames['rz1'][i])
        captureScreen('test_res/s{:03}.bmp'.format(i), size)
        sleep(1)
        print(i)
        display(obj,
                frames['x2'][i], frames['y2'][i], frames['z2'][i],
                frames['rx2'][i], frames['ry2'][i], frames['rz2'][i])
        captureScreen('test_res/u{:03}.bmp'.format(i), size)
        sleep(1)
