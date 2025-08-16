#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <windows.h>
#include <set>
#include <algorithm>
#include <bitset>
#include <iomanip>

#include "normal_forms.h"

enum validateRegime {OP_MODE, ARITY, NUM_ONES, BASIS};

enum convertingRegime {DNF_REGIME, CNF_REGIME, NORMAL_REGIME, MINIMIZED_REGIME, OPERATOR_REGIME};

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

// --------- утиліти ---------
static inline void trim(std::string& s) {
    // лівий трім
    s.erase(s.begin(), std::find_if(s.begin(), s.end(),
        [](unsigned char ch){ return !std::isspace(ch); }));
    // правий трім
    s.erase(std::find_if(s.rbegin(), s.rend(),
        [](unsigned char ch){ return !std::isspace(ch); }).base(), s.end());
}

static inline bool is_natural_or_zero(const std::string& s) {
    if (s.empty()) return false; // порожній рядок — не число
    // Перевіряємо, що всі символи — цифри
    if (!std::all_of(s.begin(), s.end(),
                     [](unsigned char c){ return std::isdigit(c); }))
        return false;
    // Додаткових перевірок не треба — 0 теж пройде
    return true;
}

bool validateInput(std::string& review, int regime, size_t optional = 0);

std::vector<std::vector<std::string>> truth_table_Create(
    int arity,
    int num_combinations,
    const std::vector<int> &sets_number,
    const std::vector<std::string> &argsMarks
);

std::string userGoodForm(
    NormalForm anf,
    const int convertingFlag,
    const std::vector<std::string> &argsMarks = {}
);

int main(void) {

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::cout << "Версія: 3.5 Beta\n";

    while (true) {

        struct BasisConfig {
            int in_num;
            std::string first_operation;

            int out_num;
            std::string second_operation;
        };

        std::cout << "Для вводу логічного виразу використовуйте \"expression\", для вводу 1-наборів використовуйте \"sets\".\n";
        std::cout << "Режим: ";
        std::string input_regime;
        std::getline(std::cin, input_regime);
        if (!validateInput(input_regime, OP_MODE)) continue;

        if (input_regime == "sets") {

            // GETTING INFORMATION

            std::cout << "Наберіть кількість аргументів функції (до 10): ";
            std::string arityInput;
            std::getline(std::cin, arityInput);
            if (!validateInput(arityInput, ARITY)) continue;

            int arity = std::stoi(arityInput);
            int num_combinations = 1 << arity;

            std::vector<std::string> argsMarks;

            for (int i = 0; i < arity; ++i) {
                argsMarks.push_back("x_" + std::to_string(arity - i));
            }

            std::cout << "Наберіть цілочисельні номери наборів (без крапок і дробових частин, наприклад: 0, 2, 5): ";
            std::string num_onesInput;
            std::getline(std::cin, num_onesInput);
            if (!validateInput(num_onesInput, NUM_ONES, num_combinations)) continue;

            std::vector<int> num_ones;
            std::stringstream num_onesstream(num_onesInput);
            std::string num_onestoken;

            auto trim = [](std::string &s) {
                s.erase(0, s.find_first_not_of(" \t\n\r"));
                s.erase(s.find_last_not_of(" \t\n\r") + 1);
            };

            while (std::getline(num_onesstream, num_onestoken, ',')) {
                trim(num_onestoken);
                num_ones.push_back(std::stoi(num_onestoken));
            }

            std::cout << "Наберіть елементний базис через /: ";
            std::string basisInput;
            std::getline(std::cin, basisInput);
            if (!validateInput(basisInput, BASIS)) continue;

            BasisConfig basis;
            std::string left = basisInput.substr(0, basisInput.find('/'));
            std::string right = basisInput.substr(basisInput.find('/')+1);

            basis.in_num = left[0] - '0';
            basis.out_num = right[0] - '0';
            basis.first_operation = left.substr(1);
            basis.second_operation = right.substr(1);

            bool is_DNF = false;

            if (basis.second_operation == "АБО" || basis.second_operation == "І-НЕ") 
                is_DNF = true;
            
            // ANALYZING INPUTED INFORMAION AND CREATING OUTPUT

            std::vector<std::vector<std::string>> truth_table = truth_table_Create(
                arity,
                num_combinations,
                num_ones, 
                argsMarks
            );

            std::vector<std::string> DNFCannonForm = cannonFormCreating(num_ones, arity, true);
            std::vector<std::string> CNFCannonForm = cannonFormCreating(num_ones, arity, false);

            // getting class, that contains our STANDART normal form
            NormalForm dnf = normalRunning(DNFCannonForm, true, "І", "АБО");
            NormalForm cnf = normalRunning(CNFCannonForm, false, "АБО", "І");
            NormalForm nf = normalRunning(is_DNF ? DNFCannonForm : CNFCannonForm, is_DNF, basis.first_operation, basis.second_operation);

            std::string dnf_userForm = userGoodForm(dnf, DNF_REGIME, argsMarks);
            std::string cnf_userForm = userGoodForm(cnf, CNF_REGIME, argsMarks);
            std::string normal_userForm = userGoodForm(nf, NORMAL_REGIME, argsMarks);












            std::cout << "DNF is : " << dnf_userForm << std::endl;
            std::cout << "CNF is : " << cnf_userForm << std::endl;
            std::cout << "NORMAL is : " << normal_userForm << std::endl;

            std::cout << "table output:\n";

            for (const auto &row : truth_table) {       // перебір рядків
                for (const auto &cell : row) {          // перебір елементів у рядку
                    std::cout << cell << " ";           // вивід з пробілом
                }
                std::cout << "\n";                      // новий рядок після кожного рядка
            }

            // break;

        }

        else {}

    }

}

