from BaseChatbot import naming, greeting, tfidf_cosim_smalltalk, symbs
from ExtractiveSummary import generate_freq_sumsent
from GoogleTestImprov import scrape_google

# Main loop
BOT_NAME = "NotGoogle"
result = [None] * 5
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
    # Getting summary
    elif query.startswith("summary"):
        try:
            ii = int(query[7:])
        except ValueError:
            print(f"{BOT_NAME}: Summary is a function that requires to be followed by a number e.g. summary(n)")
            continue
        if ii < 1 or ii > 5:
            print(f"{BOT_NAME}: Value provided to summary function out of bounds, should be from 1 to 5")
            continue
        ii -= 1
        if result[ii]:
            print(f'\n{BOT_NAME}:')
            print(f'\t{generate_freq_sumsent(result[ii][1], 3)}')
        else:
            print(f'\n{BOT_NAME}: Please enter a query before getting a summary')
    # Getting context
    elif query.startswith("context"):
        try:
            ii = int(query[7:])
        except ValueError:
            print(f"{BOT_NAME}: Context is a function that requires to be followed by a number e.g. context(n)")
            continue
        if ii < 1 or ii > 5:
            print(F"{BOT_NAME}: Value provided to context function out of bounds, should be from 1 to 5")
            continue
        ii -= 1
        if result[ii]:
            print(f'\n{BOT_NAME}:')
            lk, sent, m, m_in = result[ii]
            s = sent[m_in]
            if m_in >= 1:
                s = sent[m_in - 1] + " " + s
            if m_in <= len(sent) - 2:
                s = s + " " + sent[m_in + 1]
            print(f'\t{s}')
        else:
            print(f'\n{BOT_NAME}: Please enter a query before getting the context')
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
        print(f'\n{BOT_NAME}: ')
        result.sort(key=lambda z: z[2], reverse=True)
        for ind, cont in enumerate(result):
            lk, sent, m, m_in = cont
            print(f"\t{ind + 1}. {lk}: {sent[m_in]}")
