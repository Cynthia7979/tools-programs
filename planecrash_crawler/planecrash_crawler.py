import requests
import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup


HUB_LINK = "http://www.planecrashinfo.com/database.htm"
all_data_raw = []
"""Data Format:
{
    "date": datetime.date,
    "time": datetime.time,
    "location": (locationRaw:str, locationSpecific:str),
    "operator": str,
    "flightNo": str,
    "route": (from:str, to:str),
    "ACType": str,
    "ICAOReg": str,
    "CN": str,
    "LN": str,  # Write the same if only one is provided
    "aboard": int,
    "fatalities": int,
    "ground": int,  # Killed on ground
    "summary": str
}
For unknown data, write None.

Sample Data from 2013/2013-22.htm
{
    "date": datetime.date(2013, 11, 29),
    "time": datetime.time(20, 25),
    "location": ("Glasgow Scotland", "Glasgow Scotland"),
    "operator": 'Bond Air Services Ltd.',
    "flightNo": None,
    "route": (None, None),
    "ACType": 'Eurocopter EC135 T2',
    "ICAOReg": 'G-SPAO',
    "CN": '0546',
    "LN": '0546',
    "aboard": 3,
    "fatalities": 3,
    "ground": 5,  # Killed on ground
    "summary": "The police helicopter crashed into the roof of the Clutha Pub in central Glasgow killing at least 5 patrons along with 3 aboard he helicopter. The helicopter was carrying a civilian pilot and two Strathclyde police officers."
}
"""
date_freq = {}
time_freq = {}
location_freq = {}  # Remove "near"
operator_freq = {}
route_freq = {}
ac_type_freq = {}
summaries = []


def main(use_precrawled=False):
    # Crawl new data
    hub_soup = BeautifulSoup(requests.get(HUB_LINK).content, features="html.parser")
    # print(hub_soup)
    hub_table = hub_soup.find_all('table')[1]

    for row in hub_table.find_all('tr'):
        cells = row.find_all('td')
        for i, cell in enumerate(cells):
            if cell.text in ('<=', ' '): continue
            try:
                year_link = cell.find('strong').find('a')['href']
            except (TypeError, AttributeError):
                year_link = cell.find('a')['href']
            process_year_page(year_link)


def process_year_page(link):
    print("processing", link)
    data_objs = []
    link = 'www.planecrashinfo.com'+link
    year_page_soup = BeautifulSoup(requests.get(link).content, features='html.parser')
    for i, row in enumerate(year_page_soup.find('table').find_all('tr')):
        if i == 0: continue  # First line is title
        accident_detail_link = row.find('td').find('font').find('a')['href']
        data_obj = process_accident_detail_page(accident_detail_link)
        data_objs.append(data_obj)
    return data_objs


def process_accident_detail_page(link):
    """Terrible style warning"""
    print('   processing', link)
    link = 'www.planecrashinfo.com'+link
    detail_soup = BeautifulSoup(requests.get(link).content, features='html.parser')
    new_data_obj = {}
    for i, row in enumerate(detail_soup.find('table').find_all('tr')):
        key, value = row.find_all('td')
        if i == 0: continue  # First line is title
        elif i == 1:  # Date
            date = parse(value).date()
            new_data_obj['date'] = date
            add_freq(date_freq, date)
        elif i == 2:  # Time
            hour, minute = value[:2], value[2:]
            time = datetime.time(hour=hour, minute=minute)
            new_data_obj['time'] = time
            add_freq(time_freq, time)
        elif i == 3:  # Location
            location = (value, value.replace('Near', ''))
            new_data_obj['location'] = location
            add_freq(location_freq, location[1])
        elif i == 4:  # Operator
            new_data_obj['operator'] = value
            add_freq(operator_freq, value)
        elif i == 5:  # Flight No.
            pass  # TODO
    return new_data_obj


def add_freq(into: dict, value):
    if value in into.keys():
        into[value] += 1
    else:
        into[value] = 1


if __name__ == '__main__':
    main()
