import numpy as np
from PIL import Image


def warp(in_path, motion, warp_path, size=512):
    I2 = np.array(Image.open(in_path))

    warped = np.empty((size, size, 4), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            if motion[i][j][0] != -1:
                warped[i][j] = I2[round(motion[i][j][1])][round(motion[i][j][0])]
            else:
                warped[i][j] = np.array([0, 0, 0, 255], dtype=np.uint8)

    Image.fromarray(warped).save(warp_path)
