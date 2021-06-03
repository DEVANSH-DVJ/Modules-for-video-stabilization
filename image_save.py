import sys
import time

import numpy as np
from PIL import Image, ImageOps

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from objloader import OBJ

width, height = (250, 250)
img2obj_map = None
img2img_map = None


def img2obj():
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    depths = glReadPixels(0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)

    img2obj_map = np.array([np.array([gluUnProject(i, j, depths[i][j], modelview, projection, viewport)
                           for j in range(width)]) for i in range(height)])

    print(img2obj_map[100][100])


def captureScreen(file_name):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, None)
    image = Image.frombytes('RGBA', (width, height), data)
    image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
    image.save(file_name, 'png')


def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(60, 1, 2.0, 50.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    obj1 = OBJ('data/capsule/capsule.obj', swapyz=False)
    obj2 = OBJ('data/Chest/Chest.obj', swapyz=False)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslate(0, -1, -6)
    # glTranslate(tx / 20., ty / 20., - zpos)
    glRotate(-60, 1, 0, 0)
    # glRotate(rx, 0, 1, 0)
    glCallList(obj1.gl_list)
    glPopMatrix()

    glPushMatrix()
    glTranslate(0, 1, -6)
    glCallList(obj2.gl_list)
    glPopMatrix()

    captureScreen('1.png')

    img2obj()

    # time.sleep(1)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslate(0, -1, -6)
    # glTranslate(tx / 20., ty / 20., - zpos)
    glRotate(-65, 1, 0, 0)
    glRotate(5, 0, 1, 0)
    glCallList(obj1.gl_list)
    glPopMatrix()

    glPushMatrix()
    glTranslate(0, 1, -6)
    glRotate(5, 1, 0, 0)
    glRotate(-15, 0, 1, 0)
    glCallList(obj2.gl_list)
    glPopMatrix()

    captureScreen('2.png')
    # time.sleep(1)


if __name__ == '__main__':
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow('Projections')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    init()

    display()
