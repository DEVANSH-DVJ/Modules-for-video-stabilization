import os
import sys
import yaml

import pandas as pd

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
