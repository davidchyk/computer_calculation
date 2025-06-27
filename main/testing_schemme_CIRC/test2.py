#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logisim_builder_logicparse.py
=============================
Builds a Logisim-evolution *.circ* file from a Boolean expression.
Layout comes from **schemdraw.logicparse**: inputs at the left, output at the
right, orthogonal (Manhattan) wiring.  No GUI dependencies.

Requirements
------------
* Python ≥ 3.10
* schemdraw ≥ 0.20   →  ``pip install schemdraw``

Usage
-----
```bash
python logisim_builder_logicparse.py "(A & B) | ~C" -o demo.circ
```
"""

from __future__ import annotations

import argparse
import re
import sys
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Iterable, List, Tuple
from xml.dom import minidom

try:
    from schemdraw.parsing import logicparse as _logicparse
except ImportError as exc:  # pragma: no cover
    sys.stderr.write("✘ Please install 'schemdraw' ≥ 0.20  (pip install schemdraw)\n")
    raise SystemExit(1) from exc

# ───────────────────────────── 1. Internal AST ──────────────────────
@dataclass
class Node:
    type: str                                 # VAR / NOT / AND / OR
    children: List["Node"] = field(default_factory=list)
    varname: str | None = None                # label for VAR; can be None for temp pins
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8], init=False)
    x: int = 0                                # Logisim-pixel coordinates
    y: int = 0

# ───────────────────────────── 2. Lexer / Parser ────────────────────
_TOKEN_RE = re.compile(r"not|\(|\)|\&\&?|\|\|?|[A-Za-z]\w*")
_LITERAL = r"[A-Za-z]\w*"


def _tokenize(expr: str) -> List[str]:
    expr = (
        expr.replace("∧", "&")
        .replace("∨", "|")
        .replace("¬", "not")
        .replace("~", "not")
    )
    return _TOKEN_RE.findall(expr)


def _parse_expr(tokens: List[str]) -> Node:
    """Recursive-descent parser for &, |, not with parentheses."""

    def parse_or(i: int):
        node, i = parse_and(i)
        while i < len(tokens) and tokens[i] == "|":
            i += 1
            rhs, i = parse_and(i)
            node = Node("OR", [node, rhs])
        return node, i

    def parse_and(i: int):
        node, i = parse_not(i)
        children = [node]
        while i < len(tokens) and tokens[i] == "&":
            i += 1
            nxt, i = parse_not(i)
            children.append(nxt)
        return (Node("AND", children) if len(children) > 1 else children[0]), i

    def parse_not(i: int):
        if tokens[i] == "not":
            i += 1
            child, i = parse_atom(i)
            return Node("NOT", [child]), i
        return parse_atom(i)

    def parse_atom(i: int):
        t = tokens[i]
        if t == "(":
            i += 1
            node, i = parse_or(i)
            if i >= len(tokens) or tokens[i] != ")":
                raise ValueError("Missing ')' in expression")
            return node, i + 1
        if re.fullmatch(_LITERAL, t):
            return Node("VAR", varname=t), i + 1
        raise ValueError(f"Invalid token: {t}")

    root, pos = parse_or(0)
    if pos != len(tokens):
        raise ValueError("Extra tokens at the end of expression")
    return root

# ───────────────────────────── 3. Helpers ───────────────────────────
SCALE = 40  # inch → pixel
GATE_NAME = {"NOT": "NOT Gate", "AND": "AND Gate", "OR": "OR Gate"}


def _manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]:
    (x1, y1), (x2, y2) = a, b
    if x1 == x2 or y1 == y2:
        yield (a, b)
    else:
        yield ((x1, y1), (x2, y1))
        yield ((x2, y1), (x2, y2))

# ───────────────────────────── 4. .circ builder ─────────────────────

def build_circ(expr: str, outfile: str = "output.circ") -> None:
    """Convert *expr* to a Logisim-evolution circuit file and save to *outfile*."""
    root = _parse_expr(_tokenize(expr))  # own AST for parent-child wiring

    drawing = _logicparse(expr, outlabel="OUT")  # schemdraw layout
    drawing.draw(show=False)

    sd_elems = [
        el for el in drawing.elements if el.__class__.__name__ in {"Input", "And", "Or", "Not"}
    ]

    # preorder traversal of our AST
    nodes: List[Node] = []

    def _walk(n: Node):
        nodes.append(n)
        for c in n.children:
            _walk(c)

    _walk(root)
    if len(nodes) != len(sd_elems):
        raise RuntimeError("Element count mismatch between AST and schemdraw layout")

    # coordinates (centre of bbox)
    for n, el in zip(nodes, sd_elems):
        xmin, ymin, xmax, ymax = el.get_bbox(transform=True)
        n.x = int(((xmin + xmax) / 2) * SCALE)
        n.y = int(((ymin + ymax) / 2) * SCALE)

    # OUT pin one half-inch to the right of diagram
    out_pin = Node("VAR", varname="OUT")
    out_pin.x = int((drawing.width + 0.5) * SCALE)
    out_pin.y = nodes[0].y

    # ─── XML skeleton ───
    proj = ET.Element("project", {"source": "2.7.1", "version": "1.0"})
    proj.text = "\nThis file is intended to be loaded by Logisim (http://www.cburch.com/logisim/).\n"
    for lid, desc in [("0", "#Wiring"), ("1", "#Gates"), ("6", "#Base")]:
        ET.SubElement(proj, "lib", {"name": lid, "desc": desc})
    ET.SubElement(proj, "main", {"name": "main"})
    circ = ET.SubElement(proj, "circuit", {"name": "main"})

    # ─── wires ───
    def _connect(child: Node, parent: Node):
        for (x1, y1), (x2, y2) in _manhattan((child.x, child.y), (parent.x, parent.y)):
            ET.SubElement(circ, "wire", {"from": f"({x1},{y1})", "to": f"({x2},{y2})"})

    for p in nodes:
        for ch in p.children:
            _connect(ch, p)
    _connect(nodes[0], out_pin)  # root gate → OUT pin

    # ─── components ───
    for n in (*nodes, out_pin):
        lib = "0" if n.type == "VAR" else "1"
        comp = ET.SubElement(circ, "comp", {
            "lib": lib,
            "name": "Pin" if n.type == "VAR" else GATE_NAME[n.type],
            "loc": f"({n.x},{n.y})",
        })
        if n.type == "VAR":
            comp.append(ET.Element("a", {"name": "label", "val": n.varname or ""}))
            comp.append(ET.Element("a", {"name": "tristate", "val": "false"}))
            if n is out_pin:
                for k, v in [("output", "true"), ("facing", "west"), ("labelloc", "east")]:
                    comp.append(ET.Element("a", {"name": k, "val": v}))
        elif n.type in ("AND", "OR"):
            comp.append(ET.Element("a", {"name": "inputs", "val": str(len(n.children))}))

    # ─── write file ───
    xml_raw = ET.tostring(proj, encoding="utf-8")
    pretty = minidom.parseString(xml_raw).toprettyxml(indent="  ")
    pretty = "\n".join(pretty.split("\n")[1:])  # drop xml header inserted by minidom
    with open(outfile, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n")
        fh.write(pretty)
    print(f"✓ {outfile} сформовано (ортогональні дроти, вихід – OUT)")

# ───────────────────────────── 5. CLI wrapper ───────────────────────

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Boolean expression → Logisim .circ (schemdraw layout)"
    )
    parser.add_argument(
        "expr",
        help="Boolean expression (use &, |, ~ or ∧, ∨, ¬; parentheses allowed)",
    )
    parser.add_argument("-o", "--output", default="output.circ", help="Output .circ filename")
    args = parser.parse_args()
    build_circ(args.expr, args.output)


if __name__ == "__main__":
    _cli()