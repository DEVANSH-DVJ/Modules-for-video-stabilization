from datetime import datetime
from pytz import timezone

now = datetime.now(timezone('Asia/Kolkata'))
print(now)
print(dir(now))
print(now.strftime('%Y.%m.%d %H:%M:%S.%f %Z'))


def log(message):
    now = datetime.now(timezone('Asia/Kolkata'))
    now = now.strftime('%Y.%m.%d %H:%M:%S.%f %Z')
    print('{}: {}'.format(now, message))
