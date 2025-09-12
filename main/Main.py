from sympy.logic.boolalg import BooleanFunction
from numpy.typing import NDArray
from tkinter import messagebox
from itertools import product
from PyPDF2 import PdfReader
from sympy import sympify
from pathlib import Path
from os import PathLike
from math import ceil
import numpy as np
import tempfile

from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants
from create_pdf_output import create_pdf_main, get_true_table
from create_veich_scheme import create_veich_schemme_pdf
from operator_form2 import operator_form
from class_function import class_define
from normal_forms import normal
from alternative_minimization import minimize_function

db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
      ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]

def largest_pdf_height_cm(folder: str | PathLike) -> int:

    folder = Path(folder).expanduser().resolve()

    # 1. однорівнево скануємо теку на *.pdf
    pdf_files = [p for p in folder.iterdir() if p.suffix.lower() == ".pdf"]
    if not pdf_files: print("У теці немає PDF-файлів."); return 0

    # 2. беремо найбільший за розміром
    largest_pdf = max(pdf_files, key=lambda p: p.stat().st_size)

    # 3. перша сторінка → MediaBox → висота в поінтах
    reader = PdfReader(largest_pdf)
    page = reader.pages[0:1][0]
    mediabox = page.mediabox
    height_pt = float(mediabox.top) - float(mediabox.bottom)

    # 4. поінти → сантиметри: 1 pt = 25.4 mm = 2.54 cm / 72
    height_cm_ceil = ceil(height_pt * 2.54 / 72)

    print(f"Найбільший PDF: {largest_pdf.name}")
    print(f"Висота (1-ша сторінка): {height_cm_ceil} см")

    return height_cm_ceil

def find_args_and_sets(function_input: str) -> tuple[list[str], list[int]]:

    # 1. Розпарсимо рядок у Sympy-вираз
    expr = sympify(function_input)
    if not isinstance(expr, BooleanFunction):
        raise ValueError("Не вийшло розпізнати логічний вираз")

    # 2. Отримаємо список змінних з потрібним порядком:
    vars_sym = list(expr.free_symbols)
    vars_sym.sort(key=lambda s: (str(s)[0], -int(str(s)[1:])))
    var_names = [str(v) for v in vars_sym]

    # 3. Переберемо всі можливі бітові комбінації
    ones_indices: list[int] = []
    n = len(vars_sym)
    for bits in product([0, 1], repeat=n):
        subs = dict(zip(vars_sym, bits))
        # підставляємо й обчислюємо; результат теж булевий
        val = bool(expr.xreplace(subs))
        if val:
            # переводимо бітову кортеж у десятковий індекс
            idx = int("".join(str(b) for b in bits), 2)
            ones_indices.append(idx)

    return var_names, ones_indices

def truth_table_Create(function_regime: str, number_of_arguments: int, number_of_sets: int, number_of_function: int, optional: list = []) -> NDArray:

    result = np.empty((number_of_sets+1, number_of_arguments), dtype=object)

    if function_regime == "sets":

        result[0] = [f"$x_{k}$" for k in range(number_of_arguments, 0, -1)]

    elif function_regime == "expression":

        result[0] = [f"${x}$" for x in optional]

    for k in range(number_of_sets):
    
        bin_lst = list(format(k, f"0{number_of_arguments}b"))
        bin_lst = [int(x) for x in bin_lst]
        result[k+1] = bin_lst

    temp = [f"$y_{number_of_function}$"]

    for l in range(number_of_sets):

        if l in sets_number: temp.append("1")
        else: temp.append("0")

    # Перетворюємо список на масив NumPy
    np_temp = np.array(temp, dtype = object)

    # Перетворюємо його на двовимірний масив зі стовпцем (reshape)
    new_np_temp = np_temp.reshape(-1, 1)

    return np.hstack((result, new_np_temp))

