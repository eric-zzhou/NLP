import nltk
from nltk.corpus import conll2000
from nltk.classify import megam

""" ------------------------- Regular Expression Parser ------------------------- """
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])  # get test data
grammar = r"NP: {<[CDJNP].*>+}"  # create grammar rule using regulear expressions
cp = nltk.RegexpParser(grammar)  # create regular expression parser based on grammar rule
print(cp.accuracy(test_sents))  # evaluate chunk parser

""" ------------------------- Bigram Chunker ------------------------- """


class BigramChunker(nltk.ChunkParserI):
    def __init__(self, tr_sents):
        # Take train_data, "w" is word, "t" is POS tag, "c" is chunk tag
        train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sent)]
                      for sent in tr_sents]
        self.tagger = nltk.BigramTagger(train_data)  # create tagger

    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]  # get POS tags for sentence
        tagged_pos_tags = self.tagger.tag(pos_tags)  # use tagger on POS tags
        # Reorganizing array
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)  # return tree representation of chunks


train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])  # training dataset
bigram_chunker = BigramChunker(train_sents)  # training bigram chunker
print(bigram_chunker.accuracy(test_sents))  # evaluating results
postags = sorted(set(pos for sent in train_sents
                     for (word, pos) in sent.leaves()))
print(bigram_chunker.tagger.tag(postags))  # checking the tag rules

""" ------------------------- Consecutive Chunker ------------------------- """


class ConsecutiveNPChunkTagger(nltk.TaggerI):
    def __init__(self, tr_sents):
        train_set = []
        # Getting features for words and tracking history for sequence
        for tagged_sent in tr_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        # Using maximum entropy classifier
        self.classifier = nltk.MaxentClassifier.train(train_set, algorithm='GIS', trace=0)

    def tag(self, sentence):
        # Tag set using features and tracking history
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)


class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, tr_sents):
        # Take train_data, "w" is word, "t" is POS tag, "c" is chunk tag
        tagged_sents = [[((w, t), c) for (w, t, c) in nltk.chunk.tree2conlltags(sent)]
                        for sent in tr_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)  # create tagger

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)  # tag sentences
        conlltags = [(w, t, c) for ((w, t), c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)


# Function to generate features for consecutive parser
def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    # Previous word and its POS
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i - 1]
    # Next word and its POS
    if i == len(sentence) - 1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i + 1]
    return {"pos": pos,  # current POS
            "word": word,  # current word
            "prevpos": prevpos,  # previous word's POS
            "nextpos": nextpos,  # next word's POS
            "prevpos+pos": f"{prevpos}+{pos}",
            "pos+nextpos": f"{pos}+{nextpos}",
            "tags-since-dt": tags_since_dt(sentence, i)}  # tags since determiners


# Function to find tags since last determiner
def tags_since_dt(sentence, i):
    tags = set()
    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()  # reset to empty set
        else:
            tags.add(pos)  # add non-determiner word
    return '+'.join(sorted(tags))  # returns string


chunker = ConsecutiveNPChunker(train_sents)
print(chunker.accuracy(test_sents))
