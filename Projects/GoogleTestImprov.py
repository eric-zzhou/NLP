# https://stackoverflow.com/questions/38619478/google-search-web-scraping-with-python
# https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
import time
from urllib.request import Request, urlopen
import urllib.parse as urlpar
from bs4 import BeautifulSoup as bs
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from threading import Thread
from HTMLCleaner import text_from_html

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Constants and user input
GOOGLE_LINK = "https://www.google.com/search?q="
stop = set(stopwords.words('english') + ["com"])


def scrape_link(link, ind, query, arr):
    req = Request(
        url=link,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'}
    )
    html = urlopen(req).read().decode('utf8')
    text = text_from_html(html)
    sentences = sent_tokenize(text)
    if not sentences:
        arr[ind] = (link, ["Error in scraping"], -1, 0)
        return
    sentence_embeddings = model.encode(query + sentences)
    sims = cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:])
    index_max = np.argmax(sims)
    arr[ind] = (link, sentences, np.max(sims), index_max)


def scrape_google(search_term):
    # Webscraping portion
    # print(GOOGLE_LINK + urlpar.quote(search_term))
    query = ' '.join([w.lower() for w in word_tokenize(search_term) if w not in stop and w.isalpha()])
    # query = [query]
    query = [query]
    # print(query)
    req = Request(
        url=GOOGLE_LINK + urlpar.quote(search_term),
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'}
    )
    html = urlopen(req).read().decode('utf8')
    soup = bs(html, features='html.parser')

    divs = soup.select("#search div.g")
    links = set()
    for div in divs:
        for website in div.select('a[href]'):
            link = website['href']
            if link.startswith("https://"):
                htag = link.find('#')
                if htag != -1:
                    links.add(link[:htag])
                else:
                    links.add(link)
    # print(links, end="\n\n\n")

    links = list(links)[0:5]
    google_sents = [None] * 5
    threads = [None] * 5
    for ind, link in enumerate(links):
        threads[ind] = Thread(target=scrape_link, args=(link, ind, query, google_sents))
        threads[ind].start()
    for i in range(len(threads)):
        threads[i].join()
    return google_sents


if __name__ == "__main__":
    search_term = input('Words to search up: ')
    start_time = time.time()
    results = scrape_google(search_term)
    # print(results)
    for lk, sent, m, m_in in results:
        print(f"{lk}: {sent[m_in]}")
    print(time.time() - start_time)
