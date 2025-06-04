import subprocess
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime as dt

def check_pdflatex_installed():

    """Перевіряє, чи встановлений pdflatex."""
    try:
        subprocess.run(['pdflatex', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def compile_latex(temp_dir, latex_str, output_path):

    """
    Компілірує LaTeX рядок у PDF та зберігає його за обраним користувачем шляхом.

    :param latex_str: Строка з LaTeX кодом
    :param output_path: Повний шлях до вихідного PDF файлу
    :return: True, якщо успішно, інакше False
    """

    if not check_pdflatex_installed():
        messagebox.showerror("Помилка", "Помилка. Будь ласка, встановіть LaTeX-компілятор."); return False

    tex_file_path = os.path.join(temp_dir, "document.tex")

    # Записуємо LaTeX код у .txt файл
    print("LETS GO")
    with open("main.txt", 'w', encoding='utf-8') as te: te.write(latex_str)

    # Записуємо LaTeX код у .tex файл
    with open(tex_file_path, 'w', encoding='utf-8') as tex_file: tex_file.write(latex_str)

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

        with open("error.txt", 'w', encoding='utf-8') as te: te.write(error_message)

        messagebox.showerror("Помилка компіляції", f"Сталася помилка під час компіляції LaTeX:\n{error_message}")
        #with open("error_log.txt", "w", encoding="utf-8") as f: f.write(error_message)
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

    root.destroy()

    if file_path: return file_path
    return None

def get_true_table(list_man, num_of_args):

    table_config = ""

    for i in range(num_of_args): table_config += f"|c"
    table_config += r"!{\vrule width 1.5pt}c|"
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

        if data is None:

            new_latex_list.append(data)
            continue

        data = data.replace('∧', '\\wedge')
        data = data.replace('∨', '\\vee')
        data = data.replace('⊕', '\\oplus')

        data = replace_not_with_overline(data)

        new_latex_list.append(data)

    return new_latex_list

def get_latex_formula(args, page_width, page_height, block_width):

    latex_list = args[0]
    truth_table_list = args[1]

    truth_index = 0
    start_item_index = 0

    final_latex_formula = r"""
    \documentclass{article}

    \usepackage[utf8]{inputenc}
    \usepackage[T2A]{fontenc}
    \usepackage[english, ukrainian]{babel}
    \usepackage{lmodern}
    \usepackage{microtype}
    \usepackage{graphicx}
    \usepackage{geometry}
    \usepackage{array}
    \usepackage{float}
    \usepackage{nopageno}
    \usepackage{xcolor}
    \usepackage{hyperref} 
    \geometry{
        paperwidth=""" + f"{page_width}cm," + r"""
        paperheight=""" + f"{page_height}cm," + r"""
        left=1cm,
        right=1cm,
        top=1cm,
        bottom=1cm,
    }

    \definecolor{myteal}{RGB}{0, 128, 128}
    \definecolor{mysteelblue}{RGB}{70, 130, 180}
    \definecolor{mycoral}{RGB}{255, 127, 80}

    \hypersetup{
        colorlinks=true,
        linkcolor=myteal,      % Внутрішні посилання
        urlcolor=mysteelblue,  % Зовнішні посилання
        citecolor=mycoral      % Бібліографічні посилання
    }

    \usepackage{setspace}
    \onehalfspacing

    \emergencystretch=1em
    \sloppy

    \usepackage{amsmath, amsfonts, amssymb}

    \begin{document}

    \pagestyle{empty} % Вимикає нумерацію сторінок

    \setlength{\abovedisplayskip}{1pt}
    \setlength{\belowdisplayskip}{1pt}

    \begin{flushleft}

    {\Huge Computer Logic Analysis and Calculation Suite}

    {\Large Версія програмного забезпечення: 3.5 Beta\newline}
    {\Large Розробниками цієї програми є студенти КПІ, 1 курс 2024 року, ІО-41 \newline}

    {\large Розробка аналізу функції: Давидчук Артем \newline}
    {\large Побудова комбінаційної схеми: Білий Іван, Давидчук Артем \newline}
    {\large Парсинг функції: Троценко Максим \newline}
    {\large BackEnd: ... \newline}
    {\large FrontEnd: Єнь Данило \newline}

    {\large Примітка: \href{https://uk.wikipedia.org/wiki/%D0%9B%D0%BE%D0%B3%D1%96%D1%87%D0%BD%D1%96_%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%B8}{Умовні позначення логічних елементів} }

    {\large Якщо виникли помилки, надішліть їх нам на адресу ел. пошти: \href{mailto:belijivan9@gmail.com}{belijivan9@gmail.com} \newline}
    {\large Якщо виникли питання або пропозиції, надішліть їх нам на адресу ел. пошти: \href{mailto:artemdiachenko2007@gmail.com}{artemdiachenko2007@gmail.com} \newline}
    \newline
    \newline
    {\large Всі права застережено © 2024 -- """ + str(dt.now().year) + r"""}

    \end{flushleft}

    \newpage

    """

    while truth_index < len(truth_table_list):

        temp_deep = ""

        while start_item_index < len(latex_list):

            if latex_list[start_item_index] == None: start_item_index += 1; break

            temp_deep += r"""
            \begin{flalign*}
                &
            """ +\
            latex_list[start_item_index] + \
            r"""
                &
            \end{flalign*}"""

            start_item_index += 1

        temp = r"""\noindent
        \begin{minipage}[t]{""" + f"{block_width}cm" + r"""}
            \text{\Large Truth table for $y_""" + f"{truth_index+1}" + r"""$:}

            \begin{flalign*}&""" + \
            truth_table_list[truth_index] + r"""
            &
            \end{flalign*}
        \end{minipage}
            \begin{minipage}[t]{0.5\textwidth}
                \raggedright % Вирівнювання тексту до лівого краю всередині minipage

                \text{\Large Result of analysis of function $y_""" + f"{truth_index+1}" + r"""$:}
                
                """ + temp_deep + r"""
                \begin{flalign*}
                    &
                    \text{\large Unstable Beta! Комбінаційна схема функції $y_""" + f"{truth_index+1}" + r"""$:}
                    &
                \end{flalign*}

                \begin{figure}[H]
                    \includegraphics[height=6cm]{OUTPUT_SCHEMME_Y_""" + f"{truth_index+1}" + r""".png}
                    \label{fig:left_top_image}
                \end{figure}

                % Added:

                \begin{flalign*}
                    &
                    \text{\large Unstable Beta! Діаграма Вейча для $y_""" + f"{truth_index+1}" + r"""$:}
                    &
                \end{flalign*}

                \begin{figure}[H]
                    \includegraphics[width=0.3\linewidth]{plot""" + f"{truth_index+1}" + r""".pdf}
                    \label{fig:left_top_image}
                \end{figure}

                %%%%%%%%%%%%%%%%%%%%%%%%%%%

            \end{minipage}

            \newpage
        """

        final_latex_formula += temp
        truth_index += 1

    final_latex_formula += r"""
    \end{document}
    """

    return final_latex_formula

def create_pdf_main(temp_dir: str, args:list, page_params:list):

    print("\nСтворення PDF файлу...\n")

    page_width = page_params[0]
    page_height = page_params[1]
    block_width = page_params[2]

    latex_list = get_latex_list(args[0])
    latex_str = get_latex_formula([latex_list, args[1]], page_width, page_height, block_width)

    save_path = select_save_location()

    if save_path:
        success = compile_latex(temp_dir, latex_str, save_path)
        if success:
            print(f"PDF збережено за адресою: {save_path}")
        else:
            print("Не вдалося створити PDF.")
    else:
        print("Користувач відмінив збереження.")