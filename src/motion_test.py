import numpy as np

import OpenGL.GLU as GLU

from motion import project, unproject


def project_test(img2obj_map, size, modelview, projection, viewport):
    depths = np.ones((size, size)) * 0.99999999
    img2img_map = -np.ones((size, size, 3))

    for i in range(size):
        for j in range(size):
            pixel = GLU.gluProject(*img2obj_map[i][j], modelview, projection, viewport)
            x, y, z = round(pixel[0]), round(pixel[1]), pixel[2]
            if x < size and y < size and x >= 0 and y >= 0:
                if z < depths[x][y]:
                    img2img_map[i][j] = pixel

    return img2img_map


def unproject_test(depths, size, modelview, projection, viewport):
    img2obj_map = np.array([np.array(
        [GLU.gluUnProject(j, i, depths[i][j], modelview, projection, viewport)
         for j in range(size)]) for i in range(size)])

    return img2obj_map

