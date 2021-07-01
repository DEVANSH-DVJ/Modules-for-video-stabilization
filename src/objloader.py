import os

from PIL import Image, ImageOps

import OpenGL.GL as GL

from utils import log


def MTL(filename):
    """
    Loads a Wavefront MTL file.
    """
    dir = os.path.dirname(filename)
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise (ValueError, "mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = ImageOps.flip(Image.open(os.path.join(dir, mtl['map_Kd'])))
            image = surf.convert('RGBA').tobytes()
            ix, iy = surf.size
            texid = mtl['texture_Kd'] = GL.glGenTextures(1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texid)
            GL.glTexParameteri(
                GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(
                GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix,
                            iy, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = list(map(float, values[1:]))
    return contents


class OBJ:
    def __init__(self, filename, swapyz=False):
        """
        Loads a Wavefront OBJ file.
        """
        dir = os.path.dirname(filename)
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(os.path.join(dir, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = GL.glGenLists(1)
        GL.glNewList(self.gl_list, GL.GL_COMPILE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glFrontFace(GL.GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                GL.glBindTexture(GL.GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                GL.glColor(*mtl['Kd'])

            GL.glBegin(GL.GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    GL.glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    GL.glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                GL.glVertex3fv(self.vertices[vertices[i] - 1])
            GL.glEnd()
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glEndList()
