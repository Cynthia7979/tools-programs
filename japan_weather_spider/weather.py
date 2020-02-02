import requests
import pprint
from bs4 import BeautifulSoup as bsoup

year = 2019
month = 12
url = f"http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year={year}&month={month}"
html = requests.get(url).content
soup = bsoup(html, "html.parser", from_encoding="utf-8")
table = soup.find('table', id="tablefix1")
result = [[],[],[],[],[],
          [],[],[],[],[],
          [],[],[],[],[],
          [],[],[],[],[],]
rows = table.find_all('tr', class_='mtx')[4:]
for row in rows:
    day_data = row.find_all('td', class_='data_0_0')
    for i, data in enumerate(day_data):
        result[i].append(data.text.strip(' )').strip(' ]'))
for r in result:
    print(r)
