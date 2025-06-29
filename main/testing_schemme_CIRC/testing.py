from __future__ import annotations
import re, uuid, xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple

# ────────────────────────────── 1. Вузол дерева
@dataclass
class Node:
    type: str
    children: List['Node'] = field(default_factory=list)
    varname: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8], init=False)
    depth: int = 0
    x: int = 0
    y: int = 0
    height: int = 1  # Висота піддерева (кількість "листків" для розміщення)

# ────────────────────────────── 2. Лексер
def tokenize(expr: str) -> List[str]:
    expr = expr.replace('∧', '&').replace('∨', '|')
    return re.findall(r'not|\(|\)|\&|\||[A-Za-z]\w*', expr)

# ────────────────────────────── 3. Парсер
def parse_expr(tok: List[str]) -> Node:

    def parse_or(i):
        node, i = parse_and(i)
        while i < len(tok) and tok[i] == '|':
            i += 1
            rhs, i = parse_and(i)
            node = Node('OR', [node, rhs])
        return node, i

    def parse_and(i):
        node, i = parse_not(i)
        kids = [node]
        while i < len(tok) and tok[i] == '&':
            i += 1
            nxt, i = parse_not(i)
            kids.append(nxt)
        return (Node('AND', kids) if len(kids) > 1 else kids[0]), i

    def parse_not(i):
        if tok[i] == 'not':
            i += 1
            child, i = parse_atom(i)
            return Node('NOT', [child]), i
        return parse_atom(i)

    def parse_atom(i):
        t = tok[i]
        if t == '(':
            i += 1
            node, i = parse_or(i)
            if i >= len(tok) or tok[i] != ')':
                raise ValueError("Пропущена ')'")
            return node, i + 1
        if re.fullmatch(r'[A-Za-z]\w*', t):
            return Node('VAR', varname=t), i + 1
        raise ValueError(f"Недійсний токен: {t}")

    root, pos = parse_or(0)
    if pos != len(tok):
        raise ValueError("Зайві токени у виразі")
    return root

# ────────────────────────────── 4. Глибини / координати
def compute_depths(n: Node) -> int:

    if n.type == 'VAR':
        n.depth = 0
        n.height = 1
        return 0
    n.depth = max(compute_depths(c) for c in n.children) + 1
    n.height = sum(c.height for c in n.children)  # Висота = сума висот дітей
    return n.depth