bool validateInput(std::string& review, int regime, size_t optional) {

    // validateInput documentaion

    switch (regime) {
        case OP_MODE: {
            if (review != "sets" && review != "expression") {
                std::cerr << "Помилка вводу: Неправильний ввід режима.\n";
                return false;
            }
            return true;
        }

        case ARITY: {
            if (review.size() != 1 || review[0] < '1' || review[0] > '9') {
                std::cerr << "Помилка вводу: Неправильне значення кількості аргументів.\n";
                return false;
            }
            return true;
        }

        case NUM_ONES:  {
            std::stringstream ss(review);
            std::string token;
            std::set<size_t> seen;

            while (std::getline(ss, token, ',')) {
                trim(token);                       // прибираємо пробіли навколо
                if (token.empty()) {
                    std::cerr << "Помилка вводу: Порожнє значення або зайва кома.\n";
                    return false;
                }
                if (!is_natural_or_zero(token)) {
                    std::cerr << "Помилка вводу: '" << token << "' не є натуральним числом.\n";
                    return false;
                }

                // конвертація й перевірки
                size_t val = static_cast<size_t>(std::stoul(token));
                if (val >= optional) {
                    std::cerr << "Помилка вводу: Значення " << val
                              << " виходить за межі [0; " << (optional ? optional-1 : 0) << "].\n";
                    return false;
                }
                if (!seen.insert(val).second) {
                    std::cerr << "Помилка вводу: Значення " << val << " повторюється.\n";
                    return false;
                }
            }

            if (seen.empty()) {
                std::cerr << "Помилка вводу: Список номерів порожній.\n";
                return false;
            }
            return true;
        }

        case BASIS: {
            std::string s = review;

            // 1) рівно один '/'
            const size_t slash = s.find('/');
            if (slash == std::string::npos || slash == 0 || slash == s.size()-1
                || s.find('/', slash + 1) != std::string::npos) {
                std::cerr << "Неправильний базис. Приклад: 3І/2АБО\n";
                return false;
            }

            // 2) ліва/права частини
            std::string left  = s.substr(0, slash);
            std::string right = s.substr(slash + 1);
            if (left.empty() || right.empty()) {
                std::cerr << "Неправильний базис. Приклад: 3І/2АБО\n";
                return false;
            }

            // ---- ЛІВА: однозначне число + операція ----
            if (!std::isdigit(static_cast<unsigned char>(left[0]))) {
                std::cerr << "Неправильний базис. Число зліва має бути однозначним цілим.\n";
                return false;
            }
            std::string lNum(1, left[0]);
            std::string lOp  = left.substr(1);

            if (!is_natural_or_zero(lNum) || lOp.empty()) {
                std::cerr << "Неправильний базис. Приклад: 3І/2АБО\n";
                return false;
            }
            // перевикористовуємо ті самі правила, що й у ARITY (наприклад, [1..10])
            if (!validateInput(lNum, ARITY)) {
                std::cerr << "Неправильний базис: число зліва поза допустимим діапазоном.\n";
                return false;
            }

            // ---- ПРАВА: однозначне число + операція ----
            if (!std::isdigit(static_cast<unsigned char>(right[0]))) {
                std::cerr << "Неправильний базис. Число справа має бути однозначним цілим.\n";
                return false;
            }
            std::string rNum(1, right[0]);
            std::string rOp  = right.substr(1);

            if (!is_natural_or_zero(rNum) || rOp.empty()) {
                std::cerr << "Неправильний базис. Приклад: 3І/2АБО\n";
                return false;
            }
            if (!validateInput(rNum, ARITY)) {
                std::cerr << "Неправильний базис: число справа поза допустимим діапазоном.\n";
                return false;
            }

            // 3) пара операцій має існувати у db
            if (std::find(db.begin(), db.end(), std::make_pair(lOp, rOp)) == db.end()) {
                std::cerr << "Неправильний базис. Приклад: 3І/2АБО\n";
                return false;
            }

            return true;
        }

        default: {return true;}

    }

}

