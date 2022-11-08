# https://stackoverflow.com/questions/38619478/google-search-web-scraping-with-python

import nltk
import re
from urllib.request import Request, urlopen
import urllib.parse as urlpar
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer

# Constants and user input
MAX_SENT_LEN = 25
GOOGLE_LINK = "https://www.google.com/search?q="

search_term = input('Words to search up: ')
# Webscraping portion
print(GOOGLE_LINK + urlpar.quote(search_term))
req = Request(
    url=GOOGLE_LINK + urlpar.quote(search_term),
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
)
html = urlopen(req).read().decode('utf8')
soup = bs(html, features='html.parser')

divs = soup.select("#search div.g")
links = []
for div in divs:
    for website in div.select('a[href]'):
        link = website['href']
        if not link.startswith("/search?q="):
            links.append(link)
print(links, end="\n\n\n")

links = [links[0]]
for link in links:
    print("Getting: " + link)
    req = Request(
        url=link,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    )
    html = urlopen(req).read().decode('utf8')
    soup = bs(html, features='html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.body.get_text()
    text = text.replace(".", ". ")
    text = re.sub(r'\s+', ' ', text)
    print(text)

