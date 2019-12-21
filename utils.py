def apply_constraints(input_values, or_constraints):
    keep = []
    for constraints in or_constraints:
        values = input_values
        for constraint, string in constraints:
            if constraint == 'contains':
                values = [item for item in values if string in item]
            elif constraint == 'exclude':
                values = [item for item in values if string not in item]
        keep += values
    return list(set(keep))  # remove duplicates
