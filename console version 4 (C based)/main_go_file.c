#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include "get_data.h"

// Функція очищення буфера вводу
void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// Функція для динамічного зчитування рядка
char *readDynamicString(const char *input_string) {
    char *string = NULL;
    size_t size = 0;
    size_t capacity = 1;
    char ch;

    string = malloc(capacity * sizeof(char));
    if (string == NULL) {
        perror("Error: allocation of memory");
        exit(EXIT_FAILURE);
    }

    printf("%s: ", input_string);

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

char *truth_table(int num_of_args, int sets_number) {
    
    return;

}

void convert_to_normal(char *string, int num_of_args) {

    return;
}

void convert_to_normal_operator(char *string, int num_of_args) {

    return;
}

int validate(char *data, const int type) {

    char *endptr;
    long number;
    errno = 0;

    switch (type) {

        case 1:

            number = strtol(data, &endptr, 10);

            if (*endptr != '\0') {
                printf("Error: invalid number of arguments\n");
                return 0;
            }

            else if ((errno == ERANGE) || (number > 100)) {
                printf("Error: number is out of range\n");
                return 0;
            }

            else if (*endptr != '\0') {
                printf("Error: invalid number of arguments\n");
                return 0;
            }

            else if (number == 0) {
                printf("Error: number of arguments is zero\n");
                return 0;
            }

            return (int)number;

        case 2:

            number = strtol(data, &endptr, 10);

            if (*endptr != '\0') {
                printf("Error: invalid number of funcs\n");
                return 0;
            }

            else if ((errno == ERANGE) || (number > 100)) {
                printf("Error: number is out of range\n");
                return 0;
            }

            else if (*endptr != '\0') {
                printf("Error: invalid number of funcs\n");
                return 0;
            }

            else if (number == 0) {
                printf("Error: number of funcs is zero\n");
                return 0;
            }

            return (int)number;

        }

}

int main() {

    printf("C Version 1.0!\n");
    printf("Developded by Artem Davidchyk, Ivan Bilyi, Max Trotsenko\n");

    char *db[][2] = {
        {"AND", "OR"},
        {"AND-NOT", "AND-NOT"},
        {"OR", "AND-NOT"},
        {"OR-NOT", "OR"},
        {"OR", "AND"},
        {"OR-NOT", "OR-NOT"},
        {"AND", "OR-NOT"},
        {"AND-NOT", "AND"}
    };

    // DynamicArray ddnf_list;
    // initArray(&ddnf_list, 0);

    while (1) {

        int i = 1;
        int temp;

        char CHAR_number_of_args[3];
        int number_of_args;

        char CHAR_number_of_funcs[3];
        int number_of_funcs;

        printf("Enter the number of arguments: ");
        scanf("%s", &CHAR_number_of_args);
        temp = validate(CHAR_number_of_args, 1);

        if (!temp) {

            clearInputBuffer();
            continue;

        }

        number_of_args = (int)temp;

        int number_of_sets = 1 << number_of_args; // number_of_sets = 2^number_of_args

        printf("Enter the number of functions: ");
        scanf("%s", &CHAR_number_of_funcs);
        temp = validate(CHAR_number_of_funcs, 2);
        
        if (!temp) {

            clearInputBuffer();
            continue;

        }    

        number_of_funcs = (int)temp;
        clearInputBuffer();

        while (i <= number_of_funcs) {

            printf("-----\n");
            printf("Enter data for function f%d:\n", i);

            char *dynamicString = readDynamicString("Enter num of sets");
            size_t length = strlen(dynamicString);
            int *array = parseDynamicStringToArray(dynamicString, number_of_sets, &length);
            if (array == NULL) continue;

            /*

            for (size_t i = 0; i < length; i++) {
                printf("ARRAY: %d ", array[i]);
            }

            */

            char *basisString = readDynamicString("Enter basis with '/'");
            char **basis = splitBASIS(basisString);
            if (basis == NULL) continue;

            for (int i = 0; i < 4; i++) {
                printf("BASIS #$%d: %s\n", i, basis[i]);
            }

            int type_of;

            if ((strcmp("AND", basis[1]) == 0) || (strcmp("AND-NOT", basis[1]) == 0)) type_of = 1;
            else type_of = 0;

            printf("Type of function: %d\n", type_of);

            int in_num = atoi(basis[0]);
            int out_num = atoi(basis[2]);

            // char *data_table = truth_table(number_of_args, number_of_sets);









            printf("\n");

            free(array);
            free(dynamicString);
            free(basisString);

            i++;

        }

    }

}