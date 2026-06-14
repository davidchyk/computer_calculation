#include "expression_input.h"
#include "../string_process/string_process.h"

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

typedef enum {
    NODE_VAR,
    NODE_NOT,
    NODE_AND,
    NODE_OR
} NodeType;

typedef struct Node {
    NodeType type;
    char* name;
    struct Node *left;
    struct Node *right;
} Node;

typedef struct {
    const string s;
    size_t pos;
    bool error;
} Parser;

static void ast_free(Node *node) {

    if (node == NULL) {
        return;
    }

    ast_free(node->left);
    ast_free(node->right);

    free(node->name);
    free(node);

}

static Node *parse_expr(Parser *p, int min_precedence) {

    while (isspace((unsigned char)p->s.data[p->pos])) {
        p->pos++;
    }

    Node *left = NULL;
    char ch = p->s.data[p->pos];

    if (ch == '~') {

        p->pos++;

        Node *child = parse_expr(p, 3);

        if (child == NULL) {
            return NULL;
        }

        left = malloc(sizeof(Node));

        if (left == NULL) {
            ast_free(child);
            p->error = true;
            return NULL;
        }

        left->type = NODE_NOT;
        left->name = NULL;
        left->left = child;
        left->right = NULL;
    }

    else if (ch == '(') {

        p->pos++;

        left = parse_expr(p, 1);

        if (left == NULL) {
            return NULL;
        }

        while (isspace((unsigned char)p->s.data[p->pos])) {
            p->pos++;
        }

        if (p->s.data[p->pos] != ')') {
            ast_free(left);
            p->error = true;
            return NULL;
        }

        p->pos++;
    }

    else if (IS_LATIN(ch)) {

        size_t start = p->pos;

        while (IS_LATIN(p->s.data[p->pos])) {
            p->pos++;
        }

        while (isdigit((unsigned char)p->s.data[p->pos])) {
            p->pos++;
        }

        size_t length = p->pos - start;

        char *name = malloc(length + 1);

        if (name == NULL) {
            p->error = true;
            return NULL;
        }

        for (size_t i = 0; i < length; i++) {
            name[i] = (char)toupper((unsigned char)p->s.data[start + i]);
        }

        name[length] = '\0';

        left = malloc(sizeof(Node));

        if (left == NULL) {
            free(name);
            p->error = true;
            return NULL;
        }

        left->type = NODE_VAR;
        left->name = name;
        left->left = NULL;
        left->right = NULL;
    }

    else {
        p->error = true;
        return NULL;
    }

    while (true) {

        while (isspace((unsigned char)p->s.data[p->pos])) {
            p->pos++;
        }

        char op = p->s.data[p->pos];

        int precedence = 0;

        if (op == '|') {
            precedence = 1;
        } else if (op == '&') {
            precedence = 2;
        } else {
            break;
        }

        if (precedence < min_precedence) {
            break;
        }

        p->pos++;

        Node *right = parse_expr(p, precedence + 1);

        if (right == NULL) {
            ast_free(left);
            return NULL;
        }

        Node *parent = malloc(sizeof(Node));

        if (parent == NULL) {
            ast_free(left);
            ast_free(right);
            p->error = true;
            return NULL;
        }

        parent->type = (op == '&') ? NODE_AND : NODE_OR;
        parent->name = NULL;
        parent->left = left;
        parent->right = right;

        left = parent;
    }

    return left;
}

static bool collect_variables(Node *node, char ***vars, int *count, int *capacity) {

    if (node == NULL) {
        return true;
    }

    if (node->type == NODE_VAR) {
        for (int i = 0; i < *count; i++) {
            if (strcmp((*vars)[i], node->name) == 0) {
                return true;
            }
        }

        if (*count >= *capacity) {
            int new_capacity = (*capacity == 0) ? 4 : (*capacity * 2);

            char **tmp = realloc(*vars, new_capacity * sizeof(char *));

            if (tmp == NULL) {
                return false;
            }

            *vars = tmp;
            *capacity = new_capacity;
        }

        size_t length = strlen(node->name);

        (*vars)[*count] = malloc(length + 1);

        if ((*vars)[*count] == NULL) {
            return false;
        }

        memcpy((*vars)[*count], node->name, length + 1);

        (*count)++;

        return true;
    }

    return collect_variables(node->left, vars, count, capacity) &&
           collect_variables(node->right, vars, count, capacity);
}

static int variable_compare(const void* a, const void* b) {

    const char *left = *(const char **)a;
    const char *right = *(const char **)b;

    size_t left_letters_len = 0;
    size_t right_letters_len = 0;

    while (IS_LATIN(left[left_letters_len])) {
        left_letters_len++;
    }

    while (IS_LATIN(right[right_letters_len])) {
        right_letters_len++;
    }

    size_t min_len = left_letters_len < right_letters_len
        ? left_letters_len
        : right_letters_len;

    int letters_cmp = strncmp(left, right, min_len);

    if (letters_cmp != 0) {
        return letters_cmp;
    }

    if (left_letters_len != right_letters_len) {
        return left_letters_len < right_letters_len ? -1 : 1;
    }

    int left_number = left[left_letters_len] == '\0'
        ? -1
        : atoi(left + left_letters_len);

    int right_number = right[right_letters_len] == '\0'
        ? -1
        : atoi(right + right_letters_len);

    return right_number - left_number;
}

