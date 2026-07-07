#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>
#include <errno.h>

#include "gui/gui.h"

#include "string_process/string_process.h"
#include "core/normal_form.h"
#include "input_f/total_input.h"
#include "typing.h"

int main(void) {

    printf("Computer Calculation Tool\nAuthor: Davydchuk Artem\n\n");

    Function_Data test = {

        .index = 0,
        .argsNum = 4,
        .setsNum = 9,
        .setsArray = (int[]){0, 1, 2, 3, 4, 5, 6, 7, 8},
        .argsArray = (char*[]){"{x_4}", "{x_3}", "{x_2}", "{x_1}"},

        .from_expression_created = false,

        .basis = AND_NOR,
        .firstForm = FORM_NAND,
        .secondForm = FORM_NAND,
        .first_basisNumber = 2,
        .second_basisNumber = 2,

        .dnf_form = (string){NULL, 0u, 0u},
        .cnf_form = (string){NULL, 0u, 0u},

        .normal_form = (string){NULL, 0u, 0u},
        .operator_form = (string){NULL, 0u, 0u},
        .minimized_normal_form = (string){NULL, 0u, 0u},
        .minimized_operator_form = (string){NULL, 0u, 0u}

    };

    // set_dnf(&test);

    set_normal_form(&test);

    printf("normal_form: \n%s\n", test.normal_form.data);

    test.normal_form = (string){NULL, 0u, 0u};

    // gui_run();

    return 0;
}
