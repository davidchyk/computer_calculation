#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>

#include "string_process/string_process.h"
#include "input_f/total_input.h"
#include "typing.h"

const char *logical_form_to_string(logical_form form) {

    switch (form) {
        case FORM_AND:
            return "AND";

        case FORM_OR:
            return "OR";

        case FORM_NOR:
            return "NOR";

        case FORM_NAND:
            return "NAND";
    }

    return "UNKNOWN";
}

static void free_function_data(Function_Data *function) {

    if (function == NULL) {
        return;
    }

    free(function->setsArray);
    function->setsArray = NULL;

    if (function->argsArray != NULL) {
        for (int i = 0; i < function->argsNum; i++) {
            free(function->argsArray[i]);
        }

        free(function->argsArray);
        function->argsArray = NULL;
    }

    function->argsNum = 0;
    function->setsNum = 0;
}

int main(void) {

    printf("Computer Calculation Tool\nAuthor: Davydchuk Artem\n\n");

    /*

    FUCK CLI, FUCK TERMINAL

    while (true) {

        int num_functions = 0;

        // Inputing function

        while (true) {

            printf("Input number of functions to analyze (from 1 to 9): ");

            fflush(stdout);
            string num_functions_str = string_input();

            if (num_functions_str.data == NULL) {
                printf(ERROR("[NumFunction Error] Failed to read number of functions.\n"));
                return 1;
            }

            if (
                string_to_decimal(&num_functions_str, &num_functions) &&
                num_functions >= 1 &&
                num_functions <= 9
            ) {
                string_free(&num_functions_str);
                break;
            }

            printf(
                ERROR(
                    "[NumFunction Error] Invalid number of functions: \"%s\". Please enter a valid integer.\n"
                ),
                num_functions_str.data != NULL ? num_functions_str.data : ""
            );

            string_free(&num_functions_str);
        }

        Function_Data* functionArr = calloc(num_functions, sizeof(Function_Data));

        if (functionArr == NULL) {
            printf(ERROR("[Memory Error] Cannot allocate memory for functions.\n"));
            return 1;
        }

        for (int function_index = 0; function_index < num_functions; function_index++) {

            function_input(&functionArr[function_index], &function_index);

            printf("\n\targsNum: %d\n", functionArr[function_index].argsNum);
            printf("\tsetsNum: %d\n", functionArr[function_index].setsNum);

            printf("\tsetsArray: [");

            for (int i = 0; i < functionArr[function_index].setsNum; i++) {

                printf("%d", functionArr[function_index].setsArray[i]);

                if (i != functionArr[function_index].setsNum-1) {

                    printf(", ");

                }

            }

            printf("]\n");

            printf("\targsArray: [");

            for (int i = 0; i < functionArr[function_index].argsNum; i++) {

                printf("%s", functionArr[function_index].argsArray[i]);

                if (i != functionArr[function_index].argsNum-1) {

                    printf(", ");

                }

            }

            printf("]\n");

            printf("\tbasis of function %d: ", function_index);
    
            printf(
                "%d%s/%d%s\n\n",
                functionArr[function_index].first_basisNumber,
                logical_form_to_string(functionArr[function_index].firstForm),
                functionArr[function_index].second_basisNumber,
                logical_form_to_string(functionArr[function_index].secondForm)
            );
        }

        // solve the functions

        // deleting trashes

        for (int i = 0; i < num_functions; i++) {
            free_function_data(&functionArr[i]);
        }

        free(functionArr);

    }

    */

    return 0;
}
