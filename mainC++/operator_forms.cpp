#include <string>
#include <vector>
#include <stdexcept>

#include "normal_forms.h"
#include "operator_forms.h"

// допоміжна рекурсивна структура для груп
struct Node {
    bool isAtom = true;
    std::string atom;        // якщо атом, тут текст (наприклад "0" або вже готовий підвираз)
    std::vector<Node> group; // якщо група, тут діти

    static Node Atom(std::string s) { Node n; n.isAtom = true;  n.atom = std::move(s); return n; }
    static Node Group(std::vector<Node> g){ Node n; n.isAtom = false; n.group = std::move(g); return n; }
};

// групування по m елементів
static std::vector<Node> group_once(const std::vector<Node>& lst, int m) {
    if ((int)lst.size() <= m) return lst;
    std::vector<Node> out;
    out.reserve((lst.size() + m - 1) / m);
    for (int i = 0; i < (int)lst.size(); i += m) {
        int len = std::min(m, (int)lst.size() - i);
        if (len == 1) out.push_back(lst[i]);
        else {
            std::vector<Node> chunk;
            chunk.reserve(len);
            for (int k = 0; k < len; ++k) chunk.push_back(lst[i + k]);
            out.push_back(Node::Group(std::move(chunk)));
        }
    }
    return out;
}

static std::vector<Node> group_elements(std::vector<Node> data, int m) {
    // перший прохід
    data = group_once(data, m);
    // поки довжина > m — ще раз групуємо
    while ((int)data.size() > m) data = group_once(data, m);
    return data;
}

// вибір символу оператора за базисом
static std::string op_symbol(const std::string& op_name) {
    // "АБО"/"АБО-НЕ" -> " ∨ "; "І"/"І-НЕ" -> " ∧ "
    if (op_name == "АБО" || op_name == "АБО-НЕ") return " ∨ ";
    if (op_name == "І"   || op_name == "І-НЕ")   return " ∧ ";
    // якщо щось інше — вважай помилкою вводу
    throw std::invalid_argument("Невідомий оператор у базисі: " + op_name);
}

// рендерінг вузла з фіксованим оператором між дітьми
static std::string render_with_op(const Node& n, const std::string& op) {
    if (n.isAtom) return n.atom;
    std::string s;
    for (size_t i = 0; i < n.group.size(); ++i) {
        s += render_with_op(n.group[i], op);
        if (i + 1 < n.group.size()) s += op;
    }
    return "(" + s + ")";
}

// ===== аналог твоєї union(lst, way, begin, in_not, out_not) =====
static std::string unite(const std::vector<Node>& lst,
                         const NormalForm nf,
                         bool begin
) {

    const std::string& inner = begin ? nf.first_operation  : nf.second_operation;
    const std::string  sym   = op_symbol(inner);

    // Збираємо "(a op b op ...)"
    Node wrapper = Node::Group(lst);
    std::string expr = render_with_op(wrapper, sym);

    // Обробка not за твоїми правилами
    if ((begin && nf.in_not) || (!begin && nf.out_not)) {
        expr = "not(" + expr + ")";
    }

    // Для зовнішнього об'єднання у твоєму Python знімалась пара дужок
    // (term[1:-1]). Віддзеркалимо це:
    if (!begin && expr.size() >= 2 && expr.front() == '(' && expr.back() == ')') {
        expr = expr.substr(1, expr.size() - 2);
    }
    return expr;
}

std::string operatorRunning(const NormalForm& nf, int in_num, int out_num) {
    // 1) Для кожного терма робимо групування по in_num і об’єднуємо з урахуванням in_not
    std::vector<std::string> inner_forms;
    inner_forms.reserve(nf.structure.size());

    for (const std::string& term : nf.structure) {
        // перетворюємо "0101" у вектор атомів: ["0","1","0","1"]
        std::vector<Node> atoms;
        atoms.reserve(term.size());
        for (char c : term) atoms.push_back(Node::Atom(std::string(1, c)));

        // групуємо за in_num
        auto grouped = group_elements(std::move(atoms), in_num);

        // зливаємо (begin = true)
        inner_forms.push_back(unite(grouped, nf, true));
    }

    // 2) Зовнішнє групування списку отриманих підвиразів по out_num
    //    Спочатку перетворимо готові рядки на атоми
    std::vector<Node> outer_atoms;
    outer_atoms.reserve(inner_forms.size());
    for (auto& s : inner_forms) outer_atoms.push_back(Node::Atom(std::move(s)));

    auto grouped_outer = group_elements(std::move(outer_atoms), out_num);

    // 3) Зовнішнє об'єднання (begin = false)
    return unite(grouped_outer, nf, false);
}