#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "input_parser.h"

// Функція для перевірки, чи є рядок валідним числом
int isFloat(const char *str) {
    char *endptr;
    strtod(str, &endptr); // Перетворення в float
    return *endptr == '\0'; // Перевіряємо, чи не залишилося символів
}


// Функція для перевірки рядка та створення масиву цілих чисел
int *parseInputToArray(const char *data, int optional, size_t *arraySize) {
    // Копія рядка, щоб strtok не змінював оригінал
    char *copy = strdup(data);
    if (copy == NULL) {
        perror("Error duplicating string");
        return NULL;
    }

    // Тимчасовий масив для зберігання чисел
    size_t capacity = 10;
    size_t size = 0;
    int *array = malloc(capacity * sizeof(int));
    if (array == NULL) {
        perror("Error allocating memory");
        free(copy);
        return NULL;
    }

    // Розбиття рядка на токени
    char *token = strtok(copy, ", ");
    while (token != NULL) {
        // Перевіряємо, чи є токен числом
        if (!isFloat(token)) {
            printf("Неправильне введення наборів\n");
            free(array);
            free(copy);
            return NULL;
        }

        // Перетворюємо токен у число
        float num = strtof(token, NULL);

        // Перевіряємо, чи є число цілим
        if (!((int)num == num)) {
            printf("Неправильне значення наборів\n");
            free(array);
            free(copy);
            return NULL;
        }

        // Перетворюємо у ціле число і перевіряємо діапазон
        int intNum = (int)num;
        if (intNum >= optional || intNum < 0) {
            printf("Неправильний номер набору\n");
            free(array);
            free(copy);
            return NULL;
        }

        // Додавання числа в масив
        if (size >= capacity) {
            capacity *= 2;
            array = realloc(array, capacity * sizeof(int));
            if (array == NULL) {
                perror("Error reallocating memory");
                free(copy);
                return NULL;
            }
        }
        array[size++] = intNum;

        // Наступний токен
        token = strtok(NULL, ", ");
    }

    free(copy);
    *arraySize = size; // Повертаємо розмір масиву
    return array;      // Повертаємо сформований масив
}