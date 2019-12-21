from grammar import parser
from lexer import lexer

print(
    'Welcome to Idule interpreter!',
    'Use an "!" at the end of a query to get the lexic used for this query.'
    'Example of queries:',
    sep='\n', end=''
)
print(
    '',
    'r1 = get http://localhost/idule.txt contains toto and exclude titi or contains blabla',
    'stat r1 intersect r2 contains Trump and contains Clinton',
    sep='\n\t',
)

while True:
    test = input('>> ')
    if test[-1] == '!':
        test = test[:-1]
        lexer.input(test)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok.type)
        print(*tokens)

    if test == 'exit':
        break

    parser.parse(test)
