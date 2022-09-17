import nltk


def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())  # lowers all alphabet words
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())  # lowers all corpus words
    unusual = text_vocab - english_vocab  # gets rid of normal words
    return sorted(unusual)  # returns weird or misspelled words


print(unusual_words(nltk.corpus.gutenberg.words('austen-sense.txt')))
print(nltk.corpus.stopwords.words('english'))
