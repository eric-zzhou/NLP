from BaseChatbot import naming, greeting, tfidf_cosim_smalltalk, symbs
from ExtractiveSummary import generate_freq_summary

# Main loop
BOT_NAME = "NotGoogle"
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
        print("lol u suck")
    # Searching through corpus fo response
    # else:
    #     x = stem_tfidf(query)
    #     g = cos_sim(x)
    #     print(f'\n{ACT_BOT_NAME}: {g}')
