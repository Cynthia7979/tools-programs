import requests
import os

SUBJECTS = {'renjiao physics y9': (1, 218,
                           'http://www.100875.com.cn:1314/data/upload/wl9q2013/', "f'9q{str(i).zfill(3)}.jpg'",
                           'Ren Jiao Physics (Year 9)'),
            'renjiao chinese y9s1': (2, 147,
                           'http://d.yuwenziyuan.com/rjb/UploadFile/dzkb/9s_new/', "f'{str(i).zfill(3)}.jpg'",
                           'Ren Jiao Chinese (Year 9 Semester 1)'),
            'renjiao chinese y9s2': (28, 149,
                           'http://www.kjzhan.com/uploads/allimg/181214/', "f'1-1Q214150{str(i).zfill(3)}.jpg'",
                           'Ren Jiao Chinese (Year 9 Semester 2)')
            }
PAGE_START = 0
PAGE_END = 1
URL = 2
FILENAME = 3
NAME = 4


def main():
    while True:
        print('Available subjects:')
        for s in SUBJECTS.keys():
            print(s)
        try:
            subject = SUBJECTS[input('Enter subject: ').lower()]
            handle(subject)
        except KeyError:
            print('There is no such subject.')


def handle(subject):
    print(f'Selected {subject[NAME]}.')
    page_start = input('Enter page start, None for start at page 1: ')
    page_start = subject[PAGE_START] if page_start in ('None','') else int(page_start)
    page_end = input('Enter page end, None for end at last page: ')
    page_end = subject[PAGE_END] if page_end in ('None', '') else int(page_end)
    try:
        os.mkdir(f'./Downloads/{subject[NAME]}/')
    except FileExistsError: print('file exists')
    for i in range(page_start, page_end+1):
        print('Downloading page', i-subject[PAGE_START], '...')
        current_filename = eval(subject[FILENAME])
        current_url = f'{subject[URL]}{current_filename}'
        r = requests.get(current_url)
        with open(f'./Downloads/{subject[NAME]}/{current_filename}', "wb") as image:
            image.write(r.content)
    print('Done.')


if __name__ == '__main__':
    main()
