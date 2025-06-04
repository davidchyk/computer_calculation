import xml.etree.ElementTree as ET

def generate_circ(logic_function: str, output_file: str):
    # 1. Розбір функції (проста інтерпретація AND, OR, NOT, тощо)
    inputs = sorted(set(c for c in logic_function if c.isalpha() and c.islower()))  # Вхідні змінні
    operations = []

    tokens = logic_function.split()
    for i, token in enumerate(tokens):
        if token in {'AND', 'OR', 'NOT'}:
            operations.append((token, i))

    # 2. XML структура
    root = ET.Element('project', source="2.7.1", version="1.0")
    root.text = "This file is intended to be loaded by Logisim (http://www.cburch.com/logisim/)."

    # Бібліотеки
    libraries = [
        ("#Wiring", "0"),
        ("#Gates", "1"),
        ("#Plexers", "2"),
        ("#Arithmetic", "3"),
        ("#Memory", "4"),
        ("#I/O", "5"),
        ("#Base", "6")
    ]
    for desc, name in libraries:
        ET.SubElement(root, 'lib', desc=desc, name=name)

    # Головна схема
    main_circuit = ET.SubElement(root, 'circuit', name="main")
    ET.SubElement(main_circuit, 'a', name="circuit", val="main")

    # 2.1 Вхідні контакти
    input_pins = {}
    x, y = 100, 50  # Початкові координати для входів
    for i, var in enumerate(inputs):
        comp = ET.SubElement(main_circuit, 'comp', lib="0", loc=f"({x},{y})", name="Pin")
        ET.SubElement(comp, 'a', name="tristate", val="false")
        ET.SubElement(comp, 'a', name="label", val=var)
        input_pins[var] = (x, y)
        y += 50

    # 2.2 Компоненти операцій
    operation_comps = []
    x, y = 200, 50  # Початкові координати для операцій
    output_pins = []
    for op, idx in operations:
        gate_name = op.title() + " Gate"
        comp = ET.SubElement(main_circuit, 'comp', lib="1", loc=f"({x},{y})", name=gate_name)

        # Отримання входів операцій
        input1 = input_pins.get(tokens[idx - 2], None)
        input2 = input_pins.get(tokens[idx - 1], None)

        # Підключення дротів
        if input1:
            ET.SubElement(main_circuit, 'wire', from_=f"({input1[0]},{input1[1]})", to=f"({x - 20},{y})")
        if input2:
            ET.SubElement(main_circuit, 'wire', from_=f"({input2[0]},{input2[1]})", to=f"({x - 20},{y})")

        ET.SubElement(main_circuit, 'wire', from_=f"({x - 20},{y})", to=f"({x},{y})")

        operation_comps.append((op, (x, y)))
        output_pins.append((x, y))
        x += 100

    # 2.3 Вихідний контакт
    if output_pins:
        y += 50
        comp = ET.SubElement(main_circuit, 'comp', lib="0", loc=f"({x},{y})", name="Pin")
        ET.SubElement(comp, 'a', name="facing", val="west")
        ET.SubElement(comp, 'a', name="output", val="true")
        ET.SubElement(comp, 'a', name="label", val="Y")
        ET.SubElement(main_circuit, 'wire', from_=f"({output_pins[-1][0]},{output_pins[-1][1]})", to=f"({x},{y})")

    # 3. Збереження у файл
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Приклад виклику функції
generate_circ("a AND b OR c", "output3.circ")
