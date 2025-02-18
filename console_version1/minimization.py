from sympy.logic.boolalg import Or, And, Not
from sympy.logic.boolalg import simplify_logic
from sympy import symbols

def minimize_dnf_as_implicants(num_vars, true_terms):

    result = ""

    variable_list = symbols(f"x0:{num_vars}")
    all_combinations = [list(map(int, f"{i:0{num_vars}b}")) for i in range(2**num_vars)]
    
    minterms = []
    for index in true_terms:
        term = And(*[var if val else ~var for var, val in zip(variable_list, all_combinations[index])])
        minterms.append(term)
    
    dnf_expression = Or(*minterms)
    minimized_expression = simplify_logic(dnf_expression, form='dnf')

    def implicant_to_string(implicant):
        term_str = ["X"] * num_vars
        for lit in implicant.args if isinstance(implicant, And) else [implicant]:
            if lit in variable_list:
                term_str[variable_list.index(lit)] = "1"
            elif isinstance(lit, Not) and lit.args[0] in variable_list:
                term_str[variable_list.index(lit.args[0])] = "0"
        return "".join(term_str)

    implicants = [implicant_to_string(term) for term in minimized_expression.args] \
        if isinstance(minimized_expression, Or) else [implicant_to_string(minimized_expression)]

    for set in implicants:

        new_set = ""

        for e in set: new_set += f"{e} ∧ "

        new_set = new_set.rstrip(' ∧ ')
        result += f"({new_set}) ∨ "

    result = result.rstrip(' ∨ ')
    result = "МДНФ: " + result

    return result, implicants

def minimize_cnf_as_implicants(num_vars, false_terms):

    result = ""

    variable_list = symbols(f"x0:{num_vars}")
    all_combinations = [list(map(int, f"{i:0{num_vars}b}")) for i in range(2**num_vars)]

    maxterms = []
    for index in false_terms:
        term = Or(*[~var if val else var for var, val in zip(variable_list, all_combinations[index])])
        maxterms.append(term)

    cnf_expression = And(*maxterms)
    minimized_expression = simplify_logic(cnf_expression, form='cnf')

    def implicant_to_string(implicant):

        term_str = ["X"] * num_vars
        for lit in implicant.args if isinstance(implicant, Or) else [implicant]:
            if lit in variable_list:
                term_str[variable_list.index(lit)] = "1"
            elif isinstance(lit, Not) and lit.args[0] in variable_list:
                term_str[variable_list.index(lit.args[0])] = "0"
        return "".join(term_str)

    implicants = [implicant_to_string(term) for term in minimized_expression.args] \
        if isinstance(minimized_expression, And) else [implicant_to_string(minimized_expression)]
    
    for set in implicants:

        new_set = ""

        for e in set: new_set += f"{e} ∨ "

        new_set = new_set.rstrip(' ∨ ')
        result += f"({new_set}) ∧ "

    result = result.rstrip(' ∧ ')
    result = "МКНФ: " + result

    return result, implicants