import time
from datetime import datetime

t = "2023-11-23 20:26:01.602"
d = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
n = (time.mktime(d.timetuple())) + d.microsecond / 1000000.0
print(n)