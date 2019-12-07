import requests

print('Available subjects:')
for s in ('physics y9',):
    print(s)

subject = input('Enter subject: ')
print(subject)

if subject.lower() == 'physics y9':
    print('Selected physics (year 9)')
    page_start = input('Enter page start, None for start at page 1: ')
    page_start = 1 if page_start == 'None' else int(page_start)
    page_end = input('Enter page end, None for end at last page: ')
    page_end = 218 if page_end == 'None' else int(page_end)
    for i in range(page_start, page_end+1):
        print('Downloading page', i, '...')
        current_filename = f'9q{str(i).zfill(3)}.jpg'
        current_url = f'http://www.100875.com.cn:1314/data/upload/wl9q2013/{current_filename}'
        r = requests.get(current_url)
        with open(f'./Downloads/{current_filename}', "wb") as image:
            image.write(r.content)

