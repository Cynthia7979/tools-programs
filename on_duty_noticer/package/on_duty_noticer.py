import json
import datetime as dt
from PIL import Image, ImageFont, ImageDraw
import random
import ctypes


def main():
    print('start of program')
    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)
    today = dt.datetime.now().date()
    year, month, day = today.year, today.month, today.day
    if not today.weekday() >= 5:  # Not weekend
        group_onduty = get_group_onduty(data)
        people_in_group = data['groups'][group_onduty - 1]
        wallpaper = generate_wallpaper(year, month, day, group_onduty, people_in_group)
        wallpaper.save('D:/wallpaper.jpg')
        ctypes.windll.user32.SystemParametersInfoW(20, 0, "D:/wallpaper.jpg", 0)
        data_ = data.copy()
        data_['update'] = str(today)
        data_['lastGroup'] = group_onduty
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data_, f)


def get_group_onduty(data) -> int :
    print('getting group on duty...')
    today = dt.datetime.now().date()
    last_update = dt.datetime.strptime(data['update'], '%Y-%m-%d').date()
    days_passed = (today-last_update).days
    last_group = data["lastGroup"]
    return [3,1,2][(days_passed+last_group) % 3]


def generate_wallpaper(year, month, day, group_no:int, group_members:tuple):
    print('generating wallpaper...')
    if random.randint(0,1) == 0:  # Light theme
        bg_color = (random.randint(124, 255), random.randint(124, 255), random.randint(124, 255))
        text_color = "black"
    else:  # Dark theme
        bg_color = (random.randint(0, 124), random.randint(0, 124), random.randint(0, 124))
        text_color = "white"
    img = Image.new("RGB", (1920, 1080),bg_color)
    small = ImageFont.truetype('ZCOOLXiaoWei-Regular.ttf', 60)
    normal = ImageFont.truetype('ZCOOLXiaoWei-Regular.ttf', 140)
    large = ImageFont.truetype('ZCOOLXiaoWei-Regular.ttf', 260)
    draw = ImageDraw.Draw(img)
    draw.text((540,200), f"{year}年{month}月{day}日", text_color, font=normal)
    draw.text((550,375), f"{group_no}组值日", text_color, font=large)
    draw.text((880,650), f'组员：', text_color, font=small)
    if len(group_members) == 4:
        draw.text((520,725), "，".join(group_members), text_color, font=small)
    elif len(group_members) == 5:
        draw.text((380,725), "，".join(group_members), text_color, font=small)
    return img


# def to_days(date: dt.datetime):
#     days = 0
#     if date.year % 4 == 0:
#         days += 366
#     else:
#         days += 365

main()
