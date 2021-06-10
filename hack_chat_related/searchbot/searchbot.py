# Bot for returning search engine results based on search phrase

import hackchat
import requests
from urllib.parse import quote
from urllib.request import getproxies
from json import loads
from html2image import Html2Image

hti = Html2Image()
headers = {
    "Authorization": open('api.key').read()
}
proxies = {
    'http': ''
}
base_url = 'https://sm.ms/api/v2/'
upload_url = base_url+'upload'


def process_msg(chat: hackchat.HackChat, msg: str, sender):
    if (msg.startswith('?') or msg.startswith('/search')) and 'SearchBot' not in sender:
        print('Processing', msg)
        search_phrase = find_search_phrase(msg)
        search_link = f'https://www.google.com/search?q={search_phrase}'
        print('Getting screenshot of', search_link)
        hti.screenshot(url=search_link, save_as=search_phrase+'.png')
        img_url = upload(search_phrase+'.png')
        chat.send_message(f'![result]({img_url})')
    else:
        print(msg, 'is an ordinary message')


def find_search_phrase(msg: str):
    msg = msg.lstrip('?').strip('/search').strip()
    msg = msg.replace(' ', '-')
    msg = quote(msg)
    print('Search phrase:', msg)
    return msg


def upload(file_name):
    # headers_with_file = headers.copy()
    # headers_with_file['smfile'] = str(open(file_name, 'rb').read())
    print('Posting', headers)
    try:
        result = requests.post(upload_url, files={'smfile': open(file_name, 'rb')}, headers=headers, proxies=getproxies())
    except ValueError:
        result = requests.post(upload_url, files={'smfile': open(file_name, 'rb')}, headers=headers,
                               proxies=getproxies())
    result = loads(result.text)
    if result['success']:
        return result['data']['url']
    else:
        if result['code'] == 'image_repeated':
            return result['images']
        else:
            print('Unexpected error:', result['code'])
            return 'none'


def main():
    main_chat = hackchat.HackChat('SearchBot_1', 'cynthia!')
    main_chat.on_message += [process_msg]
    print('SearchBot running!')
    main_chat.run()


if __name__ == '__main__':
    main()
    # process_msg(hackchat.HackChat('SearchBot', 'cynthia!'), '? what is a goat?', 'sender')
