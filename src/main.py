import sys
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT


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
