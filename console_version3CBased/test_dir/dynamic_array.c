// dynamic_array.c

#include <stdio.h>
#include <stdlib.h>
#include "dynamic_array.h"

// Ініціалізація динамічного масиву
void initArray(DynamicArray *a, size_t initialCapacity) {
    a->data = malloc(initialCapacity * sizeof(int));
    if (a->data == NULL) {
        fprintf(stderr, "Error: allocation of memory\n");
        exit(EXIT_FAILURE);
    }
    a->size = 0;
    a->capacity = initialCapacity;
}

// Додавання елемента в масив
void insertArray(DynamicArray *a, int element) {
    if (a->size == a->capacity) {
        a->capacity *= 2; // Подвоюємо потужність
        int *temp = realloc(a->data, a->capacity * sizeof(int));
        if (temp == NULL) {
            fprintf(stderr, "Error: reallocation of memory\n");
            free(a->data);
            exit(EXIT_FAILURE);
        }
        a->data = temp;
    }
    a->data[a->size++] = element;
}

// Видалення елемента за індексом
void removeArray(DynamicArray *a, size_t index) {
    if (index >= a->size) {
        fprintf(stderr, "Error: index out of range\n");
        return;
    }
    for (size_t i = index; i < a->size - 1; i++) {
        a->data[i] = a->data[i + 1];
    }
    a->size--;
}

// Друк елементів масиву
void printArray(const DynamicArray *a) {
    for (size_t i = 0; i < a->size; i++) {
        printf("%d ", a->data[i]);
    }
    printf("\n");
}

// Звільнення пам'яті масиву
void freeArray(DynamicArray *a) {
    free(a->data);
    a->data = NULL;
    a->size = a->capacity = 0;
}