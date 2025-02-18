#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

typedef struct {
    char *result;
    int type;
    char **db;
} BasicResult;

typedef struct {
    BasicResult *basic_result;
    char *normal_form;
} NormalResult;

char *intToBinary(int num, int bits) {
    char *binary = malloc((bits + 1) * sizeof(char));
    if (!binary) {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }
    binary[bits] = '\0';
    for (int i = bits - 1; i >= 0; i--) {
        binary[i] = (num & 1) ? '1' : '0';
        num >>= 1;
    }
    return binary;
}

BasicResult *basic(int *sets_number, int sets_size, int type, int num_of_args) {
    BasicResult *result = malloc(sizeof(BasicResult));
    if (!result) {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }
    result->result = NULL;
    result->type = type;
    result->db = malloc(sets_size * sizeof(char *));
    if (!result->db) {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }

    size_t result_size = 256;
    result->result = malloc(result_size * sizeof(char));
    if (!result->result) {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }
    result->result[0] = '\0';

    if (type == 1) {
        for (int i = 0; i < sets_size; i++) {
            result->db[i] = intToBinary(sets_number[i], num_of_args);
        }

        for (int i = 0; i < sets_size; i++) {
            char temp[64] = "";

            for (int j = 0; j < num_of_args; j++) {
                char buffer[4];
                snprintf(buffer, sizeof(buffer), "%c ^ ", result->db[i][j]);
                strcat(temp, buffer);
            }
            temp[strlen(temp) - 3] = '\0'; // Remove the last ^

            char buffer[128];
            snprintf(buffer, sizeof(buffer), "(%s) v ", temp);
            strcat(result->result, buffer);
        }
        result->result[strlen(result->result) - 3] = '\0'; // Remove the last v

    } else {
        int total_combinations = (int)pow(2, num_of_args);
        int excluded_size = total_combinations - sets_size;

        char **time_db = malloc(excluded_size * sizeof(char *));
        if (!time_db) {
            perror("Memory allocation failed");
            exit(EXIT_FAILURE);
        }

        int index = 0;
        for (int i = 0; i < total_combinations; i++) {
            bool found = false;
            for (int j = 0; j < sets_size; j++) {
                if (i == sets_number[j]) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                time_db[index++] = intToBinary(i, num_of_args);
            }
        }

        for (int i = 0; i < excluded_size; i++) {
            for (int j = 0; j < num_of_args; j++) {
                if (time_db[i][j] == '1') {
                    time_db[i][j] = '0';
                } else {
                    time_db[i][j] = '1';
                }
            }
            result->db[i] = strdup(time_db[i]);
        }

        for (int i = 0; i < sets_size; i++) {
            char temp[128] = ""; // Виділяємо достатньо пам'яті для одного терма

            for (int j = 0; j < num_of_args; j++) {
                char buffer[8];
                snprintf(buffer, sizeof(buffer), "%c", result->db[i][j]); // Додаємо символ (0 або 1)
                strcat(temp, buffer);

                if (j < num_of_args - 1) {
                    strcat(temp, type == 1 ? " ^ " : " v "); // Додаємо ^ або v між аргументами
                }
            }

            char buffer[128];
            snprintf(buffer, sizeof(buffer), "(%s)", temp); // Обгортаємо терм у дужки
            strcat(result->result, buffer);

            if (i < sets_size - 1) {
                strcat(result->result, type == 1 ? " v " : " ^ "); // Додаємо v або ^ між термами
            }
        }

        result->result[strlen(result->result) - 3] = '\0'; // Remove the last ^

        for (int i = 0; i < excluded_size; i++) {
            free(time_db[i]);
        }
        free(time_db);
    }

    return result;
}

void freeBasicResult(BasicResult *result, int sets_size) {
    if (!result) return;
    for (int i = 0; i < sets_size; i++) {
        free(result->db[i]);
    }
    free(result->db);
    free(result->result);
    free(result);
}

NormalResult *normal(int *sets_number, int sets_size, int num_of_args, const char *basis, bool mini) {
    NormalResult *result = malloc(sizeof(NormalResult));
    if (!result) {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }
    result->basic_result = NULL;
    result->normal_form = NULL;

    if (mini) {
        // Simplified version for mini
        result->basic_result = basic(sets_number, sets_size, 1, num_of_args);
        result->normal_form = strdup(result->basic_result->result);
    } else {
        BasicResult *ddnf = basic(sets_number, sets_size, 1, num_of_args); // ДДНФ
        BasicResult *dknf = basic(sets_number, sets_size, 0, num_of_args); // ДКНФ

        size_t combined_size = strlen(ddnf->result) + strlen(dknf->result) + 128;
        result->normal_form = malloc(combined_size * sizeof(char));
        if (!result->normal_form) {
            perror("Memory allocation failed");
            exit(EXIT_FAILURE);
        }

        snprintf(result->normal_form, combined_size, "DDNF: %s\nDKNF: %s", ddnf->result, dknf->result);

        freeBasicResult(ddnf, sets_size);
        freeBasicResult(dknf, sets_size);
    }

    return result;
}

void freeNormalResult(NormalResult *result, int sets_size) {
    if (!result) return;
    if (result->basic_result) {
        freeBasicResult(result->basic_result, sets_size);
    }
    if (result->normal_form) {
        free(result->normal_form);
    }
    free(result);
}

int main() {
    int sets_number[] = {1, 2};
    int sets_size = sizeof(sets_number) / sizeof(sets_number[0]);
    int num_of_args = 3;
    const char *basis = "І";

    NormalResult *result = normal(sets_number, sets_size, num_of_args, basis, false);

    printf("Normal Form:\n%s\n", result->normal_form);

    freeNormalResult(result, sets_size);

    return 0;
}
