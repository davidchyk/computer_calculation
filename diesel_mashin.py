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
