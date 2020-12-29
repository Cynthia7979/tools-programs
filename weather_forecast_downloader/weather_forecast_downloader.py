import requests
import json
from os.path import exists
from bs4 import BeautifulSoup

HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "identity;q=1, *;q=0",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    # "Host": "vod.weathertv.cn",
    "Range": "bytes=0-",
    "Referer": "http://www.weather.com.cn/weather/101010100.shtml",
    "Sec-Fetch-Dest": "video",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.284",
    "Cookie": "UM_distinctid=17588dfca9c207-00b38ad4b6f897-4b524b59-144000-17588dfca9d4f3; f_city=%E5%8C%97%E4%BA%AC%7C101010100%7C; Hm_lvt_d2bcdd96c2f2f374ae784ba532d46fcf=1604319170,1604562930; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1609196138,1609196420,1609196437; Wa_lvt_1=1609196138,1609196420,1609196437; Wa_lvt_51=1609205428; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1609225014; Wa_lpvt_1=1609225014; Wa_lpvt_51=1609225014",
    "Host": "vod.weather.com.cn",
    "If-Range": "5dea50f2-1a2af9b",
}

VIDEO_API = "http://video.weather.com.cn/weather/video/weather_video_retrieval?keyword=&page=1&per_num=500&hotSpot=0&forecast=1&solarTerm=0&life=0&popularScience=0"


def main():
    # raw_data = json.loads(requests.get(VIDEO_API).content)
    pre_downloaded = open('video_data.json', encoding='utf-8')
    raw_data = json.load(pre_downloaded)
    raw_data = raw_data['data']['arr']
    total = len(raw_data)
    for i, video in enumerate(raw_data):
        if not exists(f'./download/{video["title"]}.mp4'):
            # print(f'Getting video {video["title"]}')
            url = 'http://video.weather.com.cn/'+video['url']
            video_page_soup = requests.get(url).content
            video_url = video_page_soup[video_page_soup.find(b'_videourl="')+len(b'_videourl="'):]
            video_url = video_url[:video_url.find(b'";')]
            video_data = requests.get(video_url, headers=HEADERS).content
            if len(video_data) > 600:  # Not forbidden
                with open(f'./download/{video["title"]}.mp4', 'wb') as f:
                    f.write(video_data)
                    print(f'Saved {video["title"]}')
            else:
                print(f'Skipping {video["title"]}: Forbidden')
        else:
            print(f'Skipping {video["title"]}: Exists')
        print(f'{i}/{total}')


if __name__ == '__main__':
    main()

