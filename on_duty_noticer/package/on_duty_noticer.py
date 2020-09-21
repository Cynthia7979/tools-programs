import json
import datetime as dt
from PIL import Image, ImageFont, ImageDraw
import random
import ctypes
import locale

# Fonts
small = ImageFont.truetype('ZCOOLXiaoWei-Regular.ttf', 60)
normal = ImageFont.truetype('ZCOOLXiaoWei-Regular.ttf', 140)
large = ImageFont.truetype('ZCOOLXiaoWei-Regular.ttf', 260)


def main():
    print('start of program')
    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)
    locale.setlocale(locale.LC_CTYPE, 'chinese')  # Support Chinese in strftime()
    today = dt.datetime.now().date()

    group_onduty = get_group_onduty(today, data)
    people_in_group = data['groups'][group_onduty - 1]
    if data['pictureMode']:
        if data['fullMode']:
            wallpaper = generate_full_pic_wallpaper(today, group_onduty, people_in_group)
        else:
            wallpaper = generate_side_pic_wallpaper(today, group_onduty, people_in_group)
    else:
        wallpaper = generate_normal_wallpaper(today, group_onduty, people_in_group)
    wallpaper.save('D:/wallpaper.png')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "D:/wallpaper.png", 0)
    if today.weekday() >= 5:
        data_ = data.copy()
        data_['update'] = str(today)
        data_['lastGroup'] = group_onduty
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data_, f)


def get_group_onduty(today, data) -> int:
    print('getting group on duty...')
    last_update = dt.datetime.strptime(data['update'], '%Y-%m-%d').date()
    days_passed = (today-last_update).days
    last_group = data["lastGroup"]
    delta = (today.weekday() == 0) *-2  # If it's Monday, then ignore extra weekend days
    return [3,1,2][(days_passed+last_group+delta) % 3]


def generate_normal_wallpaper(date, group_no:int, group_members:tuple):
    print('generating solid wallpaper...')
    if random.randint(0,1) == 0:  # Light theme
        bg_color = (random.randint(127, 255), random.randint(127, 255), random.randint(127, 255))
        text_color = "black"
    else:  # Dark theme
        bg_color = (random.randint(0, 127), random.randint(0, 127), random.randint(0, 127))
        text_color = "white"

    background = Image.new("RGB", (1920, 1080), bg_color)
    draw = ImageDraw.Draw(background)
    draw.text((500,200), date.strftime('%Y年%m月%d日'), text_color, font=normal)
    if date.weekday() >= 5:
        draw.text((450, 425), "周末快乐", text_color, font=large)
    else:
        draw.text((500,425), f"{group_no}组值日", text_color, font=large)
        draw.text((830,700), f'组员：', text_color, font=small)
        if len(group_members) == 4:
            draw.text((470,775), "，".join(group_members), text_color, font=small)
        elif len(group_members) == 5:
            draw.text((330,775), "，".join(group_members), text_color, font=small)

    return background


def generate_side_pic_wallpaper(date, group_no:int, group_members:tuple):
    print('generating side PicMode wallpaper...')
    try:
        img = Image.open('picmode_source.png')
    except FileNotFoundError:
        img = Image.open('picmode_source.jpg')
    source_img = img.crop((0, 0, 540, 1080))

    small_image = source_img.resize((80, 80))
    main_color = small_image.convert('P', palette=Image.ADAPTIVE, colors=1).convert('RGB').getcolors(80*80)[0][1]
    bg_color = tuple([255-i for i in main_color])
    if [i>127 for i in bg_color].count(True) >=2:
        text_color = 'black'
    else:
        text_color = 'white'
    background = Image.new('RGB', (1920, 1080), bg_color)

    background.paste(source_img, (0,0))
    draw = ImageDraw.Draw(background)
    draw.text((570, 225), date.strftime('%Y年%m月%d日'), text_color, font=normal)
    if date.weekday() >= 5:
        draw.text((540, 400), "周末快乐", text_color, font=large)
    else:
        draw.text((570,400), f"{group_no}组值日", text_color, font=large)
        if len(group_members) == 4:
            draw.text((570,700), "，".join(group_members), text_color, font=small)
        elif len(group_members) == 5:
            draw.text((570,700), "，".join(group_members), text_color, font=small)

    return background


def generate_full_pic_wallpaper(date, group_no:int, group_members:tuple):
    print('generating picture wallpaper...')
    if random.randint(0, 1) == 0:  # Light theme
        fg = Image.new('RGB', (1920, 1080), 'white')
        text_color = "black"
    else:  # Dark theme
        fg = Image.new('RGB', (1920, 1080), 'black')
        text_color = "white"

    try:
        background = Image.open('picmode_source.png')
    except FileNotFoundError:
        background = Image.open('picmode_source.jpg')
    background = background.resize((1920,1080)).convert('RGB')

    background = Image.blend(background, fg, 0.5)
    draw = ImageDraw.Draw(background)
    draw.text((500, 200), date.strftime('%Y年%m月%d日'), text_color, font=normal)
    if date.weekday() >= 5:
        draw.text((510, 375), "周末快乐", text_color, font=large)
    else:
        draw.text((550, 375), f"{group_no}组值日", text_color, font=large)
        draw.text((880, 650), f'组员：', text_color, font=small)
        if len(group_members) == 4:
            draw.text((520, 725), "，".join(group_members), text_color, font=small)
        elif len(group_members) == 5:
            draw.text((380, 725), "，".join(group_members), text_color, font=small)

    return background


main()
