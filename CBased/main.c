#define _CRT_SECURE_NO_WARNINGS 0   

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>   // Для isdigit
#include <stdlib.h>
#include <errno.h>    // Для errno, ERANGE
#include <limits.h>   // Для INT_MAX, INT_MIN

#define FUNC_REGIME_LEN 11+2
#define NUM_ARGS_LEN 3
#define NUM_FUNCS_LEN 3

#define FUNCTION_INPUT_REGIME 0
#define NUM_ARGS_REGIME 1
#define NUM_FUNCS_REGIME 2
#define ARRAY_SETS_REGIME 3

#define DEBUG_OUT "[DEBUG]"

typedef char* String;
typedef int* intArray;

String db[][2] = {
    {"AND", "OR"}, {"AND-NOT", "AND-NOT"}, {"OR", "AND-NOT"}, {"OR-NOT", "OR"},
    {"OR", "AND"}, {"OR-NOT", "OR-NOT"}, {"AND", "OR-NOT"}, {"AND-NOT", "AND"}
};

void clear_input_buffer();

bool validateInput(const String data, int flag, int optional_max);

String read_dynamic_line(int NumSets);

intArray get_Array(const String strArray, size_t* uniqueElem);

int main(void) {

    printf("Version 3.5 Beta\n");

    while (true) {

        int i = 1;

        printf("To enter a logical expression, use \"expression\"; to enter 1-sets, use \"sets\"\nEnter the function regime: ");

        char function_regime[FUNC_REGIME_LEN];
        fgets(function_regime, FUNC_REGIME_LEN, stdin);

        if (!validateInput(function_regime, FUNCTION_INPUT_REGIME, 0)) continue;
        function_regime[strcspn(function_regime, "\n")] = 0;

        if (!strcmp(function_regime, "sets")) {

            printf("Enter number of arguments: ");
            char NumArgs_str[NUM_ARGS_LEN];
            fgets(NumArgs_str, NUM_ARGS_LEN, stdin);
            if (!validateInput(NumArgs_str, NUM_ARGS_REGIME, 0)) continue;

            printf("Enter number of functions: ");
            char NumFunc_str[NUM_FUNCS_LEN];
            fgets(NumFunc_str, NUM_FUNCS_LEN, stdin);
            if (!validateInput(NumFunc_str, NUM_FUNCS_REGIME, 0)) continue;

            int NumArgs = atoi(NumArgs_str);
            int NumSets = 1 << NumArgs;
            int NumFuncs = atoi(NumFunc_str);

            while (i <= NumFuncs) {

                printf("\nData input for function y%d:\n", i);
                String ArraySets_str = read_dynamic_line(NumSets);
                if (!validateInput(ArraySets_str, ARRAY_SETS_REGIME, NumSets)) continue;

                size_t InputedSets = 0;
                intArray ArraySets = get_Array(ArraySets_str, &InputedSets);

                // input and analyze basis than work in 








                free(ArraySets_str);
                free(ArraySets);
                i++;

            }

        }

        else {}

    }

    return 0;

}

void clear_input_buffer() {
    int c;
    // Читаємо символи з stdin, доки не зустрінемо '\n' або кінець файлу (EOF)
    while ((c = getchar()) != '\n' && c != EOF);
}

