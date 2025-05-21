from normal_forms import normal

def KM_function(sets_number, num_of_args, num_of_function):

    def differ_by_one_bit(x, y):
        xor = x ^ y
        return xor > 0 and (xor & (xor - 1)) == 0

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

        return "\\text{Не монотонна: }" + f"y_{num_of_function}({x_bit_string}) > y_{num_of_function}({y_bit_string}) \\rightarrow " + "\\text{не входить в клас KM}", False

    return "\\text{Монотонна" "}" "\\rightarrow" + "\\text{входить в клас KM}", True

def KL_function(function_regime, sets_number, num_of_args, DDNF=None, optional=False):

    def good_looking_polynomial(polynomial):

        polynomial = polynomial.replace("_", "")

        term_list = polynomial.split(" ⊕ ")

        final_term_list = []

        for term in term_list:

            temp_list = term.split(" ∧ ")
            temp_str = ""

            if temp_list[0] == "1":

                final_term_list.append(temp_list[0])

            else:
                
                temp_list = sorted(temp_list, key=lambda x: (x[0], -int(x[1:])))

                for item in temp_list: temp_str += f"{item[0]}_{item[1]} ∧ "

                temp_str = temp_str.rstrip(" ∧ ")
                final_term_list.append(temp_str)

        final_term_list = sorted(final_term_list, key=len)
        final_str = ""

        for term in final_term_list: final_str += f"{term} ⊕ "

        final_str = final_str.rstrip(" ⊕ ")

        return final_str

    list_to_replace = [f"x{e}" for e in range(num_of_args, 0, -1)]

    if function_regime == "sets":

        def final_form_function(indices, num_vars):

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

        steps = []

        normal_result = normal(sets_number, 1, num_of_args, ('І', 'АБО'), False)
        form = ""

        steps.append("\\text{\\qquad   Покрокове знаходження поліному Жегалкіна:}")
        steps.append("\\text{\\qquad    ДДНФ функції:" "} " + f"{DDNF}")
        steps.append("\\text{\\qquad    Заміню} " "∨ " "\\text{на" "} " "⊕" " \\text{та застосую аксіому алгебри Жегалкіна }" "not(X) = X ⊕ 1" "\\text{:" "}")

        for term in normal_result[1].structure:

            new_term = ""

            for e in range(num_of_args):

                if term[e] == '1': new_term += f"X_{num_of_args - e} ∧ "
                else: new_term += f"(X_{num_of_args - e} ⊕ 1) ∧ "

            new_term = new_term.rstrip(" ∧ ")
            form += f"({new_term}) ⊕ "

        form = form.rstrip(" ⊕ ")

        steps.append("\\text{\\qquad    }" + form + r" \ ")
        steps.append("\\text{\\qquad    Розкрию дужки, викреслю парні терми та отримаю фінальну форму поліному Жегалкіна:}")

        final_form = final_form_function(sets_number, num_of_args)
        final_form = final_form.replace("+", "⊕")
        final_form = final_form.replace("*", " ∧ ")

        for i in range(num_of_args): final_form = final_form.replace(f"x{i+1}", f"X_{i+1}")
        final_form = good_looking_polynomial(final_form)

        steps.append("\\text{\\qquad    }" + final_form)

        if "∧" in final_form:

            return "\\text{Не лінійна, тому що поліном містить терм, ранг якого більший за 1: }" + f"{final_form} \\rightarrow " + "\\text{не входить в клас КЛ}", steps, False

        else:

            return "\\text{Лінійна:" "} " +  f"{final_form} \\rightarrow " + "\\text{входить в клас КЛ}", steps, True

    elif function_regime == "func":

        def final_form_function(indices, num_vars):

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

        steps = []

        normal_result = normal(sets_number, 1, num_of_args, ('І', 'АБО'), False)
        form = ""

        steps.append("\\text{\\qquad   Покрокове знаходження поліному Жегалкіна:}")
        steps.append("\\text{\\qquad    ДДНФ функції:" "} " + f"{DDNF}")
        steps.append("\\text{\\qquad    Заміню} " "∨ " "\\text{на" "} " "⊕" " \\text{та застосую аксіому алгебри Жегалкіна }" "not(X) = X ⊕ 1" "\\text{:" "}")

        for term in normal_result[1].structure:

            new_term = ""

            for e in range(num_of_args):

                if term[e] == '1': new_term += f"{optional[e]} ∧ "
                else: new_term += f"({optional[e]} ⊕ 1) ∧ "

            new_term = new_term.rstrip(" ∧ ")
            form += f"({new_term}) ⊕ "

        form = form.rstrip(" ⊕ ")

        steps.append("\\text{\\qquad    }" + form + r" \ ")
        steps.append("\\text{\\qquad    Розкрию дужки, викреслю парні терми та отримаю фінальну форму поліному Жегалкіна:}")

        final_form = final_form_function(sets_number, num_of_args)
        final_form = final_form.replace("+", "⊕")
        final_form = final_form.replace("*", " ∧ ")

        for i in range(num_of_args): final_form = final_form.replace(list_to_replace[i], optional[i])
        final_form = good_looking_polynomial(final_form)

        steps.append("\\text{\\qquad    }" + final_form)

        if "∧" in final_form:

            return "\\text{Не лінійна, тому що поліном містить терм, ранг якого більший за 1: }" + f"{final_form} \\rightarrow " + "\\text{не входить в клас КЛ}", steps, False
        
        else:

            return "\\text{Лінійна:" "} " +  f"{final_form} \\rightarrow " + "\\text{входить в клас КЛ}", steps, True

