#include "normal_form.h"

static char* get_bits(int number, int bitsNum);
static bool is_in_array(int number, int* array, int array_size);
static bool append_string(string* main_string, const char* past_string);
static string build_normal_form(function_t* function, basis_t basis);

void set_dnf(function_t* function) {

    function->dnf_form = build_normal_form(function, AND_OR);

}

void set_cnf(function_t* function) {

    function->cnf_form = build_normal_form(function, OR_AND);

}

void set_normal_form(function_t* function) {

    function->normal_form = build_normal_form(function, function->basis);

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

static string build_normal_form(function_t* function, basis_t basis) {

    string normal_form = { NULL, 0u, 0u };

    bool in_not = IN_NOT(basis);
    bool out_not = OUT_NOT(basis);

    bool in_or_operation = IN_OR_OPERATION(basis);
    bool out_or_operation = OUT_OR_OPERATION(basis);

    bool reversing = out_or_operation;

    int* termArr = NULL;
    int termArr_len = 0;
    bool termArr_owned = false;

    if (IS_DNF(basis)) {

        if (function->setsNum == 0) {

            append_string(&normal_form, "0");
            return normal_form;

        }

        else if (function->setsNum == (1 << function->argsNum)) {

            append_string(&normal_form, "1");
            return normal_form;

        }

        termArr = function->setsArray;
        termArr_len = function->setsNum;

    }

    else {

        int k = (1 << function->argsNum) - function->setsNum;

        if (k == 0) {

            append_string(&normal_form, "1");
            return normal_form;

        }

        else if (k == (1 << function->argsNum)) {

            append_string(&normal_form, "0");
            return normal_form;

        }

        termArr = (int*)malloc(sizeof(int) * k);

        if (!termArr) {

            return normal_form;
        }

        termArr_owned = true;

        for (int i = 0, j = 0; i < (1 << function->argsNum); i++) {

            if (!is_in_array(i, function->setsArray, function->setsNum)) {

                termArr[j++] = i;

            }

        }

        termArr_len = k;

    }

    if (out_not) append_string(&normal_form, "\\overline{");

    for (int i = 0; i < termArr_len; i++) {

        int term = termArr[i];
        char* termBits = get_bits(term, function->argsNum);

        if (!termBits) {

            break;

        }

        if (in_not) {

            append_string(&normal_form, "\\overline{");

        }

        else if (!in_not && termArr_len > 1) {

            append_string(&normal_form, "(");

        }

        for (int j = 0; j < function->argsNum; j++) {

            if (termBits[j] == '1') {

                if (reversing) append_string(&normal_form, "\\overline");
                append_string(&normal_form, function->argsArray[j]);

            }

            else {

                if (!reversing) append_string(&normal_form, "\\overline");
                append_string(&normal_form, function->argsArray[j]);

            }

            if (j < function->argsNum - 1) {

                in_or_operation ? append_string(&normal_form, "\\vee") : append_string(&normal_form, "\\wedge");

            }

        }

        if (in_not) {

            append_string(&normal_form, "}");

        }

        else if (!in_not && termArr_len > 1) {

            append_string(&normal_form, ")");

        }

        if (i < termArr_len - 1) {

            out_or_operation ? append_string(&normal_form, "\\vee") : append_string(&normal_form, "\\wedge");

        }

        free(termBits);

    }

    if (out_not) append_string(&normal_form, "}");

    if (termArr_owned) {
        free(termArr);
    }

    return normal_form;

}