import spacy
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_md")

doc = nlp("Elon Musk founded SpaceX")
print([(ent.text, ent.label_) for ent in doc.ents])

d = nlp("This is a text.")
print([token.tag_ for token in d])

doc = nlp("Neywork is the city of dreams. It has a population of 20.1 million")
for t in doc:
    print(t.text, t.lemma_, t.pos_, t.tag_, t.dep_,
            t.shape_, t.is_alpha, t.is_stop)
print()
tokens = nlp("python java php newyork data")
for t in tokens:
    print(t.text, t.has_vector, t.vector_norm, t.is_oov)

doc1 = nlp("Books are good")
doc2 = nlp("Wild is a good book")
print(doc1, "<->", doc2, doc1.similarity(doc2))