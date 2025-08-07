# BITTEST.py

from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants
from minimizatonTEST import quine_mccluskey_dnf, quine_mccluskey_cnf

def test_compare(num_vars: int, values: list[int], is_dnf: bool):
    """
    Порівнює мінімізацію SymPy та QMC для заданих наборів
    :param num_vars: Кількість аргументів
    :param values: Набори значень (мінтерми або макстерми)
    :param is_dnf: True для МДНФ, False для МКНФ
    """

    number_of_sets = 1 << num_vars

    if is_dnf:
        implicants_sympy = minimize_dnf_as_implicants(num_vars, values)[1]
        result_qmc = quine_mccluskey_dnf(num_vars, values)[1]
        form = "МДНФ"
    else:
        implicants_sympy = minimize_cnf_as_implicants(num_vars, [x for x in range(number_of_sets) if x not in values])[1]
        result_qmc = quine_mccluskey_cnf(num_vars, [x for x in range(number_of_sets) if x not in values])[1]
        form = "МКНФ"

    print(f"--- Порівняння результатів ({form}) для {num_vars} аргументів ---")
    print("SymPy:", implicants_sympy)
    print("QMC  :", result_qmc)
    print("Рівність:", set(implicants_sympy) == set(result_qmc))


if __name__ == '__main__':
    # === DNF приклади ===
    test_compare(num_vars=3, values=[1, 3, 5, 7], is_dnf=True)
    test_compare(num_vars=3, values=[0, 1, 2, 5, 6], is_dnf=True)
    test_compare(num_vars=4, values=[0, 3, 5, 6, 9, 10, 12, 15], is_dnf=True)
    test_compare(num_vars=4, values=[1, 4, 6, 7, 8, 10, 11, 13, 15], is_dnf=True)

    # === CNF приклади ===
    test_compare(num_vars=3, values=[0, 2, 4], is_dnf=False)
    test_compare(num_vars=3, values=[1, 2, 3, 6, 7], is_dnf=False)
    test_compare(num_vars=4, values=[2, 3, 5, 7, 11, 13], is_dnf=False)
    test_compare(num_vars=4, values=[0, 1, 3, 4, 6, 8, 9, 12, 14], is_dnf=False)