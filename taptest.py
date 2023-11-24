import subprocess

adb_id = 'SED0221625000077'

adb_path = 'ADB_PATH'

CONTACT_SELECT = (220, 460)
SEND_NAVIGATION = (500, 680)


def tap(xy):
    subprocess.Popen([adb_path, '-s', adb_id, 'shell', 'input tap {} {}'.format(xy[0], xy[1])],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)


tap(CONTACT_SELECT)


