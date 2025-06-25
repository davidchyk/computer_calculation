// dynamic_array.h

#ifndef DYNAMIC_ARRAY_H
#define DYNAMIC_ARRAY_H

#include <stdlib.h>

// Структура для динамічного масиву
typedef struct {
    int *data;          // Вказівник на масив елементів
    size_t size;        // Поточний розмір масиву
    size_t capacity;    // Потужність масиву
} DynamicArray;

// Функції для роботи з динамічним масивом
void initArray(DynamicArray *a, size_t initialCapacity);
void insertArray(DynamicArray *a, int element);
void removeArray(DynamicArray *a, size_t index);
void printArray(const DynamicArray *a);
void freeArray(DynamicArray *a);

#endif // DYNAMIC_ARRAY_H