#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

char *readDynamicString() {
    char *string = NULL;
    size_t size = 0;
    size_t capacity = 1;
    char ch;

    string = malloc(capacity * sizeof(char));
    if (string == NULL) {
        perror("Error: allocation of memory");
        exit(EXIT_FAILURE);
    }

    printf("Enter your input: ");

    while ((ch = getchar()) != '\n' && ch != EOF) {
        if (size + 1 >= capacity) {
            capacity *= 2; // Збільшуємо ємність у два рази
            string = realloc(string, capacity * sizeof(char));
            if (string == NULL) {
                perror("Error: reallocation of memory");
                exit(EXIT_FAILURE);
            }
        }
        string[size++] = ch;
    }

    string[size] = '\0'; // Додаємо термінальний нуль
    return string;
}

// Перевірка, чи є рядок числом
int isFloat(const char *str) {
    char *endptr;
    strtod(str, &endptr);
    return *endptr == '\0';
}

// Перевірка, чи є число цілим
int isInteger(float num) {
    return (int)num == num;
}

// Функція для обробки DynamicString і формування масиву цілих чисел
int *parseDynamicStringToArray(char *dynamicString, int optional, size_t *arraySize) {
    size_t capacity = 10;
    size_t size = 0;
    int *array = malloc(capacity * sizeof(int));
    if (array == NULL) {
        perror("Error allocating memory");
        return NULL;
    }

    // Розбиття рядка на токени
    char *token = strtok(dynamicString, ", ");
    while (token != NULL) {
        // Перевірка валідності числа
        if (!isFloat(token)) {
            printf("Incorrect input\n");
            free(array);
            return NULL;
        }

        float num = strtof(token, NULL);
        if (!isInteger(num)) {
            printf("Incorrect input\n");
            free(array);
            return NULL;
        }

        int intNum = (int)num;
        if (intNum >= optional || intNum < 0) {
            printf("Incorrect input\n");
            free(array);
            return NULL;
        }

        // Додавання числа в масив
        if (size >= capacity) {
            capacity *= 2;
            array = realloc(array, capacity * sizeof(int));
            if (array == NULL) {
                perror("Error reallocating memory");
                return NULL;
            }
        }
        array[size++] = intNum;

        token = strtok(NULL, ", ");
    }

    *arraySize = size;
    return array;
}

int main() {

    printf("Enter DynamicString:\n");
    char *dynamicString = readDynamicString();

    size_t arraySize = 0;
    int optional = 10;

    int *array = parseDynamicStringToArray(dynamicString, optional, &arraySize);
    if (array != NULL) {
        printf("Array of integers:\n");
        for (size_t i = 0; i < arraySize; i++) {
            printf("%d ", array[i]);
        }
        printf("\n");
        free(array);
    } else {
        printf("Error: parsing input\n");
    }

    free(dynamicString); // Звільняємо пам'ять рядка
    return 0;
}
