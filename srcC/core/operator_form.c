#include "operator_form.h"

static string build_operator_form(function_t* function);

void set_operator_form(function_t* function) {

    function->operator_form = build_operator_form(function);

}

static string build_operator_form(function_t* function) {

    string operator_form = {NULL, 0u, 0u};

    bool in_not = IN_NOT(function->basis);
    bool out_not = OUT_NOT(function->basis);

    bool in_or_operation = IN_OR_OPERATION(function->basis);
    bool out_or_operation = OUT_OR_OPERATION(function->basis);

    bool reversing = in_or_operation;

    int* termArr = NULL;
    int temporary[2];

    int termArr_len = 0;
    bool termArr_owned = false;

    switch (isfunctionTrue(function)) {

        case 1:

            append_string(&operator_form, "1");
            return operator_form;
            break;

        case 0:

            append_string(&operator_form, "0");
            return operator_form;
            break;

    }

    if (IS_DNF(function->basis)) {
        
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

            if (!termArr) return operator_form;

            for (int i = 0, j = 0; i < (1 << function->argsNum); i++) {

                if (!is_in_array(i, function->setsArray, function->setsNum)) termArr[j++] = i;

            }

            termArr_len = zeroTerm_count;
            termArr_owned = true;

        }

    }

    int a = function->first_basisNumber, b = function->second_basisNumber, m = function->setsNum*function->argsNum;

    int v, k = 1;
    int n = a;

    for (; k < INT_MAX; k++) {

        n *= b;
        v = n - m;

        if (v >= 0) break;

    }

    printf("v = %d, k = %d\n", v, k);

    char* allBits = (char*)malloc(sizeof(char) * (m+v) + 1);

    for (int i = 0; i < function->setsNum; i++) {

        char* termBits = get_bits(function->setsArray[i], function->argsNum);

        memcpy(
            allBits + i * function->argsNum,
            termBits,
            function->argsNum
        );

        free(termBits);

    }

    for (int i = 0; i < v; i++) allBits[m+i] = 'T';

    allBits[m+v] = '\0';

    printf("%s\n", allBits);

    if (out_not) append_string(&operator_form, "\\overline{");

    // TODO

    if (out_not) append_string(&operator_form, "}");

    free(allBits);

    (void)termArr_owned;
    (void)termArr_len;
    (void)reversing;
    (void)out_or_operation;
    (void)out_not;
    (void)in_not;

    /*
    
    0, 1, 2 = 000 001 010

    {([00][00])  ([01][01])} OO {([0T][TT])  ([TT][TT])}
    
    */

    return operator_form;

}
