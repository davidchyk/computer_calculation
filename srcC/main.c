#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#include "string_pack/string_pack.h"

bool get_digit_1_to_9(const char* prompt, uint8_t* out) {

    if (!out || !prompt) {
        return false;
    }

    while (true) {

        printf("%s", prompt);
        fflush(stdout);

        string temp_str = string_new();
        if (!string_read_line(&temp_str)) {
            fprintf(stderr, "Input error\n");
            string_free(&temp_str);
            return false;
        }

        if (string_length(&temp_str) == 1) {

            char ch = string_at(&temp_str, 0);

            if (ch >= '1' && ch <= '9') {

                *out = (uint8_t)(ch - '0');
                string_free(&temp_str);
                return true;

            }

        }

        string_free(&temp_str);
        printf("Incorrect input!\n");

    }

}

int main(void) {

    printf("Version 3.5 Beta (C realization)\n");

    while (true) {

        /*
        TODO:
            tmp_obj = tempfile.TemporaryDirectory()
            temp_dir = tmp_obj.name
        */

        uint8_t i = 1; // for indexing inputs

        printf("Enter mode: [E]xpression or [S]ets: ");
        fflush(stdout);

        string regime = string_new();
        if (!string_read_line(&regime)) {
            fprintf(stderr, "Input error\n");
            string_free(&regime);
            return 1;
        }

        if (string_equals_cstr(&regime, "S")) {

            // Sets mode

            uint8_t num_functions = 0;
            if (!get_digit_1_to_9("[Sets Mode] Input num of functions to analyze (max 9): ", &num_functions)) {
                string_free(&regime);
                return 1;
            }

            uint8_t num_args = 0;
            if (!get_digit_1_to_9("[Sets Mode] Input num of args (max 9): ", &num_args)) {
                string_free(&regime);
                return 1;
            }

            while (i <= num_functions) {

                printf("Enter data for function F%u:\n", (unsigned)i);

                // to continue

                i++;

            }

























        }

        else if (string_equals_cstr(&regime, "E")) {

            // Function mode

            printf("You are in Exp Mode!\n");

        }

        else {
    
            printf("You entered incorrect mode\n");

        }

        string_free(&regime);

    }

    return 0;

}