#ifndef INPUT_PARSER_H
#define INPUT_PARSER_H

#include <stddef.h>

// Функція для перевірки, чи є рядок валідним числом
int isFloat(const char *str);

// Функція для перевірки рядка та створення масиву цілих чисел
int *parseDynamicStringToArray(const char *data, int optional, size_t *arraySize);

char **splitBASIS(char *dynamicString);

#endif // INPUT_PARSER_H