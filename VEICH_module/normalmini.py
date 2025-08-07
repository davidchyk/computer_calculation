from sympy import symbols, Or, And, Not
from typing import List, Set
from itertools import combinations, product

def count_ones(n: int) -> int:
    return bin(n).count('1')

def differ_by_one_bit(a: str, b: str) -> bool:
    diff = 0
    for x, y in zip(a, b):
        if x != y:
            diff += 1
            if diff > 1:
                return False
    return diff == 1

def merge_terms(a: str, b: str) -> str:
    return ''.join([x if x == y else 'X' for x, y in zip(a, b)])

def covers(term: str, minterm: str) -> bool:
    return all(t == m or t == 'X' for t, m in zip(term, minterm))

def petrick_method(prime_implicants: List[str], minterms: List[str]) -> List[str]:
    table = []
    for minterm in minterms:
        cover = [imp for imp in prime_implicants if covers(imp, minterm)]
        table.append(cover)

    products = [[x] for x in table[0]]
    for term_list in table[1:]:
        new_products = []
        for p in products:
            for t in term_list:
                new = sorted(set(p + [t]))
                if new not in new_products:
                    new_products.append(new)
        products = new_products

    min_len = min(len(p) for p in products)
    min_products = [p for p in products if len(p) == min_len]
    min_products.sort(key=lambda x: sum(term.count('X') for term in x))

    return sorted(min_products[0])

def qmc_minimize(num_vars: int, terms: List[int], is_dnf: bool = True) -> List[str]:
    term_binaries = [f"{i:0{num_vars}b}" for i in terms]
    unchecked = set(term_binaries)
    prime_implicants = set()

    while unchecked:
        new_terms = set()
        used = set()
        for a, b in combinations(unchecked, 2):
            if differ_by_one_bit(a, b):
                merged = merge_terms(a, b)
                new_terms.add(merged)
                used.add(a)
                used.add(b)
        prime_implicants.update(unchecked - used)
        unchecked = new_terms

    return petrick_method(list(prime_implicants), term_binaries)

def minimized_implicants(num_vars: int, values: List[int], is_dnf: bool = True) -> List[str]:
    if is_dnf:
        return qmc_minimize(num_vars, values, is_dnf=True)
    else:
        return qmc_minimize(num_vars, values, is_dnf=False)
