#include <iostream>
#include <string>
#include <vector>
#include <windows.h>

int main() {

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);        // щоб і ввід читався коректно

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

    int i {1};

    std::cout << "Версія: 3.5 Beta\n";

    std::cout << "Для вводу логічного виразу використовуйте \"expression\", для вводу 1-наборів використовуйте \"sets\"";

}