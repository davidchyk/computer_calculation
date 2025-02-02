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

    # Введення вихідних значень Y (для автомата Мура)
    if type_of_automat == "МУРА":
        print("\nВведіть вихідні значення Y (або 1 або 0) для кожного стану:")
        for key in state_coding:
            while True:
                temp = input(f"Введіть стан Y (0 або 1) для {state_coding[key]}: ").strip()
                if temp in ["0", "1"]:
                    values_of_Y_coding[state_coding[key]] = int(temp)
                    break
                else:
                    print("Некоректне значення. Введіть 0 або 1.")

    # Введення переходів
    print("\nВведіть переходи між вершинами у форматі, наприклад: 000>001>010>011")
    while True:
        temp = input("Переходи: ").strip()
        if ">" in temp:
            transition_list = [code.strip() for code in temp.split('>') if code.strip()]
            # Перевірка, чи всі коди існують у state_coding
            invalid_codes = [code for code in transition_list if code not in state_coding.values()]
            if invalid_codes:
                print(
                    f"Нижченаведені коди не знайдені серед введених вершин: {', '.join(invalid_codes)}. Спробуйте ще раз.")
                continue
            if len(transition_list) < 2:
                print("Потрібно принаймні два стани для переходу. Спробуйте ще раз.")
                continue
            break
        else:
            print("Невірний формат. Використовуйте '>' для розділення переходів.")

    print(f"\nПорядок кодування переходів: {transition_list}")
    if type_of_automat == "МІЛІ":
        print("\nВведіть вихідні значення Y (або 1 або 0) для кожного стану:")

        loop_range = len(transition_list)/2
        if type(loop_range) is float:
            loop_range += 1
            loop_range = int(loop_range)
        
        for i in range(loop_range):
            while True:
                temp = input(f"Введіть стан Y (0 або 1) для {transition_list[i]} > {transition_list[i+1]}: ").strip()
                if temp in ["0", "1"]:
                    values_of_Y_coding[transition_list[i] + " > " + transition_list[i+1]] = int(temp)
                else:
                    print("Некоректне значення. Введіть 0 або 1.")
                    continue
                break

    print(values_of_Y_coding)
    triggers(type_of_trigger, transition_list)
    # Створення словника переходів
    for i in range(len(transition_list) - 1):
        current_state = transition_list[i]
        next_state = transition_list[i + 1]
        transitions.setdefault(current_state, []).append(next_state)

    print("\nСловник переходів між станами:")
    for state, next_states in transitions.items():
        print(f"{state} -> {', '.join(next_states)}")

    # Форматований вивід через tabulate у потрібному форматі
    table_data = []
    for i in range(len(transition_list) - 1):
        current_state = transition_list[i]
        next_state = transition_list[i + 1]
        from_state = list(state_coding.keys())[list(state_coding.values()).index(current_state)]
        to_state = list(state_coding.keys())[list(state_coding.values()).index(next_state)]
        transition_string = f"{current_state}>{next_state}"
        y_value = values_of_Y_coding.get(current_state, "-")  # Якщо немає Y, ставимо "-"

        table_data.append([f"{from_state} -> {to_state}", transition_string, y_value])

    print("\nФорматована таблиця переходів:")
    print(tabulate(table_data, headers=["Стани", "Переход станів", "Y"], tablefmt="github"))

