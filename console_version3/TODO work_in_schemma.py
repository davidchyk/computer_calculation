from schemdraw.parsing import logicparse

exp = "(~(X_4) & ~(X3) & ~(X2) & X1)"

g = "not (not (not(not X_3 and not X_2)) or X_1)"

g = "(not(not X_3 and not X_2) or X1)"

def convert_symbols(user_input):

    print(F"processing {user_input}")

    #Замінює символи ∨, ∧, not на відповідні &, |, ~.

    converted_input = (
        user_input.replace("∧", "&")
        .replace("∨", "|")
        .replace("not", "~")
        .replace("_", "")
    )

    return converted_input


d = logicparse(g, gateH=10, gateW=10, outlabel=r"$y_1$")
d.draw()