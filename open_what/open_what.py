import requests
from bs4 import BeautifulSoup
import psutil
import threading
from time import strftime
import os
import sys

"""
    At anytime:
        Display:
        - A HTML file saying which day it is today (ymd, ABCDE day)
    When battery is 80% and higher: 
        Open the following:
        - Huo Rong
        - Google Drive Sync
    When battery is 90% and higher AND it is not during class (7:00 ~ 3:00):
        Open the following:
        - TIM
"""

apps = {'Huo Rong': "C:/Program Files (x86)/Huorong/Sysdiag/bin/HipsMain.exe",
        'Google Drive Sync': "C:\Program Files/Google/Drive/googledrivesync.exe",
        'Opera': "C:/Users/Yirou Wang/AppData/Local/Programs/Opera/launcher.exe",
        'TIM': "C:/Program Files (x86)/Tencent/TIM/Bin/QQScLauncher.exe",
        'ExpressVPN': "C:/Program Files (x86)/ExpressVPN/xvpn-ui/ExpressVPN.exe"}


class RunExeThread(threading.Thread):
    def __init__(self, path, *args, **kwargs):
        super().__init__()
        self.path = path

    def run(self):
        path = self.path
        name = path[path.rfind('/') + 1:]
        print('Start running ' + name)
        os.system('"%s"' % path)
        print('Ran ' + name)


def try_crawl(url):
    try:
        print("Connecting to "+url)
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Retrying "+url)
        return try_crawl(url)


def get_soup(url):
    code = try_crawl(url)
    plain = code.text
    soup = BeautifulSoup(plain, "html.parser")
    return soup


def fetch_class_data(testmode=False):
    f = open("C:/Users/Yirou Wang/Documents/Programmings/tools-programs/open_what/notification.html", 'w')
    today = None
    events = []
    year = strftime("%Y")
    month = strftime("%m")
    day = strftime("%d")
    if testmode:
        soup = BeautifulSoup(open("./open_what/srcode.txt").read(), "html.parser")
    else:
        soup = get_soup("https://www.depaulcatholic.org/apps/events/{year}/{month}/calendar/?id=0".
                            format(year=year, month=month))
    for day_ele in soup.find_all('td'):
        if day_ele['class'] == ["cf", "day", "today"]:
            today = day_ele
            break
    if today.ul:  # if there is an event
        for li in today.ul.find_all('li'):
            for a in li.find_all('a'):
                print(a)
                title = a.text
                link = a.href
                text = li.span.text
                text = text.replace('\n\t', '')
                text = text.replace('\t', '')
                text = text.replace('\xa0', '')
                text = text.replace('\n\n\n', '\n')
                events.append({'title': title, 'link': link, 'text': text})
    events_to_write = """"""
    if events:
        for event in events:
            events_to_write += """
            <li><a href={link}>{title}</a></li><ul><li>{text}</li></ul>""".format(link=event['link'],
                                                                                  title=event['title'],
                                                                                  text=event['text'])
    else:
        events_to_write = """<li>Nothing to do!</li>"""
    f.write("""
    <!DOCTYPE html>
        <html>
            <head>
                <title>Notification</title>
            </head>
            <body>
                <center>
                    <h3>Today's Date is:</h3>
                    <b><h2>{month}/{day}/{year}</h2></b>
                </center>
                <b><p>Calendar:</p></b>
                <ul>{write_events}</ul>
            </body>
        </html>
    """.format(month=month, day=day, year=year, write_events=events_to_write))
    f.close()
    os.startfile('C:/Users/Yirou Wang/Documents/Programmings/tools-programs/open_what/notification.html')


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
        if battery.power_plugged:
            things_to_run.append(apps['Huo Rong'])
        things_to_run.append(apps['Google Drive Sync'])
    for app in things_to_run:
        app_thread = RunExeThread(app)
        app_thread.start()
    fetch_class_data()


if __name__ == '__main__':
    main()
    sys.exit()
