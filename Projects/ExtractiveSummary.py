# Created based on this tutorial:
# https://towardsdatascience.com/report-is-too-long-to-read-use-nlp-to-create-a-summary-6f5f7801d355

import nltk
import re
import heapq
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from collections import defaultdict
from HTMLCleaner import text_from_html

stop = set(stopwords.words('english') + ["com"])
MAX_SENT_LEN = 25


# https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup#comment28302706_1983219

def clean_text(text):
    # Cleaning up text
    # text = re.sub(r'[0-9]+', ' ', text)  # replace all numbers
    # text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)  # replace all multiple spaces in a rows
    # print(text)
    clean_text = text.lower()
    # replace characters other than [a-zA-Z0-9], digits & one or more spaces with single space
    regex_patterns = [r'\W', r'\d',
                      r'\s+']  # \W is any nonalpha numerical, \d is any number, \s+ is 1 or more whitespaces
    for regex in regex_patterns:
        clean_text = re.sub(regex, ' ', clean_text)
    # print(clean_text)

    # Break into sentences
    sentences = nltk.sent_tokenize(text)
    # print(sentences)

    # Check word importance
    clean_words = [w.lower() for w in word_tokenize(clean_text) if w not in stop]
    return clean_words, sentences


def generate_freq_sumsent(sentences, length):
    text = ' '.join(sentences)
    return generate_freq_summary(text, length)


# Frequency scoring
def generate_freq_summary(text, length):
    clean_words, sentences = clean_text(text)
    fd = FreqDist(clean_words)
    freq_sent_score = defaultdict(int)
    for sent in sentences:
        s_words = [w for w in word_tokenize(sent.lower()) if w in fd]
        if len(s_words) < MAX_SENT_LEN:
            for word in s_words:
                freq_sent_score[sent] += fd[word]
    # print(freq_sent_score)
    # Summary based on frequency
    freq_best_sents = heapq.nlargest(length, freq_sent_score, key=freq_sent_score.get)
    freq_summarized_text = ""
    for sent in sentences:
        if sent in freq_best_sents:
            freq_summarized_text += sent + ' '
    return freq_summarized_text


if __name__ == "__main__":
    # Constants and user input
    DEFAULT_LINK = "https://www.hcn.org/issues/138/barry-lopez-we-are-shaped-by-the-sound-of-wind-the-slant-of-sunlight"
    DEFAULT_SENT = 3

    url = input('Article to summarize: ')
    if url == 'd':
        url = DEFAULT_LINK
    elif url == 'custom':
        url = False
    top_n = input('Summary length (in sentences): ')
    if top_n == 'd':
        top_n = DEFAULT_SENT
    else:
        top_n = int(top_n)

    if url:
        # Webscraping portion
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        html = urlopen(req).read().decode('utf8')
        text = text_from_html(html)
    else:
        thing = input("Is custom file updated? \t")
        if 'n' in thing:
            exit(1)
        else:
            with open('customtest.txt') as f:
                text = f.readlines()
            text = '\n'.join(text)

    print("\n\nWord-Frequency Based Summary:")
    print(generate_freq_summary(text, top_n), end='\n\n\n')