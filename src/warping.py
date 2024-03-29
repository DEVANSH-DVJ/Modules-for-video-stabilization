import numba as nb
import numpy as np
from PIL import Image


@nb.njit
def warp(I2, mv, size):
    warped = np.empty((size, size, 4), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            x = round(mv[i][j][1])
            y = round(mv[i][j][0])
            if x < size and y < size and x >= 0 and y >= 0:
                warped[i][j] = I2[x][y]
            else:
                warped[i][j] = np.array([255, 0, 0, 255], dtype=np.uint8)
    return warped


def warp_save(in_path, mv, warp_path, size):
    I2 = np.array(Image.open(in_path))

    warped = warp(I2, mv, size)

    Image.fromarray(warped).save(warp_path, 'png')
