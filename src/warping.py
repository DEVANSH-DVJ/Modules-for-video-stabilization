import numpy as np
from PIL import Image


def warp(in_path, mv, warp_path, size):
    I2 = np.array(Image.open(in_path))

    warped = np.empty((size, size, 4), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            if mv[i][j][0] != -1:
                warped[i][j] = I2[round(mv[i][j][1])][round(mv[i][j][0])]
            else:
                warped[i][j] = np.array([0, 0, 0, 255], dtype=np.uint8)

    Image.fromarray(warped).save(warp_path, 'png')
