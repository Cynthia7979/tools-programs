import requests


def wu_you_hua_xue():
    max_args = [0,0,1]
    url = lambda arg1, arg2, arg3:f'http://www.56hx.cn/uploads/allimg/jc/s/{arg1}.{arg2}.{arg3}.jpg'
    for arg1 in range(1,11):
        for arg2 in range(1,11):
            for arg3 in range(1,11):
                content = requests.get(url(arg1,arg2,arg3)).content
                if '<p class="style2" align="center" style="text-align:center">亲，网站（无忧化学）改版啦！</p>'\
                   in content:  # This page doesn't exist
                    break
                else:
                    max_args[2] = arg3

