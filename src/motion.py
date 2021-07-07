import numba as nb
import numpy as np


@nb.njit
def project(img2obj_map, size, modelview, projection, viewport, zmax):
    img2img_map = -np.ones((size, size, 3))
    A = projection.T.dot(modelview.T)
    for i in range(size):
        for j in range(size):
            v_ = A.dot(
                np.array(
                    [img2obj_map[i][j][0],
                     img2obj_map[i][j][1],
                     img2obj_map[i][j][2],
                     1.0]
                )
            )
            v_ = v_ / v_[3]
            pixel = [
                (1.0 + v_[0]) * 0.5 * viewport[2] + viewport[0],
                size - 1 - (1.0 + v_[1]) * 0.5 * viewport[3] + viewport[1],
                (1.0 + v_[2]) * 0.5
            ]
            img2img_map[size - 1 - i][j] = pixel

    return img2img_map


@nb.njit
def unproject(depths, size, modelview, projection, viewport):
    img2obj_map = np.empty((size, size, 3))
    A = np.linalg.inv(projection.T.dot(modelview.T))
    for i in range(size):
        for j in range(size):
            v = np.array(
                [2.0 * (j - viewport[0]) / viewport[2] - 1.0,
                 2.0 * (i - viewport[1]) / viewport[3] - 1.0,
                 2.0 * depths[i][j] - 1.0, 1.0]
            )
            v_ = A.dot(v)
            img2obj_map[i][j] = v_[:3] / v_[3]

    return img2obj_map


def genflow(s2u, size, zmax):
    flow = np.empty((size, size, 2))
    for i in range(size):
        for j in range(size):
            flow[i, j] = (s2u[i, j, 1] - i, s2u[i, j, 0] - j)
