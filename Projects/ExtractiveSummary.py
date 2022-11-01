# Created based on this tutorial:
# https://towardsdatascience.com/report-is-too-long-to-read-use-nlp-to-create-a-summary-6f5f7801d355

import nltk
import re
import heapq
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords, reuters
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

# Constants and user input
MAX_SENT_LEN = 25
DEFAULT_LINK = "https://www.hcn.org/issues/138/barry-lopez-we-are-shaped-by-the-sound-of-wind-the-slant-of-sunlight#:~:text=Barry%20Lopez%3A%20We%20are%20shaped,Country%20News%20–%20Know%20the%20West"
DEFAULT_START = "in the"
DEFAULT_END = "of community"
DEFAULT_SENT = 3
url = input('Article to summarize: ')
if url == 'd':
    url = DEFAULT_LINK
elif url == 'custom':
    url = False
top_n = input('Summary length (in sentences): ')
if top_n == 'd':
    top_n = DEFAULT_SENT

if url:
    # Webscraping portion
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    html = urlopen(req).read().decode('utf8')

    # Limiting it down to actual content
    startstr = input("What are the first 2 words of the article? ").lower()
    if startstr == 'd':
        startstr = DEFAULT_START
    endstr = input("What are the final 2 words of the article? ").lower()
    if endstr == 'd':
        endstr = DEFAULT_END
    print("\n\n")
    raw = bs(html, 'html.parser').get_text()
    raw = raw.replace(".", ". ")
    low_raw = raw.lower()
    start = low_raw.find(startstr.lower())
    end = low_raw.rfind(endstr.lower())
    text = raw[start:(end + len(endstr))]
else:
    thing = input("Is custom file updated? \t")
    if 'n' in thing:
        exit(1)
    else:
        with open('customtest.txt') as f:
            text = f.readlines()
        text = '\n'.join(text)
# Cleaning up text
# text = re.sub(r'[0-9]+', ' ', text)  # replace all numbers
# text = re.sub(r'\[[0-9]*\]', ' ', text)
text = re.sub(r'\s+', ' ', text)  # replace all multiple spaces in a rows
# print(text)
clean_text = text.lower()
# replace characters other than [a-zA-Z0-9], digits & one or more spaces with single space
regex_patterns = [r'\W', r'\d', r'\s+']  # \W is any nonalpha numerical, \d is any number, \s+ is 1 or more whitespaces
for regex in regex_patterns:
    clean_text = re.sub(regex, ' ', clean_text)
# print(clean_text)

# Break into sentences
sentences = nltk.sent_tokenize(text)
# print(sentences)

# Check word importance
stop = set(stopwords.words('english') + ["com"])
clean_words = [w.lower() for w in word_tokenize(clean_text) if w not in stop]
fd = FreqDist(clean_words)
news_words = [w.lower() for fid in reuters.fileids() for w in reuters.words(fid) if w.isalpha()]
# print(news_words)
tf_news = TfidfVectorizer(use_idf=True, sublinear_tf=True, stop_words=stop)
tf_news_doc = tf_news.fit_transform([' '.join(news_words)])
tf = TfidfVectorizer(use_idf=True, sublinear_tf=True, stop_words=stop)
tf_this = tf.fit_transform([' '.join(w for w in word_tokenize(text.lower()) if w.isalpha())])

# Frequency scoring
freq_sent_score = defaultdict(int)
for sentence in sentences:
    s_words = [w for w in word_tokenize(sentence.lower()) if w in fd]
    if len(s_words) < MAX_SENT_LEN:
        for word in s_words:
            freq_sent_score[sentence] += fd[word]
print(freq_sent_score)
# Summary based on frequency
print("Word-Frequency Based Summary:")
freq_best_sents = heapq.nlargest(int(top_n), freq_sent_score, key=freq_sent_score.get)
freq_summarized_text = ""
for sentence in sentences:
    if sentence in freq_best_sents:
        freq_summarized_text += sentence + ' '
print(freq_summarized_text, end="\n\n\n")

# Current news doc TFIDF scoring
btf_sent_score = {}
for sentence in sentences:
    sent_len = len(word_tokenize(sentence))
    if sent_len < MAX_SENT_LEN:
        btf_sent_score[sentence] = sum(tf.transform([sentence]).data)
# Summary based on current news doc TFIDF
print("Current Article TFIDF Based Summary:")
btf_best_sents = heapq.nlargest(int(top_n), btf_sent_score, key=btf_sent_score.get)
btf_summarized_text = ""
for sentence in sentences:
    if sentence in btf_best_sents:
        btf_summarized_text += sentence + ' '
print(btf_summarized_text, end="\n\n\n")

# News TFIDF scoring
tf_sent_score = {}
for sentence in sentences:
    sent_len = len(word_tokenize(sentence))
    if sent_len < MAX_SENT_LEN:
        tf_sent_score[sentence] = sum(tf_news.transform([sentence]).data)
# Summary based on current news doc TFIDF
print("News Corpus TFIDF Based Summary:")
tf_best_sents = heapq.nlargest(int(top_n), tf_sent_score, key=tf_sent_score.get)
tf_summarized_text = ""
for sentence in sentences:
    if sentence in tf_best_sents:
        tf_summarized_text += sentence + ' '
print(tf_summarized_text)
