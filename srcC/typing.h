#ifndef TYPING_H
#define TYPING_H

#include <stdbool.h>

#include "string_process/string_process.h"

typedef enum {

    // dnf:

    AND_OR    = 0b0001,
    NAND_NAND = 0b1010,
    OR_NAND   = 0b0110,
    NOR_OR    = 0b1101,

    // cnf:

    OR_AND    = 0b0100,
    NOR_NOR   = 0b1111,
    AND_NOR   = 0b0011,
    NAND_AND  = 0b1000

    /*

    4 bits: [0 bit] [1 bit] [2 bit] [3 bit]

    0 bit = out_not
    1 bit = out_or_operation
    2 bit = in_not
    3 bit = in_or_operation

    true reversing for OR_NAND, NOR_OR, OR_AND, NOR_NOR

    so reversing = true, if 1 bit is true

    AND_OR    = 0001 = 1
    NAND_NAND = 1010 = 10
    OR_NAND   = 0110 = 6
    NOR_OR    = 1101 = 13

    OR_AND    = 0100 = 4
    NOR_NOR   = 1111 = 15
    AND_NOR   = 0011 = 3
    NAND_AND  = 1000 = 8

    out_not          = 8 & basis
    out_or_operation = 4 & basis
    reversing        = 4 & basis

    in_not           = 2 & basis
    in_or_operation  = 1 & basis
    
    is_cnf           = 1 & (basis ^ (basis >> 1))

    */

} basis_t;

typedef struct {

    // function data from input

    int index;
    int argsNum;
    int setsNum;

    int *setsArray; 
    char** argsArray;

    bool from_expression_created;

    basis_t basis;
    int first_basisNumber, second_basisNumber;

    // function data from calculations

    string dnf_form;
    string cnf_form;

    string normal_form;
    string operator_form;

    string minimized_normal_form;
    string minimized_operator_form;

    // class function add

} function_t;

#define COLOR_RED     "\033[31m"
#define COLOR_GREEN   "\033[32m"
#define COLOR_YELLOW  "\033[33m"
#define COLOR_BLUE    "\033[34m"
#define COLOR_RESET   "\033[0m"

#define TEPM_TERM -1

#define ERROR(x)  COLOR_RED x COLOR_RESET
#define TIP(x)    COLOR_YELLOW x COLOR_RESET
#define MODE(x)   COLOR_BLUE x COLOR_RESET

#define IN_NOT(x)           (8 & x)
#define IN_OR_OPERATION(x)  (4 & x)
#define OUT_NOT(x)          (2 & x)
#define OUT_OR_OPERATION(x) (1 & x)

#define IS_DNF(x)           (1 & (x ^ (x >> 1)))


#endif // TYPING_H