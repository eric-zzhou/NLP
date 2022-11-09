# Imports
import pandas as pd
import random
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

symbs = '!@#$%^&*()<>,;?\''

# Greetings, basically maps different user greetings to a random output greeting
greet_in = ('hey', 'sup', 'waddup', 'hi', 'hello', 'good day', 'heya', 'hiya', 'howdy',
            'greetings', 'yo', 'ahoy', 'ello')
greet_out = ['hey', 'hello', 'hi there', 'hi', 'heya', 'hiya', 'howdy', 'greetings', '\'ello']


def greeting(sent):
    for word in sent.split():
        if word.lower() in greet_in:
            return random.choice(greet_out)


# Small talk, basic questions and responses
small_talk_responses = {
    'how are you': 'I am fine. Thank you for asking',
    'how are you doing': 'I am fine. Thank you for asking',
    'how do you do': 'I am good. Thanks for asking',
    'how are you holding up': 'I am fine. Thank you for asking',
    'how is it going': 'It is going great. Thank you for asking',
    'good morning': 'Good Morning',
    'good afternoon': 'Good Afternoon',
    'good evening': 'Good Evening',
    'good day': 'Good day to you too',
    'whats up': 'The sky',
    'wassup': 'The sky',
    'sup': 'The sky',
    'thanks': 'Don\'t mention it. You are welcome',
    'thank you': 'Don\'t mention it. You are welcome'
}

# Getting string array of all responses
small_talk = small_talk_responses.values()
small_talk = [str(item) for item in small_talk]


# Find the closest small talk
def tfidf_cosim_smalltalk(query):
    query = [query]
    tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
    # Converts words to vectors
    tf_doc = tf.fit_transform(small_talk_responses)
    tf_query = tf.transform(query)
    # converts vert to hor list, one for each of the small talk qs
    cosineSimilarities = cosine_similarity(tf_doc, tf_query).flatten()
    related_docs_indices = cosineSimilarities.argsort()[:-2:-1]  # gets last value of the sorted list
    # Only responds if the similarity is higher than threshold of 0.98
    if cosineSimilarities[related_docs_indices] > 0.98:
        ans = [small_talk[i] for i in related_docs_indices[:1]]
        return ans[0]


# Managing name
def naming(name):
    a = name.split()
    nam = ''
    if 'my name is' in name:
        for j in a:
            if j not in 'mynameis':
                nam = j
    elif 'call me' in name:
        for j in a:
            if j not in 'callme':
                nam = j
    elif 'name is' in name:
        for j in a:
            if j not in 'nameis':
                nam = j
    elif 'change my name to' in name:
        for j in a:
            if j not in 'changemynameto':
                nam = j
    elif 'change name to' in name:
        for j in a:
            if j not in 'changenameto':
                nam = j
    else:
        nam = name
    nam = nam[0:1].upper() + nam[1:]
    return nam


