def create_logic_diagram_png(user_input, num_of_func, list_to_create):

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

    #Створює блок-схему на основі логічного виразу.

    try:

        d = logicparse(convert_symbols(user_input), outlabel=rf'$Y_{num_of_func}$')

        # Малювання та збереження схеми
        # d.draw()
        d.save(f"OUTPUT_SCHEMMA Y_{num_of_func}.png")

    except Exception as e:

        print(f"Помилка при створенні схеми. Зверніться до розробників.")