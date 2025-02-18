from PySide6.QtGui import QIcon, QAction, QKeyEvent
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QSizePolicy, QFormLayout, QMessageBox
from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtWebEngineWidgets import QWebEngineView

from formula_generator import generate

db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
      ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]


class LaTeXFormulaApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # Меню
        authors_action = QAction("Автори", self)
        authors_action.triggered.connect(self.show_authors_dialog)
        menu = self.menuBar()
        menu.addAction(authors_action)

        basis_action = QAction("Елементні базиси", self)
        basis_action.triggered.connect(self.show_basis)
        menu.addAction(basis_action)

        self.setWindowIcon(QIcon("logo.ico"))

        # Основні параметри вікна
        self.setWindowTitle("LogicMin v1.0 Beta Testing")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #0D1117; color: #C9D1D9; font-family: Arial;")

        # Основний макет
        main_layout = QVBoxLayout()

        # Поля вводу
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        self.form_layout.setSpacing(5)

        # Поля для одиничного режиму
        self.arg_label = QLabel("Кількість аргументів:")
        self.arg_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        self.arg_input = QLineEdit()
        self.arg_input.setPlaceholderText("Наприклад: 3")
        self.arg_input.setStyleSheet("background-color: #161B22; color: #C9D1D9;")

        self.sets_label = QLabel("Набори, при яких функція = 1:")
        self.sets_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        self.sets_input = QLineEdit()
        self.sets_input.setPlaceholderText("Наприклад: 1, 2, 3")
        self.sets_input.setStyleSheet("background-color: #161B22; color: #C9D1D9;")

        self.basis_label = QLabel("Елементний базис:")
        self.basis_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        self.basis_input = QLineEdit()
        self.basis_input.setPlaceholderText("Наприклад: ЗІ/ЗАБО")
        self.basis_input.setStyleSheet("background-color: #161B22; color: #C9D1D9;")

        # Повідомлення про помилку
        self.arg_error_label = QLabel("Неправильний ввід даних")
        self.arg_error_label.setStyleSheet("color: red;")
        self.arg_error_label.hide()

        self.sets_error_label = QLabel("Неправильний ввід даних")
        self.sets_error_label.setStyleSheet("color: red;")
        self.sets_error_label.hide()

        self.basis_error_label = QLabel("Неправильний ввід даних. Перегляньте елементні базиси")
        self.basis_error_label.setStyleSheet("color: red;")
        self.basis_error_label.hide()

        # Організація полів
        self.form_layout.addRow(self.arg_label, self.arg_input)
        self.form_layout.addRow(self.arg_error_label)
        self.form_layout.addRow(self.sets_label, self.sets_input)
        self.form_layout.addRow(self.sets_error_label)
        self.form_layout.addRow(self.basis_label, self.basis_input)
        self.form_layout.addRow(self.basis_error_label)

        # Кнопка перемикання режимів
        self.mode_button = QPushButton("Переключити на багаторазовий мод")
        self.mode_button.clicked.connect(self.toggle_mode)

        # Кнопка додавання полів
        self.add_field_button = QPushButton("Додати перемикальну функцію")
        self.add_field_button.clicked.connect(self.add_new_set_field)
        self.add_field_button.hide()

        # Кнопка видалення останнього поля
        self.remove_field_button = QPushButton("Видалити останню перемикальну функцію")
        self.remove_field_button.clicked.connect(self.remove_last_set_field)
        self.remove_field_button.hide()

        # Кнопка для обчислення формули
        self.show_button = QPushButton("Розрахувати")
        self.show_button.clicked.connect(self.display_formula)

        # Віджет для відображення результатів
        self.view = QWebEngineView()
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.set_initial_html()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.view)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        # Додавання елементів у макет
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.mode_button)
        main_layout.addWidget(self.add_field_button)
        main_layout.addWidget(self.remove_field_button)
        main_layout.addWidget(self.show_button)
        main_layout.addWidget(self.scroll_area)

        # Центральний віджет
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Змінні для режимів
        self.is_single_mode = True
        self.set_fields = []

    def toggle_mode(self):
        if self.is_single_mode:
            self.mode_button.setText("Переключити на одиничний мод")
            self.add_field_button.show()
            self.remove_field_button.show()
            self.sets_label.hide()
            self.sets_input.hide()
            self.is_single_mode = False
            self.add_new_set_field()
        else:
            self.mode_button.setText("Переключити на багаторазовий мод")
            self.add_field_button.hide()
            self.remove_field_button.hide()
            self.sets_label.show()
            self.sets_input.show()
            for field in self.set_fields:
                self.form_layout.removeRow(field['label'])
            self.set_fields.clear()
            self.is_single_mode = True

    def add_new_set_field(self):
        index = len(self.set_fields) + 1
        new_label = QLabel(f"Набори, при яких Y{index} = 1:")
        new_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        new_input = QLineEdit()
        new_input.setPlaceholderText(f"Наприклад: 1, 2, 3 (для Y{index})")
        new_input.setStyleSheet("background-color: #161B22; color: #C9D1D9;")
        self.form_layout.addRow(new_label, new_input)
        self.set_fields.append({'label': new_label, 'input': new_input})

    def remove_last_set_field(self):
        if self.set_fields:
            last_field = self.set_fields.pop()
            self.form_layout.removeRow(last_field['label'])
            if not self.set_fields:
                self.toggle_mode()

    def display_formula(self):
        if self.is_single_mode:
            latex_code = generate(self.arg_input.text(), self.sets_input.text(), self.basis_input.text())
        else:
            latex_code = ""
            for index, field in enumerate(self.set_fields, start=1):
                latex_code += f"y_{index} = " + generate(self.arg_input.text(), field['input'].text(), self.basis_input.text()) + "\\\\"
        self.view.setHtml(f"<html><body>$$ \\begin{{array}}{{l}} {latex_code} \\end{{array}} $$</body></html>")

    def set_initial_html(self):
        self.view.setHtml("<html><body style='background-color:#0D1117;'>Введіть дані</body></html>")

    def show_basis(self):
        text = "Дозволені елементні базиси:\n\n" + "\n".join([f"{b[0]}/{b[1]}" for b in db])
        QMessageBox.information(self, "Елементні базиси", text)

    def show_authors_dialog(self):
        QMessageBox.information(self, "Автори", "")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaTeXFormulaApp()
    window.show()
    sys.exit(app.exec())
