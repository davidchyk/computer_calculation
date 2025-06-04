from normal_forms import normal
from operator_form2 import operator_form
from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants
from class_function import class_define
from Veich_schemma import veich_create
from create_output import create_pdf_main, get_true_table
import numpy as np

db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
      ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]

def find_args_and_sets(function_input):

    def get_truth_table(num_of_args, result, org_func):

        replacer = result

        indices_where_1 = []
        for num in range(2 ** num_of_args):
            # Generate binary values for replacer
            bin_lst = list(format(num, f"0{num_of_args}b"))  # Convert num to binary string with leading zeros
            replacer = [int(x) for x in bin_lst]  # Convert binary digits to integers
            
            # Replace variables in org_func with corresponding values from replacer
            replaced_func = org_func
            for var, value in zip(result, replacer):  # Pair variables with their replacement values
                replaced_func = replaced_func.replace(var, str(value))
            
            # Replace bitwise operators with logical operators
            replaced_func = replaced_func.replace("&", " and ").replace("|", " or ").replace("~", " not ")

            # Evaluate the logical expression and cast the result to an integer
            result_value = int(eval(replaced_func))
            
            # If the function evaluates to 1, store the current index
            if result_value == 1: indices_where_1.append(num)

            # Output the evaluated result for debugging
            #print(f"Replacer: {replacer}, Evaluated Result: {result_value}") debug value

        return indices_where_1 # повертає лист з ноберами наборів на яких 1

    result = []
    org_func = function_input
 
    function_input = function_input.replace("~", "  ~ ")
    function_input = function_input.replace("(", "  ( ")
    function_input = function_input.replace(")", "  ) ")
    function_input = function_input.replace("&", "  & ")
    function_input = function_input.replace("|", "  | ")
    function_input = function_input.replace("~", " ")

    result = function_input.split(" ")

    result = [x for x in result if x]

    function_input = function_input.replace("~", " ")
    function_input = function_input.replace("(", " ")
    function_input = function_input.replace(")", " ")
    function_input = function_input.replace("&", " ")
    function_input = function_input.replace("|", " ")

    result = function_input.split(" ")

    result = [x for x in result if x]
    result = set(result)
    result = list(result)
    result = sorted(result, key=lambda x: (x[0], -int(x[1:])))

    x = get_truth_table(len(result),result,org_func)
    return result, x

def truth_table_Create(function_regime, number_of_arguments, number_of_sets, number_of_function, optional = False):

    result = np.empty((number_of_sets+1, number_of_arguments), dtype=object)

    if function_regime == "sets":

        result[0] = [f"$X_{k}$" for k in range(number_of_arguments, 0, -1)]

    elif function_regime == "func":

        result[0] = [f"${x}$" for x in optional]

    for k in range(number_of_sets):
    
        bin_lst = list(format(k, f"0{number_of_arguments}b"))
        bin_lst = [int(x) for x in bin_lst]
        result[k+1] = bin_lst

    temp = [f"$y_{number_of_function}$"]

    for l in range(number_of_sets):

        if l in sets_number: temp.append(1)
        else: temp.append(0)

    # Перетворюємо список на масив NumPy
    np_temp = np.array(temp, dtype = object)

    # Перетворюємо його на двовимірний масив зі стовпцем (reshape)
    new_np_temp = np_temp.reshape(-1, 1)

    return np.hstack((result, new_np_temp))

def conver_to_normal(function_regime, string, num_of_args, optional = False):

    if function_regime == "sets":

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
    
    elif function_regime == "func":

        index = 0
        element_index = 0
        result = ""

        while index < len(string):

            if string[index] == '0':

                result += f"not({optional[element_index]})"
                element_index += 1

            elif string[index] == '1':

                result += f"{optional[element_index]}"
                element_index += 1

            elif string[index] == 'X':

                result += "#"
                element_index += 1

            else:

                result += string[index]

            index += 1
            if element_index == len(optional): element_index = 0

        if "#" in result:

            result = result.replace("# ∧ ", "")
            result = result.replace("# ∨ ", "")
            result = result.replace(" ∨ # ", "")
            result = result.replace(" ∧ # ", "")
            result = result.replace(" ∨ #", "")
            result = result.replace(" ∧ #", "")
            result = result.replace("#", "")

        return result

