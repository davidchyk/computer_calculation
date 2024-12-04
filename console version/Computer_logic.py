from normal_forms import normal
from operator_form2 import operator_form
from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants
from graphic import graph

db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
      ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]

def truth_table(num_of_args, sets_number):

    table = []
    args = []

    for i in range(num_of_args, 0, -1): args.append(f"X{i}")
    args.append("Y")

    table.append(args)

    for num in range(2**num_of_args):

        bin_lst = list(format(num, f"0{num_of_args}b"))
        if num in sets_number: bin_lst.append("1")
        else: bin_lst.append("0")

        bin_lst = [int(x) for x in bin_lst]

        table.append(bin_lst)

    return table

def conver_to_normal(string, num_of_args):

    index = 0
    counter = num_of_args
    result = ""

    while index < len(string):

        if string[index] == '0':

            result += f"not(X_{counter})"
            counter -= 1

        elif string[index] == '1':

            result += f"X_{counter}"
            counter -= 1

        elif string[index] == 'X':

            result += "#"

            counter -= 1

        else:

            result += string[index]

        index += 1

        if counter == 0: counter = num_of_args

    if "#" in result:

        result = result.replace("# ∧ ", "")
        result = result.replace("# ∨ ", "")
        result = result.replace(" ∨ # ", "")
        result = result.replace(" ∧ # ", "")
        result = result.replace(" ∨ #", "")
        result = result.replace(" ∧ #", "")
        result = result.replace("#", "")

    return result  

def conver_to_normal_operator(string, num_of_args):

    def replacing(result, num_of_args):

        result = result.replace("# ∧ ", "")
        result = result.replace("# ∨ ", "")
        result = result.replace(" ∨ # ", "")
        result = result.replace(" ∧ # ", "")
        result = result.replace(" ∨ #", "")
        result = result.replace(" ∧ #", "")
        result = result.replace("#", "")

        result = result.replace("not(not())", "%")

        result = result.replace("% ∧ ", "")
        result = result.replace("% ∨ ", "")
        result = result.replace(" ∨ % ", "")
        result = result.replace(" ∧ % ", "")
        result = result.replace(" ∨ %", "")
        result = result.replace(" ∧ %", "")
        result = result.replace("%", "")

        for i in range(1, num_of_args+1):

            argument = f"X_{i}"
            result = result.replace(f"not(not({argument}))", argument)

        return result

    index = 0
    counter = num_of_args
    result = ""

    while index < len(string):

        if string[index] == '0':

            result += f"not(X_{counter})"
            counter -= 1

        elif string[index] == '1':

            result += f"X_{counter}"
            counter -= 1

        elif string[index] == 'X':

            result += "#"

            counter -= 1

        else:

            result += string[index]

        index += 1

        if counter == 0: counter = num_of_args

    result = replacing(result, num_of_args)

    return result  

print("Beta version 0.9")
print("\nДеякі нотатки: дужки в виводі означають певну групу, яку описує певний логічний елемент.\nПри запереченнях вгорі групи формуюються не дужками, а запереченнями.\nЯкщо над певним термом розташовані 3 заперечення, то 2 з них можна проігнорувати.")

while 1:

    try:

        number_of_arguments = float(input("\nНабери кількість аргументів функції: "))

        if number_of_arguments.is_integer() == False or number_of_arguments <= 0:

            print("Неправильний кількість аргументів. Спробуй ще раз."); continue

        number_of_sets = 2**int(number_of_arguments)

    except:

        print("Неправильне введення кількості аргументів")
        continue

    basis_update = []
    args = []

    try:

        sets_number = [int(x) for x in input("Набери числа наборів, при яких функція набуває одиниці: ").split(',')]

    except:

        print(f"Неправильно введено кількість наборів. Спробуйте ще раз.")
        continue

    if any((x >= number_of_sets) or (x < 0) for x in sets_number): print("Неправильний номер набору. Спробуй ще раз."); continue

    basis = input("Набери елементний базис через '/': ").split('/')

    if (len(basis) == 1) or ([basis[0][1::], basis[1][1::]] not in db): print("Неправильний базис. Приклад: 3І/2АБО. Спробуй ще раз."); continue

    basis_update.append((int(basis[0][0]), basis[0][1::]))
    basis_update.append((int(basis[1][0]), basis[1][1::]))

    if basis_update[1][1] in ['АБО', 'І-НЕ']: type_of = 1
    if basis_update[1][1] in ['І', 'АБО-НЕ']: type_of = 0

    in_num = int(basis_update[0][0])
    out_num = int(basis_update[1][0])

    data_table = truth_table(int(number_of_arguments), sets_number)

    normal_result = normal(sets_number, type_of, int(number_of_arguments), (basis_update[0][1], basis_update[1][1]), False)
    for line in normal_result[0]: args.append(conver_to_normal(line, int(number_of_arguments)))
    operator_result = operator_form(normal_result[1], in_num, out_num)

    args.append(f"Операторна форма при елементному базисі {'/'.join(basis)}: {conver_to_normal(operator_result, int(number_of_arguments))}")
    args.append(r" \ ")

    if type_of:

        minimize_result = minimize_dnf_as_implicants(int(number_of_arguments), sets_number)

    else:

        minimize_result = minimize_cnf_as_implicants(int(number_of_arguments), [x for x in range(2**int(number_of_arguments)) if x not in sets_number])

    args.append(conver_to_normal(minimize_result[0], int(number_of_arguments)))

    minimize_normal_result = normal(minimize_result[1], type_of, int(number_of_arguments), (basis_update[0][1], basis_update[1][1]), True)[1]

    args.append(f"Нормальна форма мінімізованої функції при {'/'.join([basis_update[0][1], basis_update[1][1]])}: {conver_to_normal(str(minimize_normal_result), int(number_of_arguments))}")

    minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)
    args.append(f"Операторна форма мінімізованої функції при елементному базисі {'/'.join(basis)}: {conver_to_normal_operator(minimize_operator_result, int(number_of_arguments))}")

    for _ in range(6): args.append(r" \ ")

    args.append("Розробник: Давидчук Артем")

    graph(args, data_table)