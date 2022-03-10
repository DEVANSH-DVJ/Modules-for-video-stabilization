from datetime import datetime
from pytz import timezone

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


def save_image(array, im_path):
    im = Image.fromarray(array)
    im.save(im_path)


def frameset_save(frameset, csv_path, plot_path):
    pd.DataFrame(frameset).to_csv(csv_path)

    fig, ax = plt.subplots(3, 2, figsize=(20, 12))

    ax[0, 0].plot(range(len(frameset['x'])), frameset['x'])
    ax[0, 0].set_ylabel('x', size=18)
    ax[0, 0].grid()

    ax[1, 0].plot(range(len(frameset['y'])), frameset['y'])
    ax[1, 0].set_ylabel('y', size=18)
    ax[1, 0].grid()

    ax[2, 0].plot(range(len(frameset['z'])), frameset['z'])
    ax[2, 0].set_ylabel('z', size=18)
    ax[2, 0].grid()

    ax[0, 1].plot(range(len(frameset['rx'])), frameset['rx'])
    ax[0, 1].yaxis.tick_right()
    ax[0, 1].yaxis.set_label_position('right')
    ax[0, 1].set_ylabel('rx', size=18, rotation=-90, labelpad=18)
    ax[0, 1].grid()

    ax[1, 1].plot(range(len(frameset['ry'])), frameset['ry'])
    ax[1, 1].yaxis.tick_right()
    ax[1, 1].yaxis.set_label_position('right')
    ax[1, 1].set_ylabel('ry', size=18, rotation=-90, labelpad=18)
    ax[1, 1].grid()

    ax[2, 1].plot(range(len(frameset['rz'])), frameset['rz'])
    ax[2, 1].yaxis.tick_right()
    ax[2, 1].yaxis.set_label_position('right')
    ax[2, 1].set_ylabel('rz', size=18, rotation=-90, labelpad=18)
    ax[2, 1].grid()

    fig.savefig(plot_path, bbox_inches='tight')
