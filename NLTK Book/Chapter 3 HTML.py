import nltk, re, pprint
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize

url = "https://www.economist.com/middle-east-and-africa/2018/04/19/lebanons-political-system-leads-to-paralysis-and" \
      "-corruption "
req = Request(
    url=url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
html = urlopen(req).read().decode('utf8')
# print(html[:60])

raw = bs(html, 'html.parser').get_text()
raw = raw.replace(".", ". ")
start = raw.find("IT IS difficult")
end = raw.rfind("limp along")
tokens = word_tokenize(raw[start:end])
text = nltk.Text(tokens)
print(text.concordance("Lebanon"))
