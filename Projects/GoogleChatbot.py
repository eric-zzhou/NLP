from BaseChatbot import naming, greeting, tfidf_cosim_smalltalk, symbs
from ExtractiveSummary import generate_freq_sumsent
from GoogleTest import scrape_google

# Main loop
BOT_NAME = "NotGoogle"
result = None
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
    else:
        result = scrape_google(query)
        # todo add numbers to link and be able to get summaries and sentences around
        print(f'\n{BOT_NAME}: ')
        result.sort(key=lambda z: z[2], reverse=True)
        for ind, cont in enumerate(result):
            lk, sent, m, m_in = cont
            print(f"\t{ind + 1}. {lk}: {sent[m_in]}")
