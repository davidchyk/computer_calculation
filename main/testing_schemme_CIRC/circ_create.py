#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logisim_builder_logicparse.py
=============================
Builds a Logisim‑evolution *.circ* file from a Boolean expression.
Layout is taken from **schemdraw.logicparse**, so inputs appear at the
left, output at the right, and all wiring is Manhattan‑orthogonal.

Requirements
------------
* Python ≥ 3.10
* schemdraw ≥ 0.20  →  ``pip install schemdraw``

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
from typing import List, Tuple
from xml.dom import minidom

try:
    from schemdraw.parsing.logic_parser import logicparse as _logicparse
except ImportError:  # pragma: no cover
    sys.stderr.write("✘ This script needs the 'schemdraw' package.  pip install schemdraw\n")
    sys.exit(1)

# ─────────────────────────────── 1. Internal AST (keeps hierarchy) ──
@dataclass
class Node:
    type: str                      # VAR / NOT / AND / OR
    children: List["Node"] = field(default_factory=list)
    varname: str | None = None     # only for VAR
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8], init=False)
    x: int = 0                     # Logisim‑pixel coordinates
    y: int = 0

# ─────────────────────────────── 2. Lexer & Recursive‑descent parser ──
_TOKEN_RE = re.compile(r"not|\(|\)|\&|\||[A-Za-z]\w*")
_LITERAL  = r"[A-Za-z]\w*"


def _tokenize(expr: str) -> List[str]:
    expr = (
        expr.replace("∧", "&")
        .replace("∨", "|")
        .replace("¬", "not")
        .replace("~", "not")
    )
    return _TOKEN_RE.findall(expr)


def _parse_expr(tokens: List[str]) -> Node:
    def parse_or(i):
        n, i = parse_and(i)
        while i < len(tokens) and tokens[i] == "|":
            i += 1
            r, i = parse_and(i)
            n = Node("OR", [n, r])
        return n, i

    def parse_and(i):
        n, i = parse_not(i)
        kids = [n]
        while i < len(tokens) and tokens[i] == "&":
            i += 1
            nxt, i = parse_not(i)
            kids.append(nxt)
        return (Node("AND", kids) if len(kids) > 1 else kids[0]), i

    def parse_not(i):
        if tokens[i] == "not":
            i += 1
            ch, i = parse_atom(i)
            return Node("NOT", [ch]), i
        return parse_atom(i)

    def parse_atom(i):
        t = tokens[i]
        if t == "(":
            i += 1
            n, i = parse_or(i)
            if i >= len(tokens) or tokens[i] != ")":
                raise ValueError("Missing ')' in expression")
            return n, i + 1
        if re.fullmatch(_LITERAL, t):
            return Node("VAR", varname=t), i + 1
        raise ValueError(f"Invalid token: {t}")

    root, pos = parse_or(0)
    if pos != len(tokens):
        raise ValueError("Extra tokens after parsing expression")
    return root

# ─────────────────────────────── 3. Helpers ──────────────────────────
SCALE = 40  # inch → pixel conversion
GATE_NAME = {"NOT": "NOT Gate", "AND": "AND Gate", "OR": "OR Gate"}


def _manhattan(a: Tuple[int, int], b: Tuple[int, int]):
    (x1, y1), (x2, y2) = a, b
    if x1 == x2 or y1 == y2:
        yield (x1, y1), (x2, y2)
    else:
        yield (x1, y1), (x2, y1)
        yield (x2, y1), (x2, y2)

# ─────────────────────────────── 4. .circ Builder ────────────────────

