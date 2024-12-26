#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int isFloat(const char *str) {
    char *endptr;
    strtod(str, &endptr);
    return *endptr == '\0';
}

// Перевірка, чи є рядок числом
int *parseDynamicStringToArray(char *dynamicString, int optional, size_t *arraySize) {

    if (strlen(dynamicString) == 0) {
        printf("Input is empty\n");
        return NULL;
    }

    size_t capacity = 10;
    size_t size = 0;
    int *array = malloc(capacity * sizeof(int));
    if (array == NULL) {
        perror("Error allocating memory"); return NULL;
    }

    char *token = strtok(dynamicString, ", ");

    while (token != NULL) {

        float num = strtof(token, NULL);

        if (!isFloat(token)) {
            printf("Incorrect input\n"); return NULL;
        }

        else if (!((int)num == num)) {
            printf("Token is not integer: %s\n", token); return NULL;
        }

        else if ((int)num >= optional || (int)num < 0) {
            printf("Token is out of range: %s\n", token); return NULL;
        }

        else {
    
            // Додаємо елемент у масив
            if (size >= capacity) {
                capacity *= 2;
                array = realloc(array, capacity * sizeof(int));
                if (array == NULL) {
                    perror("Error reallocating memory");
                    return NULL;
                }
            }

            array[size++] = (int)num;
        }

        token = strtok(NULL, ", ");
    }

    *arraySize = size; // Оновлення розміру масиву
    return array;
}

char **parseDynamicStringToCharArray(char *dynamicString, int optional, size_t *arraySize) {

    char result[4];

    if (strlen(dynamicString) == 0) {
        printf("Input is empty\n");
        return NULL;
    }

    size_t capacity = 10;
    size_t size = 0;
    int *array = malloc(capacity * sizeof(int));
    if (array == NULL) {
        perror("Error allocating memory"); return NULL;
    }

    char *token = strtok(dynamicString, "/");

    result[0] = token[0];
    result[1] = token[1];

    // дописати

    printf("Token: %s\n", token);

    return NULL;

}