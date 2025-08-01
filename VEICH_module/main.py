import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re

from minimization import minimize_dnf_as_implicants, minimize_cnf_as_implicants
from create_veich_schemme import create_veich_schemme_pdf

class KarnaughGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор схем Вейча")
        self.geometry("500x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.container = ttk.Frame(self)
        self.container.pack(anchor="w", padx=20, pady=10)

        # Тип нормальної форми (радіокнопки)
        self.nf_type_label = ttk.Label(self.container, text="Тип нормальної форми:")
        self.nf_type_label.pack(anchor="w", pady=5)

        self.nf_type_var = tk.StringVar(value="МДНФ")
        nf_frame = ttk.Frame(self.container)
        nf_frame.pack(anchor="w")
        ttk.Radiobutton(nf_frame, text="МДНФ", variable=self.nf_type_var, value="МДНФ").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(nf_frame, text="МКНФ", variable=self.nf_type_var, value="МКНФ").pack(side=tk.LEFT, padx=5)

        # Кількість аргументів
        self.arg_count_label = ttk.Label(self.container, text="Кількість аргументів (1-9):")
        self.arg_count_label.pack(anchor="w", pady=5)

        self.arg_count_spinbox = ttk.Spinbox(self.container, from_=1, to=9, width=5)
        self.arg_count_spinbox.pack(anchor="w", pady=5)

        # Набори з 1
        self.ones_label = ttk.Label(self.container, text="Номери наборів, де функція набуває значенню 1 (через кому):")
        self.ones_label.pack(anchor="w", pady=5)

        self.ones_entry = ttk.Entry(self.container, width=50)
        self.ones_entry.pack(anchor="w", pady=5)

        self.ones_error = ttk.Label(self.container, text="", foreground="red")
        self.ones_error.pack(anchor="w")

        # Аргументи (необов'язково)
        self.custom_args_label = ttk.Label(self.container, text="Назви аргументів (через кому, опціонально):")
        self.custom_args_label.pack(anchor="w", pady=5)

        self.custom_args_entry = ttk.Entry(self.container, width=50)
        self.custom_args_entry.pack(anchor="w", pady=5)

        self.custom_args_error = ttk.Label(self.container, text="", foreground="red")
        self.custom_args_error.pack(anchor="w")

        # Кнопка створення
        self.create_btn = ttk.Button(self.container, text="Створити схему Вейча", command=self.main_going)
        self.create_btn.pack(anchor="w", pady=20)

    def select_output_file(self):
        self.clear_errors()
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Оберіть місце для збереження PDF"
        )
        return filepath

    def validate_inputs(self):
        valid = True

        ones_text = self.ones_entry.get()
        maxArgs = 1 << int(self.arg_count_spinbox.get())

        try:
            if ones_text:
                values = [int(x.strip()) for x in ones_text.split(',')]
                if any(x >= maxArgs for x in values):
                    self.ones_entry.configure(background="misty rose")
                    self.ones_error.configure(text="Неправильний ввід: містить неправильний набір")
                    valid = False
        except ValueError:
            self.ones_entry.configure(background="misty rose")
            self.ones_error.configure(text="Неправильний формат: тільки числа через кому")
            valid = False

        custom_args = self.custom_args_entry.get()
        if custom_args:
            args = [x.strip() for x in custom_args.split(',')]

            pattern = re.compile(r'^[A-Za-z]\d$')
            if not all(pattern.match(arg) for arg in args):
                self.custom_args_entry.configure(background="misty rose")
                self.custom_args_error.configure(text="Кожен аргумент має бути у форматі: латинська літера + цифра (наприклад, x1)")
                valid = False

            elif len(set(args)) != len(args):
                self.custom_args_entry.configure(background="misty rose")
                self.custom_args_error.configure(text="Аргументи мають бути унікальні")
                valid = False

            elif len(args) != int(self.arg_count_spinbox.get()):
                self.custom_args_entry.configure(background="misty rose")
                self.custom_args_error.configure(text="Кількість аргументів не збігається з введеними назвами аргументів")
                valid = False

        return valid

    def clear_errors(self):
        self.ones_entry.configure(background="white")
        self.ones_error.configure(text="")
        self.custom_args_entry.configure(background="white")
        self.custom_args_error.configure(text="")

    def generate_veitch_diagram(self, filepath):
        type_of = 1 if self.nf_type_var.get() == "МДНФ" else 0
        number_of_arguments = int(self.arg_count_spinbox.get())
        number_of_sets = 1 << number_of_arguments

        sets_number = [int(x.strip()) for x in self.ones_entry.get().split(',')]
        custom_args_raw = [
            f"{x[0]}_{x[1]}" for x in [arg.strip() for arg in self.custom_args_entry.get().split(',')]
        ] if self.custom_args_entry.get().strip() else []

        if type_of == 1:
            minimize_result = minimize_dnf_as_implicants(number_of_arguments, sets_number)
        else:
            minimize_result = minimize_cnf_as_implicants(number_of_arguments, [x for x in range(number_of_sets) if x not in sets_number])

        create_veich_schemme_pdf(filepath, (type_of, minimize_result[1], sets_number, custom_args_raw))
        messagebox.showinfo("Готово", f"Схему Вейча збережено до:\n{filepath}")

    def main_going(self):
        self.clear_errors()
        try:
            if self.validate_inputs():
                filepath = self.select_output_file()
                if filepath:
                    self.generate_veitch_diagram(filepath)
        except Exception:
            messagebox.showerror("Невідома помилка", "Empty")

if __name__ == "__main__":
    app = KarnaughGUI()
    app.mainloop()
