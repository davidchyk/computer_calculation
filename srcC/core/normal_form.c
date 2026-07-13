#include "normal_form.h"

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

static string build_normal_form(function_t* function, basis_t basis) {

    string normal_form = {NULL, 0u, 0u};

    bool in_not = IN_NOT(basis);
    bool out_not = OUT_NOT(basis);

    bool in_or_operation = IN_OR_OPERATION(basis);
    bool out_or_operation = OUT_OR_OPERATION(basis);

    bool reversing = in_or_operation;

    int* termArr = NULL;
    int temporary[2];

    int termArr_len = 0;
    bool termArr_owned = false;

    switch (isfunctionTrue(function)) {

        case 1:

            append_string(&normal_form, "1");
            return normal_form;
            break;

        case 0:

            append_string(&normal_form, "0");
            return normal_form;
            break;

    }

    if (IS_DNF(basis)) {
        
        if (function->setsNum == 1) {

            temporary[0] = function->setsArray[0];
            temporary[1] = TEPM_TERM;

            termArr = temporary;
            termArr_len = 2;

            termArr_owned = false;

        }

        else {

            termArr = function->setsArray;
            termArr_len = function->setsNum;

        }

    }

    else {

        int zeroTerm_count = (1 << function->argsNum) - function->setsNum;

        if (zeroTerm_count == 1) {

            temporary[0] = termArr[0];
            temporary[1] = TEPM_TERM;

            termArr = temporary;

            termArr_len = 2;
            termArr_owned = false;

        }

        else {

            termArr = (int*)malloc(sizeof(int) * zeroTerm_count);

            if (!termArr) return normal_form;

            termArr_owned = true;

            for (int i = 0, j = 0; i < (1 << function->argsNum); i++) {

                if (!is_in_array(i, function->setsArray, function->setsNum)) termArr[j++] = i;

            }

            termArr_len = zeroTerm_count;

        }

    }

    if (out_not) append_string(&normal_form, "\\overline{");

    for (int i = 0; i < termArr_len; i++) {

        int term = termArr[i];
        char* termBits = get_bits(term, function->argsNum);

        if (!termBits) break;

        if (termBits[0] == 'T') {
            out_or_operation ? append_string(&normal_form, "0") : append_string(&normal_form, "1");
        }

        else {

            in_not ? append_string(&normal_form, "\\overline{") : append_string(&normal_form, "(");

            for (int j = 0; j < function->argsNum; j++) {

                if (termBits[j] == '1') {

                    if (reversing) append_string(&normal_form, "\\overline");
                    append_string(&normal_form, function->argsArray[j]);

                }

                else if (termBits[j] == '0') {

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

        }

        if (i < termArr_len - 1) {

            out_or_operation ? append_string(&normal_form, "\\vee") : append_string(&normal_form, "\\wedge");

        }

        free(termBits);

    }

    if (out_not) append_string(&normal_form, "}");

    if (termArr_owned) free(termArr);

    return normal_form;

}