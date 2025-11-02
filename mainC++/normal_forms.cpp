#include <string>
#include <vector>
#include <algorithm>
#include <bitset>

#include "normal_forms.h"

void NormalForm::define_NormalForm() {

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

std::vector<std::string> cannonFormCreating(
    std::vector<int> num_ones,
    int arity,
    bool is_DNF
) {

    std::vector<std::string> result;

    if (is_DNF) {

        for (int num : num_ones) {
            // перетворюємо число у двійковий рядок з фіксованою довжиною
            std::bitset<32> bits(num);  
            std::string bin_str = bits.to_string().substr(32 - arity);
            result.push_back(bin_str);
        }

    } else {

        std::vector<int> num_zero;

        for (int x = 0; x < (1 << arity); ++x) {
            if (std::find(num_ones.begin(), num_ones.end(), x) == num_ones.end()) {
                num_zero.push_back(x);
            }
        }

        for (int num : num_zero) {
            // перетворюємо число у двійковий рядок з фіксованою довжиною
            std::bitset<32> bits(num);
            std::bitset<32> inverted = ~bits;
            std::string bin_str = inverted.to_string().substr(32 - arity);
            result.push_back(bin_str);
        }

    }

    return result;

}

NormalForm normalRunning(
    std::vector<std::string> terms,
    bool is_DNF,
    std::string first_operation,
    std::string second_operation
) {

    NormalForm nf {
        .is_DNF = is_DNF,
        .first_operation = first_operation,
        .second_operation = second_operation,
        .structure = terms
    };

    nf.define_NormalForm();
    return nf;
}