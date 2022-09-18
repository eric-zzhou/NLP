import nltk

groucho_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")


def init_wfst(tokens, grammar):
    numtokens = len(tokens)  # number of word tokens
    wfst = [[None for i in range(numtokens + 1)] for j in range(numtokens + 1)]  # create (n+1) x (n+1) table
    # Loops through each word checking right side and possible left-hand sides
    for i in range(numtokens):
        productions = grammar.productions(rhs=tokens[i])
        wfst[i][i + 1] = productions[0].lhs()  # Left-hand side of equation
    return wfst


def complete_wfst(wfst, tokens, grammar, trace=False):
    # Get grammar rules in dictionary
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    numtokens = len(tokens)
    # Looping through tokens to group tokens and find categories
    for span in range(2, numtokens + 1):
        for start in range(numtokens + 1 - span):
            end = start + span
            for mid in range(start + 1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                if nt1 and nt2 and (nt1, nt2) in index:
                    wfst[start][end] = index[(nt1, nt2)]
                    if trace:
                        print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % \
                              (start, nt1, mid, nt2, end, start, index[(nt1, nt2)], end))
    return wfst


# Pretty displace of the table
def display(wfst, tokens):
    print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(wfst))))
    for i in range(len(wfst) - 1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-4s" % (wfst[i][j] or '.'), end=" ")
        print()


tokens = "I shot an elephant in my pajamas".split()
wfst0 = init_wfst(tokens, groucho_grammar)
display(wfst0, tokens)
wfst1 = complete_wfst(wfst0, tokens, groucho_grammar)
display(wfst1, tokens)
