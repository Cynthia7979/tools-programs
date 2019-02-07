import psutil
import threading
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

apps = {'Huo Rong': "C:/Program Files (x86)/Huorong/Sysdiag/bin/HipsMain.exe",
                 'Google Drive Sync': "C:\Program Files/Google/Drive/googledrivesync.exe",
                 'Opera': "C:/Users/Yirou Wang/AppData/Local/Programs/Opera/launcher.exe",
                 'TIM': "C:/Program Files (x86)/Tencent/TIM/Bin/QQScLauncher.exe"}


class RunExeThread(threading.Thread):
    def __init__(self, path, *args, **kwargs):
        super().__init__()
        self.path = path

    def run(self):
        path = self.path
        name = path[path.rfind('/')+1:]
        print('Start running '+name)
        os.system('"%s"' % path)
        print('Ran '+name)


def main():
    print("Starting up...")

    battery = psutil.sensors_battery()
    percentage = battery.percent
    current_time = int(strftime("%H"))
    things_to_run = []
    if percentage >= 80:
        if percentage >= 90:
            if 7 > current_time or 15 < current_time:
                things_to_run.append(apps['TIM'])
        things_to_run.append(apps['Huo Rong'])
        things_to_run.append(apps['Google Drive Sync'])
        things_to_run.append(apps['Opera'])
    for app in things_to_run:
        app_thread = RunExeThread(app)
        app_thread.start()


if __name__ == '__main__':
    main()
