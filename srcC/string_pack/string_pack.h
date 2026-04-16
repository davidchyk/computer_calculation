#ifndef STRING_PACK
#define STRING_PACK 1

#include <stdbool.h>

#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

/* Initialize every string with string_new, STRING_INIT, or string_init before use. */
typedef struct {

    char* data;
    size_t len;
    size_t capacity; /* excludes the trailing '\0' */

} string;

#define STRING_INIT { NULL, 0u, 0u }
#define STRING_NPOS ((size_t)-1)

static inline size_t string__max_size(void) {
    return (size_t)-2;
}

static inline bool string__add_overflows(size_t a, size_t b) {
    return a > string__max_size() - b;
}

static inline bool string__ptr_inside(const string* s, const char* ptr) {
    if (!s || !s->data || !ptr) {
        return false;
    }

#ifdef UINTPTR_MAX
    const uintptr_t begin = (uintptr_t)s->data;
    const uintptr_t value = (uintptr_t)ptr;
    const uintptr_t end = begin + s->len;

    if (end < begin) {
        return false;
    }

    return value >= begin && value <= end;
#else
    return ptr == s->data;
#endif
}

static inline string string_new(void) {
    string s = STRING_INIT;
    return s;
}

static inline void string_init(string* s) {
    if (!s) {
        return;
    }

    s->data = NULL;
    s->len = 0u;
    s->capacity = 0u;
}

static inline void string_free(string* s) {
    if (!s) {
        return;
    }

    free(s->data);
    string_init(s);
}

static inline const char* string_c_str(const string* s) {
    return (s && s->data) ? s->data : "";
}

static inline size_t string_length(const string* s) {
    return s ? s->len : 0u;
}

static inline size_t string_capacity(const string* s) {
    return s ? s->capacity : 0u;
}

static inline bool string_empty(const string* s) {
    return !s || s->len == 0u;
}

static inline bool string_reserve(string* s, size_t min_capacity) {
    if (!s || min_capacity > string__max_size()) {
        return false;
    }

    if (min_capacity <= s->capacity) {
        return true;
    }

    size_t next_capacity = s->capacity ? s->capacity : 16u;
    while (next_capacity < min_capacity) {
        if (next_capacity > string__max_size() / 2u) {
            next_capacity = min_capacity;
            break;
        }

        next_capacity *= 2u;
    }

    char* next_data = (char*)realloc(s->data, next_capacity + 1u);
    if (!next_data) {
        return false;
    }

    s->data = next_data;
    s->capacity = next_capacity;
    s->data[s->len] = '\0';
    return true;
}

static inline bool string_shrink_to_fit(string* s) {
    if (!s) {
        return false;
    }

    if (s->len == s->capacity) {
        return true;
    }

    if (s->len == 0u) {
        free(s->data);
        s->data = NULL;
        s->capacity = 0u;
        return true;
    }

    char* next_data = (char*)realloc(s->data, s->len + 1u);
    if (!next_data) {
        return false;
    }

    s->data = next_data;
    s->capacity = s->len;
    s->data[s->len] = '\0';
    return true;
}

static inline void string_clear(string* s) {
    if (!s) {
        return;
    }

    s->len = 0u;
    if (s->data) {
        s->data[0] = '\0';
    }
}

static inline bool string_assign_len(string* s, const char* data, size_t len) {
    if (!s || (!data && len != 0u) || len > string__max_size()) {
        return false;
    }

    if (len == 0u) {
        string_clear(s);
        return true;
    }

    if (string__ptr_inside(s, data)) {
        memmove(s->data, data, len);
        s->len = len;
        s->data[s->len] = '\0';
        return true;
    }

    if (!string_reserve(s, len)) {
        return false;
    }

    memcpy(s->data, data, len);
    s->len = len;
    s->data[s->len] = '\0';
    return true;
}

static inline bool string_assign_cstr(string* s, const char* cstr) {
    return string_assign_len(s, cstr ? cstr : "", cstr ? strlen(cstr) : 0u);
}

static inline bool string_assign_string(string* dst, const string* src) {
    if (!src) {
        return string_assign_cstr(dst, "");
    }

    if (dst == src) {
        return true;
    }

    return string_assign_len(dst, string_c_str(src), src->len);
}

static inline bool string_copy(string* dst, const string* src) {
    return string_assign_string(dst, src);
}

static inline bool string_resize(string* s, size_t new_len, char fill) {
    if (!s || new_len > string__max_size()) {
        return false;
    }

    if (new_len == 0u) {
        string_clear(s);
        return true;
    }

    if (!string_reserve(s, new_len)) {
        return false;
    }

    if (new_len > s->len) {
        memset(s->data + s->len, fill, new_len - s->len);
    }

    s->len = new_len;
    s->data[s->len] = '\0';
    return true;
}

static inline bool string_push_char(string* s, char ch) {
    if (!s || string__add_overflows(s->len, 1u)) {
        return false;
    }

    if (!string_reserve(s, s->len + 1u)) {
        return false;
    }

    s->data[s->len++] = ch;
    s->data[s->len] = '\0';
    return true;
}