def KC_function(sets_number, num_of_args, num_of_function): #Самодвоїстість функції

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

            return "\\text{Не самодвоїста: }" + f"y_{num_of_function}({num_bit_string}) = 1" + " \\text{ та }" f"not(y_{num_of_function}({anti_num_bit_string})) = 1" + " \\rightarrow " "\\text{не входить в клас КС}", False
        
        else:

            return "\\text{Не самодвоїста: }" + f"y_{num_of_function}({num_bit_string}) = 0" + " \\text{ та }" f"not(y_{num_of_function}({anti_num_bit_string})) = 0" + " \\rightarrow " "\\text{не входить в клас КС}", False

    return r"\text{Самодвоїста} \rightarrow \text{входить в клас КС}", True

def class_define(function_regime, sets_number, num_of_args, num_of_function, DDNF=None, optional = False):

    result = ""

    K0 = not(0 in sets_number) #Зберігає нуль

    if K0:

        K0 = "\\text{" "Зберігає нуль: }" + f"y_{num_of_function}(" + "0, "*num_of_args
        K0 = K0[:-2] + ") = 0"
        K0 = rf"{K0} \rightarrow " "\\text{входить в клас K0}", True

    else:

        K0 = "\\text{" "Не зберігає нуль: }" + f"y_{num_of_function}(" + "0, "*num_of_args
        K0 = K0[:-2] + ") = 1"
        K0 = rf"{K0} \rightarrow " "\\text{не входить в клас K0}", False

    K1 = 2**num_of_args - 1 in sets_number #Зберігкає одиницю

    if K1:

        K1 = "\\text{" "Зберігає одиницю: }" + f"y_{num_of_function}(" + "1, "*num_of_args
        K1 = K1[:-2] + ") = 1"
        K1 = rf"{K1} \rightarrow " "\\text{входить в клас K1}", True 

    else:

        K1 = "\\text{" "Не зберігає одиницю: }" + f"y_{num_of_function}(" + "1, "*num_of_args
        K1 = K1[:-2] + ") = 0"
        K1 = rf"{K1} \rightarrow " "\\text{не входить в клас K1}", False 

    KC = KC_function(sets_number, num_of_args, num_of_function)
    KM = KM_function(sets_number, num_of_args, num_of_function)

    KL = KL_function(function_regime, sets_number, num_of_args, DDNF=DDNF, optional=optional)

    result += "\\text{Функція }"+ f"y_{num_of_function}" + r"\text{: }"

    for x in [(K0[1], 0), (K1[1], 1), (KC[1], 2), (KM[1], 3), (KL[2], 4)]:

        if x[1] == 0:

            string = "\\text{входить в клас K0}" if x[0] else "\\text{не входить в клас K0}"
            result += f"{string}, "

        elif x[1] == 1:

            string = "\\text{входить в клас K1}" if x[0] else "\\text{не входить в клас K1}"
            result += f"{string}, "

        elif x[1] == 2:

            string = "\\text{входить в клас KC}" if x[0] else "\\text{не входить в клас KC}"
            result += f"{string}, "

        elif x[1] == 3:

            string = "\\text{входить в клас KM}" if x[0] else "\\text{не входить в клас KM}"
            result += f"{string}, "

        elif x[1] == 4:

            string = "\\text{входить в клас КЛ}" if x[0] else "\\text{не входить в клас КЛ}"
            result += f"{string}, "

    result += "\\text{тому за теоремою Поста-Яблонського функція } " f"y_{num_of_function} "

    if all(not(x) for x in [K0[1], K1[1], KC[1], KM[1], KL[2]]):

        result += "\\text{ ЯВЛЯЄТЬСЯ функціонально повною}"

    else:

        result += "\\text{ НЕ ЯВЛЯЄТЬСЯ функціонально повною}"

    return ["\\text{Дослідження функції } " f"y_{num_of_function}" r"\text{: }","\\text{K0: " "}" + K0[0], "\\text{K1: " "}" + K1[0], "\\text{КС: " "}" + KC[0], "\\text{КМ: " "}" + KM[0], "\\text{КЛ: " "}" + KL[0]] + KL[1] + ["\\textbf{Резюме дослідження функції }" f"y_{num_of_function}" r"\text{: }", result]