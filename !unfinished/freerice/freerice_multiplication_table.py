from selenium import webdriver

headers = {
    ':authority': 'freerice.com',
    ':method': 'GET',
    ':path': '/categories/multiplication-table',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="96", "Opera";v="82", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'
}


def main():
    browser = webdriver.Opera(executable_path='E:\Opera\82.0.4227.33\operadriver.exe')
    browser.get('https://google.com')
    input('Login in the opened browser window. After logging in, press Enter. > ')
    browser.get('https://freerice.com/categories/multiplication-table')
    title = browser.find_element_by_class_name('card-title').text
    print(title)


if __name__ == '__main__':
    main()