def assign_coords(root: Node, dx=200, dy=80, gate_width=60, gate_height=40):

    levels: Dict[int, List[Node]] = {}
    def collect(v):
        levels.setdefault(v.depth, []).append(v)
        for c in v.children:
            collect(c)
    collect(root)

    # Розташування по Y: враховуємо висоту піддерев
    for depth in sorted(levels.keys()):
        nodes = levels[depth]
        total_height = sum(n.height for n in nodes)
        y_offset = -total_height * dy // 2  # Центруємо по Y
        for node in nodes:
            node.x = depth * dx
            node.y = y_offset + (node.height * dy // 2)
            y_offset += node.height * dy

# ────────────────────────────── 5. Генерація .circ
def gate_name(n: Node) -> str:
    return {'NOT': 'NOT Gate', 'AND': 'AND Gate', 'OR': 'OR Gate'}[n.type]

def unique_out_label(used: Set[str], base="OUT") -> str:

    if base not in used: return base

    i = 1
    while f"{base}{i}" in used: i += 1
    return f"{base}{i}"

def manhattan_path(a: Tuple[int, int], b: Tuple[int, int], used_points: Set[Tuple[int, int]]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Генерує ортогональний маршрут, уникаючи використаних точок."""

    x1, y1 = a
    x2, y2 = b
    segments = []

    if x1 == x2 or y1 == y2: segments = [((x1, y1), (x2, y2))]
    else:
        # Спробуємо два маршрути: горизонталь+вертикаль або вертикаль+горизонталь
        mid1 = (x2, y1)  # Горизонталь до x2, потім вертикаль до y2
        mid2 = (x1, y2)  # Вертикаль до y2, потім горизонталь до x2
        path1 = [((x1, y1), mid1), (mid1, (x2, y2))]
        path2 = [((x1, y1), mid2), (mid2, (x2, y2))]

        # Вибираємо маршрут із меншою кількістю перетинів
        def count_crossings(path):
            crossings = 0
            for seg in path:
                x_start, x_end = min(seg[0][0], seg[1][0]), max(seg[0][0], seg[1][0])
                y_start, y_end = min(seg[0][1], seg[1][1]), max(seg[0][1], seg[1][1])
                for x in range(x_start, x_end + 10, 10):
                    for y in range(y_start, y_end + 10, 10):
                        if (x, y) in used_points:
                            crossings += 1
            return crossings

        segments = path1 if count_crossings(path1) <= count_crossings(path2) else path2

    # Оновлюємо використані точки
    for seg in segments:
        x_start, x_end = min(seg[0][0], seg[1][0]), max(seg[0][0], seg[1][0])
        y_start, y_end = min(seg[0][1], seg[1][1]), max(seg[0][1], seg[1][1])
        for x in range(x_start, x_end + 10, 10):
            for y in range(y_start, y_end + 10, 10):
                used_points.add((x, y))
    return segments

def build_circ(root: Node, filename: str):
    # --- Збір змінних ---
    vars_: Set[str] = set()
    def collect_vars(v):
        if v.type == 'VAR':
            vars_.add(v.varname or "")
        for c in v.children:
            collect_vars(c)
    collect_vars(root)
    out_lbl = unique_out_label(vars_)

    # --- XML каркас ---
    proj = ET.Element('project', {'source': '2.7.1', 'version': '1.0'})
    proj.text = ("\nThis file is intended to be loaded by Logisim "
                 "(http://www.cburch.com/logisim/).\n")
    for name, desc in [('0', '#Wiring'), ('1', '#Gates'), ('6', '#Base')]:
        ET.SubElement(proj, 'lib', {'name': name, 'desc': desc})

    # Налаштування options, mappings, toolbar (без змін)
    options = ET.SubElement(proj, 'options')
    for k, v in [('gateUndefined', 'ignore'), ('simlimit', '1000'), ('simrand', '0')]:
        ET.SubElement(options, 'a', {'name': k, 'val': v})
    mappings = ET.SubElement(proj, 'mappings')
    for m in ['Button2', 'Button3', 'Ctrl Button1']:
        ET.SubElement(mappings, 'tool', {'lib': '6', 'map': m, 'name': 'Menu Tool'})
    toolbar = ET.SubElement(proj, 'toolbar')
    for t in ['Poke Tool', 'Edit Tool', 'Text Tool']:
        tool = ET.SubElement(toolbar, 'tool', {'lib': '6', 'name': t})
        if t == 'Text Tool':
            for k, v in [('text', ''), ('font', 'SansSerif plain 12'), ('halign', 'center'), ('valign', 'base')]:
                tool.append(ET.Element('a', {'name': k, 'val': v}))
    ET.SubElement(toolbar, 'sep')
    pin_def = ET.SubElement(toolbar, 'tool', {'lib': '0', 'name': 'Pin'})
    pin_def.append(ET.Element('a', {'name': 'tristate', 'val': 'false'}))
    pin_out_tool = ET.SubElement(toolbar, 'tool', {'lib': '0', 'name': 'Pin'})
    for k, v in [('facing', 'west'), ('output', 'true'), ('labelloc', 'east')]:
        pin_out_tool.append(ET.Element('a', {'name': k, 'val': v}))
    for g in ['NOT Gate', 'AND Gate', 'OR Gate']:
        ET.SubElement(toolbar, 'tool', {'lib': '1', 'name': g})

    ET.SubElement(proj, 'main', {'name': 'main'})
    circ = ET.SubElement(proj, 'circuit', {'name': 'main'})
    for k, v in [('circuit', 'main'), ('clabel', ''),
                 ('clabelup', 'east'), ('clabelfont', 'SansSerif plain 12')]:
        circ.append(ET.Element('a', {'name': k, 'val': v}))

    # --- Список вузлів + вихідний Pin ---
    nodes: List[Node] = []
    def gather(v):
        nodes.append(v)
        for c in v.children:
            gather(c)
    gather(root)
    y_pin = Node('VAR', varname=out_lbl)
    y_pin.x = root.x + 200
    y_pin.y = root.y
    nodes.append(y_pin)

    # --- Відстеження використаних точок для проводів ---
    used_points: Set[Tuple[int, int]] = set()

    # --- Проводи (wires) ---
    for parent in nodes:
        if parent.type == 'VAR':
            continue
        for i, child in enumerate(parent.children):
            # Враховуємо зміщення входів для AND/OR гейтів
            y_offset = -20 * (len(parent.children) - 1) / 2 + 20 * i
            parent_input = (parent.x, parent.y + int(y_offset))
            for seg in manhattan_path((child.x, child.y), parent_input, used_points):
                ET.SubElement(circ, 'wire', {'from': f'({seg[0][0]},{seg[0][1]})',
                                             'to': f'({seg[1][0]},{seg[1][1]})'})
    # Вихід OR → OUT
    for seg in manhattan_path((root.x, root.y), (y_pin.x, y_pin.y), used_points):
        ET.SubElement(circ, 'wire', {'from': f'({seg[0][0]},{seg[0][1]})',
                                     'to': f'({seg[1][0]},{seg[1][1]})'})

    # --- Компоненти ---
    for n in nodes:
        lib = '0' if n.type == 'VAR' else '1'
        comp = ET.SubElement(circ, 'comp', {
            'lib': lib,
            'name': 'Pin' if n.type == 'VAR' else gate_name(n),
            'loc': f'({n.x},{n.y})'
        })
        if n.type == 'VAR':
            comp.append(ET.Element('a', {'name': 'label', 'val': n.varname or ''}))
            comp.append(ET.Element('a', {'name': 'tristate', 'val': 'false'}))
            if n is y_pin:
                for k, v in [('output', 'true'), ('facing', 'west'), ('labelloc', 'east')]:
                    comp.append(ET.Element('a', {'name': k, 'val': v}))
        elif n.type in ('AND', 'OR'):
            comp.append(ET.Element('a', {'name': 'inputs', 'val': str(len(n.children))}))

    # --- Запис у файл ---
    raw = ET.tostring(proj, 'utf-8')
    pretty = minidom.parseString(raw).toprettyxml(indent='  ')
    pretty = '\n'.join(pretty.split('\n')[1:])  # Прибираємо xml-декларацію
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write(pretty)
    print(f"✓ {filename} сформовано (ортогональні дроти, вихід - {out_lbl})")

if __name__ == '__main__':
    expr = "(X ∧ Y) ∨ not(Z)"
    root = parse_expr(tokenize(expr))
    compute_depths(root)
    assign_coords(root)
    build_circ(root, 'EXAMPLE.circ')