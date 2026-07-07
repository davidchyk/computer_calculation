#ifndef NORMAL_FORM_H
#define NORMAL_FORM_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../typing.h"

void set_normal_form(Function_Data *function_data);

void set_dnf(Function_Data *function_data);

void set_cnf(Function_Data *function_data);

#endif
