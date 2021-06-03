import sys

import numpy as np
from PIL import Image, ImageOps

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from objloader import OBJ

width, height = (500, 500)
img2obj_map = None
img2img_map = None


def img2obj():
    global img2obj_map
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    depths = glReadPixels(0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)

    img2obj_map = np.array([np.array([gluUnProject(i, j, depths[i][j], modelview, projection, viewport)
                           for j in range(width)]) for i in range(height)])


def img2img():
    global img2img_map
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    depths = np.ones((width, height)) * 0.95
    prevx = -np.ones((width, height), dtype=int)
    prevy = -np.ones((width, height), dtype=int)
    img2img_map = -np.ones((width, height, 3))

    for i in range(width):
        for j in range(height):
            pixel = gluProject(*img2obj_map[i][j], modelview, projection, viewport)
            if pixel[2] < depths[i][j]:
                img2img_map[i][j] = pixel
                x, y, z = int(pixel[0]), int(pixel[1]), pixel[2]
                if prevx[x][y] != -1:
                    img2img_map[prevx[x][y]][prevy[x][y]] = np.array([-1., -1., -1.])
                prevx[x][y], prevy[x][y] = i, j
                depths[x][y] = z


def warp():
    I2 = glReadPixels(0, 0, width, height, GL_RGB, GL_FLOAT, None)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    warped = np.zeros_like(I2)
    for i in range(width):
        for j in range(height):
            if img2img_map[i][j][0] != -1:
                warped[i][j] = I2[int(img2img_map[i][j][0])][int(img2img_map[i][j][1])]

    glDrawPixels(height, width, GL_RGB, GL_FLOAT, warped)


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

    captureScreen('output/I1.png')

    img2obj()

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

    captureScreen('output/I2.png')

    img2img()

    warp()

    captureScreen('output/WARP.png')


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
