from schemdraw.parsing import logicparse
import os

def create_logic_diagrams_png(path_to_save, logic_schemme_list):

    def convert_symbols(user_input):

        #Замінює символи ∨, ∧, not на відповідні &, |, ~.

        converted_input = (
            user_input.replace("∧", "&")
            .replace("∨", "|")
            .replace("not", "~")
            .replace("_", "")
        )

        return converted_input

    #Створює блок-схему на основі логічного виразу.

    flag = False
    counter = 1

    for input_data in logic_schemme_list:

        temp = convert_symbols(input_data)

        try:

            d = logicparse(temp, outlabel=rf'$y_{counter}$', gateH=1, gateW=3)
            temp_path = os.path.join(path_to_save, f"OUTPUT_SCHEMME_Y_{counter}.png")
            d.save(temp_path)

        except Exception as e:

            print(f"Не вдалося створити блок-схему для функції y{counter}: {e}"); flag = True

        counter += 1

    if flag: return False