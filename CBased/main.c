#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>   // Для isdigit
#include <stdlib.h>
#include <errno.h>    // Для errno, ERANGE
#include <limits.h>   // Для INT_MAX, INT_MIN

#define str char*

#define FUNC_REGIME_LEN 20+2
#define NUM_ARGS_LEN 3
#define NUM_FUNCS_LEN 3

#define FUNCTION_INPUT_REGIME 0
#define NUM_ARGS_REGIME 1
#define NUM_FUNCS_REGIME 2
#define ARRAY_SETS_REGIME 3

#define _CRT_SECURE_NO_WARNINGS 1

str db[][2] = {
    {"AND", "OR"}, {"AND-NOT", "AND-NOT"}, {"OR", "AND-NOT"}, {"OR-NOT", "OR"},
    {"OR", "AND"}, {"OR-NOT", "OR-NOT"}, {"AND", "OR-NOT"}, {"AND-NOT", "AND"}
};

void clear_input_buffer();

bool validateInput(const str data, int flag, int optional_max);

str read_dynamic_line(int NumSets);

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
                str ArraySets = read_dynamic_line(NumSets);
                if (!validateInput(ArraySets, ARRAY_SETS_REGIME, NumSets)) continue;

                




                free(ArraySets);
                i++;

            }

        }

        else {



        }

    }

    return 0;

}

void clear_input_buffer() {
    int c;
    // Читаємо символи з stdin, доки не зустрінемо '\n' або кінець файлу (EOF)
    while ((c = getchar()) != '\n' && c != EOF);
}

bool validateInput(const str data, int flag, int optional_max) {

    switch (flag) {

        case FUNCTION_INPUT_REGIME:

            if (data == NULL) {

                printf("Error: NULL\n\n");
                return false;
            }

            else if (strchr(data, '\n') == NULL) {

                printf("Overflow input: max %d symbols\n\n", FUNC_REGIME_LEN - 2);
                clear_input_buffer();
                return false;
            }

            else if (strcmp(data, "sets\n") && strcmp(data, "expression\n")) {

                printf("Incorect function regime\n\n");
                return false;
            }

            else return true;

        case NUM_FUNCS_REGIME:
        case NUM_ARGS_REGIME:

            if (data == NULL) {

                printf("Error: NULL\n\n");
                return false;
            }

            else if (strchr(data, '\n') == NULL || !isdigit((unsigned char)data[0]) || data[0] == '0') {

                printf("The number of %s must be a natural number less than or equal to 9\n\n", flag == 1 ? "arguments" : "functions");
                if (strchr(data, '\n') == NULL) clear_input_buffer();
                return false;
            }

            else return true;

        case ARRAY_SETS_REGIME:

            // TODO

            if (data == NULL) {

                printf("Error: NULL\n\n");
                return false;
            }

            else {

                size_t data_len = strlen(data);

                // 1. Створюємо копію вхідного рядка, тому що strtok модифікує оригінал
                str data_copy = (str)malloc(strlen(data) + 1);
                if (data_copy == NULL) {
                    printf("Error: NULL\n\n");
                    return false;
                }
                strcpy(data_copy, data);

                // 2. Розбиваємо рядок на токени за допомогою strtok.
                // Використовуємо " ," як роздільник для коректної обробки пробілів навколо ком.
                str token = strtok(data_copy, ", ");

                size_t first_non_whitespace_idx = 0;
                while (first_non_whitespace_idx < data_len && isspace(data[first_non_whitespace_idx])) {
                    first_non_whitespace_idx++;
                }

                // 3. Перевірка, чи ввідний рядок був порожнім або містив лише роздільники
                bool found_any_number = false; // Прапорець, щоб відстежувати, чи знайшли ми хоча б одне число
                if (token == NULL && strlen(data) == 0) {
                    printf("Inorrect input\n");
                    free(data_copy);
                    return false;
                }

                // 4. Цикл для обробки кожного токена (підрядка, що представляє число)
                while (token != NULL) {

                    found_any_number = true; // Знайшли хоча б один токен, який не є NULL

                    long num_val;
                    str endptr;
                    errno = 0; // Скидаємо errno перед викликом strtol для перевірки помилок

                    // Перетворюємо токен (підрядок) на число типу long
                    num_val = strtol(token, &endptr, 10); // 10 означає десяткову систему числення

                    // 4.1. Валідація токена:
                    // Перевірка, чи strtol дійсно перетворила число (не порожній токен або нечислові символи на початку)
                    // та чи не залишилося зайвих символів після числа (наприклад, "123abc").
                    if (endptr == token || *endptr != '\0') {
                        printf("Incorrect input: '%s' isn't a natural number\n", token);
                        free(data_copy);
                        return false;
                    }

                    // 4.2. Перевірка, чи число поміщається в `int` (якщо ви очікуєте, що воно буде int)
                    if (errno == ERANGE || (num_val < 0 || num_val >= optional_max)) {
                        printf("Invalid input: '%s' is outside the allowed range [0, %d]\n", token, optional_max - 1);
                        free(data_copy);
                        return false;
                    }

                    token = strtok(NULL, ", "); // Переходимо до наступного токена
                }

                // 5. Фінальна перевірка: якщо рядок не був порожнім, але ми не знайшли жодного дійсного числа
                // (наприклад, ввід "   ,   " або "a,b,c" без чисел взагалі).
                // Якщо data_str_input не порожній, але found_any_number false, значить ввід був "лише роздільники"
                if (strlen(data) > 0 && !found_any_number) {
                    printf("Incorrect input: no valid number found\n");
                    free(data_copy);
                    return false;
                }

                free(data_copy); // Звільняємо копію вхідного рядка
                return true;      // Всі перевірки пройшли успішно

            }

        default:

            return false;
            break;

        }

}

str read_dynamic_line(int NumSets) {

    size_t initial_size = (size_t)NumSets;
    str buffer = (str)malloc(initial_size * sizeof(char));
    if (buffer == NULL) return NULL;

    int c;
    size_t current_size = initial_size;
    size_t index = 0;

    printf("Enter the numbers of sets separated by commas for which the function takes the value 1 (from 0 to %d): ", NumSets-1); // Додаємо підказку

    while ((c = getchar()) != '\n' && c != EOF) {

        if (index >= current_size - 1) { // Якщо буфер майже повний (залишилось місце тільки для '\0')
            current_size *= 2; // Збільшуємо розмір буфера вдвічі
            str new_buffer = (str)realloc(buffer, current_size * sizeof(char));
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
        str final_buffer = (str)realloc(buffer, (index + 1) * sizeof(char));

        // Якщо realloc вдалося зменшити
        if (final_buffer != NULL) buffer = final_buffer;

        // Якщо realloc не вдалося зменшити, продовжуємо використовувати старий буфер, але це не критично
    }

    return buffer;
}