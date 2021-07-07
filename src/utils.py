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


def flow_save(flow, flow_file):
    flow.astype(np.float32).tofile(flow_file)


def flow_load(flow_file):
    return np.fromfile(flow_file, np.float32)


def flag_save(background, outside, size, flag_file):
    flag = np.zeros((size, size, 4), dtype=np.uint8)
    flag[:, :, 0] = background*255
    flag[:, :, 1] = outside*255
    flag[:, :, 3] = 255
    Image.fromarray(flag).save(flag_file, 'png')
