"""
Checks whether or not a website has updated its content.
"""

import requests
import time
import sys, os
import re
import json
import logging


def main():
    global LOGGER
    sh = logging.StreamHandler(sys.stdout)
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(sh)
    try:
        with open('URLs') as f:
            urls = json.load(f)
    except json.decoder.JSONDecodeError as e:
        if str(e) != 'Expecting value: line 1 column 1 (char 0)':
            raise e
        else:
            urls = {}
    print('Enter your URL below')
    url = input('> ')
    if not re.match("^((www.)?\S+\.(com|net|org|edu|gov|xyz)(\/\S+)?)$", url):
        LOGGER.warning('Incorrect URL format. Now exiting...')
        return
    url = 'http://'+url
    if url not in urls.keys():
        LOGGER.warning('This is the first time you queried this URL.')
        urls = update_json(urls, url)
        LOGGER.warning('It is stored and will be available for future query.')
    else:
        # print('Please choose a mode:')
        # print('1. Anything (only gives yes/no answers, significantly faster)')
        # print('2. Similarness (gives how similar the two versions are, slower)')
        # mode = input('Enter 1 or 2> ')
        # original_content = tuple(urls[url])
        # website_content = tuple(requests.get(url).content)
        original_content = urls[url]
        website_content = str(requests.get(url).content)
        if original_content == website_content: print('Website hadn\'t been updated.')
        # elif mode == 1:
        else:
            print('Website had been updated')
            urls = update_json(urls, url)
        # elif mode == 2:
        #     similarness = 0.0
        #     for i, l in enumerate(original_content):
        #         if l == website_content[i]:
        #             similarness += 1
        #     similarness /= len(original_content)
        #     print('')


def update_json(urls, url):
    try:
        website_content = requests.get(url).content
    except requests.exceptions.ConnectionError:
        LOGGER.fatal('Connection error. Now exiting...')
        return
    urls[url] = str(website_content)
    with open('URLs', 'w') as f:
        json.dump(urls, f)
    return urls


if __name__ == '__main__':
    main()
    print('bye(')
