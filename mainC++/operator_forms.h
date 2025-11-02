// operator_forms.h
#pragma once

#include <string>
#include "normal_forms.h"

// Повертає операторну форму для заданого NormalForm.
// in_num  — розмір групування всередині термів
// out_num — розмір групування між термами
std::string operatorRunning(const NormalForm& nf, int in_num, int out_num);