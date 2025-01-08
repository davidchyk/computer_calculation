from normal_forms import normal
from operator_form2 import operator_form
from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants
from graphic import graph
from class_function import class_define
from create_pdf import create_pdf_main

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

def validate(data, type, optinal = False):

    if type == "number_of_arguments":

        try:

            number_of_arguments = float(data)

            if number_of_arguments.is_integer() == False or number_of_arguments <= 0:

                print("Неправильне значення кількості аргументів"); return False

        except: print("Неправильне значення кількості аргументів"); return False

    elif type == "num_functions":

        try:

            if int(float(data)) <= 0 or float(data).is_integer() == False:
                print("Неправильне значення кількості функцій"); return False

        except: print("Неправильне значення кількості функцій"); return False

    elif type == "input_data":

        try:

            temp = [float(x) for x in data.split(',')]

            if any(x.is_integer() == False for x in temp):
                print("Неправильне значення наборів"); return False

            temp = [int(x) for x in temp]

            if any((x >= optinal) or (x < 0) for x in temp):
                print("Неправильний номер набору"); return False

        except: print("Неправильне введення наборів"); return False

    elif type == "basis":

        try:

            temp = [(int(data[0][0]), data[0][1:]), (int(data[1][0]), data[1][1:])]

            if not temp[1][1] in ["АБО", "І", "АБО-НЕ", "І-НЕ"]:
                print("Неправильний базис. Приклад: 3І/2АБО"); return False
            
            if [temp[0][1], temp[1][1]] not in db:
                print("Неправильний базис. Приклад: 3І/2АБО"); return False

        except: print("Неправильний базис. Приклад: 3І/2АБО"); return False

    return True

print("Version 1.0")
print("Головний розробник: Давидчук Артем\nІнші розробники: Білий Іван, Троценко Максим")

while 1:

    ddnf_list = []
    dknf_list = []
    normal_list = []
    operator_list = []
    minimum_list = []
    normal_minimum_list = []
    operator_minimum_list = []
    class_list = []
    i = 1

    basis_update = []
    args = []

    number_of_arguments = input("\nНаберіть кількість аргументів функції: ")
    if not validate(number_of_arguments, "number_of_arguments"): continue
    number_of_arguments = int(float(number_of_arguments))
    number_of_sets = 2**number_of_arguments

    print("\nВведіть кількість функцій, які потрібно мінімізувати:")
    num_functions = input("Кількість функцій: ")
    if not validate(num_functions, "num_functions"): continue
    num_functions = int(float(num_functions))

    while i <= num_functions:

        print("---------")

        print(f"Ввід даних для функції y{i}:")

        input_data = input("Набери числа наборів, при яких функція набуває одиниці (через кому): ").strip()
        if not validate(input_data, "input_data", number_of_sets): continue
        sets_number = [int(float(x)) for x in input_data.split(',')]

        basis = input("Наберіть елементний базис через '/': ").split('/')
        if not validate(basis, "basis"): continue

        basis_update = [(int(basis[0][0]), basis[0][1:]), (int(basis[1][0]), basis[1][1:])]

        if basis_update[1][1] in ['АБО', 'І-НЕ']: type_of = 1
        else: type_of = 0

        in_num = int(basis_update[0][0])
        out_num = int(basis_update[1][0])

        data_table = truth_table(number_of_arguments, sets_number)
        normal_result = normal(sets_number, type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), False)

        operator_result = operator_form(normal_result[1], in_num, out_num)

        ddnf_list.append("\\text{ДДНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(normal_result[0][0], number_of_arguments)}")
        dknf_list.append("\\text{ДКНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(normal_result[0][1], number_of_arguments)}")
        normal_list.append("\\text{Нормальна форма }" f"y_{i}" r"\text{: }" f"{conver_to_normal(normal_result[0][2], number_of_arguments)}")

        operator_list.append("\\text{Операторна форма }" f"y_{i}" r"\text{: }" f"{conver_to_normal(operator_result, number_of_arguments)}")

        if type_of:
            minimize_result = minimize_dnf_as_implicants(number_of_arguments, sets_number)
        else:
            minimize_result = minimize_cnf_as_implicants(number_of_arguments, [x for x in range(number_of_sets) if x not in sets_number])

        if minimize_result[2]: minimum_list.append("\\text{МДНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(minimize_result[0], number_of_arguments)}")
        else: minimum_list.append("\\text{МКНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(minimize_result[0], number_of_arguments)}")

        minimize_normal_result = normal(minimize_result[1], type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), True)[1]
        normal_minimum_list.append("\\text{Нормальна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{conver_to_normal(str(minimize_normal_result), number_of_arguments)}")

        minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)
        operator_minimum_list.append("\\text{Операторна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{conver_to_normal_operator(minimize_operator_result, number_of_arguments)}")

        class_list.extend(class_define(sets_number, number_of_arguments, i))

        i += 1

    args = ddnf_list + dknf_list + normal_list + operator_list  + minimum_list + normal_minimum_list + operator_minimum_list + class_list
    args = args + ["\\text{ }"] * 10 + ["\\text{ Розробники: Давидчук Артем, Білий Іван, Троценко Максим, Вовк Андрій}"]
    
    page_width = int(len(max(args, key=len))*0.144531255)

    print(page_width)

    create_pdf_main(args, page_width)

    #graph(args, data_table)