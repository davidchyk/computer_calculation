import xml.etree.ElementTree as ET

def generate_circ(logic_function: str, output_file: str):
    # 1. Розбір функції (проста інтерпретація AND, OR, NOT, тощо)
    inputs = sorted(set(c for c in logic_function if c.isalpha() and c.islower()))  # Вхідні змінні
    operations = []
    stack = []
    
    for token in logic_function.split():
        if token in {'AND', 'OR', 'NOT'}:
            operations.append(token)
        elif token.isalpha():
            stack.append(token)

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
        input_pins[var] = (x + 20, y)  # Збереження координат виходу контакту
        y += 50

    # 2.2 Компоненти операцій
    operation_comps = []
    x, y = 200, 50  # Початкові координати для операцій
    for op in operations:
        gate_name = op.title() + " Gate"
        comp = ET.SubElement(main_circuit, 'comp', lib="1", loc=f"({x},{y})", name=gate_name)
        operation_comps.append((op, (x + 20, y)))  # Збереження координат
        y += 50

    # 2.3 Провідники (wire)
    for inp, (to_x, to_y) in input_pins.items():
        ET.SubElement(main_circuit, 'wire', from_=f"({to_x},{to_y})", to=f"({to_x + 40},{to_y})")

    # 3. Збереження у файл
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Приклад виклику функції
generate_circ("a AND b OR c", "output.circ")