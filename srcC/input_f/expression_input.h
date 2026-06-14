#ifndef EXPRESSION_INPUT_H
#define EXPRESSION_INPUT_H

#include "../typing.h"

#define IS_LATIN(c) (((c) >= 'A' && (c) <= 'Z') || ((c) >= 'a' && (c) <= 'z'))

void expression_inputing(Function_Data* function);

#endif