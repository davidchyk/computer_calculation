import subprocess
from graphic import render_latex_formula
import os

def latex_to_pdf(latex_body, output_pdf='output.pdf'):
    # 1. Огортаємо ваш латекс-код у мінімальну структуру документу
    latex_template = r"""
        \documentclass[a4paper,12pt]{article}
        \usepackage[T1]{fontenc}
        \usepackage[utf8]{inputenc}
        \usepackage{amsmath, amssymb}
        \usepackage[ukrainian]{babel}
        \usepackage{geometry}
        \geometry{margin=1in}

        \begin{document}
        % Ваш вміст починається тут
        PLACEHOLDER
        % Ваш вміст закінчується тут
        \end{document}
        """

    # Підставляємо ваші формули замість PLACEHOLDER

    latex_body = latex_body.replace('∨', r'\vee')

    full_latex = latex_template.replace('PLACEHOLDER', latex_body)

    # 2. Пишемо це в тимчасовий .tex-файл
    temp_tex_filename = 'temp.tex'
    with open(temp_tex_filename, 'w', encoding='utf-8') as f: f.write(full_latex)

    # 3. Викликаємо pdflatex (двічі для коректних посилань, індексів тощо)
    #    `-interaction=nonstopmode` дозволяє не зупинятися на помилках інтерпретатора.
    try:

        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', temp_tex_filename],
            check=True
        )
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', temp_tex_filename],
            check=True
        )

        # Після успішної компіляції, перейменуємо temp.pdf в output_pdf
        if os.path.exists('temp.pdf'):
            os.rename('temp.pdf', output_pdf)
            print(f"PDF згенеровано: {output_pdf}")

    except subprocess.CalledProcessError as e:

        print("Помилка під час компіляції LaTeX:", e)

    finally:

        for extension in ('.aux', '.log', '.out', '.tex'):
            temp_file = 'temp' + extension
            if os.path.exists(temp_file):
                os.remove(temp_file)