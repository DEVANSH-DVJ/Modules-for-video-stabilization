from datetime import datetime

now = datetime.now()
print(now)
print(dir(now))
print(now.strftime('%Y.%m.%d %H:%M:%S.%f %Z'))