def conver_to_normal_operator(function_regime, string, num_of_args, optional = False):

    if function_regime == "sets":

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

    elif function_regime == "func":

        def replacing(result, optinal):

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

            for i in range(len(optinal)):

                argument = f"{optinal[i]}"
                result = result.replace(f"not(not({argument}))", argument)

            return result

        index = 0
        element_index = 0
        result = ""

        while index < len(string):

            if string[index] == '0':

                result += f"not({optional[element_index]})"
                element_index += 1

            elif string[index] == '1':

                result += f"{optional[element_index]}"
                element_index += 1

            elif string[index] == 'X':

                result += "#"
                element_index += 1

            else:

                result += string[index]

            index += 1
            if element_index == len(optional): element_index = 0

        result = replacing(result, optional)
        return result 

def validate(data, type, optinal = False):

    if type == "function_regime":

        if data == "func" or data == "sets": return True
        else: print("Неправильний режим введення функцій"); return False

    elif type == "function_input":

        if not data: print("Неправильне введення функції"); return False

        try:

            temp = find_args_and_sets(data)

        except: print("Неправильне введення функції"); return False

        else:

            try:

                if any(len(x) > 2 for x in temp[0]): print("Неправильне введення аргументів функції"); return False
                if not all(len(x) == 2 for x in temp[0]): print("Неправильне введення аргументів функції"); return False
                if not all((90 >= ord(x[0]) >= 65) or (122 >= ord(x[0]) >= 65) for x in temp[0]): print("Неправильне введення аргументів функції"); return False

            except: print("Неправильне введення аргументів функції"); return False

            else:

                return True

    elif type == "number_of_arguments":

        try:

            number_of_arguments = float(data)

            if number_of_arguments.is_integer() == False or number_of_arguments <= 0:

                print("Неправильне значення кількості аргументів"); return False

        except: print("Неправильне значення кількості аргументів"); return False

        else:

            if int(number_of_arguments) >= 10: print("Перевищення ліміту кількості аргументів"); return False

    elif type == "num_functions":

        try:

            if int(float(data)) <= 0 or float(data).is_integer() == False:
                print("Неправильне значення кількості функцій"); return False

        except: print("Неправильне значення кількості функцій"); return False

        else:

            if int(num_functions) >= 10: print("Перевищення ліміту кількості функцій"); return False

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

print("Version 3.5 Beta")

