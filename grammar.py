import sys

from ply import yacc
from requests import get
from utils import apply_constraints
import lexer

tokens = lexer.tokens
assignments = dict()


def p_error(t):
    if t:
        print(f"Syntax error at '{t.value}' (line {t.lineno}, column {t.lexpos})", file=sys.stderr)
    else:
        print(f"Unexpected end of file", file=sys.stderr)


def p_default(p):
    """default : assignment
    | selection
    | stat
    """
    if p[1] is not None:
        if isinstance(p[1], list):
            print("\n".join(p[1]))
        else:
            print(p[1])


def p_default_error(p):
    """default : var error
    """
    print(f"Error: your query must be a selection, stat or an assigment", file=sys.stderr)


# Other
def p_assignment(p):
    """assignment : VAR EQUALS selection
    """
    var_name = p[1]
    value = p[3]
    assignments[var_name] = value


def p_assignment_url_error(t):
    """assignment : VAR EQUALS URL
    """
    print(f"Error: you cannot assign an url to a variable", file=sys.stderr)


def p_selection(p):
    """selection : value
    """
    p[0] = p[1]


def p_selection_constrains(p):
    """selection : value constraints_chain
    """
    p[0] = apply_constraints(p[1], p[2])


def p_value(p):
    """value : get
    | var
    """
    p[0] = p[1]


# Manipulations
def p_get(p):
    """get : GET URL
    """
    url = p[2]
    r = get(url)
    p[0] = r.text.splitlines()


def p_get_error(p):
    """get : GET error
    """
    print(f"Syntax for get is `get <url>`", file=sys.stderr)


def p_stat(p):
    """stat : STAT stat_values
    """
    p[0] = f'{len(p[2])} entries'


def p_stat_values(p):
    """stat_values : stat_operation"""
    p[0] = p[1]


def p_stat_values_constraints(p):
    """stat_values : stat_operation constraints_chain
    """
    p[0] = apply_constraints(p[1], p[2])


def p_constraints_chain(p):
    """constraints_chain : or
    | and
    | constraint
    """
    if isinstance(p[1][0], tuple):  # operand isn't an or
        p[0] = [p[1]]
    else:
        p[0] = p[1]


def p_or(p):
    """or : constraint OR constraint
    | constraint OR and
    | and OR constraint
    | and OR and
    | and OR or
    | constraint OR or"""
    if isinstance(p[3][0], tuple):  # right operand isn't an or
        p[0] = [p[1], p[3]]
    else:  # right operand is an or
        p[0] = p[3] + [p[1]]


def p_and(p):
    """and : constraint AND constraint
    | constraint AND and"""
    p[0] = p[1] + p[3]


def p_constraint(p):
    """constraint : constraint_word var"""
    p[0] = [(p[1], p[2])]


def p_constraint_error(p):
    """constraint_word : error var"""
    print(f'Constraint error: constraint must be `contains` or `exclude`! "{p[1].value}" given', file=sys.stderr)


def p_var(p):
    """var : VAR
    | SEARCH
    """
    p[0] = assignments.get(p[1], p[1])


def p_stat_operation(p):
    """stat_operation : union
    | intersect
    | diff
    """
    p[0] = list(set(p[1]))


def p_stat_operation_error(p):
    """stat_operation : error
    """
    print(f'Stat error: operation must be `union`, `intersect` or `diff`! "{p[1]}" given', file=sys.stderr)


def p_union(p):
    """union : selection UNION selection"""
    p[0] = p[1] + p[3]


def p_intersect(p):
    """intersect : selection INTERSECT selection"""
    p[0] = [value for value in p[1] if value in p[3]]


def p_diff(p):
    """diff : selection DIFF selection"""
    p[0] = p[1] - p[3]


# Words
def p_constraint_word(p):
    """constraint_word : CONTAINS
    | EXCLUDE
    """
    p[0] = p[1]


parser = yacc.yacc()
