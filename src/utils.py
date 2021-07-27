from datetime import datetime
from pytz import timezone

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
import yaml


def log(message, debug=True):
    if debug:
        now = datetime.now(timezone('Asia/Kolkata'))
        now = now.strftime('%Y.%m.%d %H:%M:%S.%f %Z')
        print('{}: {}'.format(now, message))


def config_load(config_file):
    return yaml.load(open(config_file), Loader=yaml.FullLoader)


def flow_save(flow, flow_path):
    h, w, nBands = flow.shape

    with open(flow_path, 'wb') as flow_file:
        np.array(h).astype(np.int32).tofile(flow_file)
        np.array(w).astype(np.int32).tofile(flow_file)
        np.array(nBands).astype(np.int32).tofile(flow_file)
        flow.resize((h * w * nBands,))
        flow.astype(np.float32).tofile(flow_file)


def flow_load(flow_path):
    with open(flow_path, 'rb') as flow_file:
        h = np.fromfile(flow_file, np.int32, count=1)[0]
        w = np.fromfile(flow_file, np.int32, count=1)[0]
        nBands = np.fromfile(flow_file, np.int32, count=1)[0]

        flow = np.fromfile(flow_file, np.float32, count=h * w * nBands)
        flow.resize((h, w, nBands))

    return flow


def flag_save(background, outside, size, flag_file):
    flag = np.zeros((size, size, 4), dtype=np.uint8)
    flag[:, :, 0] = background*255
    flag[:, :, 1] = outside*255
    flag[:, :, 3] = 255
    Image.fromarray(flag).save(flag_file, 'png')


def frameset_save(frameset, csv_path, plot_path):
    pd.DataFrame(frameset).to_csv(csv_path)

    fig, ax = plt.subplots(3, 2, figsize=(20, 12))

    ax[0, 0].plot(range(len(frameset['dx'])), frameset['dx'])
    ax[0, 0].set_ylabel('dx', size=18)
    ax[0, 0].grid()

    ax[1, 0].plot(range(len(frameset['dy'])), frameset['dy'])
    ax[1, 0].set_ylabel('dy', size=18)
    ax[1, 0].grid()

    ax[2, 0].plot(range(len(frameset['dz'])), frameset['dz'])
    ax[2, 0].set_ylabel('dz', size=18)
    ax[2, 0].grid()

    ax[0, 1].plot(range(len(frameset['drx'])), frameset['drx'])
    ax[0, 1].yaxis.tick_right()
    ax[0, 1].yaxis.set_label_position('right')
    ax[0, 1].set_ylabel('drx', size=18, rotation=-90, labelpad=18)
    ax[0, 1].grid()

    ax[1, 1].plot(range(len(frameset['dry'])), frameset['dry'])
    ax[1, 1].yaxis.tick_right()
    ax[1, 1].yaxis.set_label_position('right')
    ax[1, 1].set_ylabel('dry', size=18, rotation=-90, labelpad=18)
    ax[1, 1].grid()

    ax[2, 1].plot(range(len(frameset['drz'])), frameset['drz'])
    ax[2, 1].yaxis.tick_right()
    ax[2, 1].yaxis.set_label_position('right')
    ax[2, 1].set_ylabel('drz', size=18, rotation=-90, labelpad=18)
    ax[2, 1].grid()

    fig.savefig(plot_path, bbox_inches='tight')