static inline bool string_pop_char(string* s, char* out) {
    if (!s || s->len == 0u) {
        return false;
    }

    --s->len;
    if (out) {
        *out = s->data[s->len];
    }

    s->data[s->len] = '\0';
    return true;
}

static inline bool string_append_len(string* s, const char* data, size_t len) {
    if (!s || (!data && len != 0u) || string__add_overflows(s->len, len)) {
        return false;
    }

    if (len == 0u) {
        return true;
    }

    const bool source_inside = string__ptr_inside(s, data);
    size_t source_offset = 0u;
    if (source_inside) {
        source_offset = (size_t)(data - s->data);
    }

    const size_t old_len = s->len;
    if (!string_reserve(s, old_len + len)) {
        return false;
    }

    const char* source = source_inside ? s->data + source_offset : data;
    memmove(s->data + old_len, source, len);
    s->len = old_len + len;
    s->data[s->len] = '\0';
    return true;
}

static inline bool string_append_cstr(string* s, const char* cstr) {
    return string_append_len(s, cstr ? cstr : "", cstr ? strlen(cstr) : 0u);
}

static inline bool string_append_string(string* dst, const string* src) {
    if (!src) {
        return true;
    }

    return string_append_len(dst, string_c_str(src), src->len);
}

static inline bool string_insert_len(string* s, size_t pos, const char* data, size_t len) {
    if (!s || pos > s->len || (!data && len != 0u) || string__add_overflows(s->len, len)) {
        return false;
    }

    if (len == 0u) {
        return true;
    }

    char* temp = NULL;
    const char* source = data;
    if (string__ptr_inside(s, data)) {
        temp = (char*)malloc(len);
        if (!temp) {
            return false;
        }

        memcpy(temp, data, len);
        source = temp;
    }

    const size_t old_len = s->len;
    if (!string_reserve(s, old_len + len)) {
        free(temp);
        return false;
    }

    memmove(s->data + pos + len, s->data + pos, old_len - pos + 1u);
    memcpy(s->data + pos, source, len);
    s->len = old_len + len;
    free(temp);
    return true;
}

static inline bool string_insert_cstr(string* s, size_t pos, const char* cstr) {
    return string_insert_len(s, pos, cstr ? cstr : "", cstr ? strlen(cstr) : 0u);
}

static inline bool string_insert_string(string* dst, size_t pos, const string* src) {
    if (!src) {
        return true;
    }

    return string_insert_len(dst, pos, string_c_str(src), src->len);
}

static inline bool string_erase(string* s, size_t pos, size_t len) {
    if (!s || pos > s->len) {
        return false;
    }

    if (len == 0u) {
        return true;
    }

    if (len > s->len - pos) {
        len = s->len - pos;
    }

    if (len == 0u) {
        return true;
    }

    memmove(s->data + pos, s->data + pos + len, s->len - pos - len + 1u);
    s->len -= len;
    return true;
}

static inline bool string_replace_range(
    string* s,
    size_t pos,
    size_t remove_len,
    const char* data,
    size_t add_len
) {
    if (!s || pos > s->len || (!data && add_len != 0u)) {
        return false;
    }

    if (remove_len > s->len - pos) {
        remove_len = s->len - pos;
    }

    const size_t kept_len = s->len - remove_len;
    if (string__add_overflows(kept_len, add_len)) {
        return false;
    }

    char* temp = NULL;
    const char* source = data;
    if (add_len != 0u && string__ptr_inside(s, data)) {
        temp = (char*)malloc(add_len);
        if (!temp) {
            return false;
        }

        memcpy(temp, data, add_len);
        source = temp;
    }

    const size_t old_len = s->len;
    const size_t new_len = kept_len + add_len;
    if (new_len != 0u && !string_reserve(s, new_len)) {
        free(temp);
        return false;
    }

    const size_t tail_pos = pos + remove_len;
    const size_t tail_len = old_len - tail_pos;
    if (add_len != remove_len && tail_len != 0u) {
        memmove(s->data + pos + add_len, s->data + tail_pos, tail_len);
    }

    if (add_len != 0u) {
        memcpy(s->data + pos, source, add_len);
    }

    s->len = new_len;
    if (s->data) {
        s->data[s->len] = '\0';
    }

    free(temp);
    return true;
}

static inline bool string_replace_cstr(string* s, size_t pos, size_t remove_len, const char* cstr) {
    return string_replace_range(s, pos, remove_len, cstr ? cstr : "", cstr ? strlen(cstr) : 0u);
}

static inline int string_compare_len(const string* s, const char* data, size_t len) {
    if (!data && len != 0u) {
        return 1;
    }

    const char* left = string_c_str(s);
    const size_t left_len = string_length(s);
    const size_t common_len = left_len < len ? left_len : len;

    if (common_len != 0u) {
        const int cmp = memcmp(left, data ? data : "", common_len);
        if (cmp != 0) {
            return cmp < 0 ? -1 : 1;
        }
    }

    if (left_len == len) {
        return 0;
    }

    return left_len < len ? -1 : 1;
}

