#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <windows.h>

#define INPUT_REGIME 0
#define ARITY 1
#define NUM_ONES 2

bool validate(std::string& review, int regime, size_t optional = 0);

int main() {

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::cout << "Версія: 3.5 Beta\n";

    while (true) {

        std::vector<std::pair<std::string, std::string>> db = {
            {"І", "АБО"},
            {"І-НЕ", "І-НЕ"},
            {"АБО", "І-НЕ"},
            {"АБО-НЕ", "АБО"},
            {"АБО", "І"},
            {"АБО-НЕ", "АБО-НЕ"},
            {"І", "АБО-НЕ"},
            {"І-НЕ", "І"}
        };

        std::cout << "Для вводу логічного виразу використовуйте \"expression\", для вводу 1-наборів використовуйте \"sets\".\n";
        std::cout << "Режим: ";
        std::string input_regime;
        std::getline(std::cin, input_regime);
        if (!validate(input_regime, INPUT_REGIME)) continue;

        if (input_regime == "sets") {

            std::cout << "Наберіть кількість аргументів функції (до 10): ";
            std::string arityInput;
            std::getline(std::cin, arityInput);
            if (!validate(arityInput, ARITY)) continue;

            size_t arity = arityInput[0] - '0';
            size_t num_combinations = size_t{1} << arity;

            std::cout << "Наберіть числа наборів, при яких функція набуває одиниці (через кому): ";
            std::string num_onesInput;
            std::getline(std::cin, num_onesInput);
            if (!validate(num_onesInput, NUM_ONES, num_combinations));

        }

        else {}

    }

}

bool validate(std::string& review, int regime, size_t optional) {

    switch (regime) {

        case INPUT_REGIME:

            if (review != "sets" && review != "expression") {

                std::cerr << "Помилка вводу: Неправильний ввід режима.\n";
                return false;

            }

            return true;

        case ARITY:

            if (!(review.size() == 1 && review[0] >= '0' && review[0] <= '9')) {

                std::cerr << "Помилка вводу: Неправильне значення кількості аргументів.\n";
                return false;

            }

            return true;

        case NUM_ONES:

            #include <iostream>
            #include <sstream>
            #include <string>
            #include <limits>

            bool validate_integer_list(const std::string& input, unsigned int bits) {
                unsigned long max_value = (1UL << bits) - 1; // 2^bits - 1
                std::istringstream ss(input);
                std::string token;
                bool found_any = false;

                while (std::getline(ss, token, ',')) {
                    // Видалення пробілів з початку і кінця
                    size_t start = token.find_first_not_of(" \t");
                    size_t end = token.find_last_not_of(" \t");

                    if (start == std::string::npos || end == std::string::npos) {
                        continue; // токен лише з пробілів
                    }

                    token = token.substr(start, end - start + 1);

                    // Спроба перетворити токен у unsigned long
                    try {
                        size_t idx;
                        unsigned long val = std::stoul(token, &idx, 10);

                        if (idx != token.length()) {
                            std::cerr << "❌ Некоректне число: \"" << token << "\" — зайві символи\n";
                            return false;
                        }

                        if (val > max_value) {
                            std::cerr << "❌ Число \"" << token << "\" > " << max_value << "\n";
                            return false;
                        }

                        found_any = true;

                    } catch (...) {
                        std::cerr << "❌ Неможливо перетворити \"" << token << "\" у число\n";
                        return false;
                    }
                }

                if (!found_any) {
                    std::cerr << "❌ Не знайдено жодного числа в межах [0, " << max_value << "]\n";
                    return false;
                }

                return true;



        default:

            return true;

    }

}