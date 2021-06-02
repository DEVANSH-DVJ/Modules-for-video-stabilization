import sys
import time

from PIL import Image, ImageOps

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from objloader import OBJ

width, height = (500, 500)


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
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    obj = OBJ('data/capsule/capsule.obj', swapyz=False)
    glTranslate(0, 0, -4)
    # glTranslate(tx / 20., ty / 20., - zpos)
    # glRotate(ry, 1, 0, 0)
    # glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)
    captureScreen('1.png')
    time.sleep(1)


if __name__ == '__main__':
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(20, 20)
    glutCreateWindow('Projections')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    init()

    display()
