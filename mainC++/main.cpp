#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <windows.h>
#include <set>
#include <algorithm>
#include <bitset>
#include <iomanip>

enum validateRegime {OP_MODE, ARITY, NUM_ONES, BASIS};

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
    const std::string &input_regime,
    int arity,
    int num_combinations,
    const std::vector<int> &sets_number,
    const std::vector<std::string> &argsMarks = {}
);

int main(void) {

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::cout << "Версія: 3.5 Beta\n";

    while (true) {

        struct BASIS_CONFIG {
            int first_num;
            std::string first_operation;

            int second_num;
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

            BASIS_CONFIG basis;
            std::stringstream basisInputstream(basisInput);
            std::string basistoken;

            // first_num
            std::getline(basisInputstream, basistoken, ',');
            basistoken.erase(0, basistoken.find_first_not_of(" \t")); // прибираємо пробіли
            basistoken.erase(basistoken.find_last_not_of(" \t") + 1);
            basis.first_num = std::stoi(basistoken);

            // first_operation
            std::getline(basisInputstream, basistoken, ',');
            basistoken.erase(0, basistoken.find_first_not_of(" \t"));
            basistoken.erase(basistoken.find_last_not_of(" \t") + 1);
            basis.first_operation = basistoken;

            // second_num
            std::getline(basisInputstream, basistoken, ',');
            basistoken.erase(0, basistoken.find_first_not_of(" \t"));
            basistoken.erase(basistoken.find_last_not_of(" \t") + 1);
            basis.second_num = std::stoi(basistoken);

            // out_operation
            std::getline(basisInputstream, basistoken);
            basistoken.erase(0, basistoken.find_first_not_of(" \t"));
            basistoken.erase(basistoken.find_last_not_of(" \t") + 1);
            basis.second_operation = basistoken;

            bool is_DNF = false;

            if (basis.first_operation == "АБО" || basis.first_operation == "І-НЕ") {
                is_DNF = true;
            }

            // ANALYZING INFORMAION AND CREATING OUTPUT

            std::vector<std::vector<std::string>> truth_table = truth_table_Create(
                input_regime,
                arity,
                num_combinations,
                num_ones
            );














            std::cout << "table output:\n";

            for (const auto &row : truth_table) {       // перебір рядків
                for (const auto &cell : row) {          // перебір елементів у рядку
                    std::cout << cell << " ";           // вивід з пробілом
                }
                std::cout << "\n";                      // новий рядок після кожного рядка
            }

            std::cout << "Good Result\n\n";

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
            trim(s);

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
            trim(left); trim(right);
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
            trim(lOp);

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
            trim(rOp);

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
    const std::string &input_regime,
    int arity,
    int num_combinations,
    const std::vector<int> &sets_number,
    const std::vector<std::string> &argsMarks
) {
    // Результуюча таблиця: (number_of_sets + 1) рядків, number_of_arguments + 1 колонок
    std::vector<std::vector<std::string>> result(num_combinations + 1, std::vector<std::string>(arity));

    // Перший рядок
    if (input_regime == "sets") {
        for (int k = 0; k < arity; ++k) {
            result[0][k] = "$x_" + std::to_string(arity - k) + "$";
        }
    } else if (input_regime == "expression") {
        for (int k = 0; k < arity; ++k) {
            result[0][k] = "$" + argsMarks[k] + "$";
        }
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