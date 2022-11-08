from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

# Webscraping portion
req = Request(
    url=input("Give a link"),
    headers={'User-Agent': 'Mozilla/5.0'}
)
# https://www.hcn.org/issues/138/barry-lopez-we-are-shaped-by-the-sound-of-wind-the-slant-of-sunlight#:~:text=Barry%20Lopez%3A%20We%20are%20shaped,Country%20News%20–%20Know%20the%20West

html = urlopen(req).read().decode('utf8')
soup = bs(html, 'html.parser')
print(soup.body.get_text())
# body2 = body.findChildren(recursive=False)
# print(body.text)
# raw = raw.replace(".", ". ")