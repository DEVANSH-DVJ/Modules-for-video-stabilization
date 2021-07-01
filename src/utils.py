from datetime import datetime
from pytz import timezone
import yaml


def log(message, debug=True):
    if debug:
        now = datetime.now(timezone('Asia/Kolkata'))
        now = now.strftime('%Y.%m.%d %H:%M:%S.%f %Z')
        print('{}: {}'.format(now, message))


def config_load(config_file):
    return yaml.load(open(config_file), Loader=yaml.FullLoader)
