import numpy as np


def project(img2obj_map, size, modelview, projection, viewport):
    img2img_map = -np.ones((size, size, 3))
    A = projection.T.dot(modelview.T)
    for i in range(size):
        for j in range(size):
            v_ = A.dot(np.array(
                [img2obj_map[i][j][0], img2obj_map[i][j][1], img2obj_map[i][j][2], 1.0]))
            v_ = v_ / v_[3]
            pixel = [(1.0 + v_[0]) * 0.5 * viewport[2] + viewport[0], (1.0 + v_[1])
                     * 0.5 * viewport[3] + viewport[1], (1.0 + v_[2]) * 0.5]
            x, y, z = round(pixel[0]), round(pixel[1]), pixel[2]
            if x < size and y < size and x >= 0 and y >= 0:
                if z < 0.95:
                    img2img_map[i][j] = pixel
    return img2img_map
