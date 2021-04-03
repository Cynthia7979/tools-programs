import requests
import sys, os
import time
from bs4 import BeautifulSoup

mirror_dir = 'F://scp-wiki-cn/mirror/'
source_dir = 'F://scp-wiki-cn/source/'
home_page = "http://scp-wiki-cn.wikidot.com/tag-search/tag/%2b原创/limit/1617366553684/order/created_at%20desc/p/{p}"
source_code_api = 'http://scp-wiki-cn.wikidot.com/ajax-module-connector.php'
source_header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "__n_id2=2c0dd940-b761-4325-b623-24baf0df8dc7; __qca=P0-1315370410-1586302676763; __gads=ID=331c2923e1446493-22f4040a08c300d0:T=1597840740:RT=1597840740:R:S=ALNI_MbbzhxVublxJScJgOTVhxJewmkOmQ; _pbjs_userid_consent_data=6683316680106290; na-unifiedid=%7B%22TDID%22%3A%22d25825eb-3c34-46dc-922f-6bddad92a330%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-02-08T03%3A02%3A58%22%7D; WIKIDOT_SESSION_ID=1615981396_96062967; wikidot_udsession=1; wikidot_udsession=1; __utmz=1.1617262409.573.25.utmcsr=scpper.com|utmccn=(referral)|utmcmd=referral|utmcct=/user/3687969; wikidot_token7=8527b50858dd4c64aa0926fa47e33f41; __utma=1.533478953.1521295561.1617326732.1617366188.577; __utmc=1; __utmt=1; __utmt_old=1; __utmb=1.148.10.1617366188",
    "Host": "scp-wiki-cn.wikidot.com",
    "Origin": "http://scp-wiki-cn.wikidot.com",
    "Referer": "http://scp-wiki-cn.wikidot.com/scp-cn-2552",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218",
    "X-Requested-With": "XMLHttpRequest",
}


def main():
    if not os.path.exists(mirror_dir):
        os.mkdir(mirror_dir)
    if not os.path.exists(source_dir):
        os.mkdir(source_dir)

    for i in range(261, 273):
        print('Iter', i)
        home_page_soup = get_soup(home_page.format(p=i))
        for link in get_links(home_page_soup):
            mirror(link)
            # save_source(link)
            time.sleep(0.1)


def get_soup(url):
    try:
        raw = requests.get(url).content
        return BeautifulSoup(raw, features="html.parser")
    except Exception as e:
        while True:
            print('Retrying', url, e)
            raw = requests.get(url).content
            return BeautifulSoup(raw, features="html.parser")


def get_links(home_page_soup):
    links = []
    table = home_page_soup.find_all('table', class_='wiki-content-table')[0]
    for row in table.find_all('tr')[1:]:
        a_element = row.find('a')
        links.append('http://scp-wiki-cn.wikidot.com/'+a_element['href'])
    print('Links got: ', links)
    return links


def mirror(link):
    page_name = get_page_name(link)
    if os.path.exists(os.path.join(mirror_dir, page_name+'.html')):
        print('SKIPPING mirroring', page_name, 'due to existing file')
        return
    print('Mirroring', page_name)

    content = request(link)

    content = str(content, encoding='utf-8')
    with open(os.path.join(mirror_dir, page_name+'.html'), 'w', encoding='utf-8') as f:
        f.write(content)
        print('Mirrored:', link)


def get_page_name(link):
    return link[link.find('cn.wikidot.com//')+len('cn.wikidot.com//'):].replace(':', ';')


def request(link, headers=None):
    succeed = False
    try:
        content = requests.get(link, headers=headers).content
        succeed = True
    except Exception as e:
        print('Initial trial failed:', link, e)
        succeed = False
    while not succeed:
        try:
            content = requests.get(link, headers=headers).content
            succeed = True
        except Exception as e:
            print('Retrying', link, e)
    return content


if __name__ == '__main__':
    main()