bool validateInput(const String data, int flag, int optional_max) {

    switch (flag) {

        case FUNCTION_INPUT_REGIME:

            if (data == NULL) {

                fprintf(stderr, "Error: Input data pointer is NULL. Cannot proceed.\n\n");
                return false;
            }

            else if (strchr(data, '\n') == NULL) {

                fprintf(stderr, "Error: Overflow input. Max %d symbols.\n\n", FUNC_REGIME_LEN - 2);
                clear_input_buffer();
                return false;
            }

            else if (strcmp(data, "sets\n") && strcmp(data, "expression\n")) {

                fprintf(stderr, "Error: Incorect function regime.\n\n");
                return false;
            }

            return true;

        case NUM_FUNCS_REGIME:
        case NUM_ARGS_REGIME:

            if (data == NULL) {

                fprintf(stderr, "Error: Input data pointer is NULL. Cannot proceed.\n\n");
                return false;
            }

            else if (strchr(data, '\n') == NULL || !isdigit((unsigned char)data[0]) || data[0] == '0') {

                fprintf(stderr, "Error: The number %s must be a natural number less than or equal to 9.\n\n", flag == NUM_ARGS_REGIME ? "arguments" : "functions");
                if (strchr(data, '\n') == NULL) clear_input_buffer();
                return false;
            }

            return true;

        case ARRAY_SETS_REGIME:

            if (data == NULL) {

                fprintf(stderr, "Error: Input data pointer is NULL. Cannot proceed.\n\n");
                return false;
            }

            else if (!isdigit(data[0])) {

                fprintf(stderr, "Error: Input must start with a non-negative number.\n\n");
                return false;

            }

            else {

                size_t data_len = strlen(data);
                size_t comma_number = 1;
                size_t token_number = 0;

                for (size_t i = 0; data[i] != '\0'; i++) {

                    if (data[i] == ',') comma_number++;

                }

                // 1. Створюємо копію вхідного рядка, тому що strtok модифікує оригінал
                String data_copy = (String)malloc(strlen(data) + 1);
                if (data_copy == NULL) {
                    fprintf(stderr, "Error: Input data pointer is NULL. Cannot proceed.\n\n");
                    return false;
                }
                strcpy(data_copy, data);

                // 2. Розбиваємо рядок на токени за допомогою strtok.
                // Використовуємо " ," як роздільник для коректної обробки пробілів навколо ком.
                String token = strtok(data_copy, " ,");

                // 3. Перевірка, чи ввідний рядок був порожнім або містив лише роздільники
                bool found_any_number = false; // Прапорець, щоб відстежувати, чи знайшли ми хоча б одне число
                if (token == NULL && strlen(data) == 0) {
                    fprintf(stderr, "Error: Incorrect input. Does not contain numbers.\n");
                    free(data_copy);
                    return false;
                }

                // 4. Цикл для обробки кожного токена (підрядка, що представляє число)
                while (token != NULL) {

                    found_any_number = true; // Знайшли хоча б один токен, який не є NULL
                    token_number++;

                    long num_val;
                    String endptr;
                    errno = 0; // Скидаємо errno перед викликом strtol для перевірки помилок

                    // Перетворюємо токен (підрядок) на число типу long
                    num_val = strtol(token, &endptr, 10); // 10 означає десяткову систему числення

                    // 4.1. Валідація токена:
                    // Перевірка, чи strtol дійсно перетворила число (не порожній токен або нечислові символи на початку)
                    // та чи не залишилося зайвих символів після числа (наприклад, "123abc").
                    if (endptr == token || *endptr != '\0') {
                        fprintf(stderr, "Error: Incorrect input ('%s' isn't a natural number).\n", token);
                        free(data_copy);
                        return false;
                    }

                    // 4.2. Перевірка, чи число поміщається в `int` (якщо ви очікуєте, що воно буде int)
                    if (errno == ERANGE || (num_val < 0 || num_val >= optional_max)) {
                        fprintf(stderr, "Error: Invalid input. %s is outside the allowed range [0, %d]\n", token, optional_max - 1);
                        free(data_copy);
                        return false;
                    }

                    token = strtok(NULL, " ,"); // Переходимо до наступного токена
                }

                // 5. Фінальна перевірка: якщо рядок не був порожнім, але ми не знайшли жодного дійсного числа
                // (наприклад, ввід "   ,   " або "a,b,c" без чисел взагалі).
                // Якщо data_str_input не порожній, але found_any_number false, значить ввід був "лише роздільники"
                if (strlen(data) > 0 && !found_any_number) {
                    fprintf(stderr, "Error: Incorrect input. Does not contain numbers.\n");
                    free(data_copy);
                    return false;
                }

                else if (token_number != comma_number) {

                    fprintf(stderr, "Error: Incorrect input. Review it.\n");
                    free(data_copy);
                    return false;

                }

                free(data_copy); // Звільняємо копію вхідного рядка
                return true;      // Всі перевірки пройшли успішно

            }

        default:

            return false;

        }

}

