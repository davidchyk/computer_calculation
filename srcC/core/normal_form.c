#include "normal_form.h"

static bool is_from_dnf(basisType basis);
static char* get_bits(int number, int bitsNum);
static bool is_in_array(int number, int* array, int array_size);
static bool append_string(string* main_string, const char* past_string);
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

    if (!result) {
        return NULL;
    }

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

static bool append_string(string* main_string, const char* past_string) {

    int pasting_length = strlen(past_string);

    if (main_string->length + pasting_length + 1 > main_string->capacity) {

        size_t new_capacity = main_string->capacity + pasting_length + 1;
        char* new_data = (char*)realloc(main_string->data, new_capacity);
        if (!new_data) {
            return false;
        }
        main_string->data = new_data;
        main_string->capacity = new_capacity;

    }

    strcpy(main_string->data + main_string->length, past_string);

    main_string->length += pasting_length;

    return true;

}

static string build_normal_form(Function_Data* function_data, basisType basis) {

    string normal_form = { NULL, 0u, 0u };

    bool in_not = false;
    bool out_not = false;

    bool in_or_symbol = false;
    bool out_or_symbol = false;

    bool reversing = false;

    int* termArr = NULL;
    int termArr_len = 0;
    bool termArr_owned = false;

    if (is_from_dnf(basis)) {

        if (function_data->setsNum == 0) {

            append_string(&normal_form, "0");
            return normal_form;

        }

        else if (function_data->setsNum == (1 << function_data->argsNum)) {

            append_string(&normal_form, "1");
            return normal_form;

        }

        termArr = function_data->setsArray;
        termArr_len = function_data->setsNum;

    }

    else {

        int k = (1 << function_data->argsNum) - function_data->setsNum;

        if (k == 0) {

            append_string(&normal_form, "1");
            return normal_form;

        }

        else if (k == (1 << function_data->argsNum)) {

            append_string(&normal_form, "0");
            return normal_form;

        }

        termArr = (int*)malloc(sizeof(int) * k);

        if (!termArr) {

            return normal_form;
        }

        termArr_owned = true;

        for (int i = 0, j = 0; i < (1 << function_data->argsNum); i++) {

            if (!is_in_array(i, function_data->setsArray, function_data->setsNum)) {

                termArr[j++] = i;

            }

        }

        termArr_len = k;

    }

    switch (basis) {

        case AND_OR:

            in_not = false;
            out_not = false;

            in_or_symbol = false;
            out_or_symbol = true;

            reversing = false;

            break;

        case NAND_NAND:

            in_not = true;
            out_not = true;

            in_or_symbol = false;
            out_or_symbol = false;

            reversing = false;

            break;

        case OR_NAND:

            in_not = false;
            out_not = true;

            in_or_symbol = true;
            out_or_symbol = false;

            reversing = true;

            break;

        case NOR_OR:

            in_not = true;
            out_not = false;

            in_or_symbol = true;
            out_or_symbol = true;

            reversing = true;

            break;

        case OR_AND:

            in_not = false;
            out_not = false;

            in_or_symbol = true;
            out_or_symbol = false;

            reversing = true;

            break;

        case NOR_NOR:

            in_not = true;
            out_not = true;

            in_or_symbol = true;
            out_or_symbol = true;

            reversing = true;

            break;

        case AND_NOR:

            in_not = false;
            out_not = true;

            in_or_symbol = false;
            out_or_symbol = true;

            reversing = false;

            break;

        case NAND_AND:

            in_not = true;
            out_not = false;

            in_or_symbol = false;
            out_or_symbol = false;

            reversing = false;

            break;

        default:

            break;

    }

    if (out_not) append_string(&normal_form, "\\overline{");

    for (int i = 0; i < termArr_len; i++) {

        int term = termArr[i];
        char* termBits = get_bits(term, function_data->argsNum);

        if (!termBits) {

            break;

        }

        if (in_not) {

            append_string(&normal_form, "\\overline{");

        }

        else if (!in_not && termArr_len > 1) {

            append_string(&normal_form, "(");

        }

        for (int j = 0; j < function_data->argsNum; j++) {

            if (termBits[j] == '1') {

                if (reversing) append_string(&normal_form, "\\overline");
                append_string(&normal_form, function_data->argsArray[j]);

            }

            else {

                if (!reversing) append_string(&normal_form, "\\overline");
                append_string(&normal_form, function_data->argsArray[j]);

            }

            if (j < function_data->argsNum - 1) {

                in_or_symbol ? append_string(&normal_form, "\\vee") : append_string(&normal_form, "\\wedge");

            }

        }

        if (in_not) {

            append_string(&normal_form, "}");

        }

        else if (!in_not && termArr_len > 1) {

            append_string(&normal_form, ")");

        }

        if (i < termArr_len - 1) {

            out_or_symbol ? append_string(&normal_form, "\\vee") : append_string(&normal_form, "\\wedge");

        }

        free(termBits);

    }

    if (out_not) append_string(&normal_form, "}");

    if (termArr_owned) {
        free(termArr);
    }

    return normal_form;

}