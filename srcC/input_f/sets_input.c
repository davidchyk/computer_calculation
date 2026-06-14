#include <string.h>

#include "../string_process/string_process.h"
#include "../typing.h"

static char* trim_spaces(char *s) {

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

static void free_args_array(char **args_array, int args_num) {

    if (args_array == NULL) {
        return;
    }

    for (int i = 0; i < args_num; i++) {
        free(args_array[i]);
    }

    free(args_array);
}

static bool parse_int_list_csv(string *input, int max_set_value, int **out_array, int *out_count) {

    if (
        input == NULL ||
        input->data == NULL ||
        out_array == NULL ||
        out_count == NULL ||
        max_set_value <= 0
    ) {
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

        if (!string_to_decimal(&token_string, &value) || value < 0 || value >= max_set_value) {
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

void sets_inputing(Function_Data *function) {

    if (function == NULL) {
        printf(
            ERROR(
                "\t[Sets Mode] [Error] Function data is not initialized.\n"
            )
        );
        return;
    }

    // argsNum

    while (true) {

        printf(
            MODE(
                "\t[Sets Mode]"
            )
            " Number of args for function F%d (from 1 to 9): ",
            function->index
        );

        fflush(stdout);

        string num_function_args_str = string_input();

        if (num_function_args_str.data == NULL) {
            printf(
                ERROR(
                    "\t[Sets Mode] [Error] Failed to read number of arguments.\n"
                )
            );
            return;
        }

        if (
            string_to_decimal(&num_function_args_str, &function->argsNum) &&
            function->argsNum >= 1 &&
            function->argsNum <= 9
        ) {
            string_free(&num_function_args_str);
            break;
        }

        printf(ERROR(
                "\t[Sets Mode] [Error] Invalid number of arguments: \"%s\". Please enter a valid integer.\n"
            ),
            num_function_args_str.data != NULL ? num_function_args_str.data : ""
        );

        string_free(&num_function_args_str);
    }

    // setsNum

    function->setsNum = 1 << function->argsNum;

    // setsArray

    while (true) {

        printf(
            MODE(
                "\t[Sets Mode]"
            )
            " Enter decimal sets for function F%d (comma-separated, example: 0, 1, 3, 7): ",
            function->index
        );

        fflush(stdout);
        string sets_input = string_input();

        if (sets_input.data == NULL) {
            printf(
                ERROR(
                    "\t[Sets Mode] [Error] Failed to read sets input.\n"
                )
            );
            return;
        }

        if (
            parse_int_list_csv(
                &sets_input,
                1 << function->argsNum,
                &function->setsArray,
                &function->setsNum
            )
        ) {
            string_free(&sets_input);
            break;
        }

        printf(
            ERROR(
                "\t[Sets Mode] [Error] Invalid sets input. Please enter valid integers from 0 to %d separated by commas.\n"
            )
            ,
            (1 << function->argsNum) - 1
        );

        string_free(&sets_input);

    }

    // argsArray

    char **args_array = malloc((function->argsNum + 1) * sizeof(char*));

    if (args_array == NULL) {
        printf(
            ERROR(
                "\t[Sets Mode] [Error] Failed to allocate memory for variables.\n"
            )
        );
        free(function->setsArray);
        function->setsArray = NULL;
        function->setsNum = 0;
        return;
    }

    for (int i = 0; i < function->argsNum + 1; i++) {
        args_array[i] = NULL;
    }

    for (int i = 0; i < function->argsNum; i++) {

        args_array[function->argsNum-(i+1)] = malloc(3 * sizeof(char));
        
        if (args_array[function->argsNum-(i+1)] == NULL) {
            printf(
                ERROR(
                    "\t[Sets Mode] [Error] Failed to allocate memory for variable names.\n"
                )
            );
            free(function->setsArray);
            function->setsArray = NULL;
            function->setsNum = 0;
            free_args_array(args_array, function->argsNum + 1);
            return;
        }

        args_array[function->argsNum-(i+1)][0] = 'X';
        args_array[function->argsNum-(i+1)][1] = (char)('0' + i);
        args_array[function->argsNum-(i+1)][2] = '\0';

    }

    function->argsArray = args_array;

}
