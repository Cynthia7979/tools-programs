import requests
import zlib
from bs4 import BeautifulSoup

RAW_CONTENT = requests.get("http://www.jjwxc.net/onebook.php?novelid=541143&chapterid=1").content
SOUP = BeautifulSoup(RAW_CONTENT
                     , features="html.parser")
a = SOUP.find('div', class_='noveltext')
print(zlib.decompress(bytes(a.text)))
