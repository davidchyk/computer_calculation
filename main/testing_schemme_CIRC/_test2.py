#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logisim_builder.py
Булевий вираз → .circ (видимий у верхньому-лівому куті, з toolbar).
"""

from __future__ import annotations
import re, uuid, xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple

# ───────────────────────── 1. Вузол дерева
@dataclass
class Node:
    type: str                               # VAR / NOT / AND / OR
    children: List['Node'] = field(default_factory=list)
    varname: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8], init=False)
    depth: int = 0
    x: int = 0
    y: int = 0

# ───────────────────────── 2. Лексер
def tokenize(expr: str) -> List[str]:
    expr = expr.replace('∧', '&').replace('∨', '|')
    return re.findall(r'not|\(|\)|\&|\||[A-Za-z]\w*', expr)

# ───────────────────────── 3. Парсер
def parse_expr(tok: List[str]) -> Node:
    def parse_or(i):
        node, i = parse_and(i)
        while i < len(tok) and tok[i] == '|':
            i += 1; rhs, i = parse_and(i)
            node = Node('OR', [node, rhs])
        return node, i
    def parse_and(i):
        node, i = parse_not(i)
        kids = [node]
        while i < len(tok) and tok[i] == '&':
            i += 1; nxt, i = parse_not(i); kids.append(nxt)
        return (Node('AND', kids) if len(kids) > 1 else kids[0]), i
    def parse_not(i):
        if tok[i] == 'not':
            i += 1; child, i = parse_atom(i)
            return Node('NOT', [child]), i
        return parse_atom(i)
    def parse_atom(i):
        t = tok[i]
        if t == '(':
            i += 1; node, i = parse_or(i)
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

# ───────────────────────── 4. Глибини / координати
def compute_depths(n: Node) -> int:
    if n.type == 'VAR':
        n.depth = 0; return 0
    n.depth = max(compute_depths(c) for c in n.children) + 1
    return n.depth

def assign_coords(root: Node,
                  dx: int = 180, dy: int = 100,
                  ox: int = 20, oy: int = 20) -> None:
    levels: Dict[int, List[Node]] = {}
    def collect(v):
        levels.setdefault(v.depth, []).append(v)
        for c in v.children: collect(c)
    collect(root)
    for depth, row in levels.items():
        for idx, n in enumerate(row):
            n.x = ox + depth * dx
            n.y = oy + idx * dy

# ───────────────────────── 5. Утиліти
def walk(root: Node) -> List[Node]:
    stack, out = [root], []
    while stack:
        n = stack.pop(); out.append(n); stack.extend(n.children)
    return out

def manhattan(a: Tuple[int,int], b: Tuple[int,int]) \
        -> List[Tuple[Tuple[int,int], Tuple[int,int]]]:
    (x1,y1),(x2,y2) = a,b
    if x1==x2 or y1==y2:
        return [((x1,y1),(x2,y2))]
    return [((x1,y1),(x1,y2)), ((x1,y2),(x2,y2))]   # V → H

def unique_out_label(used: Set[str], base="OUT") -> str:
    if base not in used: return base
    i = 1
    while f"{base}{i}" in used: i += 1
    return f"{base}{i}"

def gate_name(n: Node) -> str:
    return {'NOT':'NOT Gate','AND':'AND Gate','OR':'OR Gate'}[n.type]

# ───────────────────────── 6. Генерація .circ
def build_circ(root: Node, filename: str) -> None:
    used = {n.varname for n in walk(root) if n.type == 'VAR'}
    out_lbl = unique_out_label(used)

    proj = ET.Element('project', {'source':'2.7.1','version':'1.0'})
    proj.text = ("\nThis file is intended to be loaded by Logisim "
                 "(http://www.cburch.com/logisim/).\n")
    for n,d in [('0','#Wiring'),('1','#Gates'),('6','#Base')]:
        ET.SubElement(proj,'lib',{'name':n,'desc':d})

    # options / mappings / toolbar — як у «робочому» зразку
    opts = ET.SubElement(proj,'options')
    for k,v in [('gateUndefined','ignore'),('simlimit','1000'),('simrand','0')]:
        ET.SubElement(opts,'a',{'name':k,'val':v})

    maps = ET.SubElement(proj,'mappings')
    for b in ['Button2','Button3','Ctrl Button1']:
        ET.SubElement(maps,'tool',{'lib':'6','map':b,'name':'Menu Tool'})

    tb = ET.SubElement(proj,'toolbar')
    for t in ['Poke Tool','Edit Tool','Text Tool']:
        tool = ET.SubElement(tb,'tool',{'lib':'6','name':t})
        if t=='Text Tool':
            for k,v in [('text',''),('font','SansSerif plain 12'),
                        ('halign','center'),('valign','base')]:
                tool.append(ET.Element('a',{'name':k,'val':v}))
    ET.SubElement(tb,'sep')
    pin_in  = ET.SubElement(tb,'tool',{'lib':'0','name':'Pin'})
    pin_in.append(ET.Element('a',{'name':'tristate','val':'false'}))
    pin_out = ET.SubElement(tb,'tool',{'lib':'0','name':'Pin'})
    for k,v in [('facing','west'),('output','true'),('labelloc','east')]:
        pin_out.append(ET.Element('a',{'name':k,'val':v}))
    for g in ['NOT Gate','AND Gate','OR Gate']:
        ET.SubElement(tb,'tool',{'lib':'1','name':g})

    ET.SubElement(proj,'main',{'name':'main'})
    circ = ET.SubElement(proj,'circuit',{'name':'main'})
    for k,v in [('circuit','main'),('clabel',''),
                ('clabelup','east'),('clabelfont','SansSerif plain 12')]:
        circ.append(ET.Element('a',{'name':k,'val':v}))

    nodes = walk(root)
    y_pin = Node('VAR', varname=out_lbl); y_pin.x = root.x + 180; y_pin.y = root.y
    nodes.append(y_pin)

    # wires спершу (V → H маршрути)
    for p in nodes:
        for ch in (p.children if p.type!='VAR' else []):
            for seg in manhattan((ch.x,ch.y),(p.x,p.y)):
                ET.SubElement(circ,'wire',
                    {'from':f'({seg[0][0]},{seg[0][1]})',
                     'to':  f'({seg[1][0]},{seg[1][1]})'})
    for seg in manhattan((root.x,root.y),(y_pin.x,y_pin.y)):
        ET.SubElement(circ,'wire',
            {'from':f'({seg[0][0]},{seg[0][1]})',
             'to':  f'({seg[1][0]},{seg[1][1]})'})

    # компоненти
    for n in nodes:
        lib = '0' if n.type=='VAR' else '1'
        comp = ET.SubElement(circ,'comp',
            {'lib':lib, 'name':'Pin' if n.type=='VAR' else gate_name(n),
             'loc':f'({n.x},{n.y})'})
        if n.type=='VAR':
            comp.append(ET.Element('a',{'name':'label','val':n.varname or ''}))
            comp.append(ET.Element('a',{'name':'tristate','val':'false'}))
            if n is y_pin:
                for k,v in [('output','true'),('facing','west'),('labelloc','east')]:
                    comp.append(ET.Element('a',{'name':k,'val':v}))
        elif n.type in ('AND','OR'):
            comp.append(ET.Element('a',{'name':'inputs','val':str(len(n.children))}))

    # pretty-print
    xml = minidom.parseString(ET.tostring(proj,'utf-8')).toprettyxml(indent='  ')
    xml = '\n'.join(xml.split('\n')[1:])
    with open(filename,'w',encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write(xml)
    print(f"✓ {filename} сформовано. Вихідний Pin = «{out_lbl}»")

# ───────────────────────── 7. Приклад запуску
if __name__ == '__main__':
    expr = "(X ∧ Y) ∨ not(Z)"    # підставте свій вираз
    tree = parse_expr(tokenize(expr))
    compute_depths(tree)
    assign_coords(tree)          # верх-лівий кут, крок 180×100
    build_circ(tree, 'example2.circ')
