from normal_forms import normal
from operator_form2 import operator_form
from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants

def generate(num_args: str, sets: str, basis: str):

    def replace_not_with_overline(expression):

        stack = []
        result = []
        i = 0

        while i < len(expression):
        
            if expression[i:i+4] == 'not(':

                result.append('\\overline{')
                stack.append('}')
                i += 4

            elif expression[i] == '(':

                result.append('(')
                stack.append(')')
                i += 1

            elif expression[i] == ')' and stack:

                result.append(stack.pop())
                i += 1

            else:

                result.append(expression[i])
                i += 1

        return ''.join(result)

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

    def split_string(s: str):

        index = 0

        while index < len(s) and s[index].isdigit(): index += 1
        
        numbers = s[:index]
        letters = s[index:]

        return numbers, letters

    number_of_arguments = float(num_args)

    basis_list = basis.split("/")

    basis_update = []
    args = []

    sets_number = [int(x) for x in sets.split(',')]

    num1, str1 = split_string(basis_list[0])
    num2, str2 = split_string(basis_list[1])

    basis_update.append((int(num1), str1))
    basis_update.append((int(num2), str2))

    if basis_update[1][1] in ['АБО', 'І-НЕ']: type_of = 1
    if basis_update[1][1] in ['І', 'АБО-НЕ']: type_of = 0

    in_num = int(basis_update[0][0])
    out_num = int(basis_update[1][0])

    data_table = truth_table(int(number_of_arguments), sets_number)
    normal_result = normal(sets_number, type_of, int(number_of_arguments), (basis_update[0][1], basis_update[1][1]), False)
    for line in normal_result[0]: args.append(conver_to_normal(line, int(number_of_arguments)))
    operator_result = operator_form(normal_result[1], in_num, out_num)

    args.append(f"Операторна форма при елементному базисі {basis}: {conver_to_normal(operator_result, int(number_of_arguments))}")
    args.append(r" \ ")

    if type_of:

        minimize_result = minimize_dnf_as_implicants(int(number_of_arguments), sets_number)

    else:

        minimize_result = minimize_cnf_as_implicants(int(number_of_arguments), [x for x in range(2**int(number_of_arguments)) if x not in sets_number])

    args.append(conver_to_normal(minimize_result[0], int(number_of_arguments)))

    minimize_normal_result = normal(minimize_result[1], type_of, int(number_of_arguments), (basis_update[0][1], basis_update[1][1]), True)[1]

    args.append(f"Нормальна форма мінімізованої функції при {'/'.join([basis_update[0][1], basis_update[1][1]])}: {conver_to_normal(str(minimize_normal_result), int(number_of_arguments))}")

    minimize_operator_result = operator_form(minimize_normal_result, in_num, out_num)
    args.append(f"Операторна форма мінімізованої функції при елементному базисі {basis}: {conver_to_normal_operator(minimize_operator_result, int(number_of_arguments))}")

    latex_str = """"""

    time_data = []

    for data in args:
        
        data = data.replace(' ', r' \ ')
        time_data.append(f"{data} \n")

    latex_str = """"""

    latex_str += r"\begin{array}{l}"

    for data in args:

        data = data.replace(' ', r' \ ')

        latex_str += rf"{data} \\"

    latex_str += r"\end{array}"

    return replace_not_with_overline(latex_str)