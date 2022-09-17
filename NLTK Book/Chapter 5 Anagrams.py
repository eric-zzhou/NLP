from collections import defaultdict
import nltk

words = nltk.corpus.words.words('en')
print("stare" in words)

anagrams = defaultdict(list)
for word in words:
    key = ''.join(sorted(word))  # sorts letters in word alphabeticaally and recombines it
    anagrams[key].append(word)

# anagrams = nltk.Index((''.join(sorted(w)), w) for w in words)


def get_anagrams(s):
    return anagrams[''.join(sorted(s))]


print(get_anagrams('rates'))