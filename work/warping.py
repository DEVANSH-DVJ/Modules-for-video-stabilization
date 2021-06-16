import sys

import numpy as np
from PIL import Image, ImageOps

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from objloader import OBJ

size = 512
size1 = size - 1
img2obj_map = None
img2img_map = None
projection = None
modelview = None
viewport = None


def img2obj():
    global img2obj_map

    depths = glReadPixels(0, 0, size, size, GL_DEPTH_COMPONENT, GL_FLOAT)

    img2obj_map = np.array([np.array(
        [gluUnProject(j, i, depths[i][j], modelview, projection, viewport)
         for j in range(size)]) for i in range(size)])


def img2img():
    global img2img_map

    depths = np.ones((size, size)) * 0.95
    prevx = -np.ones((size, size), dtype=int)
    prevy = -np.ones((size, size), dtype=int)
    img2img_map = -np.ones((size, size, 3))

    for i in range(size):
        for j in range(size):
            pixel = gluProject(*img2obj_map[i][j], modelview, projection, viewport)
            x, y, z = round(pixel[0]), round(pixel[1]), pixel[2]
            if x < size and y < size and x >= 0 and y >= 0:
                if z < depths[x][y]:
                    img2img_map[i][j] = pixel



def warp():
    I2 = glReadPixels(0, 0, size, size, GL_RGBA, GL_FLOAT, None)

    glClearColor(0.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    warped = np.zeros_like(I2)
    for i in range(size):
        for j in range(size):
            if img2img_map[i][j][0] != -1:
                warped[i][j] = I2[round(img2img_map[i][j][1])][round(img2img_map[i][j][0])]

    glDrawPixels(size, size, GL_RGBA, GL_FLOAT, warped)


def warp2():
    I2 = np.array(Image.open("./output/warping/I2.png"))

    warped = np.empty((size, size, 4), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            if img2img_map[i][j][0] != -1:
                warped[size1 - i][j] = I2[size1 - round(img2img_map[i][j][1])][round(img2img_map[i][j][0])]
            else:
                warped[size1 - i][j] = np.array([0, 0, 0, 255], dtype=np.uint8)

    Image.fromarray(warped).save('./output/warping/Warp.png', 'png')


def captureScreen(file_name):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, size, size, GL_RGBA, GL_UNSIGNED_BYTE, None)
    image = Image.frombytes('RGBA', (size, size), data)
    image = ImageOps.flip(image)
    image.save(file_name, 'png')


def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(60, 1, 2.0, 50.0)
    glMatrixMode(GL_MODELVIEW)


def display(obj):
    global projection, modelview, viewport, img2img_map

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslate(0, -1, -4)
    glRotate(-60, 0, 1, 0)
    glCallList(obj.gl_list)

    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    glPopMatrix()

    captureScreen('./output/warping/I1.png')

    img2obj()

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslate(0, -1, -4)
    glRotate(-70, 0, 1, 0)
    # glRotate(5, 0, 1, 0)
    glCallList(obj.gl_list)

    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    glPopMatrix()

    captureScreen('./output/warping/I2.png')

    img2img()

    warp()

    captureScreen('./output/warping/WARP.png')

    warp2()


if __name__ == '__main__':
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(size, size)
    glutInitWindowPosition(0, 0)
    glutCreateWindow('Projections')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    init()

    obj = OBJ('../data/Chest/Chest.obj', swapyz=False)

    display(obj)
