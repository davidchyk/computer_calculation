#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <algorithm>

class NormalForm {
public:
    // Конфіг
    bool is_DNF;
    std::string first_operation;   // "І", "АБО", "І-НЕ", "АБО-НЕ"
    std::string second_operation;  // "І", "АБО", "І-НЕ", "АБО-НЕ"

    // Внутрішній стан
    bool reverse = false;
    bool in_not;
    bool out_not;
    std::string in_sign;  // "∧" або "∨"
    std::string out_sign ;   // "∨" або "∧"

    std::vector<std::string> structure;

    void define_NormalForm() {

        if (is_DNF) {
            if (first_operation == "І" || second_operation == "АБО") {
                in_sign  = "∧"; out_sign = "∨";
                in_not   = false; out_not = false;
            }
            else if (first_operation == "І-НЕ" || second_operation == "І-НЕ") {
                in_sign  = "∧"; out_sign = "∧";
                in_not   = true; out_not = true;
            }
            else if (first_operation == "АБО" || second_operation == "І-НЕ") {
                in_sign  = "∨"; out_sign = "∧";
                in_not   = false; out_not = true;
                reverse  = true;
            }
            else if (first_operation == "АБО-НЕ" || second_operation == "АБО") {
                in_sign  = "∨"; out_sign = "∨";
                in_not   = true; out_not = false;
                reverse  = true;
            }
        } else {
            if (first_operation == "АБО" || second_operation == "І") {
                in_sign  = "∨"; out_sign = "∧";
                in_not   = false; out_not = false;
            }
            else if (first_operation == "АБО-НЕ" || second_operation == "АБО-НЕ") {
                in_sign  = "∨"; out_sign = "∨";
                in_not   = true; out_not = true;
            }
            else if (first_operation == "І" || second_operation == "АБО-НЕ") {
                in_sign  = "∨"; out_sign = "∧";
                in_not   = false; out_not = true;
                reverse  = true;
            }
            else if (first_operation == "І-НЕ" || second_operation == "І") {
                in_sign  = "∨"; out_sign = "∨";
                in_not   = true; out_not = false;
                reverse  = true;
            }
        }

        if (reverse) {
            // інвертуємо 0↔1 у кожному термі
            for (auto &term : structure) {
                for (char &c : term) {
                    if (c == '1')      c = '0';
                    else if (c == '0') c = '1';
                }
            }
        }
    }

    // Побудувати рядкове представлення форми (на кшталт твого Python __str__)
    std::string to_str() const {
        std::string str_form;

        for (size_t t = 0; t < structure.size(); ++t) {
            const std::string &term = structure[t];

            std::string term_str;
            for (size_t i = 0; i < term.size(); ++i) {
                term_str += term[i];
                if (i + 1 < term.size()) term_str += " " + in_sign + " ";
            }

            term_str = "(" + term_str + ")";
            if (in_not) term_str = "not" + term_str;

            if (!str_form.empty()) str_form += " " + out_sign + " ";
            str_form += term_str;
        }

        if (out_not && !str_form.empty()) {
            str_form = "not(" + str_form + ")";
        }
        return str_form;
    }
};

std::pair<std::string, NormalForm> normal(
    std::vector<int> num_ones,
    bool is_DNF,
    int arity,
    std::string first_operation,
    std::string second_operation,
    bool is_minimization = false

);

std::pair<std::string, std::vector<std::string>> DNF_CNF_creator(std::vector<int> num_ones, int arity); 

std::pair<std::string, NormalForm> normal(
    std::vector<int> num_ones,
    bool is_DNF,
    int arity,
    std::string first_operation,
    std::string second_operation,
    bool is_minimization = false
) {

    std::vector<std::string> output;

    if (is_minimization) {


    } else {

        NormalForm normalfrom_ex();




    }





}

std::pair<std::string, std::vector<std::string>> DNF_CNF_creator(std::vector<int> num_ones, int arity) {





}

