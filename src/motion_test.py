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


if __name__ == '__main__':
    np.random.seed(0)

    size = 512
    depths = np.random.rand(size, size).astype(np.float32)
    modelview = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [-14.39999962, -1.5, 0, 1]])
    projection = np.array([[1.73205078, 0, 0, 0],
                           [0, 1.73205078, 0, 0],
                           [0, 0, -1.00020003, -1],
                           [0, 0, -2.00020003, 0]])
    viewport = np.array([0, 0, size, size]).astype(np.int32)

    img2obj_map = unproject(depths, size, modelview, projection, viewport)
    img2obj_map_test = unproject_test(depths, size, modelview, projection, viewport)
    print(img2obj_map.shape, img2obj_map_test.shape)
    diff = img2obj_map - img2obj_map_test
    thresh = 10e-10
    print(np.sum(np.abs(diff) > thresh))
    print(np.abs(diff).max())

    img2img_map = project(img2obj_map, size, modelview, projection, viewport)
    img2img_map_test = project_test(img2obj_map_test, size, modelview, projection, viewport)
    print(img2img_map.shape, img2img_map_test.shape)
    diff = img2img_map - img2img_map_test
    thresh = 1
    print(np.sum(np.abs(diff) > thresh))
    print(np.abs(diff).max())
