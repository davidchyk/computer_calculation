import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import traceback

# === ПАРАМЕТРИ ===
CELL_SIZE = 0.2  # Розмір клітинки
LINE_WIDTH = 1.2  # Товщина обведення
PADDING = 0.03  # Відступ усередині, щоб рамки не накладались

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.latex.preamble'] = r'''\usepackage{amsmath}'''

def draw_axis_brackets(ax, list_args):

    try:

        if len(list_args) == 9:

            ...

        elif len(list_args) == 8:

            # Права_правіша дужка (X8)
            ax.plot([3.6, 3.6], [3.4, 1.8], color='black', linewidth=3, zorder=100)
            ax.text(3.67, 2.6, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня_верхня дужка (X7)
            ax.plot([1.8, 3.4], [3.55, 3.55], color='black', linewidth=3, zorder=100)
            ax.text(2.6, 3.61, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Ліва_лівіша дужка (X6)
            ax.plot([0.0, 0.0], [1.8, 1.0], color='black', linewidth=3, zorder=100)
            ax.text(-0.07, 1.4, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([0.0, 0.0], [3.4, 2.6], color='black', linewidth=3, zorder=100)
            ax.text(-0.07, 3.0, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_вища дужка (X5)
            ax.plot([0.6, 1.4], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(1.0, 0.12, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([2.2, 3.0], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(2.6, 0.12, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня_нижча дужка (X4)
            ax.plot([0.2, 1.0], [3.43, 3.43], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 3.49, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.8, 2.6], [3.43, 3.43], color='black', linewidth=3, zorder=100)
            ax.text(2.2, 3.49, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Ліва_правіша дужка (X3)
            ax.plot([0.17, 0.17], [1, 0.6], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.8, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([0.17, 0.17], [1.8, 1.4], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 1.6, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([0.17, 0.17], [2.6, 2.2], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 2.4, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([0.17, 0.17], [3.4, 3.0], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 3.2, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_нижня дужка (X2)
            ax.plot([0.4, 0.8], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 0.01, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.2, 1.6], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(1.4, 0.01, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([2.0, 2.4], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(2.2, 0.01, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([2.8, 3.2], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(3.0, 0.01, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Права_лівіша дужка (X1)
            ax.plot([3.43, 3.43], [0.8, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(3.5, 0.6, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([3.43, 3.43], [1.6, 1.2], color='black', linewidth=3, zorder=100)
            ax.text(3.5, 1.4, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([3.43, 3.43], [2.4, 2.0], color='black', linewidth=3, zorder=100)
            ax.text(3.5, 2.2, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([3.43, 3.43], [3.2, 2.8], color='black', linewidth=3, zorder=100)
            ax.text(3.5, 3.0, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 7:

            # Верхня_верхня дужка (X7)
            ax.plot([1.8, 3.4], [1.95, 1.95], color='black', linewidth=3, zorder=100)
            ax.text(2.6, 2.01, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Ліва_лівіша дужка (X6)
            ax.plot([0.0, 0.0], [1.8, 1.0], color='black', linewidth=3, zorder=100)
            ax.text(-0.07, 1.4, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_вища дужка (X5)
            ax.plot([0.6, 1.4], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(1.0, 0.12, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([2.2, 3.0], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(2.6, 0.12, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня_нижча дужка (X4)
            ax.plot([0.2, 1.0], [1.83, 1.83], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 1.89, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.8, 2.6], [1.83, 1.83], color='black', linewidth=3, zorder=100)
            ax.text(2.2, 1.89, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Ліва_правіша дужка (X3)
            ax.plot([0.17, 0.17], [1, 0.6], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.8, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([0.17, 0.17], [1.8, 1.4], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 1.6, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_нижня дужка (X2)
            ax.plot([0.4, 0.8], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 0.01, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.2, 1.6], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(1.4, 0.01, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([2.0, 2.4], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(2.2, 0.01, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([2.8, 3.2], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(3.0, 0.01, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Права дужка (X1)
            ax.plot([3.43, 3.43], [0.8, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(3.5, 0.6, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([3.43, 3.43], [1.6, 1.2], color='black', linewidth=3, zorder=100)
            ax.text(3.5, 1.4, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 6:

            # Ліва_лівіша дужка (X6)
            ax.plot([0.0, 0.0], [1.8, 1.0], color='black', linewidth=3, zorder=100)
            ax.text(-0.07, 1.4, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_вища дужка (X5)
            ax.plot([0.6, 1.4], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(1.0, 0.12, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня дужка (X4)
            ax.plot([0.2, 1.0], [1.83, 1.83], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 1.89, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Ліва_правіша дужка (X3)
            ax.plot([0.17, 0.17], [1, 0.6], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.8, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([0.17, 0.17], [1.8, 1.4], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 1.6, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_нижня дужка (X2)
            ax.plot([0.4, 0.8], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 0.01, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.2, 1.6], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(1.4, 0.01, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Права дужка (X1)
            ax.plot([1.83, 1.83], [0.8, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(1.9, 0.6, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.83, 1.83], [1.6, 1.2], color='black', linewidth=3, zorder=100)
            ax.text(1.9, 1.4, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 5:

            # Нижня_вища дужка (X5)
            ax.plot([0.6, 1.4], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(1.0, 0.12, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня дужка (X4)
            ax.plot([0.2, 1.0], [1.03, 1.03], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 1.09, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Ліва дужка (X3)
            ax.plot([0.17, 0.17], [1, 0.6], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.8, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня_нижня дужка (X2)
            ax.plot([0.4, 0.8], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 0.01, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            ax.plot([1.2, 1.6], [0.05, 0.05], color='black', linewidth=3, zorder=100)
            ax.text(1.4, 0.01, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Права дужка (X1)
            ax.plot([1.83, 1.83], [0.8, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(1.9, 0.6, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 4:

            # Ліва дужка (X4)
            ax.plot([0.17, 0.17], [1, 0.6], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.8, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня дужка (X3)
            ax.plot([0.2, 0.6], [1.03, 1.03], color='black', linewidth=3, zorder=100)
            ax.text(0.4, 1.09, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Права дужка (X2)
            ax.plot([1.03, 1.03], [0.8, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(1.10, 0.6, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня дужка (X1)
            ax.plot([0.4, 0.8], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 0.12, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 3:

            # Ліва дужка (X3)
            ax.plot([0.17, 0.17], [0.6, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.52, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня дужка (X2)
            ax.plot([0.2, 0.6], [0.63, 0.63], color='black', linewidth=3, zorder=100)
            ax.text(0.4, 0.69, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Нижня дужка (X1)
            ax.plot([0.4, 0.8], [0.17, 0.17], color='black', linewidth=3, zorder=100)
            ax.text(0.6, 0.12, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 2:

            # Ліва дужка (X2)
            ax.plot([0.17, 0.17], [0.6, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.52, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

            # Верхня дужка (X2)
            ax.plot([0.2, 0.4], [0.63, 0.63], color='black', linewidth=3, zorder=100)
            ax.text(0.3, 0.69, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        elif len(list_args) == 1:

            # Ліва дужка (X1)
            ax.plot([0.17, 0.17], [0.6, 0.4], color='black', linewidth=3, zorder=100)
            ax.text(0.11, 0.52, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

    except Exception: return False
    return True

def draw_kmap_with_tight_rounded_boxes(kmap, groups, list_args, filename):

    """
    Малює карту Вейча та додає обведення груп із заокругленими прямокутниками.
    Тепер обведення не заходить на сусідні клітинки!
    """

    try:

        cell_size=CELL_SIZE

        rows, cols = kmap.shape
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        # **Правильний масштаб під клітинки**
        fig.set_size_inches(cols * cell_size * 6, rows * cell_size * 6)

        # 1) Малюємо таблицю (сітку)
        for r in range(rows):
            for c in range(cols):
                x = c * cell_size
                y = (rows - 1 - r) * cell_size  # **Y правильно масштабується**

                # Прямокутник сітки
                ax.add_patch(Rectangle(
                    (x, y),
                    cell_size,
                    cell_size,
                    fill=False,
                    edgecolor='black',
                    linewidth=0.8
                ))

                # Текст (значення у клітинці)
                ax.text(
                    x + cell_size / 2,
                    y + cell_size / 2,
                    r"\texttt{" f"{kmap[r, c]}" "}",
                    ha='center',
                    va='center',
                    fontsize=20
                )

        for group in groups:

            mini_groups = groups[group][0]
            color = groups[group][1]
            line_type = groups[group][2]

            for mini_group in mini_groups:

                # Визначаємо точні межі групи
                min_r = mini_group[0]
                min_c = mini_group[1]

                max_r = mini_group[2]
                max_c = mini_group[3]

                # **Правильне позиціонування**
                x_rect = min_c * cell_size + PADDING  # Легкий внутрішній відступ
                y_rect = (rows - 1 - max_r) * cell_size + PADDING  # Виправлений Y
                width = (max_c - min_c + 1) * cell_size - 2 * PADDING  # Щоб не виходило за клітинку
                height = (max_r - min_r + 1) * cell_size - 2 * PADDING

                # Округлений прямокутник, який не виходить за межі
                rounded_box = FancyBboxPatch(
                    (x_rect, y_rect),
                    width, height,
                    boxstyle=f"round,pad=0.02",  # Мінімальне заокруглення без виходу за клітинки
                    edgecolor=color,
                    linewidth=LINE_WIDTH,
                    facecolor='none',
                    linestyle=line_type  # Задаємо стиль лінії
                )
                ax.add_patch(rounded_box)

        ax.set_xticks([])
        ax.set_yticks([])

        edge_rows = {0, rows - 1}
        edge_cols = {0, cols - 1}

        # Видаляємо крайні клітинки (Rectangle)
        for patch in list(ax.patches):
            if not isinstance(patch, Rectangle):
                continue  # пропустити обведення (FancyBboxPatch та ін.)

            x, y = patch.get_xy()
            c = int(x / cell_size)
            r = rows - 1 - int(y / cell_size)

            if r in edge_rows or c in edge_cols:
                patch.remove()

        # Видаляємо крайні тексти (Text)
        for text in list(ax.texts):
            x, y = text.get_position()
            c = int(x / cell_size)
            r = rows - 1 - int(y / cell_size)

            if r in edge_rows or c in edge_cols:
                text.remove()

            ax.set_xlim(0, cols * cell_size)
            ax.set_ylim(0, rows * cell_size)

        # Скільки "ластика" залізатиме в середину (оптимально ~0.5-1 клітинки)
        fade_depth = cell_size * 0.9

        # Верхній край
        ax.add_patch(Rectangle(
            (0, rows * cell_size - fade_depth),
            cols * cell_size, fade_depth,
            facecolor='white',
            edgecolor='none',
            alpha=1.0,
            zorder=10
        ))

        # Нижній край
        ax.add_patch(Rectangle(
            (0, 0),
            cols * cell_size, fade_depth,
            facecolor='white',
            edgecolor='none',
            alpha=1.0,
            zorder=10
        ))

        # Лівий край
        ax.add_patch(Rectangle(
            (0, 0),
            fade_depth, rows * cell_size,
            facecolor='white',
            edgecolor='none',
            alpha=1.0,
            zorder=10
        ))

        # Правий край
        ax.add_patch(Rectangle(
            (cols * cell_size - fade_depth, 0),
            fade_depth, rows * cell_size,
            facecolor='white',
            edgecolor='none',
            alpha=1.0,
            zorder=10
        ))

        if not draw_axis_brackets(ax, list_args): return False

        #plt.show()

        # Збереження у файл
        plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        print(f"Зображення збережено у файл: {filename}")

    except Exception: return False
    return True

def paint(filename, data: tuple):

    try:

        kmap, forming_groups, num_of_args, list_args = data

        print("input kmap:")
        print(kmap)

        if not list_args:

            for x in range(num_of_args, 0, -1): list_args.append(f"x_{x}")

        print(list_args)

    except Exception: return False
    return draw_kmap_with_tight_rounded_boxes(kmap, forming_groups, list_args, filename)

def veich_create(filename, type, minimized_term_term_list, sets_number, list_args):

    """
    TODO

    GLOBAL:

    [x] 1. Потрібно також будувати для МКНФ

    Veich_schemme:

    [] 1. Бувають моменти, що якщо весь стопчик буде 1, то межі груп будуть дещо дивно відображатись, тому для них особлива логіка
    [] 2. Якщо мінімізація заповнює всі клітинки: написати логіку для цього випадку
    [] 3. При кількості аргументів в 1, крива група

    В Paint:

    [] 0. Добудувати розмітку для 9 аргументів
    [] 1. Коли вже >= 5 аргументів, то потрібно трохи зміщувати рисунок, або видалити рамки, щоб все вмістилось
    [] 2. Коли виявиться, що функція була введена в режимі func, тобто можливі великі прописні аргументи: це потрібно врахувати, щоб лінії в діаграмі їх не перекривали, а звідси і зміщення трохи також змінюється
    [] 3. Можливо також потрібно буде змінювати шрифт аргументів при великій їх кількості перемикальної фукнції
    [] 4. Перевірити правильність розтавлення ліній (дивитись за BACK_VEICH правильний порядок)
    """

    try:

        def differ(s1: str, s2: str) -> bool:

            """
            Повертає True, якщо s1 і s2 не відрізняються (ідентичні)
            або відрізняються рівно на 1 символ; інакше False.
            """

            normal_dict = {}
            index = 0

            for x in range(len(s1)):

                if s1[x] != "X": normal_dict[index] = s1[x]
                index += 1

            for key, value in normal_dict.items():

                if value != s2[key]: return False

            return True

        def find_all_neighbors(points: list, origin: tuple) -> list:

            neighbors = set()
            queue = [origin]

            while queue:
                current = queue.pop(0)
                for point in points:
                    if point not in neighbors and abs(point[0] - current[0]) <= 1 and abs(point[1] - current[1]) <= 1:
                        neighbors.add(point)
                        queue.append(point)

            print(f"For coord: {origin}, neighbors: {list[neighbors]}")

            return list(neighbors)

        def find_min_max(points):

            min_x = min(point[0] for point in points)
            max_x = max(point[0] for point in points)
            min_y = min(point[1] for point in points)
            max_y = max(point[1] for point in points)

            return min_x, min_y, max_x, max_y

        def generate_add_coordinates(start_coord, rows, cols):

            def define_matrix(coord, rows, cols):

                x, y = coord

                if x == 0 and y == 0:

                    return "left_top_corner"

                elif x == 0 and y == cols-1:

                    return "right_top_corner"

                elif x == rows-1 and y == 0:

                    return "left_bottom_corner"

                elif x == rows-1 and y == cols-1:

                    return "right_bottom_corner"

                elif x == 0:

                    return "top_side_part"

                elif x == rows-1:

                    return "bottom_side_part"

                elif y == 0:

                    return "left_side_part"

                elif y == cols-1:

                    return "right_side_part"

                return None

            result_coords = []
            x, y = start_coord

            type_coord = define_matrix(start_coord, rows, cols)

            if type_coord == "left_top_corner":

                result_coords.append((x+rows+1, y+1))
                result_coords.append((x+rows+1, y+cols+1))
                result_coords.append((x+1, y+cols+1))

            elif type_coord == "right_top_corner":

                result_coords.append((x+rows+1, y+1))
                result_coords.append((x+rows+1, y-cols+1))
                result_coords.append((x+1, y-cols+1))

            elif type_coord == "left_bottom_corner":

                result_coords.append((x-rows+1, y+1))
                result_coords.append((x-rows+1, y+cols+1))
                result_coords.append((x+1, y+cols+1))

            elif type_coord == "right_bottom_corner":

                result_coords.append((x-rows+1, y+1))
                result_coords.append((x-rows+1, y-cols+1))
                result_coords.append((x+1, y-cols+1))

            elif type_coord == "top_side_part":

                result_coords.append((x+rows+1, y+1))

            elif type_coord == "bottom_side_part":

                result_coords.append((x-rows+1, y+1))

            elif type_coord == "left_side_part":

                result_coords.append((x+1, y+cols+1))

            elif type_coord == "right_side_part":

                result_coords.append((x+1, y-cols+1))

            return result_coords

        def get_front_group_config(group_index):

            total_colors = len(colors)
            total_linestyles = len(line_configurations)
            # Використовуємо цілу частину від ділення для визначення типу лінії
            linestyle_index = group_index // total_colors  
            # Індекс кольору – залишок від ділення
            color_index = group_index % total_colors  
            # Якщо group_idx перевищує кількість комбінацій, можна циклічно повертати значення
            linestyle_index %= total_linestyles

            return [colors[color_index], line_configurations[linestyle_index]]

        def del_one(FRONT, shape: tuple) -> list:

            result = []
            rows, cols = shape

            print(f"rows: {rows} cols: {cols}")

            for i in np.where(np.all(FRONT == 1, axis=1))[0]:

                result.append((int(i)+1, 0))
                result.append((int(i)+1, cols-1))

            for j in np.where(np.all(FRONT == 1, axis=0))[0]:

                result.append((0, int(j)+1))
                result.append((rows-1, int(j)+1))
    
            print(f"result of deleting: {result}")

            return result

        if type: WORK_minimized_term_term_list = minimized_term_term_list
        else:

            WORK_minimized_term_term_list = []

            for t in minimized_term_term_list:

                t = (t.replace("0", "_")
                     .replace("1", "0")
                     .replace("_", "1"))

                WORK_minimized_term_term_list.append(t)

        result = dict()
        bin_sets = []

        num_of_groups = len(WORK_minimized_term_term_list)
        num_of_args = len(WORK_minimized_term_term_list[0])

        if num_of_groups > 64: return None

        for set_strc in sets_number: bin_sets.append(format(int(set_strc), f'0{num_of_args}b'))

        if num_of_args == 9:

            FRONT_veich_structure = np.zeros((16, 32), dtype=int)
            BACK_veich_structure = [

                ["010101100", "010101110", "010111110", "010111100", "010110100", "010110110", "010100110", "010100100", "011101100", "011101110", "011111110", "011111100", "011110100", "011110110", "011100110", "011100100", "110101100", "110101110", "110111110", "110111100", "110110100", "110110110", "110100110", "110100100", "111101100", "111101110", "111111110", "111111100", "111110100", "111110110", "111100110", "111100100"],
                ["010101101", "010101111", "010111111", "010111101", "010110101", "010110111", "010100111", "010100101", "011101101", "011101111", "011111111", "011111101", "011110101", "011110111", "011100111", "011100101", "110101101", "110101111", "110111111", "110111101", "110110101", "110110111", "110100111", "110100101", "111101101", "111101111", "111111111", "111111101", "111110101", "111110111", "111100111", "111100101"],
                ["010101001", "010101011", "010111011", "010111001", "010110001", "010110011", "010100011", "010100001", "011101001", "011101011", "011111011", "011111001", "011110001", "011110011", "011100011", "011100001", "110101001", "110101011", "110111011", "110111001", "110110001", "110110011", "110100011", "110100001", "111101001", "111101011", "111111011", "111111001", "111110001", "111110011", "111100011", "111100001"],
                ["010101000", "010101010", "010111010", "010111000", "010110000", "010110010", "010100010", "010100000", "011101000", "011101010", "011111010", "011111000", "011110000", "011110010", "011100010", "011100000", "110101000", "110101010", "110111010", "110111000", "110110000", "110110010", "110100010", "110100000", "111101000", "111101010", "111111010", "111111000", "111110000", "111110010", "111100010", "111100000"],
                ["010001100", "010001110", "010011110", "010011100", "010010100", "010010110", "010000110", "010000100", "011001100", "011001110", "011011110", "011011100", "011010100", "011010110", "011000110", "011000100", "110001100", "110001110", "110011110", "110011100", "110010100", "110010110", "110000110", "110000100", "111001100", "111001110", "111011110", "111011100", "111010100", "111010110", "111000110", "111000100"],
                ["010001101", "010001111", "010011111", "010011101", "010010101", "010010111", "010000111", "010000101", "011001101", "011001111", "011011111", "011011101", "011010101", "011010111", "011000111", "011000101", "110001101", "110001111", "110011111", "110011101", "110010101", "110010111", "110000111", "110000101", "111001101", "111001111", "111011111", "111011101", "111010101", "111010111", "111000111", "111000101"],
                ["010001001", "010001011", "010011011", "010011001", "010010001", "010010011", "010000011", "010000001", "011001001", "011001011", "011011011", "011011001", "011010001", "011010011", "011000011", "011000001", "110001001", "110001011", "110011011", "110011001", "110010001", "110010011", "110000011", "110000001", "111001001", "111001011", "111011011", "111011001", "111010001", "111010011", "111000011", "111000001"],
                ["010001000", "010001010", "010011010", "010011000", "010010000", "010010010", "010000010", "010000000", "011001000", "011001010", "011011010", "011011000", "011010000", "011010010", "011000010", "011000000", "110001000", "110001010", "110011010", "110011000", "110010000", "110010010", "110000010", "110000000", "111001000", "111001010", "111011010", "111011000", "111010000", "111010010", "111000010", "111000000"],
                ["000101100", "000101110", "000111110", "000111100", "000110100", "000110110", "000100110", "000100100", "001101100", "001101110", "001111110", "001111100", "001110100", "001110110", "001100110", "001100100", "100101100", "100101110", "100111110", "100111100", "100110100", "100110110", "100100110", "100100100", "101101100", "101101110", "101111110", "101111100", "101110100", "101110110", "101100110", "101100100"],
                ["000101101", "000101111", "000111111", "000111101", "000110101", "000110111", "000100111", "000100101", "001101101", "001101111", "001111111", "001111101", "001110101", "001110111", "001100111", "001100101", "100101101", "100101111", "100111111", "100111101", "100110101", "100110111", "100100111", "100100101", "101101101", "101101111", "101111111", "101111101", "101110101", "101110111", "101100111", "101100101"],
                ["000101001", "000101011", "000111011", "000111001", "000110001", "000110011", "000100011", "000100001", "001101001", "001101011", "001111011", "001111001", "001110001", "001110011", "001100011", "001100001", "100101001", "100101011", "100111011", "100111001", "100110001", "100110011", "100100011", "100100001", "101101001", "101101011", "101111011", "101111001", "101110001", "101110011", "101100011", "101100001"],
                ["000101000", "000101010", "000111010", "000111000", "000110000", "000110010", "000100010", "000100000", "001101000", "001101010", "001111010", "001111000", "001110000", "001110010", "001100010", "001100000", "100101000", "100101010", "100111010", "100111000", "100110000", "100110010", "100100010", "100100000", "101101000", "101101010", "101111010", "101111000", "101110000", "101110010", "101100010", "101100000"],
                ["000001100", "000001110", "000011110", "000011100", "000010100", "000010110", "000000110", "000000100", "001001100", "001001110", "001011110", "001011100", "001010100", "001010110", "001000110", "001000100", "100001100", "100001110", "100011110", "100011100", "100010100", "100010110", "100000110", "100000100", "101001100", "101001110", "101011110", "101011100", "101010100", "101010110", "101000110", "101000100"],
                ["000001101", "000001111", "000011111", "000011101", "000010101", "000010111", "000000111", "000000101", "001001101", "001001111", "001011111", "001011101", "001010101", "001010111", "001000111", "001000101", "100001101", "100001111", "100011111", "100011101", "100010101", "100010111", "100000111", "100000101", "101001101", "101001111", "101011111", "101011101", "101010101", "101010111", "101000111", "101000101"],
                ["000001001", "000001011", "000011011", "000011001", "000010001", "000010011", "000000011", "000000001", "001001001", "001001011", "001011011", "001011001", "001010001", "001010011", "001000011", "001000001", "100001001", "100001011", "100011011", "100011001", "100010001", "100010011", "100000011", "100000001", "101001001", "101001011", "101011011", "101011001", "101010001", "101010011", "101000011", "101000001"],
                ["000001000", "000001010", "000011010", "000011000", "000010000", "000010010", "000000010", "000000000", "001001000", "001001010", "001011010", "001011000", "001010000", "001010010", "001000010", "001000000", "100001000", "100001010", "100011010", "100011000", "100010000", "100010010", "100000010", "100000000", "101001000", "101001010", "101011010", "101011000", "101010000", "101010010", "101000010", "101000000"]

            ]

            line_configurations = [

                "-",
                "--",
                ":",
                "-."

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#32CD32",  # LimeGreen
                "#DC143C",  # Crimson
                "#FFD700",  # Gold
                "#9400D3",  # DarkViolet
                "#FF8C00",  # DarkOrange
                "#00CED1",  # DarkTurquoise
                "#FF1493",  # DeepPink
                "#00008B",  # DarkBlue
                "#90EE90",  # LightGreen
                "#FF0000",  # Red
                "#FFFFE0",  # LightYellow
                "#000000",  # Black
                "#FF7F50",  # Coral
                "#20B2AA",  # LightSeaGreen
                "#C71585"   # MediumVioletRed

            ] # 16

        elif num_of_args == 8:

            FRONT_veich_structure = np.zeros((16, 16), dtype=int)
            BACK_veich_structure = [

                ["10101100", "10101110", "10111110", "10111100", "10110100", "10110110", "10100110", "10100100", "11101100", "11101110", "11111110", "11111100", "11110100", "11110110", "11100110", "11100100"],
                ["10101101", "10101111", "10111111", "10111101", "10110101", "10110111", "10100111", "10100101", "11101101", "11101111", "11111111", "11111101", "11110101", "11110111", "11100111", "11100101"],
                ["10101001", "10101011", "10111011", "10111001", "10110001", "10110011", "10100011", "10100001", "11101001", "11101011", "11111011", "11111001", "11110001", "11110011", "11100011", "11100001"],
                ["10101000", "10101010", "10111010", "10111000", "10110000", "10110010", "10100010", "10100000", "11101000", "11101010", "11111010", "11111000", "11110000", "11110010", "11100010", "11100000"],
                ["10001100", "10001110", "10011110", "10011100", "10010100", "10010110", "10000110", "10000100", "11001100", "11001110", "11011110", "11011100", "11010100", "11010110", "11000110", "11000100"],
                ["10001101", "10001111", "10011111", "10011101", "10010101", "10010111", "10000111", "10000101", "11001101", "11001111", "11011111", "11011101", "11010101", "11010111", "11000111", "11000101"],
                ["10001001", "10001011", "10011011", "10011001", "10010001", "10010011", "10000011", "10000001", "11001001", "11001011", "11011011", "11011001", "11010001", "11010011", "11000011", "11000001"],
                ["10001000", "10001010", "10011010", "10011000", "10010000", "10010010", "10000010", "10000000", "11001000", "11001010", "11011010", "11011000", "11010000", "11010010", "11000010", "11000000"],
                ["00101100", "00101110", "00111110", "00111100", "00110100", "00110110", "00100110", "00100100", "01101100", "01101110", "01111110", "01111100", "01110100", "01110110", "01100110", "01100100"],
                ["00101101", "00101111", "00111111", "00111101", "00110101", "00110111", "00100111", "00100101", "01101101", "01101111", "01111111", "01111101", "01110101", "01110111", "01100111", "01100101"],
                ["00101001", "00101011", "00111011", "00111001", "00110001", "00110011", "00100011", "00100001", "01101001", "01101011", "01111011", "01111001", "01110001", "01110011", "01100011", "01100001"],
                ["00101000", "00101010", "00111010", "00111000", "00110000", "00110010", "00100010", "00100000", "01101000", "01101010", "01111010", "01111000", "01110000", "01110010", "01100010", "01100000"],
                ["00001100", "00001110", "00011110", "00011100", "00010100", "00010110", "00000110", "00000100", "01001100", "01001110", "01011110", "01011100", "01010100", "01010110", "01000110", "01000100"],
                ["00001101", "00001111", "00011111", "00011101", "00010101", "00010111", "00000111", "00000101", "01001101", "01001111", "01011111", "01011101", "01010101", "01010111", "01000111", "01000101"],
                ["00001001", "00001011", "00011011", "00011001", "00010001", "00010011", "00000011", "00000001", "01001001", "01001011", "01011011", "01011001", "01010001", "01010011", "01000011", "01000001"],
                ["00001000", "00001010", "00011010", "00011000", "00010000", "00010010", "00000010", "00000000", "01001000", "01001010", "01011010", "01011000", "01010000", "01010010", "01000010", "01000000"]

            ]

            line_configurations = [

                "-",
                "--",
                ":",
                "-."

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#32CD32",  # LimeGreen
                "#DC143C",  # Crimson
                "#FFD700",  # Gold
                "#9400D3",  # DarkViolet
                "#FF8C00",  # DarkOrange
                "#00CED1",  # DarkTurquoise
                "#FF1493",  # DeepPink
                "#00008B",  # DarkBlue
                "#90EE90",  # LightGreen
                "#FF0000",  # Red
                "#FFFFE0",  # LightYellow
                "#000000",  # Black
                "#FF7F50",  # Coral
                "#20B2AA",  # LightSeaGreen
                "#C71585"   # MediumVioletRed

            ] # 16

        elif num_of_args == 7:

            FRONT_veich_structure = np.zeros((8, 16), dtype=int)
            BACK_veich_structure = [

                ["0101100", "0101110", "0111110", "0111100", "0110100", "0110110", "0100110", "0100100", "1101100", "1101110", "1111110", "1111100", "1110100", "1110110", "1100110", "1100100"],
                ["0101101", "0101111", "0111111", "0111101", "0110101", "0110111", "0100111", "0100101", "1101101", "1101111", "1111111", "1111101", "1110101", "1110111", "1100111", "1100101"],
                ["0101001", "0101011", "0111011", "0111001", "0110001", "0110011", "0100011", "0100001", "1101001", "1101011", "1111011", "1111001", "1110001", "1110011", "1100011", "1100001"],
                ["0101000", "0101010", "0111010", "0111000", "0110000", "0110010", "0100010", "0100000", "1101000", "1101010", "1111010", "1111000", "1110000", "1110010", "1100010", "1100000"],
                ["0001100", "0001110", "0011110", "0011100", "0010100", "0010110", "0000110", "0000100", "1001100", "1001110", "1011110", "1011100", "1010100", "1010110", "1000110", "1000100"],
                ["0001101", "0001111", "0011111", "0011101", "0010101", "0010111", "0000111", "0000101", "1001101", "1001111", "1011111", "1011101", "1010101", "1010111", "1000111", "1000101"],
                ["0001001", "0001011", "0011011", "0011001", "0010001", "0010011", "0000011", "0000001", "1001001", "1001011", "1011011", "1011001", "1010001", "1010011", "1000011", "1000001"],
                ["0001000", "0001010", "0011010", "0011000", "0010000", "0010010", "0000010", "0000000", "1001000", "1001010", "1011010", "1011000", "1010000", "1010010", "1000010", "1000000"]

            ]

            line_configurations = [

                "-",
                "--",
                ":",
                "-."

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#32CD32",  # LimeGreen
                "#DC143C",  # Crimson
                "#FFD700",  # Gold
                "#9400D3",  # DarkViolet
                "#FF8C00",  # DarkOrange
                "#00CED1",  # DarkTurquoise
                "#FF1493",  # DeepPink
                "#00008B",  # DarkBlue
                "#90EE90",  # LightGreen
                "#FF0000",  # Red
                "#FFFFE0",  # LightYellow
                "#000000",  # Black
                "#FF7F50",  # Coral
                "#20B2AA",  # LightSeaGreen
                "#C71585"   # MediumVioletRed

            ] # 16

        elif num_of_args == 6:

            FRONT_veich_structure = np.zeros((8, 8), dtype=int)
            BACK_veich_structure = [

                ["101100", "101110", "111110", "111100", "110100", "110110", "100110", "100100"],
                ["101101", "101111", "111111", "111101", "110101", "110111", "100111", "100101"],
                ["101001", "101011", "111011", "111001", "110001", "110011", "100011", "100001"],
                ["101000", "101010", "111010", "111000", "110000", "110010", "100010", "100000"],
                ["001100", "001110", "011110", "011100", "010100", "010110", "000110", "000100"],
                ["001101", "001111", "011111", "011101", "010101", "010111", "000111", "000101"],
                ["001001", "001011", "011011", "011001", "010001", "010011", "000011", "000001"],
                ["001000", "001010", "011010", "011000", "010000", "010010", "000010", "000000"]

            ]

            line_configurations = [

                "-",
                "--"

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#32CD32",  # LimeGreen
                "#DC143C",  # Crimson
                "#FFD700",  # Gold
                "#9400D3",  # DarkViolet
                "#FF8C00",  # DarkOrange
                "#00CED1",  # DarkTurquoise
                "#FF1493",  # DeepPink
                "#00008B",  # DarkBlue
                "#90EE90",  # LightGreen
                "#FF0000",  # Red
                "#FFFFE0",  # LightYellow
                "#000000",  # Black
                "#FF7F50",  # Coral
                "#20B2AA",  # LightSeaGreen
                "#C71585"   # MediumVioletRed

            ] # 16

        elif num_of_args == 5:

            #

            FRONT_veich_structure = np.zeros((4, 8), dtype=int)
            BACK_veich_structure = [

                ["01100", "01110", "11110", "11100", "10100", "10110", "00110", "00100"],
                ["01101", "01111", "11111", "11101", "10101", "10111", "00111", "00101"],
                ["01001", "01011", "11011", "11001", "10001", "10011", "00011", "00001"],
                ["01000", "01010", "11010", "11000", "10000", "10010", "00010", "00000"]

            ]

            line_configurations = [

                "-"

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#32CD32",  # LimeGreen
                "#DC143C",  # Crimson
                "#FFD700",  # Gold
                "#9400D3",  # DarkViolet
                "#FF8C00",  # DarkOrange
                "#00CED1",  # DarkTurquoise
                "#FF1493",  # DeepPink
                "#00008B",  # DarkBlue
                "#90EE90",  # LightGreen
                "#FF0000",  # Red
                "#FFFFE0",  # LightYellow
                "#000000",  # Black
                "#FF7F50",  # Coral
                "#20B2AA",  # LightSeaGreen
                "#C71585"   # MediumVioletRed

            ] # 16

        elif num_of_args == 4:

            # done

            FRONT_veich_structure = np.zeros((4, 4), dtype=int)
            BACK_veich_structure = [

                ["1100", "1101", "1001", "1000"],
                ["1110", "1111", "1011", "1010"],
                ["0110", "0111", "0011", "0010"],
                ["0100", "0101", "0001", "0000"]

            ]

            line_configurations = [

                "-"

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#DC143C",  # Crimson
                "#32CD32",  # LimeGreen
                "#FFD700",  # Gold
                "#9400D3",  # DarkViolet
                "#FF8C00",  # DarkOrange
                "#00CED1",  # DarkTurquoise
                "#FF1493"   # DeepPink

            ] # 8

        elif num_of_args == 3:

            # done

            FRONT_veich_structure = np.zeros((2, 4), dtype=int)
            BACK_veich_structure = [

                ["110", "111", "101", "100"],
                ["010", "011", "001", "000"]

            ]

            line_configurations = [

                "-"

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#DC143C",  # Crimson
                "#32CD32",  # LimeGreen
                "#FFD700"   # Gold

            ] # 4

        elif num_of_args == 2:

            # done

            FRONT_veich_structure = np.zeros((2, 2), dtype=int)
            BACK_veich_structure = [

                ["11", "10"],
                ["01", "00"]

            ]

            line_configurations = [

                "-"

            ]

            colors = [

                "#4169E1",  # RoyalBlue
                "#DC143C"   # Crimson

            ] # 2

        elif num_of_args == 1:

            # done

            FRONT_veich_structure = np.zeros((2, 1), dtype=int)
            BACK_veich_structure = [

                ["1"],
                ["0"]

            ]

            line_configurations = [

                "-"

            ]

            colors = [

                "#4169E1"  # RoyalBlue

            ] # 1

        BACK_veich_structure = np.array(BACK_veich_structure, dtype=str)
        initial_MAIN_coord_groups = []

        for num in bin_sets:

            row_indices, col_indices = np.where(BACK_veich_structure == num)
            row = row_indices[0]
            col = col_indices[0]
            FRONT_veich_structure[row, col] = 1

        for minimized_term in WORK_minimized_term_term_list:

            group = []

            for idx, val in np.ndenumerate(BACK_veich_structure):

                val = str(val)
                if differ(minimized_term, val): group.append((idx[0], idx[1]))

            initial_MAIN_coord_groups.append(group)

        # initial_coord_groups --- це список, який має в собі групи, а в кожній групі є координати, які входять до мінімізаційного терму

        rows, cols = FRONT_veich_structure.shape

        print(f"initial_MAIN_coord_groups:\n{initial_MAIN_coord_groups}")

        updated_MAIN_coord_groups = []
        updated_EXTENDED_coord_groups = []

        NEW_FRONT_veich_structure = np.zeros((rows+2, cols+2), dtype=int)
        NEW_BACK_veich_structure = np.empty((rows+2, cols+2), dtype=object)

        """Для ФРОНТОВОЇ таблиці Вейча"""

        # Сторони
        top_side = FRONT_veich_structure[0, :]          # Верхня сторона
        bottom_side = FRONT_veich_structure[-1, :]      # Нижня сторона
        left_side = FRONT_veich_structure[:, 0]         # Ліва сторона
        right_side = FRONT_veich_structure[:, -1]       # Права сторона

        # Кути (як 1x1 матриці для узгодженості)
        top_left_corner = np.array([[FRONT_veich_structure[0, 0]]])      # Верхній лівий
        top_right_corner = np.array([[FRONT_veich_structure[0, -1]]])    # Верхній правий
        bottom_left_corner = np.array([[FRONT_veich_structure[-1, 0]]])  # Нижній лівий
        bottom_right_corner = np.array([[FRONT_veich_structure[-1, -1]]]) # Нижній правий

        # Заповнюємо верхній рядок
        NEW_FRONT_veich_structure[0, 0] = bottom_right_corner[0, 0]
        NEW_FRONT_veich_structure[0, 1:cols+1] = bottom_side
        NEW_FRONT_veich_structure[0, cols+1] = bottom_left_corner[0, 0]

        # Заповнюємо середні рядки (1–4)
        NEW_FRONT_veich_structure[1:rows+1, 1:cols+1] = FRONT_veich_structure  # Центральна частина
        NEW_FRONT_veich_structure[1:rows+1, 0] = right_side  # Ліва сторона
        NEW_FRONT_veich_structure[1:rows+1, cols+1] = left_side  # Права сторона

        # Заповнюємо нижній рядок
        NEW_FRONT_veich_structure[rows+1, 0] = top_right_corner[0, 0]
        NEW_FRONT_veich_structure[rows+1, 1:cols+1] = top_side
        NEW_FRONT_veich_structure[rows+1, cols+1] = top_left_corner[0, 0]

        """Для ЗАДНЬОЇ таблиці Вейча"""

        # Сторони
        top_side = BACK_veich_structure[0, :]          # Верхня сторона
        bottom_side = BACK_veich_structure[-1, :]      # Нижня сторона
        left_side = BACK_veich_structure[:, 0]         # Ліва сторона
        right_side = BACK_veich_structure[:, -1]       # Права сторона

        # Кути (як 1x1 матриці для узгодженості)
        top_left_corner = np.array([[BACK_veich_structure[0, 0]]], dtype=object)      # Верхній лівий
        top_right_corner = np.array([[BACK_veich_structure[0, -1]]], dtype=object)    # Верхній правий
        bottom_left_corner = np.array([[BACK_veich_structure[-1, 0]]], dtype=object)  # Нижній лівий
        bottom_right_corner = np.array([[BACK_veich_structure[-1, -1]]], dtype=object) # Нижній правий

        # Заповнюємо верхній рядок
        NEW_BACK_veich_structure[0, 0] = bottom_right_corner[0, 0]
        NEW_BACK_veich_structure[0, 1:cols+1] = bottom_side
        NEW_BACK_veich_structure[0, cols+1] = bottom_left_corner[0, 0]

        # Заповнюємо середні рядки (1–4)
        NEW_BACK_veich_structure[1:rows+1, 1:cols+1] = BACK_veich_structure  # Центральна частина
        NEW_BACK_veich_structure[1:rows+1, 0] = right_side  # Ліва сторона
        NEW_BACK_veich_structure[1:rows+1, cols+1] = left_side  # Права сторона

        # Заповнюємо нижній рядок
        NEW_BACK_veich_structure[rows+1, 0] = top_right_corner[0, 0]
        NEW_BACK_veich_structure[rows+1, 1:cols+1] = top_side
        NEW_BACK_veich_structure[rows+1, cols+1] = top_left_corner[0, 0]

        for group in initial_MAIN_coord_groups:

            updated_MAIN_coord_groups.append([])
            updated_EXTENDED_coord_groups.append([])

            for coord in group:

                updated_MAIN_coord_groups[-1].append((coord[0]+1, coord[1]+1))

                for new_coord in generate_add_coordinates(coord, rows, cols):

                    if new_coord not in del_one(FRONT_veich_structure, NEW_FRONT_veich_structure.shape):

                        updated_EXTENDED_coord_groups[-1].append(new_coord)

        print(f"FRONT_veich_structure:\n{FRONT_veich_structure}")
        print(f"NEW_FRONT_veich_structure:\n{NEW_FRONT_veich_structure}")

        print("\n")

        print(f"updated_EXTENDED_coord_groups:\n{updated_EXTENDED_coord_groups}")
        print(f"updated_MAIN_coord_groups:\n{updated_MAIN_coord_groups}")

        num_count_of_groups = 0

        for group in updated_MAIN_coord_groups:

            result[num_count_of_groups+1] = []
            temp = []
            added_temp = []

            for main_coord in group:

                neighbors = find_all_neighbors(updated_MAIN_coord_groups[num_count_of_groups] + updated_EXTENDED_coord_groups[num_count_of_groups], main_coord)
                if neighbors in temp: continue

                temp.append(neighbors)

            print(f"for group: {group} its temp is {temp}")

            for mini_group in temp:

                added_temp.append(find_min_max(mini_group))

            result[num_count_of_groups+1].append(added_temp)

            group_front_config = get_front_group_config(num_count_of_groups)
            result[num_count_of_groups+1].extend(group_front_config)

            num_count_of_groups += 1

        print(result)
        group_config = (NEW_FRONT_veich_structure, result, num_of_args, list_args)

    except Exception: return False
    return paint(filename, group_config)

def create_veich_schemme_pdf(temp_dir, veich_schemme_list):

    print(f"temp_dir: {temp_dir}, veich_schemme_list: {veich_schemme_list}")

    try:

        count = 1
        for veich_config in veich_schemme_list:

            filename = os.path.join(temp_dir, f"plot{count}.pdf")
            if veich_create(filename, *veich_config) == False: return False

            count += 1

    except Exception as e:

        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":

    create_veich_schemme_pdf(".", [(1, ['X0X0'], [0, 2, 8, 10], [])])