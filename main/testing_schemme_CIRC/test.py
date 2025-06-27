from schemdraw.parsing.logic_parser import logicparse

d = logicparse('((A & B) | C) & D', outlabel='Y')
d.draw(show=True)                 # обовʼязково: обчислює геометрію

for el in d.elements:
    print(type(el).__name__)
    print('  anchors:', list(el.anchors.keys()))
    if 'out' in el.anchors:        # для воріт – точка виходу
        print('   out →', tuple(el.anchors['out']))