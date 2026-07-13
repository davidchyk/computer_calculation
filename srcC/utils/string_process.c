#include "string_process.h"

string string_input(void) {

    string s = { NULL, 0u, 0u };

    size_t buffer_size = 128u;
    char* buffer = (char*)malloc(buffer_size);

    if (!buffer) {
        return s;
    }

    size_t length = 0u;
    int ch;

    while ((ch = getchar()) != '\n' && ch != EOF) {

        if (length + 1 >= buffer_size) {
            size_t new_buffer_size = buffer_size * 2u;
            char* new_buffer = (char*)realloc(buffer, new_buffer_size);
            if (!new_buffer) {
                free(buffer);
                return s;
            }
            buffer = new_buffer;
            buffer_size = new_buffer_size;
        }
        buffer[length++] = (char)ch;

    }

    buffer[length] = '\0';

    s.data = buffer;
    s.length = length;
    s.capacity = buffer_size - 1u; // Exclude the null terminator

    return s;
}

void string_free(string *s) {

    if (s == NULL) {
        return;
    }

    free(s->data);

    s->data = NULL;
    s->length = 0u;
    s->capacity = 0u;
}

bool string_to_decimal(const string* str, int* out_value) {

    char *end;
    long value;

    if (str == NULL || str->data == NULL || str->data[0] == '\0' || out_value == NULL) {
        return false;
    }

    errno = 0;
    value = strtol(str->data, &end, 10);

    // Якщо не було прочитано жодної цифри
    if (str->data == end) {
        return false;
    }

    // Пропускаємо пробіли в кінці
    while (isspace((unsigned char)*end)) {
        end++;
    }

    // Якщо після числа залишились зайві символи
    if (*end != '\0') {
        return false;
    }

    // Переповнення long
    if (errno == ERANGE) {
        return false;
    }

    // Перевірка меж int
    if (value < INT_MIN || value > INT_MAX) {
        return false;
    }

    *out_value = (int)value;
    return true;
}

bool append_string(string* main_string, const char* past_string) {

    int pasting_length = strlen(past_string);

    if (main_string->length + pasting_length + 1 > main_string->capacity) {

        size_t new_capacity = main_string->capacity + pasting_length + 1;
        char* new_data = (char*)realloc(main_string->data, new_capacity);

        if (!new_data) {
            return false;
        }

        main_string->data = new_data;
        main_string->capacity = new_capacity;

    }

    strcpy(main_string->data + main_string->length, past_string);

    main_string->length += pasting_length;

    return true;

}