# https://stackoverflow.com/questions/38619478/google-search-web-scraping-with-python

from urllib.request import Request, urlopen
import urllib.parse as urlpar
from bs4 import BeautifulSoup as bs
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from HTMLCleaner import text_from_html

# todo multithreading

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Constants and user input
GOOGLE_LINK = "https://www.google.com/search?q="
stop = set(stopwords.words('english') + ["com"])


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
    google_sents = []
    for link in links:
        # print("Getting: " + link)
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
        if not sentences:
            google_sents.append((link, "Error in scraping", -1, -1))
            continue
        sentence_embeddings = model.encode(query + sentences)
        sims = cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:])
        index_max = np.argmax(sims)
        google_sents.append((link, sentences, np.max(sims), index_max))
        # print(generate_freq_summary(text, 3))
        # print(sentences[index_max])
    return google_sents


if __name__ == "__main__":
    search_term = input('Words to search up: ')
    results = scrape_google(search_term)
    # print(results)
    for lk, sent, m, m_in in results:
        print(f"{lk}: {sent[m_in]}")
