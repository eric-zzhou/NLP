import math

import nltk
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop = set(stopwords.words('english') + ["com"])

url = input("What link would you like to scrape? ")
# https://www.cnn.com/2022/09/20/sport/magnus-carlsen-hans-niemann-chess-spt-intl/index.html
req = Request(
    url=url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
html = urlopen(req).read().decode('utf8')
# print(html[:60])

startstr = input("What are the first 2 words of the article? ").lower()  # shortly after
endstr = input("What are the final 2 words of the article? ").lower()  # a solution

raw = bs(html, 'html.parser').get_text().lower()
raw = raw.replace(".", ". ")
start = raw.find(startstr)
end = raw.rfind(endstr)
tokens = word_tokenize(raw[start:(end + len(endstr))])
length = len(tokens)

lemmatizer = WordNetLemmatizer()
clean_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop and token.isalpha()]
text = nltk.Text(clean_tokens)
print([clean_tokens])

fdist = FreqDist(text)
print(fdist.most_common(15))
print(sorted(w for w in set(text) if fdist[w] > int(length / 250)))

