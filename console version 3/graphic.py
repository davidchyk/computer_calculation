import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

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

def render_latex_formula(latex_str, data_table):

    latex_str = latex_str.replace('∧', '\\wedge')
    latex_str = latex_str.replace('V', '\\vee')
    latex_str = latex_str.replace('⊕', '\\oplus')

    latex_str = replace_not_with_overline(latex_str)

    plt.figure(figsize=(20, 8))
    plt.text(0, 1, f"{latex_str}", fontsize=20, ha='left', va='top', fontdict={'family': 'Times New Roman'})
    plt.axis('off')

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.axis('off')
    table = ax.table(cellText=data_table[1:], colLabels=data_table[0], cellLoc='center', loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)

    table.auto_set_column_width([0.2])

    plt.show(block=True)

def graph(args, data_table):

    latex_str = """"""

    for data in args:

        data = data.replace(' ', r' \ ')

        latex_str += f"${data}$ \n"

    render_latex_formula(latex_str, data_table)