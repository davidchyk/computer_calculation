from typing import List, Tuple
from itertools import combinations

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

def quine_mccluskey_dnf(num_vars: int, minterms: List[int]) -> List[str]:
    """Мінімізація МДНФ"""

    result = ""

    terms = [f"{i:0{num_vars}b}" for i in minterms]
    unchecked = set(terms)
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

    for t in list(prime_implicants):

        new_set = ""

        for e in t: new_set += f"{e} ∧ "

        new_set = new_set.rstrip(' ∧ ')
        result += f"({new_set}) ∨ "

    result = result.rstrip(' ∨ ')

    return result, list(prime_implicants), True

def quine_mccluskey_cnf(num_vars: int, maxterms: List[int]) -> List[str]:
    """Мінімізація МКНФ"""

    result = ""
    terms = [f"{i:0{num_vars}b}" for i in maxterms]
    unchecked = set(terms)
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

        for t in list(prime_implicants):

            new_set = ""

            for e in t: new_set += f"{e} ∧ "

            new_set = new_set.rstrip(' ∧ ')
            result += f"({new_set}) ∨ "

        result = result.rstrip(' ∨ ')

    return result, list(prime_implicants), False
