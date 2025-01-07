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

def KM_function(sets_number, num_of_args):

    def differ_by_one_bit(x, y):
        xor = x ^ y
        return xor > 0 and (xor & (xor - 1)) == 0

    """
    Перевіряє монотонність булевої функції.
    
    sets_number: список номерів наборів, при яких функція істинна.
    num_of_args: кількість аргументів (змінних) функції.
    
    Повертає True, якщо функція монотонна, інакше False.
    """

    n = 2 ** num_of_args  # Кількість наборів
    truth_table = [1 if i in sets_number else 0 for i in range(n)]  # Генерація таблиці істинності

    flag = False

    # Перевірка монотонності
    for x in range(n):

        for y in range(x + 1, n):

            if differ_by_one_bit(x, y):  # Перевіряємо, чи x є підмножиною y

                if truth_table[x] > truth_table[y]: flag = True; break  # Якщо f(x) > f(y), функція не монотонна

        if flag: break

    if flag:

        x_bit_string = ', '.join(list(format(x, f'0{num_of_args}b')))
        y_bit_string = ', '.join(list(format(y, f'0{num_of_args}b')))

        return f"Не монотонна: f({x_bit_string}) > f({y_bit_string}) => не входить в клас KM", False

    return "Монотонна => входить в клас KM", True

def KL_function(sets_number, num_of_args): #Лінійність функції TODO

    steps = ""

    def final_form_function(indices, num_vars):
        """
        Обчислює поліном Жегалкіна для заданої булевої функції.

        :param indices: Список індексів, де функція набуває значення 1
        :param num_vars: Кількість змінних
        :return: Строка, що представляє поліном Жегалкіна
        """
        size = 2 ** num_vars
        # Ініціалізуємо вектор функції
        f = [0] * size
        for idx in indices:
            if 0 <= idx < size:
                f[idx] = 1
            else:
                raise ValueError(f"Індекс {idx} виходить за межі допустимого діапазону для {num_vars} змінних.")

        # Виконуємо перетворення Мёбіуса (алгоритм Жегалкіна)
        for i in range(num_vars):
            for j in range(size):
                if j & (1 << i):
                    f[j] ^= f[j ^ (1 << i)]

        # Генеруємо мономи
        monomials = []
        for i in range(size):
            if f[i]:
                if i == 0:
                    monomials.append("1")
                else:
                    vars_in_monomial = []
                    for bit in range(num_vars):
                        if i & (1 << bit):
                            vars_in_monomial.append(f"x{bit+1}")
                    monomials.append('*'.join(vars_in_monomial))
        
        # Формуємо поліном
        if not monomials:
            return "0"
        else:
            return ' + '.join(monomials)

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

    steps += "\nПокрокове знаходження поліному Жегалкіна: \n"
    steps += f"ДДНФ функції: {start_form}" + "\n"
    steps += "Заміню ∨ на ⊕ та застосую аксіому алгебри Жегалкіна not(X) = X ⊕ 1: \n"

    for term in normal_result[1].structure:

        new_term = ""

        for e in range(num_of_args):

            if term[e] == '1': new_term += f"X_{num_of_args - e} ∧ "
            else: new_term += f"(X_{num_of_args - e} ⊕ 1) ∧ "

        new_term = new_term.rstrip(" ∧ ")
        form += f"({new_term}) ⊕ "

    form = form.rstrip(" ⊕ ")

    steps += form + "\n"
    steps += "Викреслю парні терми та отримаю фінальну форму поліному Жегалкіна: \n"

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

    final_form = final_form_function(sets_number, num_of_args)
    final_form = final_form.replace("+", "⊕")
    final_form = final_form.replace("*", " ∧ ")

    for i in range(num_of_args): final_form = final_form.replace(f"x{i+1}", f"X_{i+1}")

    steps += final_form

    if "∧" in final_form:

        return f"Не лінійна, тому що поліном містить терм, ранг якого більший за 1: {final_form} => не входить в клас КЛ", steps, False
    
    else:

        return f"Лінійна: {final_form} => входить в клас КЛ", steps, True