if __name__ == "__main__":
    # https://www.microsoft.com/en-us/download/details.aspx?id=a333c41c-9704-4412-9fbc-15bb1fb7f5c3
    # Reading and cleaning data
    data = pd.read_csv(r"C:\Users\ezhou\PycharmProjects\NLP\Projects\WikiQA.tsv", sep='\t')
    data = data[data['Label'] == 1]
    data = data.reset_index()
    data = data.drop(['QuestionID', 'DocumentID', 'DocumentTitle',
                      'SentenceID', 'Label', 'index'], axis=1)

    # Combining into a list with all the text
    lm = WordNetLemmatizer()

    all_text = {}
    og_text = {}
    for index, row in data.iterrows():
        question = []
        for word in nltk.pos_tag(nltk.word_tokenize(''.join(
                filter(lambda i: i not in symbs, row['Question'])).lower()),
                                 tagset="universal"):
            w, p = word
            # print(w, p)
            if p == "VERB":
                question.append(lm.lemmatize(w, pos="v"))
            elif p == "NOUN":
                question.append(lm.lemmatize(w, pos="n"))
            elif p == "ADJ":
                question.append(lm.lemmatize(w, pos="a"))
            else:
                question.append(w)
        question = ' '.join(question)
        og_text[question] = row['Question']
        all_text[question] = row['Sentence']
    all_text = [str(item).lower() for item in all_text]
    # print(len(all_text))
    # print(og_text)

    stemmed_doc = []
    for text in all_text:
        tp = []
        for word in nltk.pos_tag(nltk.word_tokenize(text), tagset="universal"):
            w, p = word
            if p == "VERB":
                tp.append(lm.lemmatize(w, pos="v"))
            elif p == "NOUN":
                tp.append(lm.lemmatize(w, pos="n"))
            elif p == "ADJ":
                tp.append(lm.lemmatize(w, pos="a"))
            else:
                tp.append(w)
        stemmed_doc.append(' '.join(tp))
    tf = TfidfVectorizer(use_idf=True, sublinear_tf=True, stop_words=stopwords.words('english'))
    tf_doc = tf.fit_transform(stemmed_doc)


    # print(tf_doc.todense())

    # Stemming and figuring out importance of terms using tfidf
    def stem_tfidf(query):
        stemmed_query = []
        for word in nltk.pos_tag(nltk.word_tokenize(query.lower()),
                                 tagset="universal"):
            w, p = word
            # print(w, p)
            if p == "VERB":
                stemmed_query.append(lm.lemmatize(w, pos="v"))
            elif p == "NOUN":
                stemmed_query.append(lm.lemmatize(w, pos="n"))
            elif p == "ADJ":
                stemmed_query.append(lm.lemmatize(w, pos="a"))
            else:
                stemmed_query.append(w)
        stemmed_query = [' '.join(stemmed_query)]
        tf_query = tf.transform(stemmed_query)
        return tf_query


    # Getting cosine similarity between things and getting the answer
    def cos_sim(x):
        cosineSimilarities = cosine_similarity(tf_doc, x).flatten()
        # print(list(cosineSimilarities))
        related_docs_indices = cosineSimilarities.argsort()[:-2:-1]
        # print(related_docs_indices)
        if cosineSimilarities[related_docs_indices] > 0.5:
            ans = [data.loc[data['Question'] == og_text[all_text[i]]] for i in related_docs_indices[:1]]
            for item in ans:
                return item['Sentence'].iloc[0]
        else:
            k = 'I am sorry, I cannot help you with this one. Hope to in the future. Cheers :)'
            return k


    # Main loop
    BOT_NAME = "Bob"
    n = input(f'\nHello, my name is {BOT_NAME}. What is your name?:\t')
    name = naming(n)  # naming function
    while True:
        # User query
        query = input(f'\nHi {name}, I am {BOT_NAME}. How can I help you? If you want to exit, type Bye. : \t')
        query = ''.join((filter(lambda i: i not in symbs, query.lower())))
        # Exit
        if query == 'bye':
            print(f'\n{BOT_NAME}: This is {BOT_NAME} signing off. Bye, take care {name}')
            break

        # Changing names
        elif 'my name is' in query or 'call me' in query or 'name is' in query or 'change my name to' in query \
                or 'change name to' in query:
            name = naming(query)
            print(f'\n{BOT_NAME}: Your name is {name}')
        elif 'what' in query and 'my' in query and 'name' in query:
            print(name)
        elif 'what' in query and 'your' in query and 'name' in query:
            print(f"My name is {BOT_NAME}. Nice to meet you!")
        # Greeting
        elif greeting(query) is not None:
            print(f'\n{BOT_NAME}: {greeting(query)} {name}')
        # Small talk
        elif tfidf_cosim_smalltalk(query) is not None:
            x = tfidf_cosim_smalltalk(query)
            print(f'\n{BOT_NAME}: {x}')
        # Searching through corpus fo response
        else:
            x = stem_tfidf(query)
            g = cos_sim(x)
            print(f'\n{BOT_NAME}: {g}')
