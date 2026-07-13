#ifndef NORMAL_FORM_H
#define NORMAL_FORM_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../utils/typing.h"
#include "../utils/utils.h"

void set_normal_form(function_t *function);

void set_dnf(function_t *function);

void set_cnf(function_t *function);

#endif // NORMAL_FORM_H
