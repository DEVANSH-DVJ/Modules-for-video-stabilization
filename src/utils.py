from datetime import datetime
from pytz import timezone
import yaml
import numpy as np
from PIL import Image


def log(message, debug=True):
    if debug:
        now = datetime.now(timezone('Asia/Kolkata'))
        now = now.strftime('%Y.%m.%d %H:%M:%S.%f %Z')
        print('{}: {}'.format(now, message))


def config_load(config_file):
    return yaml.load(open(config_file), Loader=yaml.FullLoader)


def flow_save(flow, flow_path):
    height, width, nBands = flow.shape
    assert nBands == 2, "Number of bands = {} != 2".format(nBands)
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    assert u.shape == v.shape, "Invalid flow shape"
    height, width = u.shape

    with open(flow_path, 'wb') as flow_file:
        np.array(width).astype(np.int32).tofile(flow_file)
        np.array(height).astype(np.int32).tofile(flow_file)
        tmp = np.zeros((height, width*nBands))
        tmp[:, np.arange(width)*2] = u
        tmp[:, np.arange(width)*2 + 1] = v
        tmp.astype(np.float32).tofile(flow_file)


def flow_load(flow_path):
    with open(flow_path, 'rb') as flow_file:
        w = np.fromfile(flow_file, np.int32, count=1)[0]
        h = np.fromfile(flow_file, np.int32, count=1)[0]

        flow = np.fromfile(flow_file, np.float32, count=h * w * 2)
        flow.resize((h, w, 2))

    return flow


def flag_save(background, outside, size, flag_file):
    flag = np.zeros((size, size, 4), dtype=np.uint8)
    flag[:, :, 0] = background*255
    flag[:, :, 1] = outside*255
    flag[:, :, 3] = 255
    Image.fromarray(flag).save(flag_file, 'png')
