import sys

import numpy as np
from PIL import Image, ImageOps

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from objloader import OBJ

import numba as nb

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
    winx = 0
    winy = 100
    v = np.array([2.0 * (winx - viewport[0]) / viewport[2] - 1.0, 2.0 * (winy -
                 viewport[1]) / viewport[3] - 1.0, 2.0 * depths[winy][winx] - 1.0, 1.0])
    print(v.shape)
    A = np.linalg.inv(projection.T.dot(modelview.T))
    print(A)
    v_ = A.dot(v)
    print(v_)
    v_ = v_ / v_[3]
    print(v_)
    pixel = gluUnProject(
        winx, winy, depths[winy][winx], modelview, projection, viewport)
    print("Pixel:", pixel)

    img2obj_map = np.array([np.array(
        [gluUnProject(j, i, depths[i][j], modelview, projection, viewport)
         for j in range(size)]) for i in range(size)])


@nb.jit(nopython=True)
def unproject(depths, size, modelview, projection, viewport):
    img2obj_map = np.empty((size, size, 3))
    A = np.linalg.inv(projection.T.dot(modelview.T))
    for i in range(size):
        for j in range(size):
            v = np.array([2.0 * (j - viewport[0]) / viewport[2] - 1.0,
                          2.0 * (i - viewport[1]) / viewport[3] - 1.0,
                          2.0 * depths[i][j] - 1.0, 1.0])
            v_ = A.dot(v)
            img2obj_map[i][j] = v_[:3]/v_[3]
    return img2obj_map


def img2img():
    global img2img_map

    depths = np.ones((size, size)) * 0.95
    prevx = -np.ones((size, size), dtype=int)
    prevy = -np.ones((size, size), dtype=int)
    img2img_map = -np.ones((size, size, 3))

    v = np.array([img2obj_map[0][0][0], img2obj_map[0][0][1], img2obj_map[0][0][2], 1.0])
    print(projection.T)
    print(modelview.shape)
    print(v.shape)
    print(modelview.T.dot(v))
    v_ = projection.T.dot(modelview.T).dot(v)
    v_ = v_/v_[3]
    print((v_[0]*0.5+0.5)*viewport[2]+viewport[0])
    print((v_[1]*0.5+0.5)*viewport[3]+viewport[1])
    print((1.0+v_[2])*0.5)
    pixel = gluProject(*img2obj_map[0][0], modelview, projection, viewport)
    print("Pixel:", pixel)

    for i in range(size):
        for j in range(size):
            pixel = gluProject(*img2obj_map[i][j], modelview, projection, viewport)
            x, y, z = round(pixel[0]), round(pixel[1]), pixel[2]
            if x < size and y < size and x >= 0 and y >= 0:
                if z < depths[x][y]:
                    img2img_map[i][j] = pixel


@nb.jit(nopython=True)
def project(img2obj_map, size, modelview, projection, viewport):
    img2img_map = -np.ones((size, size, 3))
    A = projection.T.dot(modelview.T)
    for i in range(size):
        for j in range(size):
            v_ = A.dot(np.array(
                [img2obj_map[i][j][0], img2obj_map[i][j][1], img2obj_map[i][j][2], 1.0]))
            v_ = v_ / v_[3]
            pixel = [(1.0 + v_[0]) * 0.5 * viewport[2] + viewport[0], (1.0 + v_[1])
                     * 0.5 * viewport[3] + viewport[1], (1.0 + v_[2]) * 0.5]
            x, y, z = round(pixel[0]), round(pixel[1]), pixel[2]
            if x < size and y < size and x >= 0 and y >= 0:
                if z < 0.95:
                    img2img_map[i][j] = pixel
    return img2img_map


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

    # img2obj()
    depths = glReadPixels(0, 0, size, size, GL_DEPTH_COMPONENT, GL_FLOAT)
    img2obj_map = unproject(depths, size, modelview, projection, viewport)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslate(0, -1, -4)
    glRotate(-70, 0, 1, 0)
    glCallList(obj.gl_list)

    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    glPopMatrix()

    captureScreen('./output/warping/I2.png')

    # img2img()
    img2img_map = project(img2obj_map, size, modelview, projection, viewport)

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

    for i in range(10):
        display(obj)
