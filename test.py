# from sklearn.feature_extraction.text import TfidfVectorizer
#
# hello = "chicken nuggets are cool chicken nuggets are cool chicken chicken are are are are are are"
# tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
# tf_yes = tf.fit_transform([hello])
# print(tf_yes, end="\n\n\n")
#
# something = tf.transform([" chicken cool chicken, chicken hello my name is lol"])
# print(type(something))
# print(something)
# print(sum(something.data))

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


sentences = [
    "Einstein age death",
    "Einstein died in 2015",
    "Bob died in 2015",
    "Einstein was a scientist"
]
sentence_embeddings = model.encode(sentences)
print(cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:]))
