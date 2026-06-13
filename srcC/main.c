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

int main(void) {

    printf("Computer Calculation Tool\nAuthor: Davydchuk Artem\n\n");

    while (true) {

        int num_functions = 0;

        // Input number of functions to analyze: n (1 <= n <= 9)

        while (true) {

            printf("Input number of functions to analyze (from 1 to 9): ");

            fflush(stdout);
            string num_functions_str = string_input();

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

        }

        // solve the functions sets problem

        // deleting trashes

        for (int i = 0; i < num_functions; i++) {
            free(functionArr[i].setsArray);
            free(functionArr[i].argsArray);
        }

        free(functionArr);

    }

    return 0;
}