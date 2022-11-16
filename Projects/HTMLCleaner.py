from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from urllib.request import Request, urlopen
from nltk import sent_tokenize


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def check_sents(element):
    count = 0
    for sent in sent_tokenize(element):
        if len(sent.strip().split()) >= 3:
            count += 1
    if count >= 3:
        return True
    else:
        return False


def text_from_html(body):
    soup = bs(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    split_text = " ".join(visible_texts).split("\n")
    # print(split_text)
    actual_texts = filter(check_sents, split_text)
    # print(list(actual_texts))
    return ' '.join(text.strip() for text in actual_texts)


if __name__ == "__main__":
    url = r"https://www.nationalgeographic.com/science/article/einstein-relativity-lasers-solar-genius-science#:~:text=Albert%20Einstein%20is%20justly%20famous,%2C%20gravity%2C%20and%20the%20universe"
    req = Request(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'}
    )
    html = urlopen(req).read().decode('utf8')
    # bs1 = bs(html, 'html.parser')
    # with open("test.txt", "w") as text_file:
    #     text_file.write(" ".join(bs1.findAll(text=True)))
    print(text_from_html(html))