while 1:

    global_output = []
    global_truth_table_output = []
    basis_update = []
    list_to_create = []
    i = 1

    print("\nДля вводу функції використовуйте func, для вводу наборів використовуйте sets")
    function_regime = input("Введіть режим введення функцій (func або sets): ")
    if not validate(function_regime, "function_regime"): continue

    if function_regime == "sets":

        number_of_arguments = input("\nНаберіть кількість аргументів функції (до 10): ")
        if not validate(number_of_arguments, "number_of_arguments"): continue
        number_of_arguments = int(float(number_of_arguments))
        number_of_sets = 2**number_of_arguments

        num_functions = input("Введіть кількість функцій, які потрібно проаналізувати (до 10): ")
        if not validate(num_functions, "num_functions"): continue
        num_functions = int(float(num_functions))

        while i <= num_functions:

            print(f"\nВвід даних для функції y{i}:")

            input_data = input("Наберіть числа наборів, при яких функція набуває одиниці (через кому): ").strip()
            if not validate(input_data, "input_data", number_of_sets): continue
            sets_number = [int(float(x)) for x in input_data.split(',')]

            basis = input("Наберіть елементний базис через /: ").split('/')
            if not validate(basis, "basis"): continue

            basis_update = [(int(basis[0][0]), basis[0][1:]), (int(basis[1][0]), basis[1][1:])]

            if basis_update[1][1] in ['АБО', 'І-НЕ']: type_of = 1
            else: type_of = 0

            in_num = int(basis_update[0][0])
            out_num = int(basis_update[1][0])

            #Analize function

            truth_table = truth_table_Create(function_regime, number_of_arguments, number_of_sets, i)
            normal_result = normal(sets_number, type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), False)
            operator_result = operator_form(normal_result[1], in_num, out_num)

            if type_of: minimize_result = minimize_dnf_as_implicants(number_of_arguments, sets_number)
            else: minimize_result = minimize_cnf_as_implicants(number_of_arguments, [x for x in range(number_of_sets) if x not in sets_number])

            print(minimize_result)

            minimize_normal_result = normal(minimize_result[1], type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), True)[1]
            minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)

            list_to_create.append(conver_to_normal(function_regime, minimize_result[0], number_of_arguments))

            #Forming Output

            global_truth_table_output.append(get_true_table(truth_table, number_of_arguments))

            DDNF = conver_to_normal(function_regime, normal_result[0][0], number_of_arguments)

            global_output.append("\\text{ДДНФ }" f"y_{i}" r"\text{: }" f"{DDNF}")
            global_output.append("\\text{ДКНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, normal_result[0][1], number_of_arguments)}")
            global_output.append("\\text{Нормальна форма }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime,normal_result[0][2], number_of_arguments)}")
            global_output.append("\\text{Операторна форма }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, operator_result, number_of_arguments)}")

            if minimize_result[2]: global_output.append("\\text{МДНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, minimize_result[0], number_of_arguments)}")
            else: global_output.append("\\text{МКНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, minimize_result[0], number_of_arguments)}")

            global_output.append("\\text{Нормальна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, str(minimize_normal_result), number_of_arguments)}")
            global_output.append("\\text{Операторна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{conver_to_normal_operator(function_regime, minimize_operator_result, number_of_arguments)}")
            global_output.extend(class_define(function_regime, sets_number, number_of_arguments, i, DDNF=DDNF))
            global_output.append(None)

            i += 1

    elif function_regime == "func":

        num_functions = input("Введіть кількість функцій, які потрібно проаналізувати (до 10): ")
        if not validate(num_functions, "num_functions"): continue
        num_functions = int(float(num_functions))

        while i <= num_functions:

            print(f"\nВвід даних для функції y{i}:")

            function_input = input(f"Набери функцію y{i} (як AND використовуйте &, як OR використовуйте |, як NOT використовуйте ~): ")
            if not validate(function_input, "function_input"): continue
            function_data = find_args_and_sets(function_input)

            sets_number = function_data[1]
            args_list = function_data[0]
            args_list = [f"{x[0]}_{x[1]}" for x in args_list]

            number_of_arguments = len(args_list)
            number_of_sets = 2**number_of_arguments

            basis = input("Наберіть елементний базис через /: ").split('/')
            if not validate(basis, "basis"): continue

            basis_update = [(int(basis[0][0]), basis[0][1:]), (int(basis[1][0]), basis[1][1:])]

            if basis_update[1][1] in ['АБО', 'І-НЕ']: type_of = 1
            else: type_of = 0

            in_num = int(basis_update[0][0])
            out_num = int(basis_update[1][0])

            #Analize function

            truth_table = truth_table_Create(function_regime, number_of_arguments, number_of_sets, i, optional=args_list)
            normal_result = normal(sets_number, type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), False)
            operator_result = operator_form(normal_result[1], in_num, out_num)

            if type_of: minimize_result = minimize_dnf_as_implicants(number_of_arguments, sets_number)
            else: minimize_result = minimize_cnf_as_implicants(number_of_arguments, [x for x in range(number_of_sets) if x not in sets_number])

            minimize_normal_result = normal(minimize_result[1], type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), True)[1]
            minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)

            list_to_create.append(conver_to_normal(function_regime, minimize_result[0], number_of_arguments, args_list))

            #Forming Output

            global_truth_table_output.append(get_true_table(truth_table, number_of_arguments))

            DDNF = conver_to_normal(function_regime, normal_result[0][0], number_of_arguments, optional=args_list)

            global_output.append("\\text{ДДНФ }" f"y_{i}" r"\text{: }" f"{DDNF}")
            global_output.append("\\text{ДКНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, normal_result[0][1], number_of_arguments, args_list)}")
            global_output.append("\\text{Нормальна форма }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime,normal_result[0][2], number_of_arguments, args_list)}")
            global_output.append("\\text{Операторна форма }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, operator_result, number_of_arguments, args_list)}")

            if minimize_result[2]: global_output.append("\\text{МДНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, minimize_result[0], number_of_arguments, args_list)}")
            else: global_output.append("\\text{МКНФ }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, minimize_result[0], number_of_arguments, args_list)}")

            global_output.append("\\text{Нормальна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{conver_to_normal(function_regime, str(minimize_normal_result), number_of_arguments, args_list)}")
            global_output.append("\\text{Операторна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{conver_to_normal_operator(function_regime, minimize_operator_result, number_of_arguments, args_list)}")
            global_output.extend(class_define(function_regime, sets_number, number_of_arguments, i, optional=args_list, DDNF=DDNF))
            global_output.append(None)

            i += 1

    BLOCK1_width = (number_of_arguments+1)*1.5

    page_width = max(int(len(max((item for item in global_output if item is not None), key=len))*0.15), 44)
    page_height = max(number_of_sets, 30)

    output_difficult = round(max(page_width * 4 / 23, page_height * 4 / 23), 2)

    if output_difficult > 100:

        print(f"\nВаша функція має складність виводу: {output_difficult}%, що перевищує 100%.\nНажаль Latex-компілятор не зможе створити PDF файл вивід :(\n")

    else:

        print(f"\nСкладність виводу функції {output_difficult}%, що < 100%:")
        create_pdf_main([global_output, global_truth_table_output], [page_width, page_height, BLOCK1_width], list_to_create)