def converting_string(is_operator: bool, function_regime: str, string: str, num_of_args: int, optional: list = []) -> str:

    def replacing(main_input: str, optional: int | list[str]) -> str:

        result = (main_input.replace("# ∧ ", "")
                      .replace("# ∨ ", "")
                      .replace(" ∨ # ", "")
                      .replace(" ∧ # ", "")
                      .replace(" ∨ #", "")
                      .replace(" ∧ #", "")
                      .replace("#", "")
                      .replace("not(not())", "%")
                      .replace("% ∧ ", "")
                      .replace("% ∨ ", "")
                      .replace(" ∨ % ", "")
                      .replace(" ∧ % ", "")
                      .replace(" ∨ %", "")
                      .replace(" ∧ %", "")
                      .replace("%", ""))

        if isinstance(optional, list):

            for i in range(len(optional)):

                argument = f"{optional[i]}"
                result = result.replace(f"not(not({argument}))", argument)

        else:

            for i in range(1, num_of_args+1):

                argument = f"x_{i}"
                result = result.replace(f"not(not({argument}))", argument)

        return result

    index = 0
    result = ""

    if function_regime == "sets":

        counter = num_of_args

        while index < len(string):

            if string[index] == '0':

                result += f"not(x_{counter})"
                counter -= 1

            elif string[index] == '1':

                result += f"x_{counter}"
                counter -= 1

            elif string[index] == 'X':

                result += "#"
                counter -= 1

            else:

                result += string[index]

            index += 1
            if counter == 0: counter = num_of_args

        if is_operator: result = replacing(result, num_of_args)
        elif not is_operator and "#" in result:

            result = result.replace("# ∧ ", "")
            result = result.replace("# ∨ ", "")
            result = result.replace(" ∨ # ", "")
            result = result.replace(" ∧ # ", "")
            result = result.replace(" ∨ #", "")
            result = result.replace(" ∧ #", "")
            result = result.replace("#", "")

    elif function_regime == "expression":

        element_index = 0

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

        if is_operator: result = replacing(result, optional)
        elif not is_operator and "#" in result:

            result = result.replace("# ∧ ", "")
            result = result.replace("# ∨ ", "")
            result = result.replace(" ∨ # ", "")
            result = result.replace(" ∧ # ", "")
            result = result.replace(" ∨ #", "")
            result = result.replace(" ∧ #", "")
            result = result.replace("#", "")

    return result

def validate(data, type, optinal = 0):

    if type == "function_regime":

        if data == "expression" or data == "sets": return True
        else: print("Неправильний режим введення функцій"); return False

    elif type == "function_input":

        if not data:

            print("HE")
            print("Неправильне введення функції"); return False

        try:

            temp = find_args_and_sets(data)

        except Exception as e:

            print(F"Error 001: {str(e)}")
            print("Неправильне введення функції"); return False

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

