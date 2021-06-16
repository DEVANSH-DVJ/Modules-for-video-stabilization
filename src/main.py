import sys
import yaml

import OpenGL.GL as GL
import OpenGL.GLUT as GLUT

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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