static inline int string_compare_cstr(const string* s, const char* cstr) {
    return string_compare_len(s, cstr ? cstr : "", cstr ? strlen(cstr) : 0u);
}

static inline int string_compare_string(const string* a, const string* b) {
    return string_compare_len(a, string_c_str(b), string_length(b));
}

static inline bool string_equals_len(const string* s, const char* data, size_t len) {
    return string_length(s) == len && string_compare_len(s, data, len) == 0;
}

static inline bool string_equals_cstr(const string* s, const char* cstr) {
    return string_equals_len(s, cstr ? cstr : "", cstr ? strlen(cstr) : 0u);
}

static inline bool string_equals_string(const string* a, const string* b) {
    return string_equals_len(a, string_c_str(b), string_length(b));
}

static inline size_t string_find_len(const string* s, const char* needle, size_t needle_len, size_t start) {
    const size_t haystack_len = string_length(s);
    const char* haystack = string_c_str(s);

    if (!needle && needle_len != 0u) {
        return STRING_NPOS;
    }

    if (start > haystack_len) {
        return STRING_NPOS;
    }

    if (needle_len == 0u) {
        return start;
    }

    if (needle_len > haystack_len - start) {
        return STRING_NPOS;
    }

    for (size_t i = start; i <= haystack_len - needle_len; ++i) {
        if (memcmp(haystack + i, needle, needle_len) == 0) {
            return i;
        }
    }

    return STRING_NPOS;
}

static inline size_t string_find_cstr(const string* s, const char* needle, size_t start) {
    return string_find_len(s, needle ? needle : "", needle ? strlen(needle) : 0u, start);
}

static inline bool string_contains_cstr(const string* s, const char* needle) {
    return string_find_cstr(s, needle, 0u) != STRING_NPOS;
}

static inline bool string_replace_all_cstr(string* s, const char* needle, const char* replacement) {
    if (!s || !needle || needle[0] == '\0') {
        return false;
    }

    const size_t needle_len = strlen(needle);
    const char* replacement_text = replacement ? replacement : "";
    const size_t replacement_len = strlen(replacement_text);
    size_t pos = 0u;

    while ((pos = string_find_len(s, needle, needle_len, pos)) != STRING_NPOS) {
        if (!string_replace_range(s, pos, needle_len, replacement_text, replacement_len)) {
            return false;
        }

        pos += replacement_len;
    }

    return true;
}

static inline bool string_starts_with_len(const string* s, const char* prefix, size_t prefix_len) {
    if (prefix_len > string_length(s) || (!prefix && prefix_len != 0u)) {
        return false;
    }

    return prefix_len == 0u || memcmp(string_c_str(s), prefix, prefix_len) == 0;
}

static inline bool string_starts_with_cstr(const string* s, const char* prefix) {
    return string_starts_with_len(s, prefix ? prefix : "", prefix ? strlen(prefix) : 0u);
}

static inline bool string_ends_with_len(const string* s, const char* suffix, size_t suffix_len) {
    const size_t len = string_length(s);
    if (suffix_len > len || (!suffix && suffix_len != 0u)) {
        return false;
    }

    return suffix_len == 0u || memcmp(string_c_str(s) + len - suffix_len, suffix, suffix_len) == 0;
}

static inline bool string_ends_with_cstr(const string* s, const char* suffix) {
    return string_ends_with_len(s, suffix ? suffix : "", suffix ? strlen(suffix) : 0u);
}

static inline bool string_substr(const string* s, size_t pos, size_t len, string* out) {
    if (!s || !out || pos > s->len) {
        return false;
    }

    if (len > s->len - pos) {
        len = s->len - pos;
    }

    return string_assign_len(out, string_c_str(s) + pos, len);
}

static inline char string_at(const string* s, size_t index) {
    return (s && index < s->len) ? s->data[index] : '\0';
}

static inline bool string_set_at(string* s, size_t index, char ch) {
    if (!s || index >= s->len) {
        return false;
    }

    s->data[index] = ch;
    return true;
}

static inline void string_swap(string* a, string* b) {
    if (!a || !b || a == b) {
        return;
    }

    const string temp = *a;
    *a = *b;
    *b = temp;
}

static inline bool string_read_line_from(FILE* input, string* out) {
    if (!input || !out) {
        return false;
    }

    string line = string_new();
    int ch = 0;

    while ((ch = fgetc(input)) != EOF) {
        if (ch == '\n') {
            break;
        }

        if (ch == '\r') {
            const int next = fgetc(input);
            if (next != '\n' && next != EOF) {
                ungetc(next, input);
            }
            break;
        }

        if (!string_push_char(&line, (char)ch)) {
            string_free(&line);
            return false;
        }
    }

    if (ch == EOF && string_empty(&line)) {
        string_free(&line);
        return false;
    }

    string_swap(out, &line);
    string_free(&line);
    return true;
}

static inline bool string_read_line(string* out) {
    return string_read_line_from(stdin, out);
}

#endif
