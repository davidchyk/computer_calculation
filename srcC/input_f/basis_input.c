#include "basis_input.h"

#include "../typing.h"
#include "../string_process/string_process.h"

#include <ctype.h>
#include <stdio.h>
#include <string.h>

static void skip_spaces(const char **p) {

    while (isspace((unsigned char)**p)) {
        (*p)++;
    }

}

static bool parse_number_1_to_9(const char **p, int *out_number) {

    skip_spaces(p);

    if (**p < '1' || **p > '9') {
        return false;
    }

    *out_number = **p - '0';
    (*p)++;

    if (isdigit((unsigned char)**p)) {
        return false;
    }

    return true;
}

static bool parse_form_without_leading_space(const char **p, logical_form *out_form) {

    if (!isalpha((unsigned char)**p)) {
        return false;
    }

    char word[16];
    int length = 0;

    while (isalpha((unsigned char)**p)) {
        if (length >= 15) {
            return false;
        }

        word[length] = (char)toupper((unsigned char)**p);
        length++;
        (*p)++;
    }

    word[length] = '\0';

    if (strcmp(word, "AND") == 0) {
        *out_form = FORM_AND;
        return true;
    }

    if (strcmp(word, "OR") == 0) {
        *out_form = FORM_OR;
        return true;
    }

    if (strcmp(word, "NOR") == 0) {
        *out_form = FORM_NOR;
        return true;
    }

    if (strcmp(word, "NAND") == 0) {
        *out_form = FORM_NAND;
        return true;
    }

    return false;
}

static bool map_forms_to_basis(logical_form first, logical_form second, basisType *out_basis) {

    if (first == FORM_AND && second == FORM_OR) {
        *out_basis = AND_OR;
        return true;
    }

    if (first == FORM_NAND && second == FORM_NAND) {
        *out_basis = NAND_NAND;
        return true;
    }

    if (first == FORM_OR && second == FORM_NAND) {
        *out_basis = OR_NAND;
        return true;
    }

    if (first == FORM_NOR && second == FORM_OR) {
        *out_basis = NOR_OR;
        return true;
    }

    if (first == FORM_OR && second == FORM_AND) {
        *out_basis = OR_AND;
        return true;
    }

    if (first == FORM_NOR && second == FORM_NOR) {
        *out_basis = NOR_NOR;
        return true;
    }

    if (first == FORM_AND && second == FORM_NOR) {
        *out_basis = AND_NOR;
        return true;
    }

    if (first == FORM_NAND && second == FORM_AND) {
        *out_basis = NAND_AND;
        return true;
    }

    return false;
}

void basis_inputing(Function_Data* function) {

    if (function == NULL) {
        printf(
            ERROR(
                "\t[Basis Inputing] [Error] Function data is not initialized.\n"
            )
        );
        return;
    }

    while (true) {

        printf("\t[Basis Inputing] Basis for function F%d: ", function->index);

        fflush(stdout);
        string basis_input = string_input();

        if (basis_input.data == NULL) {
            printf(
                ERROR(
                    "\t[Basis Inputing] [Error] Failed to read basis input.\n"
                )
            );
            return;
        }

        else if (!strcmp(basis_input.data, "all")) {

            printf(
                TIP(
                    "\t[Basis Inputing] Avaliable basis form (without input-numbers):\n"
                    "\t\tAND/OR\n"
                    "\t\tNAND/NAND\n"
                    "\t\tOR/NAND\n"
                    "\t\tNOR/OR\n"
                    "\t\tOR/AND\n"
                    "\t\tNOR/NOR\n"
                    "\t\tAND/NOR\n"
                    "\t\tNAND/AND\n"
                )
            );

            string_free(&basis_input);
            continue;

        }

        const char *p = basis_input.data;

        int first_number = 0;
        int second_number = 0;

        logical_form first_form;
        logical_form second_form;

        basisType basis;
        bool is_valid = true;

        if (!parse_number_1_to_9(&p, &first_number)) {
            is_valid = false;
        }

        if (is_valid && !parse_form_without_leading_space(&p, &first_form)) {
            is_valid = false;
        }

        if (is_valid) {
            skip_spaces(&p);

            if (*p != '/') {
                is_valid = false;
            }
        }

        if (is_valid) {
            p++;
        }

        if (is_valid && !parse_number_1_to_9(&p, &second_number)) {
            is_valid = false;
        }

        if (is_valid && !parse_form_without_leading_space(&p, &second_form)) {
            is_valid = false;
        }

        if (is_valid) {
            skip_spaces(&p);

            if (*p != '\0') {
                is_valid = false;
            }
        }

        if (is_valid && !map_forms_to_basis(first_form, second_form, &basis)) {
            is_valid = false;
        }

        if (is_valid) {
            function->first_basisNumber = first_number;
            function->second_basisNumber = second_number;
            function->basis = basis;
            function->firstForm = first_form;
            function->secondForm = second_form;

            string_free(&basis_input);
            return;
        }

        printf(
            ERROR(
                "\t[Basis Inputing] [Error] Invalid basis input: \"%s\". Use format like 3AND/2OR or check avaliable basis by enter \"all\".\n"
            ),
            basis_input.data != NULL ? basis_input.data : ""
        );

        string_free(&basis_input);
    }
}
