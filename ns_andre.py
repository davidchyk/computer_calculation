from tabulate import tabulate

def graph_func():
    state_coding = {}
    transitions = {}
    values_of_Y_coding = {}

    # Введення типу автомата
    while True:
        try:
            type_of_automat = input("Введіть тип автомата, Мура або Мілі: ").strip().upper()
            if type_of_automat not in ["МУРА", "МІЛІ"]:
                print("Некоректний ввід автомата")
                continue
            break
        except ValueError:
            print("Помилка типу даних")

    # Введення типу тригера
    while True:
        try:
            type_of_trigger = input("Введіть тип тригера: RS, T, D, JK: ").strip().upper()
            if type_of_trigger not in ["RS", "T", "D", "JK"]:
                print("Некоректний ввід тригера")
                continue
            break
        except ValueError:
            print("Помилка типу даних")

    # Отримання префікса і кількості вершин
    state_prefix = input("Введіть префікс для назв вершин (наприклад, Z): ").strip()
    while True:
        try:
            number_of_states = int(input("Введіть кількість вершин: "))
            if number_of_states <= 0:
                print("Кількість вершин повинна бути позитивним числом. Спробуйте ще раз.")
                continue
            break
        except ValueError:
            print("Будь ласка, введіть ціле число.")

    # Введення кодування вершин
    print("\nВведіть кодування вершин (станів):")
    for i in range(number_of_states):
        while True:
            code = input(f"Кодування вершини {state_prefix}{i}: ").strip()
            if not code:
                print("Кодування не може бути порожнім. Спробуйте ще раз.")
                continue
            if code in state_coding.values():
                print("Цей код вже використовується. Введіть унікальний код.")
                continue
            state_coding[f"{state_prefix}{i}"] = code
            break

    # Введення вихідних значень Y
    if type_of_automat == "МУРА":
        print("\nВведіть вихідні значення Y (0 або 1) для кожного стану:")
        for key in state_coding:
            while True:
                temp = input(f"Введіть стан Y (0 або 1) для {state_coding[key]}: ").strip()
                if temp in ["0", "1"]:
                    values_of_Y_coding[state_coding[key]] = int(temp)
                    break
                else:
                    print("Некоректне значення. Введіть 0 або 1.")
    elif type_of_automat == "МІЛІ":
        print("\nВведіть вихідні значення Y (0 або 1) для кожного переходу:")
        # Тут ключ буде у форматі "current > next"
        # Кількість переходів буде рівна len(transition_list) - 1, але ми поки що не знаємо transition_list
        # Тому введення Y для Мілі буде здійснюватися пізніше після введення переходів

    # Введення переходів
    print("\nВведіть переходи між вершинами у форматі, наприклад: 000>001>010>011")
    while True:
        temp_input = input("Переходи: ").strip()
        if ">" in temp_input:
            transition_list = [code.strip() for code in temp_input.split('>') if code.strip()]
            # Перевірка, чи всі коди існують у state_coding
            invalid_codes = [code for code in transition_list if code not in state_coding.values()]
            if invalid_codes:
                print(f"Нижченаведені коди не знайдені серед введених вершин: {', '.join(invalid_codes)}. Спробуйте ще раз.")
                continue
            if len(transition_list) < 2:
                print("Потрібно принаймні два стани для переходу. Спробуйте ще раз.")
                continue
            break
        else:
            print("Невірний формат. Використовуйте '>' для розділення переходів.")

    print(f"\nПорядок кодування переходів: {transition_list}")

    # Якщо автомат Мілі – введення Y для переходів
    if type_of_automat == "МІЛІ":
        for i in range(len(transition_list) - 1):
            while True:
                key_y = transition_list[i] + " > " + transition_list[i+1]
                temp = input(f"Введіть стан Y (0 або 1) для переходу {transition_list[i]} > {transition_list[i+1]}: ").strip()
                if temp in ["0", "1"]:
                    values_of_Y_coding[key_y] = int(temp)
                    break
                else:
                    print("Некоректне значення. Введіть 0 або 1.")

    # Отримання кодування тригера (функція triggers повертає словник з кодами)
    trigger_transition = triggers(type_of_trigger, transition_list)
    
    # Побудова фінальної таблиці
    table_data = []
    num_transitions = len(transition_list) - 1
    for i in range(num_transitions):
        current_state = transition_list[i]
        next_state = transition_list[i+1]
        # Визначаємо Y для переходу
        if type_of_automat == "МУРА":
            y_val = values_of_Y_coding.get(current_state, "-")
        else:  # МІЛІ
            y_val = values_of_Y_coding.get(current_state + " > " + next_state, "-")
        
        # Формування значення тригера залежно від типу
        if type_of_trigger == "RS":
            # Припускаємо, що довжина коду однакова для всіх станів (наприклад, 1 або більше символів)
            r_val = "".join([trigger_transition[f"R{j+1}"][i] for j in range(len(transition_list[0]))])
            s_val = "".join([trigger_transition[f"S{j+1}"][i] for j in range(len(transition_list[0]))])
            row = [current_state, next_state, y_val, r_val, s_val]
            header = ["Z", "Z(i+1)", "Y", "R", "S"]
        elif type_of_trigger == "T":
            t_val = "".join([trigger_transition[f"T{j+1}"][i] for j in range(len(transition_list[0]))])
            row = [current_state, next_state, y_val, t_val]
            header = ["Z", "Z(i+1)", "Y", "T"]
        elif type_of_trigger == "D":
            d_val = "".join([trigger_transition[f"D{j+1}"][i] for j in range(len(transition_list[0]))])
            row = [current_state, next_state, y_val, d_val]
            header = ["Z", "Z(i+1)", "Y", "D"]
        elif type_of_trigger == "JK":
            j_val = "".join([trigger_transition[f"J{j+1}"][i] for j in range(len(transition_list[0]))])
            k_val = "".join([trigger_transition[f"K{j+1}"][i] for j in range(len(transition_list[0]))])
            row = [current_state, next_state, y_val, j_val, k_val]
            header = ["Z", "Z(i+1)", "Y", "J", "K"]
        table_data.append(row)

    print("\nФорматована таблиця переходів:")
    print(tabulate(table_data, headers=header, tablefmt="github"))

