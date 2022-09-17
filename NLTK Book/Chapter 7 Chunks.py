import nltk
from nltk.corpus import conll2000

""" Regular Expression Parser """
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
grammar = r"NP: {<[CDJNP].*>+}"
cp = nltk.RegexpParser(grammar)
print(cp.evaluate(test_sents))

""" Unigram Chunker """

