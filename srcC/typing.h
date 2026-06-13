#ifndef TYPING_H
#define TYPING_H

#include <stdbool.h>

typedef enum {
    AND_OR,
    NAND_NAND,
    OR_NAND,
    NOR_OR,
    OR_AND,
    NOR_NOR,
    AND_NOR,
    NAND_AND
} basisType;

typedef struct {

    // function data from input

    int index;
    int argsNum;
    int setsNum;

    int *setsArray;
    char** argsArray;

    bool from_expression_created;

    basisType basis;
    int first_basisNumber, second_basisNumber;

    // function data from calculations

} Function_Data;

#define COLOR_RED     "\033[31m"
#define COLOR_GREEN   "\033[32m"
#define COLOR_YELLOW  "\033[33m"
#define COLOR_BLUE    "\033[34m"
#define COLOR_RESET   "\033[0m"

#define ERROR(x)   COLOR_RED x COLOR_RESET
#define WARNING(x) COLOR_YELLOW x COLOR_RESET
#define MODE(x)    COLOR_BLUE x COLOR_RESET

#endif // TYPING_H