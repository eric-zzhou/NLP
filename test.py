from sklearn.feature_extraction.text import TfidfVectorizer

hello = "chicken nuggets are cool chicken nuggets are cool chicken chicken are are are are are are"
tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
tf_yes = tf.fit_transform([hello])
print(tf_yes, end="\n\n\n")

something = tf.transform([" chicken cool chicken, chicken"])
print(type(something))
print(something)
print(sum(something.data))
