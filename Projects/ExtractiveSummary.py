# Created based on this tutorial:
# https://towardsdatascience.com/report-is-too-long-to-read-use-nlp-to-create-a-summary-6f5f7801d355

import nltk
import re
import heapq
import numpy as np
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Constants and user input
MAX_SENT_LEN = 30
url = input('Article to summarize: ')
# https://www.cnn.com/2022/09/20/sport/magnus-carlsen-hans-niemann-chess-spt-intl/index.html
top_n = input('Summary length (in sentences): ')

# Webscraping portion
req = Request(
    url=url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
html = urlopen(req).read().decode('utf8')

# Limiting it down to actual content
startstr = input("What are the first 2 words of the article? ").lower()  # shortly after
endstr = input("What are the final 2 words of the article? ").lower()  # a solution
raw = bs(html, 'html.parser').get_text().lower()
raw = raw.replace(".", ". ")
start = raw.find(startstr)
end = raw.rfind(endstr)
text = raw[start:(end + len(endstr))]

# Cleaning up text
# text = re.sub(r'[0-9]+', ' ', text)  # replace all numbers
# text = re.sub(r'\[[0-9]*\]', ' ', text)
text = re.sub(r'\s+', ' ', text)  # replace all multiple spaces in a rows
print(text)
clean_text = text
# replace characters other than [a-zA-Z0-9], digits & one or more spaces with single space
regex_patterns = [r'\W', r'\d', r'\s+']  # \W is any nonalpha numerical, \d is any number, \s+ is 1 or more whitespaces
for regex in regex_patterns:
    clean_text = re.sub(regex, ' ', clean_text)
print(clean_text)

# Break into sentences
sentences = nltk.sent_tokenize(text)
print(sentences)

# todo maybe make this tfidf instead
# Check word frequency
stop = set(stopwords.words('english') + ["com"])
fd = nltk.FreqDist(w.lower() for w in nltk.word_tokenize(clean_text) if w not in stop)
print(dict(fd))

# sentence_score = {}
# for sentence in sentences:
#     for word in nltk.word_tokenize(sentence.lower()):
#         if word in word_count.keys():
#             if len(sentence.split(' ')) < MAX_SENT_LEN:
#                 if sentence not in sentence_score.keys():
#                     sentence_score[sentence] = word_count[word]
#                 else:
#                     sentence_score[sentence] += word_count[word]

# Generate summary
# best_sentences = heapq.nlargest(int(top_n), sentence_score, key=sentence_score.get)
# summarized_text = []
# sentences = nltk.sent_tokenize(text)
# for sentence in sentences:
#     if sentence in best_sentences:  # TODO this seems stupid
#         summarized_text.append(sentence)
#
# summary = "\n".join(summarized_text)
#
# print(summary)
