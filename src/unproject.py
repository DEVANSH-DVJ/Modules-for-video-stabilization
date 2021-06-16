import numpy as np


def unproject(depths, size, modelview, projection, viewport):
    img2obj_map = np.empty((size, size, 3))
    A = np.linalg.inv(projection.T.dot(modelview.T))
    for i in range(size):
        for j in range(size):
            v = np.array([2.0 * (j - viewport[0]) / viewport[2] - 1.0,
                          2.0 * (i - viewport[1]) / viewport[3] - 1.0,
                          2.0 * depths[i][j] - 1.0, 1.0])
            v_ = A.dot(v)
            img2obj_map[i][j] = v_[:3] / v_[3]
    return img2obj_map