while True:

    tmp_obj = tempfile.TemporaryDirectory()
    temp_dir = tmp_obj.name

    global_truth_table_output = []
    number_of_arguments = int()
    veich_schemme_list = []
    global_output = []
    basis_update = []
    i = 1

    print("\nДля вводу логічного виразу використовуйте \"expression\", для вводу 1-наборів використовуйте \"sets\"")
    function_regime = input("Введіть режим введення функцій (expression або sets): ")
    if not validate(function_regime, "function_regime"): continue

    if function_regime == "sets":

        number_of_arguments = input("\nНаберіть кількість аргументів функції (до 10): ")
        if not validate(number_of_arguments, "number_of_arguments"): continue
        number_of_arguments = int(float(number_of_arguments))
        number_of_sets = 1 << number_of_arguments

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

            print(operator_result)

            #if type_of: minimize_result = minimize_dnf_as_implicants(number_of_arguments, sets_number)
            #else: minimize_result = minimize_cnf_as_implicants(number_of_arguments, [x for x in range(number_of_sets) if x not in sets_number])

            if type_of: minimize_result = minimize_function(number_of_arguments, sets_number, 'dnf')
            else: minimize_result = minimize_function(number_of_arguments, sets_number, 'cnf')

            minimize_normal_result = normal(minimize_result[1], type_of, number_of_arguments, (basis_update[0][1], basis_update[1][1]), True)[1]
            minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)

            veich_schemme_list.append((type_of, minimize_result[1], sets_number, []))

            # Forming Output

            global_truth_table_output.append(get_true_table(truth_table, number_of_arguments))

            DDNF = converting_string(False, function_regime, normal_result[0][0], number_of_arguments)

            global_output.append("\\text{ДДНФ }" f"y_{i}" r"\text{: }" f"{DDNF}")
            global_output.append("\\text{ДКНФ }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, normal_result[0][1], number_of_arguments)}")
            global_output.append("\\text{Нормальна форма }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime,normal_result[0][2], number_of_arguments)}")
            global_output.append("\\text{Операторна форма }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, operator_result, number_of_arguments)}")

            if minimize_result[2]: global_output.append("\\text{МДНФ }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, minimize_result[0], number_of_arguments)}")
            else: global_output.append("\\text{МКНФ }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, minimize_result[0], number_of_arguments)}")

            global_output.append("\\text{Нормальна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, str(minimize_normal_result), number_of_arguments)}")
            global_output.append("\\text{Операторна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{converting_string(True, function_regime, minimize_operator_result, number_of_arguments)}")
            global_output.extend(class_define(function_regime, sets_number, number_of_arguments, i, DDNF=DDNF))
            global_output.append(None)

            i += 1

    elif function_regime == "expression":

        num_functions = input("Введіть кількість функцій, які потрібно проаналізувати (до 10): ")
        if not validate(num_functions, "num_functions"): continue
        num_functions = int(float(num_functions))

        while i <= num_functions:

            print(f"\nВвід даних для функції y{i}:")

            function_input = input(f"Набери функцію y{i} (як AND використовуйте &, як OR використовуйте |, як NOT використовуйте ~): ")
            if not validate(function_input, "function_input"): continue
            function_data = find_args_and_sets(function_input)

            sets_number = function_data[1]

            print(f"sets number: {sets_number}")

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

            veich_schemme_list.append((type_of, minimize_result[1], sets_number, args_list))

            #Forming Output

            global_truth_table_output.append(get_true_table(truth_table, number_of_arguments))

            DDNF = converting_string(False, function_regime, normal_result[0][0], number_of_arguments, optional=args_list)

            global_output.append("\\text{ДДНФ }" f"y_{i}" r"\text{: }" f"{DDNF}")
            global_output.append("\\text{ДКНФ }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, normal_result[0][1], number_of_arguments, args_list)}")
            global_output.append("\\text{Нормальна форма }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime,normal_result[0][2], number_of_arguments, args_list)}")
            global_output.append("\\text{Операторна форма }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, operator_result, number_of_arguments, args_list)}")

            if minimize_result[2]: global_output.append("\\text{МДНФ }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, minimize_result[0], number_of_arguments, args_list)}")
            else: global_output.append("\\text{МКНФ }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, minimize_result[0], number_of_arguments, args_list)}")

            global_output.append("\\text{Нормальна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{converting_string(False, function_regime, str(minimize_normal_result), number_of_arguments, args_list)}")
            global_output.append("\\text{Операторна форма мінімізованої функції }" f"y_{i}" r"\text{: }" f"{converting_string(True, function_regime, minimize_operator_result, number_of_arguments, args_list)}")
            global_output.extend(class_define(function_regime, sets_number, number_of_arguments, i, optional=args_list, DDNF=DDNF))
            global_output.append(None)

            i += 1

    BLOCK1_width = (number_of_arguments+1)*1.5

    page_width = max(int(len(max((item for item in global_output if item is not None), key=len))*0.15), 44)
    page_height = max(number_of_sets, 30, largest_pdf_height_cm(temp_dir))

    output_difficult = round(max(page_width * 4 / 23, page_height * 4 / 23), 2)

    if output_difficult > 100:

        print(f"\nВаша функція має складність виводу: {output_difficult}%, що перевищує 100%.\nНажаль Latex-компілятор не зможе створити PDF файл вивід :(\n")

    else:

        if not create_veich_schemme_pdf(temp_dir, veich_schemme_list):

            messagebox.showerror("Помилка", "Не вдалося створити діаграми Вейча для функцій, звідси й pdf файл."); continue

        page_height += largest_pdf_height_cm(temp_dir)
        create_pdf_main(temp_dir, [global_output, global_truth_table_output], [page_width, page_height, BLOCK1_width])

    tmp_obj.cleanup()