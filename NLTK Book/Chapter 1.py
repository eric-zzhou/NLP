from nltk.book import *

text1.similar("monstrous")

fdist1 = FreqDist(text1)
fdist1.most_common(50)
print(fdist1['whale'])

# Returns sorted list of all words in text1 that are longer than 10 letters and occur more than 5 times
print(sorted(w for w in set(text1) if len(w) > 10 and fdist1[w] > 5))


def lexical_diversity(text):
    return len(set(text)) / len(text)


def percentage(count, total):
    return 100 * count / total