String read_dynamic_line(int NumSets) {

    size_t initial_size = (size_t)NumSets;
    String buffer = (String)malloc(initial_size * sizeof(char));
    if (buffer == NULL) return NULL;

    int c;
    size_t current_size = initial_size;
    size_t index = 0;

    printf("Enter the numbers of sets separated by commas for which the function takes the value 1 (from 0 to %d): ", NumSets-1); // Додаємо підказку

    while ((c = getchar()) != '\n' && c != EOF) {

        if (index >= current_size - 1) { // Якщо буфер майже повний (залишилось місце тільки для '\0')
            current_size *= 2; // Збільшуємо розмір буфера вдвічі
            String new_buffer = (String)realloc(buffer, current_size * sizeof(char));
            if (new_buffer == NULL) {
                free(buffer);
                return NULL;
            }
            buffer = new_buffer;
        }
        buffer[index++] = (char)c;
    }
    buffer[index] = '\0'; // Додаємо нульовий термінатор

    // Оптимізація: Зменшити буфер до фактичного розміру, якщо потрібно
    if (index + 1 < current_size) {
        String final_buffer = (String)realloc(buffer, (index+1) * sizeof(char));

        // Якщо realloc вдалося зменшити
        if (final_buffer != NULL) buffer = final_buffer;

        // Якщо realloc не вдалося зменшити, продовжуємо використовувати старий буфер, але це не критично
    }

    return buffer;
}

intArray get_Array(const String strArray, size_t* uniqueElem) {

    size_t count = 1;

    for (size_t i = 0; strArray[i] != '\0'; i++) {

        if (strArray[i] == ',') count++;
    }

    size_t data_len = strlen(strArray);

    // Створюємо копію вхідного рядка, тому що strtok модифікує оригінал.
    // (+1 для нуль-термінатора)
    String strArray_copy = (String)malloc(data_len + 1);
    intArray result_array = (intArray)malloc(count * sizeof(int));

    if (strArray_copy == NULL) {
        fprintf(stderr, "Error: Failed to allocate memory for string copy.");
        free(strArray_copy);
        free(result_array);
        return NULL;
    }

    strcpy(strArray_copy, strArray);

    if (result_array == NULL) {
        fprintf(stderr, "Error: Malloc for array of integers.");
        free(strArray_copy);
        free(result_array);
        return NULL;
    }

    // Використовуємо " ," як роздільник для коректної обробки пробілів навколо ком та багаторазових пробілів.
    // strtok автоматично ігнорує багаторазові роздільники та початкові/кінцеві роздільники
    // (для початкових ми вже маємо валідацію, яка це відсікає).
    String token = strtok(strArray_copy, " ,"); // " " як роздільник для пробілів
    size_t index = 0;

    while (token != NULL) {

        bool addFlag = true;
        long num_val;
        String endptr;

        // errno = 0; // Можна не скидати, оскільки припускається валідований рядок
                     // і проблем з strtol не очікується.

        // Перетворюємо токен на число.
        // Оскільки рядок валідований, помилок перетворення не очікується.
        num_val = (int)strtol(token, &endptr, 10);

        for (size_t k = 0; k < index; k++) {

            if (result_array[k] == num_val) {
                addFlag = false;
                break;
            }

        }

        if (addFlag) {
            result_array[index] = (int)num_val; // Додаємо число до масиву
            index++;
        }
        token = strtok(NULL, " ,"); // Переходимо до наступного токена
    }

    if (index < count) {

        intArray Temp_result_array = (intArray)realloc(result_array, index*sizeof(int));

        if (Temp_result_array == NULL) {

            fprintf(stderr, "Error: Malloc error for temporary.");
            return NULL;
        }

        result_array = Temp_result_array;

    }

    *uniqueElem = index;

    free(strArray_copy); // Звільняємо копію вхідного рядка
    return result_array; // Повертаємо динамічний масив чисел

}
