import requests
import sys, os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *

mirror_dir = 'F://scp-wiki-cn/mirror/'
source_dir = 'F://scp-wiki-cn/source/'

driver = 'chrome'

# 所有页面
home_page = "http://scp-wiki-cn.wikidot.com/tag-search/limit/1617539958174/order/created_at%20desc/"
# 所有fragment分类
# home_page = "http://scp-wiki-cn.wikidot.com/tag-search/category/fragment/limit/1617461727142/order/created_at%20desc/"
# 所有原创
# home_page = "http://scp-wiki-cn.wikidot.com/tag-search/tag/%2b原创/limit/1617366553684/order/created_at%20desc/"
# 所有原创成人内容
# home_page = "http://scp-wiki-cn.wikidot.com/tag-search/tag/%2b原创/category/adult/limit/1617444176386/order/created_at%20desc/"
# 所有原创图书馆
# home_page = "http://scp-wiki-cn.wikidot.com/tag-search/tag/%2b原创/category/wanderers-adult/limit/1617445267227/order/created_at%20desc/"
home_page += 'p/{p}'
start_page = 3
end_page = 914

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Cookie": "__n_id2=2c0dd940-b761-4325-b623-24baf0df8dc7; __qca=P0-1315370410-1586302676763; __gads=ID=331c2923e1446493-22f4040a08c300d0:T=1597840740:RT=1597840740:R:S=ALNI_MbbzhxVublxJScJgOTVhxJewmkOmQ; _pbjs_userid_consent_data=6683316680106290; na-unifiedid=%7B%22TDID%22%3A%22d25825eb-3c34-46dc-922f-6bddad92a330%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-02-08T03%3A02%3A58%22%7D; wikidot_udsession=1; wikidot_udsession=1; __utmz=1.1617262409.573.25.utmcsr=scpper.com|utmccn=(referral)|utmcmd=referral|utmcct=/user/3687969; wikidot_token7=4875975f575dc231c46977643726a30e; __utmc=1; __utma=1.533478953.1521295561.1617418092.1617443573.580; __utmt=1; __utmt_old=1; __utmb=1.30.10.1617443573; WIKIDOT_SESSION_ID=1617444480_76706048",
    "Host": "scp-wiki-cn.wikidot.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://scp-wiki-cn.wikidot.com/adult:interrogation/noredirect/true",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218"
}


def main():
    if not os.path.exists(mirror_dir):
        os.mkdir(mirror_dir)
        print('Target directory does not exist, creating...')

    # 此处代码修改自[CSharperMantle/scp_fetcher_bs4](https://github.com/CSharperMantle/scp_fetcher_bs4)
    if driver == 'chrome':
        browser = webdriver.Chrome()
    elif driver == 'firefox':
        browser = webdriver.Chrome()
    elif driver == 'opera':
        browser = webdriver.Opera()
    else:
        raise ValueError('"driver" variable needs to be one of "chrome", "opera" or "firefox".')
    browser.implicitly_wait(5)
    browser.get('https://scp-wiki-cn.wikidot.com')
    input('请在打开的窗口中登录，完成后按回车键>')

    print('Mirroring from', home_page)
    print('Mirroring into', mirror_dir, '...')
    print('Saving source code to', source_dir, '...')

    for i in range(start_page, end_page+1):
        print('Iter', i)
        home_page_soup = get_soup(home_page.format(p=i))
        for link in get_links(home_page_soup):
            mirror(link)
            # save_source(link, browser)
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

    if "/adult:" in link:
        print("Mirroring", page_name, 'with category-specific method')
        content = request(link +'/noredirect/true', headers=headers)
    else:
        print('Mirroring', page_name)
        content = request(link, headers=headers)

    try:
        content = str(content, encoding='utf-8')
    except UnicodeDecodeError:
        print("WARNING: SKIPPING", page_name, "as it contains non-utf-8 content")
        return
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


def save_source(link, browser):
    """
    此处代码修改自[CSharperMantle/scp_fetcher_bs4](https://github.com/CSharperMantle/scp_fetcher_bs4)
    """
    page_name = get_page_name(link)
    if os.path.exists(os.path.join(source_dir, page_name+'.txt')):
        print('SKIPPING saving source of', page_name, 'due to existing file')
        return
    if 'deleted;' in page_name:
        print('SKIPPING saving source of', page_name, 'because it is in deleted: category')
        return
    print('Getting source code of', page_name)

    try:
        browser.get(link)

        elem_more_options_button = browser.find_element_by_id('more-options-button')
        elem_more_options_button.click()

        elem_view_source_button = browser.find_element_by_id('view-source-button')
        elem_view_source_button.click()
    except (NoSuchElementException, ElementClickInterceptedException):
        succeed = False
        while not succeed:
            print('Cannot find more-options or view-source button, retrying...')
            try:
                browser.get(link)

                elem_more_options_button = browser.find_element_by_id('more-options-button')
                elem_more_options_button.click()

                elem_view_source_button = browser.find_element_by_id('view-source-button')
                elem_view_source_button.click()

                succeed = True
            except NoSuchElementException:
                pass

    try:
        text_page_source = browser.find_element_by_class_name('page-source').text
    except NoSuchElementException:
        succeed = False
        while not succeed:
            print('Cannot find .page-source, retrying...')
            try:
                text_page_source = browser.find_element_by_class_name('page-source').text

                succeed = True
            except NoSuchElementException:
                pass

    with open(os.path.join(source_dir, page_name+'.txt'), 'w', encoding='utf-8') as f:
        f.write(text_page_source)
        print('Source saved:', link)


if __name__ == '__main__':
    main()
