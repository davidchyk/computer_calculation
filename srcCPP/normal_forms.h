#ifndef NORMAL_FORMS_H
#define NORMAL_FORMS_H

#include <string>
#include <vector>

// Клас NormalForm
class NormalForm {
public:
    // Конфіг
    bool is_DNF;
    std::string first_operation;   // "І", "АБО", "І-НЕ", "АБО-НЕ"
    std::string second_operation;  // "І", "АБО", "І-НЕ", "АБО-НЕ"
    std::vector<std::string> structure;

    // Внутрішній стан
    bool reverse = false;
    bool in_not;
    bool out_not;
    std::string in_sign;   // "∧" або "∨"
    std::string out_sign;  // "∨" або "∧"

    void define_NormalForm();
};

// Створення канонічної форми (ДНФ / КНФ)
std::vector<std::string> cannonFormCreating(
    std::vector<int> num_ones,
    int arity,
    bool is_DNF
);

// Конструктор NormalForm
NormalForm normalRunning(
    std::vector<std::string> terms,
    bool is_DNF,
    std::string first_operation,
    std::string second_operation
);

#endif // NORMAL_FORMS_H