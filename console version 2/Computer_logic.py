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

    ddnf_list = []
    dknf_list = []
    normal_list = []
    operator_list = []
    minimum_list = []
    normal_minimum_list = []
    operator_minimum_list = []

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

    #Старт системи
    print("\nВведіть кількість функцій, які потрібно мінімізувати:")

    try:

        num_functions = int(input("Кількість функцій: "))

        if num_functions <= 0:
            print("Кількість функцій має бути додатною. Спробуйте ще раз.")
            continue

        for i in range(num_functions):

            print(f"\nОбробка функції №{i + 1}:")

            try:
                sets_number = [int(x) for x in input("Набери числа наборів, при яких функція набуває одиниці: ").split(',')]

            except:
                print("Неправильне введення наборів. Спробуйте ще раз.")
                continue

            if any((x >= number_of_sets) or (x < 0) for x in sets_number):
                print("Неправильний номер набору. Спробуйте ще раз.")
                continue

            basis = input("Набери елементний базис через '/': ").split('/')

            if len(basis) != 2 or ([basis[0][1:], basis[1][1:]] not in db):
                print("Неправильний базис. Приклад: 3І/2АБО. Спробуйте ще раз.")
                continue

            basis_update = [
                (int(basis[0][0]), basis[0][1:]),
                (int(basis[1][0]), basis[1][1:])
            ]

            if basis_update[1][1] in ['АБО', 'І-НЕ']:
                type_of = 1
            elif basis_update[1][1] in ['І', 'АБО-НЕ']:
                type_of = 0
            else:
                print("Неправильний тип базису. Пропускаємо цю функцію.")
                continue

            in_num = int(basis_update[0][0])
            out_num = int(basis_update[1][0])

            data_table = truth_table(int(number_of_arguments), sets_number)
            normal_result = normal(sets_number, type_of, int(number_of_arguments), (basis_update[0][1], basis_update[1][1]), False)

            ddnf_list.append(f"ДДНФ f{i+1}: {conver_to_normal(normal_result[0][0], int(number_of_arguments))}")
            dknf_list.append(f"ДКНФ f{i+1}: {conver_to_normal(normal_result[0][1], int(number_of_arguments))}")
            normal_list.append(f"Нормальна форма f{i+1}: {conver_to_normal(normal_result[0][2], int(number_of_arguments))}")

            operator_result = operator_form(normal_result[1], in_num, out_num)
            operator_list.append(f"Операторна форма f{i+1}: {conver_to_normal(operator_result, int(number_of_arguments))}")

            if type_of:
                minimize_result = minimize_dnf_as_implicants(int(number_of_arguments), sets_number)
            else:
                minimize_result = minimize_cnf_as_implicants(int(number_of_arguments), [x for x in range(2**int(number_of_arguments)) if x not in sets_number])

            if minimize_result[2]: minimum_list.append(f"МДНФ f{i+1}: {conver_to_normal(minimize_result[0], int(number_of_arguments))}")
            else: minimum_list.append(f"МКНФ f{i+1}: {conver_to_normal(minimize_result[0], int(number_of_arguments))}")

            minimize_normal_result = normal(minimize_result[1], type_of, int(number_of_arguments), (basis_update[0][1], basis_update[1][1]), True)[1]
            normal_minimum_list.append(f"Нормальна форма мінімізованої функції f{i+1}: {conver_to_normal(str(minimize_normal_result), int(number_of_arguments))}")

            minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)
            operator_minimum_list.append(f"Операторна форма мінімізованої функції f{i+1}: {conver_to_normal_operator(minimize_operator_result, int(number_of_arguments))}")

        args = ddnf_list + dknf_list + normal_list + operator_list + [r" \ "]+ minimum_list + normal_minimum_list + operator_minimum_list

        for _ in range(6): args.append(r" \ ")
        args.append("Розробник: Давидчук Артем")
        args.append("Розробник: Білий Іван")

        graph(args, data_table)

    except Exception as e:
        print(e)
        print("Заново нахуй")
        continue