def triggers(type_of_trigger, transition_list):
    # Визначаємо кількість переходів, для яких буде проводитися обчислення кодування тригера.
    # Ми працюємо з переходами: від transition_list[i] до transition_list[i+1]
    num_transitions = len(transition_list) - 1
    # Ініціалізація словника з кодами тригера
    coding_trigger = {}
    
    if type_of_trigger == "RS":
        # Ініціалізуємо ключі для кожного біту (залежить від довжини коду першого стану)
        for j in range(len(transition_list[0])):
            coding_trigger[f"R{j+1}"] = []
            coding_trigger[f"S{j+1}"] = []
        # Обчислення для кожного переходу
        for i in range(num_transitions):
            temp = transition_list[i]
            temp_next = transition_list[i+1]
            for j in range(len(temp)):
                if temp[j] == "0" and temp_next[j] == "0":
                    coding_trigger[f"R{j+1}"].append("*")
                    coding_trigger[f"S{j+1}"].append("0")
                elif temp[j] == "0" and temp_next[j] == "1":
                    coding_trigger[f"R{j+1}"].append("0")
                    coding_trigger[f"S{j+1}"].append("1")
                elif temp[j] == "1" and temp_next[j] == "0":
                    coding_trigger[f"R{j+1}"].append("1")
                    coding_trigger[f"S{j+1}"].append("0")
                elif temp[j] == "1" and temp_next[j] == "1":
                    coding_trigger[f"R{j+1}"].append("0")
                    coding_trigger[f"S{j+1}"].append("*")
                    
    elif type_of_trigger == "T":
        for j in range(len(transition_list[0])):
            coding_trigger[f"T{j+1}"] = []
        for i in range(num_transitions):
            temp = transition_list[i]
            temp_next = transition_list[i+1]
            for j in range(len(temp)):
                if temp[j] == "0" and temp_next[j] == "0":
                    coding_trigger[f"T{j+1}"].append("0")
                elif temp[j] == "0" and temp_next[j] == "1":
                    coding_trigger[f"T{j+1}"].append("1")
                elif temp[j] == "1" and temp_next[j] == "0":
                    coding_trigger[f"T{j+1}"].append("1")
                elif temp[j] == "1" and temp_next[j] == "1":
                    coding_trigger[f"T{j+1}"].append("0")
                    
    elif type_of_trigger == "D":
        for j in range(len(transition_list[0])):
            coding_trigger[f"D{j+1}"] = []
        for i in range(num_transitions):
            temp = transition_list[i]
            temp_next = transition_list[i+1]
            for j in range(len(temp)):
                if temp[j] == "0" and temp_next[j] == "0":
                    coding_trigger[f"D{j+1}"].append("0")
                elif temp[j] == "0" and temp_next[j] == "1":
                    coding_trigger[f"D{j+1}"].append("1")
                elif temp[j] == "1" and temp_next[j] == "0":
                    coding_trigger[f"D{j+1}"].append("0")
                elif temp[j] == "1" and temp_next[j] == "1":
                    coding_trigger[f"D{j+1}"].append("1")
                    
    elif type_of_trigger == "JK":
        for j in range(len(transition_list[0])):
            coding_trigger[f"J{j+1}"] = []
            coding_trigger[f"K{j+1}"] = []
        for i in range(num_transitions):
            temp = transition_list[i]
            temp_next = transition_list[i+1]
            for j in range(len(temp)):
                if temp[j] == "0" and temp_next[j] == "0":
                    coding_trigger[f"J{j+1}"].append("0")
                    coding_trigger[f"K{j+1}"].append("*")
                elif temp[j] == "0" and temp_next[j] == "1":
                    coding_trigger[f"J{j+1}"].append("1")
                    coding_trigger[f"K{j+1}"].append("*")
                elif temp[j] == "1" and temp_next[j] == "0":
                    coding_trigger[f"J{j+1}"].append("*")
                    coding_trigger[f"K{j+1}"].append("1")
                elif temp[j] == "1" and temp_next[j] == "1":
                    coding_trigger[f"J{j+1}"].append("*")
                    coding_trigger[f"K{j+1}"].append("0")
                    
    return coding_trigger

if __name__ == '__main__':
    graph_func()
