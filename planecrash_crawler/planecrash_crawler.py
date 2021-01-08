import requests
import datetime
import dateutil
from bs4 import BeautifulSoup


HUB_LINK = "http://www.planecrashinfo.com/database.htm"


def main(use_precrawled=False):
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
    link = 'www.planecrashinfo.com'+link
    print("processing", link)


def process_accident_page(link):
    pass


if __name__ == '__main__':
    main()
