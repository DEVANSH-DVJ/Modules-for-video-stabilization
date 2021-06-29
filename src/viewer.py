import sys

import pygame
import pygame.constants as pygc

import OpenGL.GL as GL
import OpenGL.GLU as GLU

from objloader import OBJ

pygame.init()
size = 512
srf = pygame.display.set_mode((size, size), pygc.OPENGL | pygc.DOUBLEBUF)

obj = OBJ(sys.argv[1], swapyz=False)

clock = pygame.time.Clock()

GL.glMatrixMode(GL.GL_PROJECTION)
GL.glLoadIdentity()
GLU.gluPerspective(60.0, 1.0, 2.0, 10000.0)
GL.glEnable(GL.GL_DEPTH_TEST)
GL.glMatrixMode(GL.GL_MODELVIEW)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5
rotate, move = False, False
while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygc.QUIT:
            sys.exit()
        elif e.type == pygc.KEYDOWN and e.key == pygc.K_ESCAPE:
            sys.exit()
        elif e.type == pygc.MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos -= 1
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == pygc.MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == pygc.MOUSEMOTION:
            i, j = e.rel
            if rotate:
                ry += i
                rx += j
            elif move:
                tx += i
                ty -= j

    GL.glClearColor(0.0, 1.0, 1.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()

    GL.glPushMatrix()
    GL.glRotate(rx, 1, 0, 0)
    GL.glRotate(ry, 0, 1, 0)
    GL.glTranslate(tx / 20., ty / 20., -zpos)
    GL.glCallList(obj.gl_list)
    GL.glPopMatrix()

    pygame.display.flip()
    print(tx / 20., ty / 20., -zpos, rx, ry)