static void free_vars(char **vars, int vars_count) {

    if (vars == NULL) {
        return;
    }

    for (int i = 0; i < vars_count; i++) {
        free(vars[i]);
    }

    free(vars);
}

static bool eval_ast(Node *node, char **vars, int vars_count, int decimal_set) {

    switch (node->type) {
        case NODE_VAR: {
            int index = -1;

            for (int i = 0; i < vars_count; i++) {
                if (strcmp(vars[i], node->name) == 0) {
                    index = i;
                    break;
                }
            }

            if (index < 0) {
                return false;
            }

            int bit_index = vars_count - 1 - index;

            return ((decimal_set >> bit_index) & 1) != 0;
        }

        case NODE_NOT:
            return !eval_ast(node->left, vars, vars_count, decimal_set);

        case NODE_AND:
            return eval_ast(node->left, vars, vars_count, decimal_set) &&
                   eval_ast(node->right, vars, vars_count, decimal_set);

        case NODE_OR:
            return eval_ast(node->left, vars, vars_count, decimal_set) ||
                   eval_ast(node->right, vars, vars_count, decimal_set);
    }

    return false;
}

void expression_inputing(Function_Data* function) {

    if (function == NULL) {
        printf(
            ERROR(
                "\t[Expression Mode] [Error] Function data is not initialized.\n"
            )
        );
        return;
    }

    printf(
        MODE(
            "\t[Expression Mode]"
        )
        " rules for inputing boolean expression:\n"
        "\t\t~ = not\n"
        "\t\t& = and\n"
        "\t\t| = or\n"
        "\t\t() = brackets\n"
        "\t\tVariables must be only latin letter (or latters) + optional number\n"
        "\t\tCorrect input: Q3 & ~Q2 | ~(ABC22 & X)\n"
        "\t\tWrong input: ... \n"
    );

    while (true) {

        printf(
            MODE(
                "\t[Expression Mode]"
            )
            " Input boolean expression for function F%d: ", function->index
        );

        fflush(stdout);

        string expression_str = string_input();

        if (expression_str.data == NULL) {
            printf(
                ERROR(
                    "\t[Expression Mode] [Error] Failed to read expression input.\n"
                )
            );
            return;
        }

        Parser parser = {
            .s = expression_str,
            .pos = 0,
            .error = false
        };

        Node *root = parse_expr(&parser, 1);

        while (isspace((unsigned char)parser.s.data[parser.pos])) {
            parser.pos++;
        }

        if (root == NULL || parser.error || parser.s.data[parser.pos] != '\0') {
            ast_free(root);

            printf(
                ERROR(
                    "\t[Expression Mode] [Error] Invalid expression: \"%s\". Please use only variables, ~, &, | and brackets.\n"
                ),
                expression_str.data != NULL ? expression_str.data : ""
            );

            string_free(&expression_str);
            continue;
        }

        char **vars = NULL;
        int vars_count = 0;
        int vars_capacity = 0;

        if (!collect_variables(root, &vars, &vars_count, &vars_capacity)) {
            ast_free(root);
            free_vars(vars, vars_count);
            string_free(&expression_str);

            printf(
                ERROR(
                    "\t[Expression Mode] [Error] Failed to process variables due to memory allocation error.\n"
                )
            );
            return;
        }

        if (vars_count < 1 || vars_count > 9) {
            ast_free(root);
            free_vars(vars, vars_count);

            printf(
                ERROR(
                    "\t[Expression Mode] [Error] Expression must contain from 1 to 9 unique variables.\n"
                )
            );

            string_free(&expression_str);
            continue;
        }

        qsort(vars, vars_count, sizeof(char *), variable_compare);

        int total_sets = 1 << vars_count;
        int *sets = malloc(total_sets * sizeof(int));

        if (sets == NULL) {
            ast_free(root);
            free_vars(vars, vars_count);
            string_free(&expression_str);

            printf(
                ERROR(
                    "\t[Expression Mode] [Error] Failed to allocate memory for truth sets.\n"
                )
            );
            return;
        }

        int sets_count = 0;

        for (int decimal_set = 0; decimal_set < total_sets; decimal_set++) {
            if (eval_ast(root, vars, vars_count, decimal_set)) {
                sets[sets_count] = decimal_set;
                sets_count++;
            }
        }

        ast_free(root);
        string_free(&expression_str);

        if (sets_count == 0) {
            free(sets);
            sets = NULL;
        }

        else {

            int *tmp = realloc(sets, sets_count * sizeof(int));

            if (tmp != NULL) {
                sets = tmp;
            }
        }

        function->argsNum = vars_count;
        function->setsNum = sets_count;
        function->argsArray = vars;
        function->setsArray = sets;
        break;
    }

}
