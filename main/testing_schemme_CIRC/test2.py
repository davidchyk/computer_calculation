#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tidy_logisim.py
  1. Парсить логічний вираз із  not, ∧, ∨  (N-арні AND/OR підтримуються автоматично)
  2. Розташовує дерево за алгоритмом Reingold–Tilford (tidy tree)
  3. Показує результат у Tk-вікні + генерує  example.circ
"""

# Нехай комбінаційна схема буде будуватись за рівнями вертикальними (перший рівень вхідні дані, другий-k рівень рівень внутрішньої визначеності, k+1-n-рівень --- зовнішної)

from __future__ import annotations
import re, uuid, xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import tkinter as tk


# ─────────────────────────────────────── 1. Node: поле level
@dataclass
class Node:
    type: str
    children: List['Node'] = field(default_factory=list)
    varname: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8], init=False)
    # ↓ tidy-layout залишаємо, раптом знадобиться
    prelim: float = 0.0
    modifier: float = 0.0
    depth: int = 0
    level: int = 0          # ← НОВЕ поле
    x: int = 0
    y: int = 0


# ────────────────────────────────────────── 2. Лексер
def tokenize(expr: str) -> List[str]:
    expr = expr.replace('∧', '&').replace('∨', '|')
    return re.findall(r'not|\(|\)|\&|\||[A-Za-z]\w*', expr)


# ────────────────────────────────────────── 3. Рекурсивний парсер
def parse_expr(tok: List[str]) -> Node:
    def parse_or(i):       # ... | ...
        node, i = parse_and(i)
        while i < len(tok) and tok[i] == '|':
            i += 1
            rhs, i = parse_and(i)
            node = Node('OR', [node, rhs])
        return node, i

    def parse_and(i):      # ... & ...
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
        raise ValueError(f"Неприпустимий токен: {t}")

    root, pos = parse_or(0)
    if pos != len(tok):
        raise ValueError("Зайві токени у виразі")
    return root


# ────────────────────────────────────────── 4. Tidy-алгоритм (Reingold–Tilford)
def first_walk(v: Node, depth: int = 0, sibling_sep: float = 1.0) -> None:
    v.depth = depth
    if not v.children:               # лист
        v.prelim = 0.0
        return

    for c in v.children:
        first_walk(c, depth + 1, sibling_sep)

    # центр батька над дітьми
    mid = (v.children[0].prelim + v.children[-1].prelim) / 2
    v.prelim = mid

    # виправити перекриття
    shift = 0.0
    for i in range(1, len(v.children)):
        left = v.children[i - 1]
        right = v.children[i]
        while left_subtree_right(left) + sibling_sep > right_subtree_left(right):
            d = (left_subtree_right(left) + sibling_sep) - right_subtree_left(right)
            move_subtree(right, d)
            shift += d

    if shift:
        mid = (v.children[0].prelim + v.children[-1].prelim) / 2
        v.prelim = mid


def left_subtree_right(v: Node) -> float:
    if not v.children:
        return v.prelim
    return v.children[-1].prelim + v.children[-1].modifier


def right_subtree_left(v: Node) -> float:
    if not v.children:
        return v.prelim
    return v.children[0].prelim + v.children[0].modifier


def move_subtree(v: Node, shift: float) -> None:
    v.prelim += shift
    v.modifier += shift


def second_walk(v: Node, m: float = 0.0,
                dx: int = 120, dy: int = 80,
                ox: int = 20,  oy: int = 20) -> None:
    v.x = int((v.prelim + m) * dx + ox)
    v.y = v.depth * dy + oy
    for c in v.children:
        second_walk(c, m + v.modifier, dx, dy, ox, oy)


def tidy_layout(root: Node,
                dx: int = 120, dy: int = 80,
                ox: int = 20,  oy: int = 20) -> None:
    first_walk(root)
    second_walk(root, dx=dx, dy=dy, ox=ox, oy=oy)


# ────────────────────────────────────────── 5. Допоміжне
def walk(root: Node) -> List[Node]:
    stack, out = [root], []
    while stack:
        n = stack.pop()
        out.append(n)
        stack.extend(reversed(n.children))    # порядок неважливий
    return out


# ────────────────────────────────────────── 6. Tk-вікно
class TreeGUI(tk.Tk):
    def __init__(self, root_node: Node):
        super().__init__()
        self.title("Tidy parse tree")
        canvas = tk.Canvas(self, bg="white", scrollregion=(0, 0, 3000, 3000))
        sbx = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        sby = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        canvas.config(xscrollcommand=sbx.set, yscrollcommand=sby.set)
        sbx.pack(side=tk.BOTTOM, fill=tk.X)
        sby.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        r = 20
        for n in walk(root_node):
            canvas.create_oval(n.x - r, n.y - r, n.x + r, n.y + r,
                               fill="#e0f0ff", outline="#000")
            txt = n.varname if n.type == 'VAR' else n.type
            canvas.create_text(n.x, n.y, text=txt, font=("TkDefaultFont", 9))
            for ch in n.children:
                canvas.create_line(n.x, n.y + r, ch.x, ch.y - r,
                                   arrow=tk.LAST)

        self.update_idletasks()
        w, h = canvas.bbox("all")[2:4]
        self.geometry(f"{min(800, w + 40)}x{min(600, h + 40)}")

# ────────────────────────────────────────── 7. .circ-файл
def gate_name(n: Node) -> str:
    return {'NOT': 'NOT Gate', 'AND': 'AND Gate', 'OR': 'OR Gate'}[n.type]

def generate_circ(root: Node, filename="example2.circ") -> None:
    proj = ET.Element('project', {'source': '2.7.1', 'version': '1.0'})
    proj.text = ("\nThis file is intended to be loaded by Logisim "
                 "(http://www.cburch.com/logisim/).\n")
    for n, d in [('0', '#Wiring'), ('1', '#Gates')]:
        ET.SubElement(proj, 'lib', {'name': n, 'desc': d})
    ET.SubElement(proj, 'main', {'name': 'main'})
    circ = ET.SubElement(proj, 'circuit', {'name': 'main'})

    nodes = walk(root)

    # wires: спершу вертикальні, потім горизонтальні
    def add_wire(a: Tuple[int, int], b: Tuple[int, int]):
        ET.SubElement(circ, 'wire',
                      {'from': f'({a[0]},{a[1]})', 'to': f'({b[0]},{b[1]})'})

    # дроти: горизонталь → вертикаль → коротка горизонталь
    for p in nodes:
        for ch in p.children:
            add_wire((p.x + 20, p.y), (ch.x - 20, p.y))   # →
            add_wire((ch.x - 20, p.y), (ch.x - 20, ch.y)) # ↓ / ↑
            add_wire((ch.x - 20, ch.y), (ch.x,     ch.y)) # →

    # компоненти
    for n in nodes:
        lib = '0' if n.type == 'VAR' else '1'
        comp = ET.SubElement(circ, 'comp',
            {'lib': lib,
             'name': 'Pin' if n.type == 'VAR' else gate_name(n),
             'loc': f'({n.x},{n.y})'})
        if n.type == 'VAR':
            ET.SubElement(comp, 'a', {'name': 'label', 'val': n.varname or ''})
            ET.SubElement(comp, 'a', {'name': 'tristate', 'val': 'false'})
        elif n.type in ('AND', 'OR'):
            ET.SubElement(comp, 'a', {'name': 'inputs',
                                       'val': str(len(n.children))})

    xml = minidom.parseString(ET.tostring(proj, 'utf-8'))\
                 .toprettyxml(indent='  ')
    xml = '\n'.join(xml.split('\n')[1:])
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write(xml)
    print("✓ example.circ сформовано (координати — tidy layout)")

def compute_depths(n: Node) -> int:
    if n.type == 'VAR':          # лист (x1, x2, …)
        n.depth = 0
        return 0
    # глибина = 1 + максимальна глибина серед дітей
    n.depth = max(compute_depths(c) for c in n.children) + 1
    return n.depth

# ─────────────────────────────────────── 2. Рівні від входів до виходу
def assign_levels(root: Node) -> None:
    """Записує у n.level номер колонки, рахуючи від входів (0)"""
    def dfs(v: Node) -> int:
        if v.type == 'VAR':
            v.level = 0
            return 0
        v.level = max(dfs(ch) for ch in v.children) + 1
        return v.level
    dfs(root)

# ─────────────────────────────────────── 3. Вертикальні колонки (layout)
def vertical_layer_layout(root: Node,
                          dx: int = 160,  # крок між колонками
                          dy: int = 80,   # крок між елементами у колонці
                          ox: int = 40,   # відступ ліворуч
                          oy: int = 40) -> None:
    """x = колонка (level), y = позиція всередині колонки"""
    assign_levels(root)

    # ¹ стабільний обхід, щоб порядок у колонці відповідав порядку у виразі
    levels: dict[int, list[Node]] = {}
    for n in walk(root):                     # walk з твого коду
        levels.setdefault(n.level, []).append(n)

    for lvl, nodes in levels.items():
        for idx, n in enumerate(nodes):
            n.x = ox + lvl * dx
            n.y = oy + idx * dy

# ────────────────────────────────────────── 8. Демо-запуск
if __name__ == "__main__":
    expr = "(X3 ∧ X2) ∨ X1"           # ← твій приклад
    ast  = parse_expr(tokenize(expr))
    vertical_layer_layout(ast)        # ← ось він, новий макет
    generate_circ(ast)                # example_layered.circ
    TreeGUI(ast).mainloop()    