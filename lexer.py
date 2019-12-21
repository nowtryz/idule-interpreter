from ply import lex

tokens = (
    'EQUALS',
    'AND', 'OR',
    'GET', 'STAT',
    'CONTAINS', 'EXCLUDE',
    'UNION', 'INTERSECT', 'DIFF',
    'SEARCH',
    'VAR',
    'URL',
)

restricted_words = {
    'and': 'AND',
    'or': 'OR',
    'get': 'GET',
    'stat': 'STAT',
    'contains': 'CONTAINS',
    'exclude': 'EXCLUDE',
    'union': 'UNION',
    'intersect': 'INTERSECT',
    'diff': 'DIFF',
}

t_ignore = ' \t'
t_EQUALS = r'='


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t


def t_URL(t):
    r'https?:\/\/(?:[A-Za-z0-9][-\w.]*\.[A-Za-z]{2,}|[\w]*)(?:\/[-.\w]+)*'
    return t


def t_NAME(t):
    r'[A-Za-z][\w-]*'
    t.type = restricted_words.get(t.value, 'VAR')
    return t


def t_SEARCH(t):
    r'\w+'
    return t


lexer = lex.lex()
