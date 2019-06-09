import requests
import urllib

response = None
page = urllib.urlopen('https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=11022534')
data = eval(page.read())

for key in data.keys():
    print(key, ':')
    print(data[key])
