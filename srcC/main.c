#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>

#include "string_process.h"

typedef enum {
    AND_OR,
    NAND_NAND,
    OR_NAND,
    NOR_OR,
    OR_AND,
    NOR_NOR,
    AND_NOR,
    NAND_AND
} basis_type;

typedef struct {
    // function data from input

    int index;
    int num_functions_args;
    int num_sets_count;

    int *decimal_sets_array;
    char** args_array;

    basis_type basis;
    bool from_expression_created;

    // function data from calculations

} Function_Data;

static char *trim_spaces(char *s) {

    while (isspace((unsigned char)*s)) {
        s++;
    }

    if (*s == '\0') {
        return s;
    }

    char *end = s + strlen(s) - 1;

    while (end > s && isspace((unsigned char)*end)) {
        end--;
    }

    end[1] = '\0';

    return s;
}

static bool parse_int_list_csv(string *input, int **out_array, int *out_count) {

    if (input == NULL || input->data == NULL || out_array == NULL || out_count == NULL) {
        return false;
    }

    size_t capacity = 4;
    size_t count = 0;

    int *array = malloc(capacity * sizeof(int));

    if (array == NULL) {
        return false;
    }

    char *start = input->data;

    while (true) {

        char *comma = strchr(start, ',');

        if (comma != NULL) {
            *comma = '\0';
        }

        char *token = trim_spaces(start);

        if (*token == '\0') {
            free(array);
            return false;
        }

        int value;

        string token_string = {
            .data = token,
            .length = strlen(token),
            .capacity = strlen(token)
        };

        if (!string_to_decimal(&token_string, &value)) {
            free(array);
            return false;
        }

        if (count >= capacity) {
            size_t new_capacity = capacity * 2;

            int *tmp = realloc(array, new_capacity * sizeof(int));

            if (tmp == NULL) {
                free(array);
                return false;
            }

            array = tmp;
            capacity = new_capacity;
        }

        array[count] = value;
        count++;

        if (comma == NULL) {
            break;
        }

        start = comma + 1;
    }

    if (count == 0 || count > INT_MAX) {
        free(array);
        return false;
    }

    int *tmp = realloc(array, count * sizeof(int));

    if (tmp != NULL) {
        array = tmp;
    }

    *out_array = array;
    *out_count = (int)count;

    return true;
}

int main(void) {

    printf("Computer Calculation Tool\nAuthor: Davydchuk Artem\n");

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
                "[NumFunction Error] Invalid number of functions: \"%s\". Please enter a valid integer.\n",
                num_functions_str.data != NULL ? num_functions_str.data : ""
            );

            string_free(&num_functions_str);
        }

        Function_Data *function_arr = calloc(num_functions, sizeof(Function_Data));

        if (function_arr == NULL) {
            printf("[Memory Error] Cannot allocate memory for functions.\n");
            return 1;
        }

        for (int function_index = 0; function_index < num_functions; function_index++) {

            printf("Input data for function F%d:\n", function_index);

            function_arr[function_index].index = function_index;

            bool is_expression_regime = false;
            int num_functions_args = 0;
            int sets_count = 0;
            int *sets_array = NULL;
            char *args_array = NULL;

            // Input type of function input: [E]xpression or [S]ets

            while (true) {

                printf("\tEnter input mode: [E]xpression or [S]ets: ");
                fflush(stdout);

                string input_mode = string_input();

                if (strcmp(input_mode.data, "E") == 0 || strcmp(input_mode.data, "e") == 0) {
                    is_expression_regime = true;
                    string_free(&input_mode);
                    break;
                }

                if (strcmp(input_mode.data, "S") == 0 || strcmp(input_mode.data, "s") == 0) {
                    string_free(&input_mode);
                    break;
                }

                printf(
                    "\t[Error] Invalid input mode \"%s\". Please enter 'E/e' for Expression or 'S/s' for Sets.\n",
                    input_mode.data != NULL ? input_mode.data : ""
                );

                string_free(&input_mode);
            }

            function_arr[function_index].from_expression_created = is_expression_regime;

            // expression mode TODO

            if (is_expression_regime) {

                // Getting expression

                while (true) {

                    printf(
                        "\t[Expression Mode] Write the expression for function F%d: ",
                        function_index
                    );

                    fflush(stdout);
                    string expression_str = string_input();

                    //

                    string_free(&expression_str);

                }

            }

            // sets mode

            else {

                while (true) {

                    printf(
                        "\t[Sets Mode] Number of args for function F%d (from 1 to 9): ",
                        function_index
                    );

                    fflush(stdout);

                    string num_functions_args_str = string_input();

                    if (
                        string_to_decimal(&num_functions_args_str, &num_functions_args) &&
                        num_functions_args >= 1 &&
                        num_functions_args <= 9
                    ) {
                        string_free(&num_functions_args_str);
                        break;
                    }

                    printf(
                        "\t[Sets Mode] [Error] Invalid number of arguments: \"%s\". Please enter a valid integer.\n",
                        num_functions_args_str.data != NULL ? num_functions_args_str.data : ""
                    );

                    string_free(&num_functions_args_str);
                }

                while (true) {

                    printf(
                        "\t[Sets Mode] Enter decimal sets for function F%d (comma-separated, example: 0, 1, 3, 7): ",
                        function_index
                    );

                    fflush(stdout);

                    string sets_input = string_input();

                    if (parse_int_list_csv(&sets_input, &sets_array, &sets_count)) {
                        string_free(&sets_input);
                        break;
                    }

                    printf(
                        "\t[Sets Mode] [Error] Invalid sets input. Please enter valid integers separated by commas.\n"
                    );

                    string_free(&sets_input);

                }

                char **args_array = malloc((num_functions_args + 1) * sizeof(char*));

                for (int i = 1; i < num_functions_args+1; i++) {
                    args_array[i-1] = malloc(3 * sizeof(char));
                    args_array[i-1][0] = 'x';
                    args_array[i-1][1] = (char)('0' + i);
                    args_array[i-1][2] = '\0';

                }

            }

            for (int i = 0; i < sets_count; i++) {
                printf("\t\tSet %d: %d\n", i + 1, sets_array[i]);
            }

            function_arr[function_index].num_functions_args = num_functions_args;
            function_arr[function_index].num_sets_count = sets_count;
            function_arr[function_index].decimal_sets_array = sets_array;
            function_arr[function_index].args_array = args_array;

        }

        // solve the functions sets problem

        // deleting trashes

        for (int i = 0; i < num_functions; i++) {
            free(function_arr[i].decimal_sets_array);
            free(function_arr[i].args_array);
        }

        free(function_arr);
    }

    return 0;
}