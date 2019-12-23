from sys import stderr
from ply import yacc
from requests import get, RequestException
from utils import apply_constraints
import lexer

tokens = lexer.tokens
assignments = dict()


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno}, column {p.lexpos})", file=stderr)
    else:
        print("Unexpected end of file", file=stderr)


def p_default(p):
    """default : assignment
    | selection
    | stat"""
    if p[1] is not None:
        if isinstance(p[1], list):
            print("\n".join(p[1]))
        else:
            print(p[1])


def p_default_error(p):
    """default : var error"""
    print("Error: your query must be a selection, stat or an assigment", file=stderr)


# Other
def p_assignment(p):
    """assignment : VAR EQUALS selection"""
    var_name = p[1]
    value = p[3]
    assignments[var_name] = value


def p_assignment_url_error(p):
    """assignment : VAR EQUALS URL"""
    print("Error: you cannot assign an url to a variable", file=stderr)


def p_selection(p):
    """selection : value"""
    p[0] = p[1]


def p_selection_constrains(p):
    """selection : value constraints_chain"""
    p[0] = apply_constraints(p[1], p[2])


def p_value(p):
    """value : get
    | var"""
    p[0] = p[1]


# Manipulations
def p_get(p):
    """get : GET URL"""
    url = p[2]
    try:
        r = get(url)
        p[0] = r.text.splitlines()
    except RequestException:
        p[0] = []
        print("An error occurred while fetching", url, file=stderr)


def p_get_error(p):
    """get : GET error"""
    print("Syntax error: syntax for get is `get <url>`", file=stderr)


def p_stat(p):
    """stat : STAT stat_values"""
    p[0] = f'{len(p[2])} entries'


def p_stat_error(p):
    """stat : STAT selection"""
    print('Syntax error: syntax for stat is `stat <set> (intersect | diff | union) <set> [<constraint>]`', file=stderr)


def p_stat_values(p):
    """stat_values : stat_operation"""
    p[0] = p[1]


def p_stat_values_constraints(p):
    """stat_values : stat_operation constraints_chain"""
    p[0] = apply_constraints(p[1], p[2])


def p_stat_operation_error(p):
    """stat_operation : selection UNION
    | selection INTERSECT
    | selection DIFF"""
    print(f'Missing right operand for {p[2]}', file=stderr)


def p_stat_operation_unknown(p):
    """stat_operation : selection error selection"""
    print(f'Syntax error: operation must be `union`, `intersect` or `diff`!", {p[1]}, "given', file=stderr)


def p_stat_operation_union(p):
    """stat_operation : selection UNION selection"""
    p[0] = p[1] + p[3]


def p_stat_operation_intersect(p):
    """stat_operation : selection INTERSECT selection"""
    p[0] = [value for value in p[1] if value in p[3]]


def p_stat_operation_diff(p):
    """stat_operation : selection DIFF selection"""
    p[0] = [value for value in p[1] if value not in p[3]]


def p_constraints_chain(p):
    """constraints_chain : constraint"""
    p[0] = [p[1]]


def p_constraints_chain_or(p):
    """constraints_chain : or"""
    p[0] = p[1]


def p_or(p):
    """or : constraint OR constraint"""
    p[0] = [p[1], p[3]]


def p_or_recursive(p):
    """or : constraint OR or"""
    p[0] = p[3] + [p[1]]


def p_constraint_and(p):
    """constraint : constraint AND constraint"""
    p[0] = p[1] + p[3]


def p_constraint(p):
    """constraint : CONTAINS var
    | EXCLUDE var"""
    p[0] = [(p[1], p[2])]


def p_constraint_error(p):
    """constraint : error var"""
    print(f'Constraint error: constraint must be `contains` or `exclude`! "{p[1].value}" given', file=stderr)


def p_var(p):
    """var : VAR
    | SEARCH"""
    p[0] = assignments.get(p[1], p[1])


parser = yacc.yacc()
