from schemdraw.parsing.logic_parser import logicparse
import os

def create_logic_diagrams_pdf(path_to_save, logic_schemme_list):

    for i, input_data in enumerate(logic_schemme_list, start=1):

        try:

            if input_data == "()":

                temp = "Z & Z"

            else:

                temp = (
                    input_data.replace("∧", "&")
                    .replace("∨", "|")
                    .replace("not", "~")
                    .replace("_", "")
                )

            print(f"temp is {temp}")

            d = logicparse(temp, outlabel=rf'$y_{i}$', gateH=1, gateW=3)
            temp_path = os.path.join(path_to_save, f"OUTPUT_SCHEMME_Y_{i}.pdf")
            d.save(temp_path)

        except Exception as e: print(f"Не вдалося створити блок-схему для функції y{i}: {e}"); return False

    return True