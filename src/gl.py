import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT


def init(cam):
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(cam['fovy'], cam['aspect'], cam['zNear'], cam['zFar'])

    GL.glMatrixMode(GL.GL_MODELVIEW)


def start(size, argv):
    GLUT.glutInit(argv)

    GLUT.glutInitDisplayMode(GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(size, size)
    GLUT.glutInitWindowPosition(0, 0)
    GLUT.glutCreateWindow('Projections')

    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
