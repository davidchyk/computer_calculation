from normal_forms import normal

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

def KM_function(sets_number, num_of_args): #Монотонність функції

    ...

def KL_function(sets_number, num_of_args): #Лінійність функції

    final_form = ""

    term_monitoring = []

    def combinations(y_term, x_term):

        if x_term: x_term = x_term.replace(" ", " ∧ ")

        one_flag = False

        term = ""

        y_list = y_term.split(" ")

        list_of_combinations = [format(x, f"0{len(y_list)}b") for x in range(2**len(y_list))]

        for combination in list_of_combinations:

            if int(combination) == 0 and len(x_term) == 0: one_flag = True

            temp = ""
            index = 0

            for e in combination:

                if e == "1": temp += y_list[index] + " ∧ "
                index += 1

            temp += x_term

            temp = temp.rstrip(" ∧ ")

            if not temp.isspace() and len(temp) != 0:

                term += temp + " ⊕ "
                term = term.replace("Y", "X")

                temp = temp.replace("Y", "X")
                term_monitoring.append(temp)

        if one_flag: term += "1"

        return term

    normal_result = normal(sets_number, 1, num_of_args, ('І', 'АБО'), False)
    form = ""

    start_form = conver_to_normal(normal_result[0][0], num_of_args)

    final_term_list = []

    print(normal_result[1].structure)

    print("Покрокове знаходження поліному Жегалкіна: ")

    print(start_form)

    print("Застосую заміни: ")

    for term in normal_result[1].structure:

        new_term = ""

        for e in range(num_of_args):

            if term[e] == '1': new_term += f"X_{num_of_args - e} ∧ "
            else: new_term += f"(X_{num_of_args - e} ⊕ 1) ∧ "

        new_term = new_term.rstrip(" ∧ ")
        form += f"({new_term}) ⊕ "

    form = form.rstrip(" ⊕ ")

    print(form)

    for term in normal_result[1].structure:

        x_term = ""
        y_term = ""

        for e in range(num_of_args):

            if term[e] == "1": x_term += f"X_{num_of_args - e} "
            else: y_term += f"Y_{num_of_args - e} "

        y_term = y_term.rstrip(" ")
        x_term = x_term.rstrip(" ")

        temp = combinations(y_term, x_term)
        temp = temp.rstrip(" ⊕ ")

        final_term_list.append(temp)

    for term in final_term_list:

        final_form += f"({term}) ⊕ "

    final_form = final_form.rstrip(" ⊕ ")

    return final_form

def KC_function(sets_number, num_of_args): #Самодвоїстість функції

    anti_sets_number = [x for x in range(2**num_of_args) if x not in sets_number]

    print(f"anti_sets_number: {anti_sets_number}")

    for num in range(2**num_of_args):

        anti_num = 2**num_of_args - num - 1

        if num in sets_number and anti_num in sets_number:
            
            return (num, anti_num)

        elif num in anti_sets_number and anti_num in anti_sets_number:

            return (num, anti_num)

    return True

def class_define(sets_number, num_of_args):

    K0 = not(0 in sets_number) #Зберігає нуль
    K1 = 2**num_of_args - 1 in sets_number #Зберігкає одиницю

    KC = KC_function(sets_number, num_of_args)
    KL = KL_function(sets_number, num_of_args)

    return f"K0: {K0}, K1: {K1}, KC: {KC}, KL: {KL}"

print(class_define([0, 1, 2, 3, 4], 4))