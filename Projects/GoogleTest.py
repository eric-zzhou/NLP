# https://stackoverflow.com/questions/38619478/google-search-web-scraping-with-python

import re
from urllib.request import Request, urlopen
import urllib.parse as urlpar
from bs4 import BeautifulSoup as bs
from ExtractiveSummary import generate_freq_summary
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from HTMLCleaner import text_from_html
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Constants and user input
MAX_SENT_LEN = 25
GOOGLE_LINK = "https://www.google.com/search?q="
stop = set(stopwords.words('english') + ["com"])

search_term = input('Words to search up: ')
query = ' '.join([w.lower() for w in word_tokenize(search_term) if w not in stop and w.isalpha()])
# query = [query]
query = [query]
print(query)

# Webscraping portion
print(GOOGLE_LINK + urlpar.quote(search_term))
req = Request(
    url=GOOGLE_LINK + urlpar.quote(search_term),
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36'}
)
html = urlopen(req).read().decode('utf8')
soup = bs(html, features='html.parser')

divs = soup.select("#search div.g")
links = []
for div in divs:
    for website in div.select('a[href]'):
        link = website['href']
        if link.startswith("https://"):
            links.append(link)
print(links, end="\n\n\n")

links = links[0:5]
for link in links:
    print("Getting: " + link)
    req = Request(
        url=link,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'}
    )
    html = urlopen(req).read().decode('utf8')
    # soup = bs(html, features='html.parser')
    # # kill all script and style elements
    # for script in soup(["script", "style"]):
    #     script.extract()  # rip it out
    # # get text
    # text = soup.body.get_text()
    # text = text.replace(".", ". ")
    # text = re.sub(r'\s+', ' ', text)
    text = text_from_html(html)
    # print(generate_freq_summary(text, 5), end="\n\n\n")
    sentences = sent_tokenize(text)
    sentence_embeddings = model.encode(query + sentences)
    index_max = np.argmax(cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:]))
    # print(generate_freq_summary(text, 3))
    print(sentences[index_max])