def KC_function(sets_number, num_of_args): #Самодвоїстість функції

    temp = False

    anti_sets_number = [x for x in range(2**num_of_args) if x not in sets_number]

    for num in range(2**num_of_args):

        anti_num = 2**num_of_args - num - 1

        if (num in sets_number) and (anti_num in sets_number):
            
            temp = (num, anti_num, 1)

        elif (num in anti_sets_number) and (anti_num in anti_sets_number):

            temp = (num, anti_num, 0)

    if temp:

        num_bit_string = ', '.join(list(format(num, f'0{num_of_args}b'))) # 9 = 1, 0, 0, 1
        anti_num_bit_string = ', '.join(list(format(anti_num, f'0{num_of_args}b')))

        if temp[2]:

            return f"Не самодвоїста: f({num_bit_string}) = 1 та not(f({anti_num_bit_string})) = 1 => не входить в клас КС", False
        
        else:

            return f"Не самодвоїста: f({num_bit_string}) = 0 та not(f({anti_num_bit_string})) = 0 => не входить в клас KC", False

    return "Самодвоїста => входить в клас КС", True

def class_define(sets_number, num_of_args, num_of_function):

    result = ""

    K0 = not(0 in sets_number) #Зберігає нуль

    if K0:

        K0 = f"Зберігає нуль: f(" + "0, "*num_of_args
        K0 = K0[::-2] + ") = 0"
        K0 = f"{K0} => входить в клас K0", True 

    else:

        K0 = f"Не зберігає нуль: f(" + "0, "*num_of_args
        K0 = K0[:-2] + ") = 1"
        K0 = f"{K0} => не входить в клас K0", False 

    K1 = 2**num_of_args - 1 in sets_number #Зберігкає одиницю

    if K1:

        K1 = f"Зберігає одиницю: f(" + "1, "*num_of_args
        K1 = K1[::-2] + ") = 1"
        K1 = f"{K1} => входить в клас K1", True 

    else:

        K1 = f"Не зберігає одиницю: f(" + "1, "*num_of_args
        K1 = K1[:-2] + ") = 0"
        K1 = f"{K1} => не входить в клас K1", False 

    KC = KC_function(sets_number, num_of_args)
    KL = KL_function(sets_number, num_of_args)
    KM = KM_function(sets_number, num_of_args)

    result += "\nРезюме:\n"
    result += f"Функція y_{num_of_function} "

    for x in [(K0[1], 0), (K1[1], 1), (KC[1], 2), (KM[1], 3), (KL[2], 4)]:

        if x[1] == 0:

            string = "входить в клас K0" if x[0] else "не входить в клас K0"
            result += f"{string}, "

        elif x[1] == 1:

            string = "входить в клас K1" if x[0] else "не входить в клас K1"
            result += f"{string}, "

        elif x[1] == 2:

            string = "входить в клас KC" if x[0] else "не входить в клас KC"
            result += f"{string}, "

        elif x[1] == 3:

            string = "входить в клас KM" if x[0] else "не входить в клас KM"
            result += f"{string}, "

        elif x[1] == 4:

            string = "входить в клас КЛ" if x[0] else "не входить в клас КЛ"
            result += f"{string}, "

    result += f"тому за теоремою Поста-Яблонського функція y_{num_of_function} "

    if all(not(x) for x in [K0[1], K1[1], KC[1], KM[1], KL[2]]):

        result += "ЯВЛЯЄТЬСЯ функціонально повною"

    else:

        result += "НЕ ЯВЛЯЄТЬСЯ функціонально повною"

    return f"K0: {K0[0]}\nK1: {K1[0]}\nKC: {KC[0]}\nKM: {KM[0]}\nKL: {KL[0]} {KL[1]}\n{result}"

print(class_define([1], 3, 1))