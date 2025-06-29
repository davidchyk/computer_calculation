import pandas as pd

# === Ввід користувача ===
auto_type = input("Введіть тип автомата (Мура/Мілі): ").strip().lower()
trigger_type = input("Введіть тип тригера (T/D/JK/RS): ").strip().upper()
num_triggers = int(input("Скільки тригерів (кількість Q): ").strip())
num_outputs = int(input("Скільки виходів Y (наприклад 3): ").strip())

# === Ввід станів ===
print("\nВведення станів:")
states = {}
state_order = []
while True:
    state_name = input("Назва стану (наприклад Z1, Enter щоб завершити): ").strip()
    if not state_name:
        break
    y_output = input(f"Вихід {state_name} (у двійковому вигляді, довжина {num_outputs}): ").strip()
    states[state_name] = y_output.zfill(num_outputs)
    state_order.append(state_name)

# === Кодування станів
state_encoding = {
    state: format(i, f'0{num_triggers}b') for i, state in enumerate(state_order)
}

# === Ввід переходів
print("\nВведення переходів:")
transitions = []
while True:
    src = input("З якого стану (наприклад Z1, Enter щоб завершити): ").strip()
    if not src:
        break
    dst = input("У який стан (наприклад Z2): ").strip()
    x_inputs = input("Вхідні умови (наприклад x0 або -): ").strip().split(',')
    if auto_type == "мура":
        y_list = []
    else:
        y_list = input("Виходи (наприклад y1 або -, якщо немає): ").strip().split(',')
    transitions.append((src, dst, x_inputs, y_list))

# === Таблиці збудження
def get_trigger_inputs(trigger, qn, qn1):
    if trigger == "T":
        return {'T': int(qn != qn1)}
    elif trigger == "D":
        return {'D': qn1}
    elif trigger == "JK":
        if qn == 0 and qn1 == 0: return {'J': 0, 'K': '-'}
        if qn == 0 and qn1 == 1: return {'J': 1, 'K': '-'}
        if qn == 1 and qn1 == 0: return {'J': '-', 'K': 1}
        if qn == 1 and qn1 == 1: return {'J': '-', 'K': 0}
    elif trigger == "RS":
        if qn == 0 and qn1 == 0: return {'R': '-', 'S': 0}
        if qn == 0 and qn1 == 1: return {'R': 0, 'S': 1}
        if qn == 1 and qn1 == 0: return {'R': 1, 'S': 0}
        if qn == 1 and qn1 == 1: return {'R': 0, 'S': '-'}
    return {}

# === Формування таблиці
table = []
for src, dst, x_list, y_list in transitions:
    src_code = state_encoding[src]
    dst_code = state_encoding[dst]

    for x in x_list:
        row = {}
        # Поточні Q
        for i in range(num_triggers):
            row[f"Q{i+1}"] = int(src_code[i])

        # Наступні Q
        for i in range(num_triggers):
            row[f"Q{i+1}_next"] = int(dst_code[i])

        # Вхідна умова
        row["X"] = x if x != '-' else '-'

        # Виходи
        if auto_type == "мура":
            y_bin = states[dst].zfill(num_outputs)
        else:
            y_bin = ['0'] * num_outputs
            for y in y_list:
                if y.startswith("y") and y[1:].isdigit():
                    idx = int(y[1:]) - 1
                    if 0 <= idx < num_outputs:
                        y_bin[idx] = '1'
        for j in range(num_outputs):
            row[f"y{j+1}"] = int(y_bin[j])

        # Тригери
        for i in range(num_triggers):
            q_cur = int(src_code[i])
            q_next = int(dst_code[i])
            trig_vals = get_trigger_inputs(trigger_type, q_cur, q_next)
            for k, v in trig_vals.items():
                row[f"{k}{i+1}"] = v

        table.append(row)

# === Вивід
df = pd.DataFrame(table)
print("\n=== Таблиця переходів та тригерів ===")
print(df.to_string(index=False))
