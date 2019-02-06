import psutil
from time import strftime
import os, sys

"""
TODO:
    When battery is 80% and higher: 
        Open the following:
        - Huo Rong
        - Google Drive Sync
        - Opera
    When battery is 90% and higher AND it is not during class (7:00 ~ 3:00):
        Open the following:
        - TIM
"""

things_to_run = {'Huo Rong': "C:/Program Files (x86)/Huorong/Sysdiag/bin/HipsMain.exe",
                 'Google Drive Sync': "C:\Program Files\Google\Drive\googledrivesync.exe",
                 'Opera': }

def run(path):
    os.system('"%s"' % path)


sys.stdout.write('Starting up...')

battery = psutil.sensors_battery()
percentage = battery.percent
current_time = int(strftime("%H"))

