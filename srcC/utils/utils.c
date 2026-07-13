#include "utils.h"

int isfunctionTrue(function_t* function) {

    if (function->setsNum == (1 << function->argsNum)) return 1;

    if (function->setsNum == 0) return 0;

    return -1;

}

char* get_bits(int number, int bitsNum) {

    if (number == TEPM_TERM) {

        char* result = (char*)malloc(sizeof(char) + 1);

        result[0] = 'T';
        result[1] = '\0';
        return result;

    }

    char* result = (char*)malloc(sizeof(char) * bitsNum + 1);

    if (!result) return NULL;

    for (int i = bitsNum - 1; i >= 0; i--) {

        result[bitsNum-i-1] = (1 << i & number) ? '1' : '0';

    }

    result[bitsNum] = '\0';

    return result;

}

bool is_in_array(int number, int* array, int array_size) {

    for (int i = 0; i < array_size; i++) {

        if (array[i] == number) {

            return true;

        }

    }

    return false;

}