def triggers(type_of_trigger, transition_list):
    loop_range = len(transition_list)/2
    coding_trigger = {}
    if type_of_trigger == "RS":
        #запис кодування RS тригера
        if type(loop_range) is float:
            loop_range += 1
            loop_range = int(loop_range)
        print("is working")
        for j in range(len(transition_list[0])):
            coding_trigger[f"R{j+1}"] = []
            coding_trigger[f"S{j+1}"] = []
        for i in range(loop_range):
            temp = transition_list[i]
            temp_next = transition_list[i+1]
            while True:
                print(f"org:{transition_list}")
                print(f"len temp: {len(temp)}")
                print(f"len temp_next: {len(temp_next)}")
                print(f"range len temp{range(len(temp))}")

                print(f"debug: {coding_trigger}")
                for j in range(len(temp)):
                    print(f"index J:{j}")
                    if temp[j] == "0" and temp_next[j] == "0":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"R{j+1}"].append("*")
                        coding_trigger[f"S{j+1}"].append("0")
                    elif temp[j] == "0" and temp_next[j] == "1":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"R{j+1}"].append("0")
                        coding_trigger[f"S{j+1}"].append("1")
                    elif temp[j] == "1" and temp_next[j] == "0":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"R{j+1}"].append("1")
                        coding_trigger[f"S{j+1}"].append("0")
                    elif temp[j] == "1" and temp_next[j] == "1":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"R{j+1}"].append("0")
                        coding_trigger[f"S{j+1}"].append("*")
                break
    elif type_of_trigger == "T":
            #запис кодування T тригера
            if type(loop_range) is float:
                loop_range += 1
                loop_range = int(loop_range)
            print("is working")
            for j in range(len(transition_list[0])):
                coding_trigger[f"T{j+1}"] = []
            for i in range(loop_range):
                temp = transition_list[i]
                temp_next = transition_list[i+1]
                while True:
                    print(f"org:{transition_list}")
                    print(f"len temp: {len(temp)}")
                    print(f"len temp_next: {len(temp_next)}")
                    print(f"range len temp{range(len(temp))}")

                    print(f"debug: {coding_trigger}")
                    for j in range(len(temp)):
                        print(f"index J:{j}")
                        if temp[j] == "0" and temp_next[j] == "0":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"T{j+1}"].append("0")
                        elif temp[j] == "0" and temp_next[j] == "1":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"T{j+1}"].append("1")
                        elif temp[j] == "1" and temp_next[j] == "0":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"T{j+1}"].append("1")
                        elif temp[j] == "1" and temp_next[j] == "1":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"T{j+1}"].append("0")
                break
    elif type_of_trigger == "D":
            #запис кодування D тригера
            if type(loop_range) is float:
                loop_range += 1
                loop_range = int(loop_range)
            print("is working")
            for j in range(len(transition_list[0])):
                coding_trigger[f"D{j+1}"] = []
            for i in range(loop_range):
                temp = transition_list[i]
                temp_next = transition_list[i+1]
                while True:
                    print(f"org:{transition_list}")
                    print(f"len temp: {len(temp)}")
                    print(f"len temp_next: {len(temp_next)}")
                    print(f"range len temp{range(len(temp))}")

                    print(f"debug: {coding_trigger}")
                    for j in range(len(temp)):
                        print(f"index J:{j}")
                        if temp[j] == "0" and temp_next[j] == "0":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"D{j+1}"].append("0")
                        elif temp[j] == "0" and temp_next[j] == "1":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"D{j+1}"].append("1")
                        elif temp[j] == "1" and temp_next[j] == "0":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"D{j+1}"].append("0")
                        elif temp[j] == "1" and temp_next[j] == "1":
                            print(f"elements: {temp[j]}, and {temp_next[j]} ")
                            coding_trigger[f"D{j+1}"].append("1")
                break
    elif type_of_trigger == "JK":
        #запис кодування JK тригера
        if type(loop_range) is float:
            loop_range += 1
            loop_range = int(loop_range)
        print("is working")
        for j in range(len(transition_list[0])):
            coding_trigger[f"J{j+1}"] = []
            coding_trigger[f"K{j+1}"] = []
        for i in range(loop_range):
            temp = transition_list[i]
            temp_next = transition_list[i+1]
            while True:
                print(f"org:{transition_list}")
                print(f"len temp: {len(temp)}")
                print(f"len temp_next: {len(temp_next)}")
                print(f"range len temp{range(len(temp))}")

                print(f"debug: {coding_trigger}")
                for j in range(len(temp)):
                    print(f"index J:{j}")
                    if temp[j] == "0" and temp_next[j] == "0":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"J{j+1}"].append("0")
                        coding_trigger[f"K{j+1}"].append("*")
                    elif temp[j] == "0" and temp_next[j] == "1":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"J{j+1}"].append("1")
                        coding_trigger[f"K{j+1}"].append("*")
                    elif temp[j] == "1" and temp_next[j] == "0":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"J{j+1}"].append("*")
                        coding_trigger[f"K{j+1}"].append("1")
                    elif temp[j] == "1" and temp_next[j] == "1":
                        print(f"elements: {temp[j]}, and {temp_next[j]} ")
                        coding_trigger[f"J{j+1}"].append("*")
                        coding_trigger[f"K{j+1}"].append("0")
                
                break
         
    print(coding_trigger)

if __name__ == '__main__':
    graph_func()
