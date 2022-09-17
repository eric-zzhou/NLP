import nltk
from nltk.corpus import names
from nltk.classify import apply_features
import random

# Getting labeled data
labeled_names = ([(name, 'male') for name in names.words("male.txt")] +
                 [(name, 'female') for name in names.words("female.txt")])
random.shuffle(labeled_names)


# Function to get features
def gender_features(name):
    name = name.lower()
    features = {"first_letter": name[0],
                "last_letter": name[-1],
                "suffix": name[-2:]}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features[f"count({letter})"] = name.count(letter)
    return features


# Split into training and test sets
# featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
# train_set, test_set = featuresets[500:], featuresets[:500]
train_set = apply_features(gender_features, labeled_names[1500:])
devtest_names = labeled_names[500:1500]
devtest_set = apply_features(gender_features, devtest_names)
test_set = apply_features(gender_features, labeled_names[:500])
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Testing classifier
# print(classifier.classify(gender_features("Neo")))
# print(classifier.classify(gender_features("Trinity")))
print(nltk.classify.accuracy(classifier, devtest_set))

# Error analysis
errors = []
for (name, tag) in devtest_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append((tag, guess, name))

for (tag, guess, name) in sorted(errors):
    print(f"correct={tag:<8} guess={guess:<8} name={name:<30}")

classifier.show_most_informative_features(5)

# Testing
print(nltk.classify.accuracy(classifier, test_set))
