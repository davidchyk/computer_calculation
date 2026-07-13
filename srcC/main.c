#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>
#include <errno.h>

#include "utils/typing.h"
#include "utils/string_process.h"
#include "utils/utils.h"

#include "gui/gui.h"

#include "core/normal_form.h"
#include "core/operator_form.h"

int main(void) {

    printf("Computer Calculation Helper\nAuthor: Davydchuk Artem\n\n");

    function_t test = {

        .index = 0,
        .argsNum = 3,
        .setsNum = 3,
        .setsArray = (int[]){0, 1, 2},
        .argsArray = (char*[]){"{x_3}", "{x_2}", "{x_1}"},

        .from_expression_created = false,

        .basis = NAND_AND,
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
    // set_cnf(&test);
    set_normal_form(&test);
    set_operator_form(&test);

    // printf("normal_form: \n%s\n", test.normal_form.data);
    printf("operator_form: \n%s\n", test.operator_form.data);

    test.normal_form = (string){NULL, 0u, 0u};

    // gui_run();

    return 0;
}
