# Bot for returning search engine results based on search phrase

import hackchat
from urllib.parse import quote
from html2image import Html2Image


def process_msg(chat, msg: str, sender):
    hti = Html2Image()
    if msg.startswith('?') or msg.startswith('/search'):
        search_phrase = find_search_phrase(msg)
        search_link = f'https://www.google.com/search?q={search_phrase}'
        hti.screenshot(url=search_link, save_as='result.png')
        # upload('result.png')


def find_search_phrase(msg: str):
    msg = msg.lstrip('?').strip('/search').strip()
    msg = msg.replace(' ', '-')
    msg = quote(msg)
    return msg


def upload(file_name):
    pass


def main():
    main_chat = hackchat.HackChat('SearchBot', 'cynthia!')
    main_chat.on_message += []


if __name__ == '__main__':
    # main()
    process_msg('chat', '? what is a goat?', 'sender')
