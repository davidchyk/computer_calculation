#ifndef STRING_PROCESS_H
#define STRING_PROCESS_H

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>
#include <ctype.h>
#include <stdbool.h>

typedef struct {
    char* data;
    size_t length;
    size_t capacity;
} string;

string string_input(void);

void string_free(string *s);

bool string_to_decimal(const string* str, int* out_value);

#endif // STRING_PROCESS_H