std::vector<std::vector<std::string>> truth_table_Create(
    int arity,
    int num_combinations,
    const std::vector<int> &sets_number,
    const std::vector<std::string> &argsMarks
) {
    // Результуюча таблиця: (number_of_sets + 1) рядків, number_of_arguments + 1 колонок
    std::vector<std::vector<std::string>> result(num_combinations + 1, std::vector<std::string>(arity));

    // Перший рядок
    for (int k = 0; k < arity; ++k) {
        result[0][k] = "$" + argsMarks[k] + "$";
    }

    // Заповнення бінарних комбінацій
    for (int k = 0; k < num_combinations; ++k) {
        std::string bin = std::bitset<32>(k).to_string().substr(32 - arity);
        for (int j = 0; j < arity; ++j) {
            result[k + 1][j] = std::string(1, bin[j]);
        }
    }

    // Додаємо колонку з y
    std::vector<std::string> col_y;
    col_y.push_back("$y$");
    for (int l = 0; l < num_combinations; ++l) {
        bool found = false;
        for (int s : sets_number) {
            if (l == s) {
                found = true;
                break;
            }
        }
        col_y.push_back(found ? "1" : "0");
    }

    // Додаємо колонку y до результату
    for (int i = 0; i < result.size(); ++i) {
        result[i].push_back(col_y[i]);
    }

    return result;
}

std::string userGoodForm(
    NormalForm anf,
    const int convertingFlag,
    const std::vector<std::string> &argsMarks
) {

    std::string output;

    switch (convertingFlag) {
    
        case (DNF_REGIME): {

            for (size_t t = 0; t < anf.structure.size(); ++t) {
                const std::string &term = anf.structure[t];

                std::string term_str;
                for (size_t i = 0; i < term.size(); ++i) {

                    if (term[i] == '0') {
                        term_str += "not(" + argsMarks[i] + ")";
                    } else {
                        term_str += argsMarks[i];
                    }

                    if (i + 1 < term.size()) term_str += " ∧ ";
                }

                term_str = "(" + term_str + ")";

                if (!output.empty()) output += " ∨ ";
                output += term_str;
            }

            return output;

        }

        case (CNF_REGIME): {

            for (size_t t = 0; t < anf.structure.size(); ++t) {
                const std::string &term = anf.structure[t];

                std::string term_str;
                for (size_t i = 0; i < term.size(); ++i) {

                    if (term[i] == '0') {
                        term_str += "not(" + argsMarks[i] + ")";
                    } else {
                        term_str += argsMarks[i];
                    }

                    if (i + 1 < term.size()) term_str += " ∨ ";
                }

                term_str = "(" + term_str + ")";

                if (!output.empty()) output += " ∧ ";
                output += term_str;
            }

            return output;

        }

        case (NORMAL_REGIME): {

            for (size_t t = 0; t < anf.structure.size(); ++t) {
                const std::string &term = anf.structure[t];

                std::string term_str;
                for (size_t i = 0; i < term.size(); ++i) {

                    if (term[i] == '0') {
                        term_str += "not(" + argsMarks[i] + ")";
                    } else {
                        term_str += argsMarks[i];
                    }

                    if (i + 1 < term.size()) term_str += " " + anf.in_sign + " ";
                }

                term_str = "(" + term_str + ")";
                if (anf.in_not) term_str = "not" + term_str;

                if (!output.empty()) output += " " + anf.out_sign + " ";
                output += term_str;
            }

            if (anf.out_not) output = "not(" + output + ")";
            return output;

        }

        default: {

            return output;

        }

    }

}