def build_circ(expr: str, outfile: str = "output.circ") -> None:
    """Convert *expr* to a Logisim‑evolution circuit file."""
    # 1. Parse into own AST for connectivity
    root = _parse_expr(_tokenize(expr))

    # 2. Obtain layout from schemdraw.logicparse
    drawing = _logicparse(expr, outlabel="OUT")
    drawing.draw(show=False)

    # Take only logic elements & inputs (schemdraw order = preorder)
    sd_elems = [
        el for el in drawing.elements if el.__class__.__name__ in {"Input", "And", "Or", "Not"}
    ]

    # 3. Gather AST nodes in preorder to align with sd_elems
    nodes: List[Node] = []

    def _collect(n: Node):
        nodes.append(n)
        for c in n.children:
            _collect(c)

    _collect(root)
    if len(nodes) != len(sd_elems):
        raise RuntimeError("Mismatch between AST nodes and schemdraw elements")

    # 4. Copy coordinates (centre of bbox) & scale
    for n, el in zip(nodes, sd_elems):
        xmin, ymin, xmax, ymax = el.get_bbox(transform=True)
        n.x = int(((xmin + xmax) / 2) * SCALE)
        n.y = int(((ymin + ymax) / 2) * SCALE)

    # 5. Create OUT pin just beyond rightmost element
    out_pin = Node("VAR", varname="OUT")
    out_pin.x = int((drawing.width + 0.5) * SCALE)
    out_pin.y = nodes[0].y

    # ───── XML skeleton
    proj = ET.Element("project", {"source": "2.7.1", "version": "1.0"})
    proj.text = "\nThis file is intended to be loaded by Logisim (http://www.cburch.com/logisim/).\n"
    for lid, desc in [("0", "#Wiring"), ("1", "#Gates"), ("6", "#Base")]:
        ET.SubElement(proj, "lib", {"name": lid, "desc": desc})
    ET.SubElement(proj, "main", {"name": "main"})
    circ = ET.SubElement(proj, "circuit", {"name": "main"})

    # ───── Wires
    def _connect(src: Node, dst: Node):
        for seg in _manhattan((src.x, src.y), (dst.x, dst.y)):
            ET.SubElement(
                circ,
                "wire",
                {"from": f"({seg[0][0]},{seg[0][1]})", "to": f"({seg[1][0]},{seg[1][1]})"},
            )

    for parent in nodes:
        for child in parent.children:
            _connect(child, parent)
    _connect(nodes[0], out_pin)  # root → OUT

    # ───── Components
    for n in nodes + [out_pin]:
        lib = "0" if n.type == "VAR" else "1"
        comp = ET.SubElement(
            circ,
            "comp",
            {
                "lib": lib,
                "name": "Pin" if n.type == "VAR" else GATE_NAME[n.type],
                "loc": f"({n.x},{n.y})",
            },
        )
        if n.type == "VAR":
            comp.append(ET.Element("a", {"name": "label", "val": n.varname or ""}))
            comp.append(ET.Element("a", {"name": "tristate", "val": "false"}))
            if n is out_pin:
                for k, v in [("output", "true"), ("facing", "west"), ("labelloc", "east")]:
                    comp.append(ET.Element("a", {"name": k, "val": v}))
        elif n.type in ("AND", "OR"):
            comp.append(ET.Element("a", {"name": "inputs", "val": str(len(n.children))}))

    # ───── Pretty‑print & save
    xml_raw = ET.tostring(proj, "utf-8")
    pretty = minidom.parseString(xml_raw).toprettyxml(indent="  ")
    pretty = "\n".join(pretty.split("\n")[1:])  # strip XML decl.
    with open(outfile, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write(pretty)
    print(f"✓ {outfile} сформовано (ортогональні дроти, вихід – OUT)")

# ─────────────────────────────── 5. CLI wrapper ─────────────────────

def _cli():
    p = argparse.ArgumentParser(description="Boolean expression → Logisim .circ via schemdraw logicparse")
    p.add_argument("expr", help="Boolean expression in C‑style syntax (use &, |, ~ or ∧, ∨, ¬)"),
    p.add_argument("-o", "--output", default="output.circ", help="Output .circ filename")
    args = p.parse_args()
    build_circ(args.expr, args.output)


if __name__ == "__main__":
    _cli()
