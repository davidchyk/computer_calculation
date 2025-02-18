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

        self.setWindowIcon(QIcon(r"C:\Users\artem\OneDrive\Desktop\CompLogic\inverted_logo.ico"))

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

        # Додавання полів у форму
        self.form_layout.addRow(self.arg_label, self.arg_input)
        self.form_layout.addRow(self.sets_label, self.sets_input)
        self.form_layout.addRow(self.basis_label, self.basis_input)

        # Кнопка перемикання режимів
        self.mode_button = QPushButton("Переключити на багаторазовий мод")
        self.mode_button.clicked.connect(self.toggle_mode)

        # Кнопка додавання полів для багаторазового режиму
        self.add_field_button = QPushButton("Додати набір для наступного y")
        self.add_field_button.clicked.connect(self.add_new_set_field)
        self.add_field_button.hide()  # Спочатку прихована

        # Кнопка для обчислення формули
        self.show_button = QPushButton("Розрахувати")
        self.show_button.clicked.connect(self.display_formula)

        # QWebEngineView для відображення формули
        self.view = QWebEngineView()
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.set_initial_html()

        # Контейнер для прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.view)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        # Додавання елементів у основний макет
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.mode_button)
        main_layout.addWidget(self.add_field_button)
        main_layout.addWidget(self.show_button)
        main_layout.addWidget(self.scroll_area)

        # Центральний віджет
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Змінні для режимів
        self.is_single_mode = True
        self.set_fields = []  # Список для багаторазового режиму

    def toggle_mode(self):
        """Перемикання між одиничним та багаторазовим режимами."""
        if self.is_single_mode:
            # Перемикання на багаторазовий режим
            self.mode_button.setText("Переключити на одиничний мод")
            self.add_field_button.show()
            self.is_single_mode = False

            # Приховати поле "Набори, при яких функція = 1"
            self.sets_label.hide()
            self.sets_input.hide()

            # Додати перше поле для багаторазового режиму
            self.add_new_set_field()
        else:
            # Перемикання на одиничний режим
            self.mode_button.setText("Переключити на багаторазовий мод")
            self.add_field_button.hide()
            self.is_single_mode = True

            # Показати поле "Набори, при яких функція = 1"
            self.sets_label.show()
            self.sets_input.show()

            # Видалити всі додаткові поля багаторазового режиму
            for field in self.set_fields:
                self.form_layout.removeRow(field['label'])
            self.set_fields.clear()

    def add_new_set_field(self):
        """Додати нове поле для багаторазового режиму."""
        index = len(self.set_fields) + 1
        new_label = QLabel(f"Набори, при яких y{index} = 1:")
        new_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        new_input = QLineEdit()
        new_input.setPlaceholderText(f"Наприклад: 1, 2, 3 (для y{index})")
        new_input.setStyleSheet("background-color: #161B22; color: #C9D1D9;")
        self.form_layout.addRow(new_label, new_input)
        self.set_fields.append({'label': new_label, 'input': new_input})

    def display_formula(self):
        """Обчислення формули на основі вводу."""
        if self.is_single_mode:
            latex_code = generate(self.arg_input.text(), self.sets_input.text(), self.basis_input.text())
        else:
            latex_code = ""
            for index, field in enumerate(self.set_fields, start=1):
                latex_code += f"y_{index} = " + generate(self.arg_input.text(), field['input'].text(), self.basis_input.text()) + "\\\\"
        self.view.setHtml(f"<html><body>$$ \\begin{{array}}{{l}} {latex_code} \\end{{array}} $$</body></html>")

    def set_initial_html(self):
        """Встановлення початкового HTML-контенту."""
        self.view.setHtml("<html><body style='background-color:#0D1117;'>Введіть дані</body></html>")

    def show_basis(self):
        """Відображення елементних базисів."""
        text = "Дозволені елементні базиси:\n\n" + "\n".join([f"{b[0]}/{b[1]}" for b in db])
        QMessageBox.information(self, "Елементні базиси", text)

    def show_authors_dialog(self):
        """Відображення інформації про авторів."""
        QMessageBox.information(self, "Автори", "Розробник: Давидчук Артем")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaTeXFormulaApp()
    window.show()
    sys.exit(app.exec())
