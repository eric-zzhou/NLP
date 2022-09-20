import nltk
from nltk.sem import chat80
from nltk import load_parser

nltk.data.show_cfg('grammars/book_grammars/sql0.fcfg')  # grammar configuration
cp = load_parser('grammars/book_grammars/sql0.fcfg')  # load grammar
query = "Which cities are in China"  # query
trees = list(cp.parse(query.split()))  # parse the query
answer = trees[0].label()['SEM']  # get the SEM parts, the meaning
answer = [s for s in answer if s]  # get rid of nulls
q = ' '.join(answer)  # combine into string
print(q)

# Putting query into SQL table
rows = chat80.sql_query('corpora/city_database/city.db', q)
print([r[0] for r in rows], end=" ")
