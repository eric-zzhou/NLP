import nltk

''' Gutenberg stuff '''
from nltk.corpus import gutenberg

# print(gutenberg.fileids())
# emma = gutenberg.words('austen-emma.txt')

# for fileid in gutenberg.fileids():
#     num_chars = len(gutenberg.raw(fileid))
#     num_words = len(gutenberg.words(fileid))
#     num_sents = len(gutenberg.sents(fileid))  # sentences
#     num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
#     # Prints avg len of words, avg len of sentences, average num of repeats
#     print(round(num_chars / num_words), round(num_words / num_sents), round(num_words / num_vocab), fileid)

# macbeth_sentences = gutenberg.sents('shakespeare-macbeth.txt')
# print(macbeth_sentences)

''' Webtext'''
# from nltk.corpus import webtext
# for fileid in webtext.fileids():
#     print(fileid, webtext.raw(fileid)[:65],
#

'''Brown '''
# from nltk.corpus import brown
#
# brown.categories()
# brown.fileids()
# brown.words(categories='news')
# brown.words(fileids=['cg22'])
# brown.sents(categories=['news', 'editorial', 'reviews'])
#
# cfd = nltk.ConditionalFreqDist(
#     (genre, word)
#     for genre in brown.categories()
#     for word in brown.words(categories=genre))
# genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
# modals = ['can', 'could', 'may', 'might', 'must', 'will']
# cfd.tabulate(conditions=genres, samples=modals)

''' Reuters '''
# from nltk.corpus import reuters
# reuters.categories()
# reuters.categories('training/9865')
# reuters.fileids('barley')
# reuters.fileids(['barley', 'corn'])

''' Presidential Inauguration '''
from nltk.corpus import inaugural

cfd = nltk.ConditionalFreqDist(
    (target, fid[:4])
    for fid in inaugural.fileids()
    for w in inaugural.words(fid)
    for target in ['america', 'citizen']
    if w.lower().startswith(target))
cfd.plot()
