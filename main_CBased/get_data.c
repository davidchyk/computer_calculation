#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

char* db[][2] = {
    {"AND", "OR"},
    {"AND-NOT", "AND-NOT"},
    {"OR", "AND-NOT"},
    {"OR-NOT", "OR"},
    {"OR", "AND"},
    {"OR-NOT", "OR-NOT"},
    {"AND", "OR-NOT"},
    {"AND-NOT", "AND"}
};

int isFloat(const char *str);

int* parseDynamicStringToArray(char *dynamicString, int optional, size_t *arraySize);

char** splitBASIS(char *dynamicString);

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

char **splitBASIS(char *dynamicString) {
    // Масив із 4 елементів
    char **staticArray = malloc(4 * sizeof(char *));
    if (staticArray == NULL) {
        perror("Error allocating memory for staticArray");
        return NULL;
    }

    // Розділення рядка
    char *part1 = strtok(dynamicString, "/");
    char *part2 = strtok(NULL, "/");

    if (part1 == NULL || part2 == NULL) {
        printf("Input string does not contain both parts separated by '/'.\n");
        free(staticArray);
        return NULL;
    }

    // Елемент 1: перший символ part1
    staticArray[0] = malloc(2 * sizeof(char)); // Один символ + термінальний нуль
    if (staticArray[0] == NULL) {
        perror("Error allocating memory for staticArray[0]");
        free(staticArray);
        return NULL;
    }
    staticArray[0][0] = part1[0];
    staticArray[0][1] = '\0';

    // Елемент 2: part1 без першого символу
    staticArray[1] = strdup(part1 + 1);
    if (staticArray[1] == NULL) {
        perror("Error allocating memory for staticArray[1]");
        free(staticArray[0]);
        free(staticArray);
        return NULL;
    }

    // Елемент 3: перший символ part2
    staticArray[2] = malloc(2 * sizeof(char)); // Один символ + термінальний нуль
    if (staticArray[2] == NULL) {
        perror("Error allocating memory for staticArray[2]");
        free(staticArray[0]);
        free(staticArray[1]);
        free(staticArray);
        return NULL;
    }
    staticArray[2][0] = part2[0];
    staticArray[2][1] = '\0';

    // Елемент 4: part2 без першого символу
    staticArray[3] = strdup(part2 + 1);
    if (staticArray[3] == NULL) {
        perror("Error allocating memory for staticArray[3]");
        free(staticArray[0]);
        free(staticArray[1]);
        free(staticArray[2]);
        free(staticArray);
        return NULL;
    }

    for (int i = 0; i < 8; i++) {

        if (strcmp(db[i][0], staticArray[1]) == 0 && strcmp(db[i][1], staticArray[3]) == 0) return staticArray;

    }

    printf("Incorrect basis\n");
    return NULL;
}

//normal_forms:

//operator_form2:

//minimization: