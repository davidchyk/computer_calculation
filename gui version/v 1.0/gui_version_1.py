from PySide6.QtGui import QIcon, QAction, QKeyEvent
from sys import argv, exit
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QSizePolicy, QFormLayout, QMessageBox 
from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtWebEngineWidgets import QWebEngineView

from formula_generator import generate

db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
        ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]

class LaTeXFormulaApp(QMainWindow):

    def __init__(self):

        super().__init__()

        authors_action = QAction("Автори", self)
        authors_action.triggered.connect(self.show_authors_dialog)
        menu = self.menuBar()
        menu.addAction(authors_action)  # Додаємо "Автори" безпосередньо в меню

        basis_action = QAction("Елементні базиси", self)
        basis_action.triggered.connect(self.show_basis)
        menu = self.menuBar()
        menu.addAction(basis_action)  # Додаємо "Автори" безпосередньо в меню

        self.setWindowIcon(QIcon(r"C:\Users\artem\OneDrive\Desktop\CompLogic\inverted_logo.ico"))

        # Основні параметри вікна
        self.setWindowTitle("LogicMin v1.0 Beta Testing")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #0D1117; color: #C9D1D9; font-family: Arial;")

        # Основний макет
        main_layout = QVBoxLayout()

        # Макет для полів вводу
        form_layout = QFormLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)  # Внутрішні відступи для всього макету
        form_layout.setSpacing(5)  # Відстань між полями та лейблами
 
        # Поля для введення
        self.arg_label = QLabel("Кількість аргументів:")
        self.arg_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        self.arg_input = QLineEdit()
        self.arg_input.setPlaceholderText("Наприклад: 3")
        self.arg_input.textChanged.connect(lambda: self.clear_error(self.arg_error_label, self.arg_input))
        self.arg_input.setStyleSheet("background-color: #161B22; color: #C9D1D9; font-size: 14px; padding: 6px; border-radius: 5px; border: 1px solid #30363D;")

        self.sets_label = QLabel("Набори, при яких функція = 1:")
        self.sets_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        self.sets_input = QLineEdit()
        self.sets_input.setPlaceholderText("Наприклад: 1, 2, 3")
        self.sets_input.textChanged.connect(lambda: self.clear_error(self.sets_error_label, self.sets_input))
        self.sets_input.setStyleSheet("background-color: #161B22; color: #C9D1D9; font-size: 14px; padding: 6px; border-radius: 5px; border: 1px solid #30363D;")

        self.basis_label = QLabel("Елементний базис:")
        self.basis_label.setStyleSheet("font-size: 14px; color: #C9D1D9;")
        self.basis_input = QLineEdit()
        self.basis_input.setPlaceholderText("Наприклад: ЗІ/ЗАБО")
        self.basis_input.textChanged.connect(lambda: self.clear_error(self.basis_error_label, self.basis_input))
        self.basis_input.setStyleSheet("background-color: #161B22; color: #C9D1D9; font-size: 14px; padding: 6px; border-radius: 5px; border: 1px solid #30363D;")

        # Повідомлення про помилку для кожного поля
        self.arg_error_label = QLabel("Неправильний ввід даних")
        self.arg_error_label.setStyleSheet("color: red;")
        self.arg_error_label.hide()

        self.sets_error_label = QLabel("Неправильний ввід даних")
        self.sets_error_label.setStyleSheet("color: red;")
        self.sets_error_label.hide()

        self.basis_error_label = QLabel("Неправильний ввід даних. Перегляньте елементні базиси")
        self.basis_error_label.setStyleSheet("color: red;")
        self.basis_error_label.hide()

        # Створення вертикальних макетів для полів вводу та повідомлень про помилку
        arg_input_layout = QVBoxLayout()
        arg_input_layout.addWidget(self.arg_error_label)
        arg_input_layout.addWidget(self.arg_input)

        sets_input_layout = QVBoxLayout()
        sets_input_layout.addWidget(self.sets_error_label)
        sets_input_layout.addWidget(self.sets_input)

        basis_input_layout = QVBoxLayout()
        basis_input_layout.addWidget(self.basis_error_label)
        basis_input_layout.addWidget(self.basis_input)

        # Додавання лейблів і відповідних полів (з повідомленнями про помилку) в формовий макет
        form_layout.addRow(self.arg_label, arg_input_layout)
        form_layout.addRow(self.sets_label, sets_input_layout)
        form_layout.addRow(self.basis_label, basis_input_layout)

        self.setStyleSheet("""
            QLabel {
                font-family: 'Roboto', sans-serif;  /* Замініть 'Roboto' на будь-який інший шрифт */
                font-size: 16px;
                font-weight: bold;
                color: #C9D1D9;
            }
            QLineEdit {
                background-color: #161B22;
                color: #C9D1D9;
                padding: 6px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #30363D;
            }
            QPushButton {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border: 2px solid white;
                border-radius: 5px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        # Кнопка для відображення формули
        self.show_button = QPushButton("Розрахувати")
        self.show_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border: 2px solid white;
                border-radius: 5px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.show_button.clicked.connect(self.display_formula)

        # QWebEngineView для відображення LaTeX
        self.view = QWebEngineView()
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.set_initial_html()  # Встановлення початкового HTML-контенту з темним фоном

        self.view.setContextMenuPolicy(Qt.NoContextMenu)

        # Контейнер для прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.view)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        # Додавання макетів до основного макету
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.show_button)
        main_layout.addWidget(self.scroll_area)

        # Центральний віджет
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Початковий масштаб
        self.zoom_level = 1.0  # 1.0 - це 100% в QWebEngineView

        # Центральний віджет
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Додаємо змінні для перетягування
        self.is_dragging = False
        self.last_mouse_position = QPoint()

        # Задаємо обробку подій для scroll_area
        self.scroll_area.viewport().installEventFilter(self)

    def validate_inputs(self):

        def basis_correct(basis: str):

            db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
                ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]

            def split_string(s: str):

                index = 0

                while index < len(s) and s[index].isdigit(): index += 1
                
                numbers = s[:index]
                letters = s[index:]

                return numbers, letters

            try:

                basis_list = basis.split("/")

            except Exception as e:

                return False

            else:

                if len(basis_list) == 1: return False

                try:

                    num_1, str_1 = split_string(basis_list[0])
                    num_2, str_2 = split_string(basis_list[1])

                except Exception as e:

                    return False

                else:

                    if any(len(x) == 0 for x in [num_1, num_2, str_1, str_2]): return False

                    if any(not x.isdigit() for x in num_1): return False
                    if any(not x.isdigit() for x in num_2): return False


                    if not([str_1, str_2] in db): return False

            return True

        self.clear_error_styles()

        has_error = False
        db = [['І', 'АБО'], ['І-НЕ', 'І-НЕ'], ['АБО', 'І-НЕ'], ['АБО-НЕ', 'АБО'],
        ['АБО', 'І'], ['АБО-НЕ', 'АБО-НЕ'], ['І', 'АБО-НЕ'], ['І-НЕ', 'І']]

        num_of_args = self.arg_input.text()
        sets_number = self.sets_input.text()
        basis = self.basis_input.text()

        try:

            float(num_of_args)

        except Exception as e:

            self.display_error(self.arg_error_label, self.arg_input)
            has_error = True

        else:

            if not(float(num_of_args).is_integer() and float(num_of_args) > 0):

                self.display_error(self.arg_error_label, self.arg_input)
                has_error = True

        try:

            sets_number = [int(x) for x in sets_number.split(',')]

        except Exception as e:

            self.display_error(self.sets_error_label, self.sets_input)
            has_error = True

        else:

            if not(all(x >= 0 for x in sets_number) and all(sets_number.count(x) == 1 for x in sets_number)):

                self.display_error(self.sets_error_label, self.sets_input)
                has_error = True

            try:

                if any(x >= 2**int(num_of_args) for x in sets_number):

                    self.display_error(self.sets_error_label, self.sets_input)
                    has_error = True

            except Exception as e:

                pass

        try:

            basis.split('/')

        except Exception as e:

            self.display_error(self.basis_error_label, self.basis_input)
            has_error = True

        else:

            if not(basis_correct(basis)):

                self.display_error(self.basis_error_label, self.basis_input)
                has_error = True

        return has_error

    def show_basis(self):

        text = "Дозволені елементні базиси:\n\n"

        for basis in db: text += f"{basis[0]}/{basis[1]}\n"

        text = text.rstrip(", ")

        QMessageBox.information(self, "Елементні базиси", text)

    def display_error(self, error_label, widget):
        error_label.show()
        widget.setStyleSheet("border: 1px solid red;")

    def clear_error(self, error_label, widget):
        # Приховує повідомлення про помилку і скидає стиль
        error_label.hide()
        widget.setStyleSheet("")

    def clear_error_styles(self):
        # Очищення повідомлень про помилки та стилів полів
        self.clear_error(self.arg_error_label, self.arg_input)
        self.clear_error(self.sets_error_label, self.sets_input)
        self.clear_error(self.basis_error_label, self.basis_input)

    def show_authors_dialog(self):
        # Відображення інформації про програму та авторів
        QMessageBox.information(self, "Автори (з ІО-41):", 
                                "Основна логіка: Давидчук Артем\n"
                                "Вивід та фомули: Білий Іван, Давидчук Артем\n"
                                "Таблиця істинності: Троценко Максим\n"
                                "(Порошенко випусти мене)")

    def set_initial_html(self):

        # HTML з темним фоном для відображення за замовчуванням
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
          <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap">
          <style>
            body {
                background-color: #0D1117;
                color: #C9D1D9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: 'Roboto', sans-serif;
            }
            p {
                font-size: 24px;
                font-weight: bold;
            }
          </style>
        </head>
        <body>
          <p>Введіть дані та натисніть "Розрахувати" або клавішу Enter</p>
        </body>
        </html>
        """

        self.view.setHtml(html_content)

        self.basis_input.setStyleSheet("")

    def clear_output(self):
        # Очищення HTML-контенту у QWebEngineView
        self.view.setHtml("<html><body style='background-color:#0D1117;'></body></html>")

    def keyPressEvent(self, event: QKeyEvent):
        # Перевіряємо, чи була натиснута клавіша Enter
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.display_formula()

    def display_formula(self):

        if not self.validate_inputs():

            latex_code = generate(self.arg_input.text(), self.sets_input.text(), self.basis_input.text())

            # Формування HTML-коду для відображення формули через MathJax
            html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                <script>
                    MathJax = {{
                    options: {{
                        enableMenu: false  // Вимикає контекстне меню MathJax
                    }},
                    tex: {{
                        displayMath: [['$$', '$$']],  // Застосування display-режиму для формул
                    }},
                    chtml: {{
                        displayAlign: 'left',  // Вирівнювання формул за лівим краєм
                        displayIndent: '0'     // Відсутність додаткового відступу
                    }}
                    }};
                </script>
                <style>
                    body {{
                        background-color: #0D1117;
                        color: white;
                        margin: 0;
                        padding: 20px; /* Відступ від країв */
                        font-size: 16px;
                        text-align: left; /* Вирівнювання тексту по лівому краю */
                    }}
                    p {{
                        text-align: left; /* Вирівнювання тексту по лівому краю */
                        margin: 0;
                    }}
                    .mjx-display {{
                        text-align: left !important; /* Примусове вирівнювання формул за лівим краєм */
                    }}
                    .MathJax {{
                        width: 100%;
                        display: inline-block;
                        text-align: left !important; /* Примусове вирівнювання всіх формул за лівим краєм */
                    }}
                </style>
                </head>
                <body>
                <p>$$ \\begin{{array}}{{l}} {latex_code} \\end{{array}} $$</p>
                </body>
                </html>
                """

            self.view.setHtml(html_content)

        else:

            self.clear_output()

    def wheelEvent(self, event):
        # Масштабування за допомогою прокрутки коліщатка миші
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()

    def zoom_in(self):
        # Збільшення масштабу
        self.zoom_level += 0.1  # Збільшуємо на 10%
        self.view.setZoomFactor(self.zoom_level)

    def zoom_out(self):
        # Зменшення масштабу
        if self.zoom_level > 0.2:
            self.zoom_level -= 0.1  # Зменшуємо на 10%
            self.view.setZoomFactor(self.zoom_level)

    def eventFilter(self, source, event):
        # Перевіряємо, чи подія відбувається у viewport
        if source is self.scroll_area.viewport():
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.is_dragging = True
                    self.last_mouse_position = event.globalPosition().toPoint()
            elif event.type() == QEvent.Type.MouseMove:
                if self.is_dragging:
                    # Виконуємо прокрутку при переміщенні миші
                    delta = event.globalPosition().toPoint() - self.last_mouse_position
                    self.last_mouse_position = event.globalPosition().toPoint()
                    self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() - delta.x())
                    self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().value() - delta.y())
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.is_dragging = False
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(argv)
    window = LaTeXFormulaApp()
    window.show()
    exit(app.exec())