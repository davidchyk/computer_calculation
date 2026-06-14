#include "total_input.h"

#include <string.h>

#include "sets_input.h"
#include "expression_input.h"
#include "basis_input.h"

void function_input(Function_Data* function, const int* index) {

    if (function == NULL || index == NULL) {
        printf(ERROR("\t[Error] Function input target is not initialized.\n"));
        return;
    }

    printf("Input data for function F%d:\n", *index);

    function->index = *index;

    bool is_expression_regime = false;

    while (true) {

        printf("\tEnter input mode: [E]xpression or [S]ets: ");

        fflush(stdout);
        string input_mode = string_input();

        if (input_mode.data == NULL) {
            printf(ERROR("\t[Error] Failed to read input mode.\n"));
            return;
        }

        if (strcmp(input_mode.data, "E") == 0 || strcmp(input_mode.data, "e") == 0) {
            is_expression_regime = true;
            string_free(&input_mode);
            break;
        }

        if (strcmp(input_mode.data, "S") == 0 || strcmp(input_mode.data, "s") == 0) {
            string_free(&input_mode);
            break;
        }

        printf(ERROR(
                "\t[Error] Invalid input mode \"%s\". Please enter 'E/e' for Expression or 'S/s' for Sets.\n"
            ),
            input_mode.data != NULL ? input_mode.data : ""
        );

        string_free(&input_mode);
    }

    function->from_expression_created = is_expression_regime;

    if (is_expression_regime) { // expression mode

        expression_inputing(function);

    }

    else { // sets mode

        sets_inputing(function);

    }

    // basis inputing

    basis_inputing(function);

}