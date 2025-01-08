import subprocess
import os
import shutil
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox

def check_pdflatex_installed():

    """Перевіряє, чи встановлений pdflatex."""
    try:
        subprocess.run(['pdflatex', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def compile_latex(latex_str, output_path):

    print("compiling latex...")

    """
    Компілірує LaTeX рядок у PDF та зберігає його за обраним користувачем шляхом.

    :param latex_str: Строка з LaTeX кодом
    :param output_path: Повний шлях до вихідного PDF файлу
    :return: True, якщо успішно, інакше False
    """
    if not check_pdflatex_installed():
        messagebox.showerror("Помилка", "pdflatex не встановлено. Будь ласка, встановіть LaTeX-компілятор.")
        return False

    # Створюємо тимчасову папку
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_file_path = os.path.join(temp_dir, "document.tex")
        
        # Записуємо LaTeX код у .tex файл
        with open(tex_file_path, 'w', encoding='utf-8') as tex_file:
            tex_file.write(latex_str)
        
        # Виконуємо компіляцію
        try:
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file_path],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            error_message = e.stdout.decode() + "\n" + e.stderr.decode()
            messagebox.showerror("Помилка компіляції", f"Сталася помилка під час компіляції LaTeX:\n{error_message}")
            return False
        
        # Шлях до згенерованого PDF
        generated_pdf = os.path.join(temp_dir, "document.pdf")
        
        if not os.path.exists(generated_pdf):
            messagebox.showerror("Помилка", "Не вдалося створити PDF файл.")
            return False
        
        # Копіюємо PDF у вказане місце
        try:
            shutil.copyfile(generated_pdf, output_path)
            messagebox.showinfo("Успіх", f"PDF успішно створено: {output_path}")
            return True
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти PDF файл:\n{e}")
            return False

def select_save_location():

    """Відкриває діалогове вікно для вибору місця збереження PDF."""
    root = tk.Tk()
    root.withdraw()  # Ховає головне вікно

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Зберегти PDF як"
    )

    if file_path:
        return file_path
    else:
        return None

def get_true_table(list_man, num_of_args, num_of_function):

    print("forming true table...")

    table_config = ""

    for i in range(num_of_args): table_config += f"|c"
    table_config += r"!{\vrule width 1.5pt}"
    for i in range(num_of_function): table_config += f"c|"
    table_config = "{" + table_config + "}"

    table_content = """"""

    for x in range(2**num_of_args+1):

        temping = ""

        for item in list_man[x]: temping += f"{item} & "

        temping  = r"""\hline
        """ + temping[:-2] + r"\\"

        table_content += f"""
        {temping}"""

    table_content += r"""
        \hline"""

    final = r"""\begin{tabular}""" + table_config + table_content +r"""
    \end{tabular}"""

    return final

def get_latex_list(args):

    print("getting latex list...")

    def replace_not_with_overline(expression):

        stack = []
        result = []
        i = 0

        while i < len(expression):
        
            if expression[i:i+4] == 'not(':

                result.append('\\overline{')
                stack.append('}')
                i += 4

            elif expression[i] == '(':

                result.append('(')
                stack.append(')')
                i += 1

            elif expression[i] == ')' and stack:

                result.append(stack.pop())
                i += 1

            else:

                result.append(expression[i])
                i += 1

        return ''.join(result)

    new_latex_list = []

    for data in args:

        #data = data.replace(' ', r' \ ')

        data = data.replace('∧', '\\wedge')
        data = data.replace('∨', '\\vee')
        data = data.replace('⊕', '\\oplus')

        data = replace_not_with_overline(data)

        new_latex_list.append(data)

    return new_latex_list

def get_latex_formula(latex_list, page_width):

    print("getting latex formula...")

    final_latex_formula = r"""
    \documentclass{article}

    \usepackage[utf8]{inputenc}
    \usepackage[T1]{fontenc}
    \usepackage[english, ukrainian]{babel}
    \usepackage{lmodern}
    \usepackage{microtype}
    \usepackage{geometry}
    \usepackage{array}
    \geometry{
        paperwidth=""" + f"{page_width}cm," + r"""
        paperheight=30cm,
        left=1cm,
        right=1cm,
        top=1cm,
        bottom=1cm,
    }

    \usepackage{setspace}
    \onehalfspacing

    \pagestyle{empty} % Вимикає нумерацію сторінок

    \emergencystretch=1em
    \sloppy

    \usepackage{amsmath, amsfonts, amssymb}

    \begin{document}

    \setlength{\abovedisplayskip}{-2pt}
    \setlength{\belowdisplayskip}{-2pt}
    """

    for data in latex_list:

        temp = r"""
    \begin{flalign*}
    &
    """ +\
    data + \
        r"""
    &
    \end{flalign*}
    """

        final_latex_formula += temp

    ttt = r"""
    \end{document}
    """

    final_latex_formula += ttt

    return final_latex_formula

def create_pdf_main(args, page_width):

    print("start...")

    latex_list = get_latex_list(args)
    latex_str = get_latex_formula(latex_list, page_width)

    save_path = select_save_location()

    if save_path:
        success = compile_latex(latex_str, save_path)
        if success:
            print(f"PDF збережено за адресою: {save_path}")
        else:
            print("Не вдалося створити PDF.")
    else:
        print("Користувач відмінив збереження.")