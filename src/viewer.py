import sys

import pygame
from pygame.locals import *
from pygame.constants import *

import OpenGL.GL as GL
import OpenGL.GLU as GLU

from objloader import OBJ

pygame.init()
viewport = (512, 512)
hx = viewport[0] / 2
hy = viewport[1] / 2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

obj = OBJ(sys.argv[1], swapyz=False)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(60.0, width / float(height), 2.0, 10000.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5
rotate = move = False
while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos = zpos - 1
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                ry += i
                rx += j
            elif move:
                tx += i
                ty -= j

    glClearColor(0.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # RENDER OBJECT
    glPushMatrix()
    glRotate(rx, 1, 0, 0)
    glRotate(ry, 0, 1, 0)
    glTranslate(tx / 20., ty / 20., - zpos)
    glCallList(obj.gl_list)
    glPopMatrix()

    print(tx / 20, ty / 20, -zpos, rx, ry)
    pygame.display.flip()
