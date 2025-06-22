import pandas as pd
from sympy import symbols, SOPform

# === Ввід користувача ===
auto_type = input("Введіть тип автомата (Мура/Мілі): ").strip()
trigger_type = input("Введіть тип тригера (T/D): ").strip()
num_triggers = int(input("Скільки тригерів (кількість Q): ").strip())
num_outputs = int(input("Скільки виходів Y: ").strip())

# === Ввід станів ===
print("\nВведення станів:")
states = {}
while True:
    state_name = input("Назва стану (наприклад Z1, Enter щоб завершити): ").strip()
    if not state_name:
        break
    y_output = input(f"Вихід {state_name} (у двійковому вигляді, довжина {num_outputs}): ").strip()
    states[state_name] = y_output.zfill(num_outputs)

# === Ввід переходів ===
print("\nВведення переходів:")
transitions = {}
while True:
    src = input("З якого стану (наприклад Z1, Enter щоб завершити): ").strip()
    if not src:
        break
    dst = input("У який стан (наприклад Z2): ").strip()
    x_inputs = input("Вхідні умови (через кому, наприклад x0,x1 або -): ").strip().split(",")
    if auto_type.lower() == "мура":
        y_list = []
    else:
        y_list = input("Виходи (через кому, наприклад y0,y1): ").strip().split(",")
    transitions[(src, dst)] = (y_list, x_inputs)

# === Кодування станів ===
unique_states = list(states.keys())
bit_width = len(bin(len(unique_states) - 1)) - 2
state_encoding = {
    state: format(i, f'0{max(bit_width, num_triggers)}b') for i, state in enumerate(unique_states)
}

# === Побудова таблиці ===
table = []
for (src, dst), (y_list, x_list) in transitions.items():
    for x in x_list:
        src_code = state_encoding[src]
        dst_code = state_encoding[dst]
        if x == "-":
            x_val = "-"
        elif x.startswith("x") and x[1].isdigit():
            x_val = int(x[1])
        else:
            raise ValueError(f"Невірний формат вхідної умови: {x}")

        if auto_type.lower() == "мура":
            y_bin = states[dst].zfill(num_outputs)
        else:
            y_bin = y_list[0].zfill(num_outputs) if y_list else '0'*num_outputs

        row = {}

        # Поточні значення Q
        for i in range(num_triggers):
            row[f"Q{i+1}"] = int(src_code[i]) if i < len(src_code) else 0
        row["X"] = x_val

        # Наступні значення Q
        for i in range(num_triggers):
            row[f"Q{i+1}_next"] = int(dst_code[i]) if i < len(dst_code) else 0

        # Значення Y
        for j in range(num_outputs):
            row[f"y{j+1}"] = int(y_bin[j]) if j < len(y_bin) else 0

        # Значення тригерів
        for i in range(num_triggers):
            q_cur = int(src_code[i]) if i < len(src_code) else 0
            q_next = int(dst_code[i]) if i < len(dst_code) else 0
            row[f"T{i+1}"] = int(q_cur != q_next)

        table.append(row)

# === Створення та вивід таблиці ===
df = pd.DataFrame(table)
print("\n=== Таблиця переходів та виходів ===")
print(df.to_string(index=False))
