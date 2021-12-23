import requests
import random
from time import time
from os import getcwd, chdir

print(getcwd())
chdir('./steam_captcha_crawler/')  # For my env only - comment this out if you experience error

cookies = {
    "Host": "steamcommunity.com",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Chromium";v="96", "Opera";v="82", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33',
    'sec-ch-ua-platform': "Windows",
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'image',
    'Referer': 'https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Fdiscord.com%2Fapi%2Fconnections%2Fsteam%2Fcallback%3Fstate%3D9c3d04a5f42ed4f4b86d9fca028fe4e2&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select',
    'Accept-Encoding': 'gzip, deflate, br'
}

proxy = {
    # If this does not work, use 8.88.888.8:8888.
    # If you do not use a proxy, comment out this variable and the proxy argument.
    'https': '127.0.0.1:7890',
    'http': '127.0.0.1:7890'
}


def brute_force_gid(n):
    for i in range(n):
        gid = None  # Still can't figure out how to get a valid gid
        gid = random.randint(0, 99999999999999999999)

        with open(f'./downloaded/{gid if gid else "default"}.png', 'wb') as f:
            f.write(requests.get(
                'http://steamcommunity.com/login/rendercaptcha/'+(f'?gid={gid}' if gid else ''),
                cookies=cookies,
                proxies=proxy
            ).content)


def get_a_bunch_of_steams(n):
    for i in range(n):
        with open(f'./downloaded/default_{time()}.png', 'wb') as f:
            f.write(requests.get(
                'http://steamcommunity.com/login/rendercaptcha/',
                cookies=cookies,
                proxies=proxy
            ).content)


if __name__ == '__main__':
    get_a_bunch_of_steams(50)
