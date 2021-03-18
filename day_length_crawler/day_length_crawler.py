# This program is used to fetch and analyze day length data of Florence
# from https://dateandtime.info/citysunrisesunset.php
# For my Math assignment

import requests
import datetime
import time
from bs4 import BeautifulSoup


def main():
    day_lengths = {}
    URL = "https://dateandtime.info/citysunrisesunset.php?id=3176959&month={month}&year=2019"
    for month in range(1, 13):
        soup = get_soup(URL.format(month=month))
        day_lengths.update(get_day_lengths(soup))
    print(day_lengths)

    # Get longest and shortest day lengths
    dates = list(day_lengths.keys())
    lengths = list(day_lengths.values())
    shortest = lengths.index(min(lengths))
    print('Date with shortest day length:',
          dates[shortest].strftime('%j'),
          lengths[shortest], 'hours')
    longest = lengths.index(max(lengths))
    print('Date with longest day length:',
          dates[longest].strftime('%j'),
          lengths[longest], 'hours')


def get_soup(url):
    raw = requests.get(url).content
    return BeautifulSoup(raw, features="html.parser")


def get_day_lengths(soup: BeautifulSoup):
    day_lengths = {}
    table = soup.find_all('table', class_='sunrise_table')[1]
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        all_cells = row.find_all('td')
        # for cell in all_cells: print(cell)
        date_text = all_cells[0].text
        date_text = date_text.replace('\n', '').replace('\t', '').strip()
        day_length_text = all_cells[-1].text.replace('\t', '').replace('\n', '')
        print(date_text, day_length_text)
        date = datetime.datetime.strptime(date_text, "%a, %B %d").replace(year=2019)
        day_length = datetime.datetime.strptime(day_length_text, '%H:%M:%S')
        day_length_hours = in_hours(day_length)
        day_lengths[date] = day_length_hours
    return day_lengths


def in_hours(dt: datetime.datetime):
    return dt.hour + dt.minute / 60 + dt.second / 60 / 60


if __name__ == '__main__':
    main()
