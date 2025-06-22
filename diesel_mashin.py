def define_states(auto_type: str):
    """
    Повертає словник станів залежно від типу автомата.
    """
    if auto_type == "Мура":
        return {
            "A": "0",
            "B": "1",
            "C": "0",
            "D": "1"
        }
    elif auto_type == "Мілі":
        return {
            "A": "-",
            "B": "-",
            "C": "-",
            "D": "-"
        }
    else:
        raise ValueError("Невідомий тип автомата: має бути 'Мура' або 'Мілі'")


def define_transitions(auto_type: str):
    """
    Повертає словник переходів залежно від типу автомата.
    """
    if auto_type == "Мура":
        return {
            ("A", "B"): ([], ["x0"]),
            ("B", "C"): ([], ["x1"]),
            ("C", "A"): ([], ["x0", "x1"])
        }
    elif auto_type == "Мілі":
        return {
            ("A", "B"): (["y0"], ["x0"]),
            ("B", "C"): (["y1"], ["x1"]),
            ("C", "A"): (["y0"], ["x0", "x1"])
        }
    else:
        raise ValueError("Невідомий тип автомата: має бути 'Мура' або 'Мілі'")


# === Вхідні параметри ===
auto_type = "Мура"       # або "Мілі"
trigger_type = "T"       # або "D", "JK", "RS" — поки лише зберігається

# === Завантаження структури ===
states = define_states(auto_type)
transitions = define_transitions(auto_type)

# === Вивід даних ===
print(f"Тип автомата: {auto_type}")
print(f"Тип тригера: {trigger_type}")

print("\nСтан → вихід:")
for state, output in states.items():
    print(f"  {state} → {output}")

print("\nПереходи (поточний → наступний):")
for (src, dst), (y_list, x_list) in transitions.items():
    y_out = ', '.join(y_list) if y_list else "-"
    x_in = ', '.join(x_list)
    print(f"  {src} → {dst} | x: [{x_in}] → y: [{y_out}]")

import pandas as pd

# === Вхідні параметри ===
auto_type = "Мура"  # або "Мілі"
trigger_type = "T"  # тип тригера — наразі підтримуються T-тригери

# === Кодування станів у двійкову форму ===
state_encoding = {
    "A": "00",
    "B": "01",
    "C": "10",
    "D": "11"
}

# === Словник вершин (станів) ===
def define_states(auto_type: str):
    if auto_type == "Мура":
        return {
            "A": "000",  # Вихід y1y2y3 для стану A
            "B": "100",
            "C": "010",
            "D": "001"
        }
    elif auto_type == "Мілі":
        return {
            "A": "-",
            "B": "-",
            "C": "-",
            "D": "-"
        }

# === Словник ребер ===
def define_transitions(auto_type: str):
    if auto_type == "Мура":
        return {
            ("A", "B"): ([], ["00"]),
            ("B", "C"): ([], ["01"]),
            ("C", "A"): ([], ["00", "01"])
        }
    elif auto_type == "Мілі":
        return {
            ("A", "B"): (["100"], ["00"]),
            ("B", "C"): (["010"], ["01"]),
            ("C", "A"): (["001"], ["00", "01"])
        }

# === Генерація структурної таблиці ===
def generate_transition_table(auto_type, trigger_type):
    states = define_states(auto_type)
    transitions = define_transitions(auto_type)

    rows = []

    for (src, dst), (y_list, x_list) in transitions.items():
        src_code = state_encoding[src]
        dst_code = state_encoding[dst]

        for x in x_list:
            if auto_type == "Мура":
                y_output = states[dst]
            else:
                y_output = y_list[0] if y_list else "-"

            # T-тригери: T_i = 1, якщо біт i змінюється
            T = [str(int(src_code[i] != dst_code[i])) for i in range(len(src_code))]

            row = {
                "Z^t": src_code,
                "X1X2": x,
                "Z^(t+1)": dst_code,
                "Y1Y2Y3": y_output,
                "T1": T[0],
                "T2": T[1]
            }
            rows.append(row)

    return pd.DataFrame(rows)

# === Побудова таблиці ===
df = generate_transition_table(auto_type, trigger_type)
print(df.to_string(index=False))
