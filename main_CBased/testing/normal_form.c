#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char **structure;
    int type;
    const char *way[2];
    char in_sign;
    char out_sign;
    bool in_not;
    bool out_not;
    bool reverse;
} NormalForm;

// Ініціалізація NormalForm
NormalForm *initNormalForm(char **structure, int type, const char *way[2]) {
    NormalForm *nf = (NormalForm *)malloc(sizeof(NormalForm));
    if (!nf) {
        printf("Memory allocation failed");
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }
    nf->structure = structure;
    nf->type = type;
    nf->way[0] = way[0];
    nf->way[1] = way[1];
    nf->in_sign = '\0';
    nf->out_sign = '\0';
    nf->in_not = false;
    nf->out_not = false;
    nf->reverse = false;
    return nf;
}

// Визначення властивостей NormalForm
void defineNormalForm(NormalForm *nf) {

    if (nf->type == 1) {

        if (strcmp(nf->way[0], "І") == 0 && strcmp(nf->way[1], "АБО") == 0) {
            nf->in_sign = '^';
            nf->out_sign = 'v';
            nf->in_not = false;
            nf->out_not = false;

        } else if (strcmp(nf->way[0], "І-НЕ") == 0 && strcmp(nf->way[1], "І-НЕ") == 0) {
            nf->in_sign = '^';
            nf->out_sign = '^';
            nf->in_not = true;
            nf->out_not = true;

        } else if (strcmp(nf->way[0], "АБО") == 0 && strcmp(nf->way[1], "І-НЕ") == 0) {
            nf->in_sign = 'v';
            nf->out_sign = '^';
            nf->in_not = false;
            nf->out_not = true;
            nf->reverse = true;

        } else if (strcmp(nf->way[0], "АБО-НЕ") == 0 && strcmp(nf->way[1], "АБО") == 0) {
            nf->in_sign = 'v';
            nf->out_sign = 'v';
            nf->in_not = true;
            nf->out_not = false;
            nf->reverse = true;

        }
    } else {
        if (strcmp(nf->way[0], "АБО") == 0 && strcmp(nf->way[1], "І") == 0) {
            nf->in_sign = 'v';
            nf->out_sign = '^';
            nf->in_not = false;
            nf->out_not = false;

        } else if (strcmp(nf->way[0], "АБО-НЕ") == 0 && strcmp(nf->way[1], "АБО-НЕ") == 0) {
            nf->in_sign = 'v';
            nf->out_sign = 'v';
            nf->in_not = true;
            nf->out_not = true;

        } else if (strcmp(nf->way[0], "І") == 0 && strcmp(nf->way[1], "АБО-НЕ") == 0) {
            nf->in_sign = '^';
            nf->out_sign = 'v';
            nf->in_not = false;
            nf->out_not = true;
            nf->reverse = true;

        } else if (strcmp(nf->way[0], "І-НЕ") == 0 && strcmp(nf->way[1], "І") == 0) {
            nf->in_sign = '^';
            nf->out_sign = '^';
            nf->in_not = true;
            nf->out_not = false;
            nf->reverse = true;

        }

    }

    if (nf->reverse) {

        for (int i = 0; nf->structure[i] != NULL; i++) {

            size_t length = strlen(nf->structure[i]);

            for (size_t j = 0; j < length; j++) {

                if (nf->structure[i][j] == '1') {
                    nf->structure[i][j] = '0';
                } else if (nf->structure[i][j] == '0') {
                    nf->structure[i][j] = '1';
                } else {
                    printf("Error: Unexpected character '%c' in structure[%d][%zu]\n", nf->structure[i][j], i, j);
                    break;
                }

            }

        }

    }

}

// Виведення NormalForm
void printNormalForm(NormalForm *nf) {
    if (nf->out_not) {
        printf("not("); // Відкриваємо not для всього виразу
    }

    for (int i = 0; nf->structure[i] != NULL; i++) {
        if (nf->in_not) {
            printf("not"); // Додаємо not перед кожним термом, якщо in_not
        }
        printf("(");
        for (int j = 0; nf->structure[i][j] != '\0'; j++) {
            printf("%c", nf->structure[i][j]); // Друкуємо символ
            if (nf->structure[i][j + 1] != '\0') {
                printf(" %c ", nf->in_sign); // Додаємо in_sign між символами
            }
        }
        printf(")");
        if (nf->structure[i + 1] != NULL) {
            printf(" %c ", nf->out_sign); // Додаємо out_sign між термами
        }
    }

    if (nf->out_not) {
        printf(")"); // Закриваємо not для всього виразу
    }

    printf("\n");
}

// Основна функція
int main() {

    char structure_0[] = "110";
    char structure_1[] = "101";
    char *structure[] = {structure_0, structure_1, NULL};
    const char *way[] = {"І-НЕ", "І"};

    NormalForm *nf = initNormalForm(structure, 0, way);
    defineNormalForm(nf);
    printNormalForm(nf);

    free(nf);
    return 0;
}