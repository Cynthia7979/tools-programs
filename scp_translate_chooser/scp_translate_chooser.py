﻿import requests
from bs4 import BeautifulSoup
import os
import sys


class SCPPage(object):
    def __init__(self, url, beautifulsoup, title=None):
        try:
            self.url = url
            self.length = len(beautifulsoup.get_text())
            self.title = beautifulsoup.title.string
        except AttributeError:
            if title:
                self.title = title
            else:
                self.title = url

    def __gt__(self, other):
        return self.length > other.length

    def __le__(self, other):
        return self.length <= other.length

    def __eq__(self, other):
        return self.length == other.length

    def __str__(self):
        return "* [{}]({})".format(self.title, self.url)


def crawl_scp(minimum, maximum, maximumentries, precise):
    f1 = open('temp.md', 'w')
    f1.write("# SCP Web Spider Results\n")
    result = []
    for number in ["scp-"+(str(num).zfill(3)) for num in range(minimum, maximum+1)]:
        interwiki_url = "http://scpnet.org/interwiki/scp-wiki/?lang=en&page="+number
        wiki_url = "http://scp-wiki.net/"+number
        interwiki_soup = get_soup(interwiki_url)
        wiki_soup = get_soup(wiki_url)
        if ("中文" not in [a.string for a in interwiki_soup.find_all('a')]) and \
                (wiki_soup.title.string != "SCP Foundation"):
            entry = SCPPage("http://scp-wiki.net/"+number, wiki_soup, title=number)
            result.append(entry)
            f1.write(str(entry)+"\n")
        print(number+" processed")
        if len(result) >= maximumentries and not precise:
            break
    result.sort()
    result = result[:maximumentries]
    f1.close()
    f2 = open('result.md', 'w')
    f2.write("# SCP Web Spider Results\n")
    for r in result:
        f2.write(str(r) + "\n")
    f2.close()
    os.remove('temp.md')
    return result


def try_crawl(url):
    try:
        print("Connecting to "+url)
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Retrying "+url)
        return try_crawl(url)


def get_soup(url):
    code = try_crawl(url)
    plain = code.text
    soup = BeautifulSoup(plain, "html.parser")
    return soup


def main():
    arg = sys.argv
    minimum, maximum, number_of_articles = [int(x) for x in arg[1:4]]
    try:
        precise_mode = bool(arg[4])
    except IndexError:
        precise_mode = False
    print("Searching for {0} SCP entries in from {1} to {2}".format(number_of_articles, minimum, maximum))
    result = crawl_scp(minimum, maximum, number_of_articles, precise_mode)
    print("Result:\n"+';\n'.join([str(e) for e in result]))


if __name__ == '__main__':
    main()

