def differ_by_one_bit(a: str, b: str) -> bool:
    return sum(x != y for x, y in zip(a, b)) == 1

def merge_terms(a: str, b: str) -> str:
    return ''.join(x if x == y else 'X' for x, y in zip(a, b))

def covers(term: str, minterm: str) -> bool:
    return all(t == m or t == 'X' for t, m in zip(term, minterm))

def group_terms(terms):
    grouped = {}
    for term in terms:
        ones = term.count('1')
        grouped.setdefault(ones, set()).add(term)
    return grouped

def reduce_terms(grouped):
    new_groups = set()
    used = set()
    keys = sorted(grouped.keys())

    for i in range(len(keys) - 1):
        for a in grouped[keys[i]]:
            for b in grouped[keys[i + 1]]:
                if differ_by_one_bit(a, b):
                    merged = merge_terms(a, b)
                    new_groups.add(merged)
                    used.add(a)
                    used.add(b)

    prime_implicants = set()
    for group in grouped.values():
        for term in group:
            if term not in used:
                prime_implicants.add(term)

    return new_groups, prime_implicants

def generate_prime_implicants(minterms: list[str]) -> set[str]:
    grouped = group_terms(minterms)
    prime_implicants = set()

    while grouped:
        new_grouped, new_primes = reduce_terms(grouped)
        prime_implicants.update(new_primes)
        grouped = group_terms(new_grouped)

    return prime_implicants

def build_coverage_chart(prime_implicants: list[str], minterms: list[str]) -> dict[str, list[str]]:
    chart = {}
    for m in minterms:
        chart[m] = [pi for pi in prime_implicants if covers(pi, m)]
    return chart

def petrick_method(chart: dict[str, list[str]]) -> list[str]:
    # Побудова добутку сум (Петрик)
    products = [[x] for x in chart[next(iter(chart))]]
    for minterm in list(chart.keys())[1:]:
        new_products = []
        for prod in products:
            for implicant in chart[minterm]:
                combined = sorted(set(prod + [implicant]))
                if combined not in new_products:
                    new_products.append(combined)
        products = new_products

    # Мінімізація за розміром і кількістю X
    products.sort(key=lambda p: (len(p), sum(t.count('X') for t in p)))
    return sorted(products[0])

def qmc_minimize(num_vars: int, on_set: list[int]) -> list[str]:
    # 1. Перетворити у бітові терми
    minterms = [f"{i:0{num_vars}b}" for i in sorted(on_set)]

    # 2. Генерація простих імплікантів
    prime_implicants = generate_prime_implicants(minterms)

    # 3. Побудова таблиці покриття
    chart = build_coverage_chart(list(prime_implicants), minterms)

    # 4. Метод Петрика
    minimal_cover = petrick_method(chart)

    return minimal_cover

def minimize_function(num_vars: int, indices: list[int], form: str = 'dnf'):

    if form == 'dnf':

        if indices:
            
            result = ""
            implicants = qmc_minimize(num_vars, indices)
        
            for t in implicants:

                new_set = ""

                for e in t: new_set += f"{e} ∧ "

                new_set = new_set.rstrip(' ∧ ')
                result += f"({new_set}) ∨ "

            result = result.rstrip(' ∨ ')

            return result, implicants, True
        
        return ("", [""], True)

    else:

        implicants = []
        result = ""
        indices0 = sorted(set(range(2 ** num_vars)) - set(indices))

        if indices0:

            for term in qmc_minimize(num_vars, indices0):

                implicants.append(term.replace("0", "_").replace("1", "0").replace("_", "1"))

            for t in implicants:

                new_set = ""

                for e in t: new_set += f"{e} ∨ "

                new_set = new_set.rstrip(' ∨ ')
                result += f"({new_set}) ∧ "

            result = result.rstrip(' ∧ ')

            return result, implicants, False

        else: return ("", [""], False)
