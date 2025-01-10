t = "not(not(not(not(not(not(X_3)) ∧ not(not(X_2 ∧ X_1))) ∧ not(not(not(not(X_3))) ∧ not(not(not(X_2) ∧ X_1))))) ∧ not(not(not(not(X_4) ∧ X_3)) ∧ not(not(not(X_2) ∧ not(X_1)))))"

from schemdraw.parsing import logicparse

def convert_symbols(user_input):

    #Замінює символи ∨, ∧, not на відповідні &, |, ~.

    converted_input = (
        user_input.replace("∧", "&")
        .replace("∨", "|")
        .replace("not", "~")
        .replace("_", "")
    )

    return converted_input

print(convert_symbols(t))

d = logicparse(convert_symbols(t), outlabel=rf'$Y_1$')
d.draw(r'schemma3.png')