#include "normal_form.h"

static bool is_from_dnf(basisType basis);
static char* get_bits(int number, int bitsNum);
static bool is_in_array(int number, int* array, int array_size);
static void append_string(string* main_string, const char* past_string);
static string build_normal_form(Function_Data* function_data, basisType basis);

void set_dnf(Function_Data* function_data) {

    function_data->dnf_form = build_normal_form(function_data, AND_OR);
    
}

void set_cnf(Function_Data* function_data) {

    function_data->cnf_form = build_normal_form(function_data, OR_AND);

}

void set_normal_form(Function_Data* function_data) {

    function_data->normal_form = build_normal_form(function_data, function_data->basis);

}

static bool is_from_dnf(basisType basis) {

    return (basis == AND_OR || basis == NAND_NAND || basis == OR_NAND || basis == NOR_OR);

}

static char* get_bits(int number, int bitsNum) {

    char* result = (char*)malloc(sizeof(char) * bitsNum + 1);

    for (int i = bitsNum - 1; i >= 0; i--) {

	    result[bitsNum - i - 1] = (1 << i & number) ? '1' : '0';

    }

    result[bitsNum] = '\0';

	return result;

}

static bool is_in_array(int number, int* array, int array_size) {

    for (int i = 0; i < array_size; i++) {

        if (array[i] == number) {

            return true;

        }

    }

    return false;

}

static void append_string(string* main_string, const char* past_string) {

    int pasting_length = strlen(past_string);

    if (main_string->length + pasting_length + 1 > main_string->capacity) {

        size_t new_capacity = main_string->capacity + pasting_length + 1;
        char* new_data = (char*)realloc(main_string->data, new_capacity);
        if (!new_data) {
            return;
        }
        main_string->data = new_data;
        main_string->capacity = new_capacity;

    }

    strcpy(main_string->data + main_string->length, past_string);

    main_string->length += pasting_length;

}

static string build_normal_form_v1(Function_Data* function_data, basisType basis) {

    string normal_form = { NULL, 0u, 0u };

    if (is_from_dnf(basis)) {

        if (function_data->setsNum == 0) {

            append_string(&normal_form, "0");
            return normal_form;

        }

        switch (basis) {

            case AND_OR:

                for (int i = 0; i < function_data->setsNum; i++) {

                    int minterm = function_data->setsArray[i];
                    char* mintermBits = get_bits(minterm, function_data->argsNum);

                    if (function_data->setsNum > 1) {

                        append_string(&normal_form, "(");

                    }

                    for (int j = 0; j < function_data->argsNum; j++) {

                        if (mintermBits[j] == '0') {

                            append_string(&normal_form, "\\overline");
                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                        else {

                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                    }

                    if (i < function_data->setsNum - 1) {

                        append_string(&normal_form, "\\vee");

                    }

                    free(mintermBits);

                }

                break;

            case NAND_NAND:

                append_string(&normal_form, "\\overline{");

                for (int i = 0; i < function_data->setsNum; i++) {

                    int minterm = function_data->setsArray[i];
                    char* mintermBits = get_bits(minterm, function_data->argsNum);

                    append_string(&normal_form, "\\overline{");

                    for (int j = 0; j < function_data->argsNum; j++) {

                        if (mintermBits[j] == '0') {

                            append_string(&normal_form, "\\overline");
                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                        else {

                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                    }

                    append_string(&normal_form, "}");

                    if (i < function_data->setsNum - 1) {

                        append_string(&normal_form, "\\wedge");

                    }

                    free(mintermBits);

                }

                append_string(&normal_form, "}");

                break;

            case OR_NAND:

                append_string(&normal_form, "\\overline{");

                for (int i = 0; i < function_data->setsNum; i++) {

                    if (function_data->setsNum > 1) {

                        append_string(&normal_form, "(");

                    }

                    int minterm = function_data->setsArray[i];
                    char* mintermBits = get_bits(minterm, function_data->argsNum);

                    for (int j = 0; j < function_data->argsNum; j++) {

                        if (mintermBits[j] == '1') {

                            append_string(&normal_form, "\\overline");
                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                        else {

                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                        if (j < function_data->argsNum - 1) {

                            append_string(&normal_form, "\\vee");

                        }

                    }

                    if (function_data->setsNum > 1) {

                        append_string(&normal_form, ")");

                    }

                    if (i < function_data->setsNum - 1) {

                        append_string(&normal_form, "\\wedge");

                    }

                    free(mintermBits);

                }

                append_string(&normal_form, "}");

                break;

            case NOR_OR:

                for (int i = 0; i < function_data->setsNum; i++) {

                    append_string(&normal_form, "\\overline{");

                    int minterm = function_data->setsArray[i];
                    char* mintermBits = get_bits(minterm, function_data->argsNum);

                    for (int j = 0; j < function_data->argsNum; j++) {

                        if (mintermBits[j] == '1') {

                            append_string(&normal_form, "\\overline");
                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                        else {

                            append_string(&normal_form, function_data->argsArray[j]);

                        }

                        if (j < function_data->argsNum - 1) {

                            append_string(&normal_form, "\\vee");

                        }

                    }

                    append_string(&normal_form, "}");

                    if (i < function_data->setsNum - 1) {

                        append_string(&normal_form, "\\vee");

                    }

                    free(mintermBits);

                }

                break;

            default:

                break;

        }

    }

    else {

        printf("we here");

        // generate maxterm array from setsArray

        int* maxterm = (int*)malloc(sizeof(int) * ((1 << function_data->argsNum) - function_data->setsNum));

        for (int i = 0, j = 0; i < (1 << function_data->argsNum); i++) {

            if (!is_in_array(i, function_data->setsArray, function_data->setsNum)) {

                maxterm[j++] = i;

            }

        }

    }

    return normal_form;

}