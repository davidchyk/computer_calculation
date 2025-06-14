from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.pyplot as plt
import numpy as np
import traceback
import os

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

    [x] 1. Бувають моменти, що якщо весь стопчик буде 1, то межі груп будуть дещо дивно відображатись, тому для них особлива логіка
    [] 2. Якщо мінімізація заповнює всі клітинки: написати логіку для цього випадку
    [] 3. При кількості аргументів в 1, крива група

    В Paint:

    [] 0. Добудувати розмітку для 9 аргументів
    [] 1. Коли вже >= 5 аргументів, то потрібно трохи зміщувати рисунок, або видалити рамки, щоб все вмістилось
    [] 2. Коли виявиться, що функція була введена в режимі func, тобто можливі великі прописні аргументи: це потрібно врахувати, щоб лінії в діаграмі їх не перекривали, а звідси і зміщення трохи також змінюється
    [] 3. Можливо також потрібно буде змінювати шрифт аргументів при великій їх кількості перемикальної фукнції
    [] 4. TODO TODO Перевірити правильність розтавлення ліній (дивитись за BACK_VEICH правильний порядок)
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

                ["000001100", "000001101", "000001001", "000001000", "000011100", "000011101", "000011001", "000011000", "001001100", "001001101", "001001001", "001001000", "001011100", "001011101", "001011001", "001011000", "100001100", "100001101", "100001001", "100001000", "100011100", "100011101", "100011001", "100011000", "101001100", "101001101", "101001001", "101001000", "101011100", "101011101", "101011001", "101011000"],
                ["000001110", "000001111", "000001011", "000001010", "000011110", "000011111", "000011011", "000011010", "001001110", "001001111", "001001011", "001001010", "001011110", "001011111", "001011011", "001011010", "100001110", "100001111", "100001011", "100001010", "100011110", "100011111", "100011011", "100011010", "101001110", "101001111", "101001011", "101001010", "101011110", "101011111", "101011011", "101011010"],
                ["000000110", "000000111", "000000011", "000000010", "000010110", "000010111", "000010011", "000010010", "001000110", "001000111", "001000011", "001000010", "001010110", "001010111", "001010011", "001010010", "100000110", "100000111", "100000011", "100000010", "100010110", "100010111", "100010011", "100010010", "101000110", "101000111", "101000011", "101000010", "101010110", "101010111", "101010011", "101010010"],
                ["000000100", "000000101", "000000001", "000000000", "000010100", "000010101", "000010001", "000010000", "001000100", "001000101", "001000001", "001000000", "001010100", "001010101", "001010001", "001010000", "100000100", "100000101", "100000001", "100000000", "100010100", "100010101", "100010001", "100010000", "101000100", "101000101", "101000001", "101000000", "101010100", "101010101", "101010001", "101010000"],
                ["000101100", "000101101", "000101001", "000101000", "000111100", "000111101", "000111001", "000111000", "001101100", "001101101", "001101001", "001101000", "001111100", "001111101", "001111001", "001111000", "100101100", "100101101", "100101001", "100101000", "100111100", "100111101", "100111001", "100111000", "101101100", "101101101", "101101001", "101101000", "101111100", "101111101", "101111001", "101111000"],
                ["000101110", "000101111", "000101011", "000101010", "000111110", "000111111", "000111011", "000111010", "001101110", "001101111", "001101011", "001101010", "001111110", "001111111", "001111011", "001111010", "100101110", "100101111", "100101011", "100101010", "100111110", "100111111", "100111011", "100111010", "101101110", "101101111", "101101011", "101101010", "101111110", "101111111", "101111011", "101111010"],
                ["000100110", "000100111", "000100011", "000100010", "000110110", "000110111", "000110011", "000110010", "001100110", "001100111", "001100011", "001100010", "001110110", "001110111", "001110011", "001110010", "100100110", "100100111", "100100011", "100100010", "100110110", "100110111", "100110011", "100110010", "101100110", "101100111", "101100011", "101100010", "101110110", "101110111", "101110011", "101110010"],
                ["000100100", "000100101", "000100001", "000100000", "000110100", "000110101", "000110001", "000110000", "001100100", "001100101", "001100001", "001100000", "001110100", "001110101", "001110001", "001110000", "100100100", "100100101", "100100001", "100100000", "100110100", "100110101", "100110001", "100110000", "101100100", "101100101", "101100001", "101100000", "101110100", "101110101", "101110001", "101110000"],
                ["010001100", "010001101", "010001001", "010001000", "010011100", "010011101", "010011001", "010011000", "011001100", "011001101", "011001001", "011001000", "011011100", "011011101", "011011001", "011011000", "110001100", "110001101", "110001001", "110001000", "110011100", "110011101", "110011001", "110011000", "111001100", "111001101", "111001001", "111001000", "111011100", "111011101", "111011001", "111011000"],
                ["010001110", "010001111", "010001011", "010001010", "010011110", "010011111", "010011011", "010011010", "011001110", "011001111", "011001011", "011001010", "011011110", "011011111", "011011011", "011011010", "110001110", "110001111", "110001011", "110001010", "110011110", "110011111", "110011011", "110011010", "111001110", "111001111", "111001011", "111001010", "111011110", "111011111", "111011011", "111011010"],
                ["010000110", "010000111", "010000011", "010000010", "010010110", "010010111", "010010011", "010010010", "011000110", "011000111", "011000011", "011000010", "011010110", "011010111", "011010011", "011010010", "110000110", "110000111", "110000011", "110000010", "110010110", "110010111", "110010011", "110010010", "111000110", "111000111", "111000011", "111000010", "111010110", "111010111", "111010011", "111010010"],
                ["010000100", "010000101", "010000001", "010000000", "010010100", "010010101", "010010001", "010010000", "011000100", "011000101", "011000001", "011000000", "011010100", "011010101", "011010001", "011010000", "110000100", "110000101", "110000001", "110000000", "110010100", "110010101", "110010001", "110010000", "111000100", "111000101", "111000001", "111000000", "111010100", "111010101", "111010001", "111010000"],
                ["010101100", "010101101", "010101001", "010101000", "010111100", "010111101", "010111001", "010111000", "011101100", "011101101", "011101001", "011101000", "011111100", "011111101", "011111001", "011111000", "110101100", "110101101", "110101001", "110101000", "110111100", "110111101", "110111001", "110111000", "111101100", "111101101", "111101001", "111101000", "111111100", "111111101", "111111001", "111111000"],
                ["010101110", "010101111", "010101011", "010101010", "010111110", "010111111", "010111011", "010111010", "011101110", "011101111", "011101011", "011101010", "011111110", "011111111", "011111011", "011111010", "110101110", "110101111", "110101011", "110101010", "110111110", "110111111", "110111011", "110111010", "111101110", "111101111", "111101011", "111101010", "111111110", "111111111", "111111011", "111111010"],
                ["010100110", "010100111", "010100011", "010100010", "010110110", "010110111", "010110011", "010110010", "011100110", "011100111", "011100011", "011100010", "011110110", "011110111", "011110011", "011110010", "110100110", "110100111", "110100011", "110100010", "110110110", "110110111", "110110011", "110110010", "111100110", "111100111", "111100011", "111100010", "111110110", "111110111", "111110011", "111110010"],
                ["010100100", "010100101", "010100001", "010100000", "010110100", "010110101", "010110001", "010110000", "011100100", "011100101", "011100001", "011100000", "011110100", "011110101", "011110001", "011110000", "110100100", "110100101", "110100001", "110100000", "110110100", "110110101", "110110001", "110110000", "111100100", "111100101", "111100001", "111100000", "111110100", "111110101", "111110001", "111110000"]

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

                ["00001100", "00001101", "00001001", "00001000", "00011100", "00011101", "00011001", "00011000", "01001100", "01001101", "01001001", "01001000", "01011100", "01011101", "01011001", "01011000"],
                ["00001110", "00001111", "00001011", "00001010", "00011110", "00011111", "00011011", "00011010", "01001110", "01001111", "01001011", "01001010", "01011110", "01011111", "01011011", "01011010"],
                ["00000110", "00000111", "00000011", "00000010", "00010110", "00010111", "00010011", "00010010", "01000110", "01000111", "01000011", "01000010", "01010110", "01010111", "01010011", "01010010"],
                ["00000100", "00000101", "00000001", "00000000", "00010100", "00010101", "00010001", "00010000", "01000100", "01000101", "01000001", "01000000", "01010100", "01010101", "01010001", "01010000"],
                ["00101100", "00101101", "00101001", "00101000", "00111100", "00111101", "00111001", "00111000", "01101100", "01101101", "01101001", "01101000", "01111100", "01111101", "01111001", "01111000"],
                ["00101110", "00101111", "00101011", "00101010", "00111110", "00111111", "00111011", "00111010", "01101110", "01101111", "01101011", "01101010", "01111110", "01111111", "01111011", "01111010"],
                ["00100110", "00100111", "00100011", "00100010", "00110110", "00110111", "00110011", "00110010", "01100110", "01100111", "01100011", "01100010", "01110110", "01110111", "01110011", "01110010"],
                ["00100100", "00100101", "00100001", "00100000", "00110100", "00110101", "00110001", "00110000", "01100100", "01100101", "01100001", "01100000", "01110100", "01110101", "01110001", "01110000"],
                ["10001100", "10001101", "10001001", "10001000", "10011100", "10011101", "10011001", "10011000", "11001100", "11001101", "11001001", "11001000", "11011100", "11011101", "11011001", "11011000"],
                ["10001110", "10001111", "10001011", "10001010", "10011110", "10011111", "10011011", "10011010", "11001110", "11001111", "11001011", "11001010", "11011110", "11011111", "11011011", "11011010"],
                ["10000110", "10000111", "10000011", "10000010", "10010110", "10010111", "10010011", "10010010", "11000110", "11000111", "11000011", "11000010", "11010110", "11010111", "11010011", "11010010"],
                ["10000100", "10000101", "10000001", "10000000", "10010100", "10010101", "10010001", "10010000", "11000100", "11000101", "11000001", "11000000", "11010100", "11010101", "11010001", "11010000"],
                ["10101100", "10101101", "10101001", "10101000", "10111100", "10111101", "10111001", "10111000", "11101100", "11101101", "11101001", "11101000", "11111100", "11111101", "11111001", "11111000"],
                ["10101110", "10101111", "10101011", "10101010", "10111110", "10111111", "10111011", "10111010", "11101110", "11101111", "11101011", "11101010", "11111110", "11111111", "11111011", "11111010"],
                ["10100110", "10100111", "10100011", "10100010", "10110110", "10110111", "10110011", "10110010", "11100110", "11100111", "11100011", "11100010", "11110110", "11110111", "11110011", "11110010"],
                ["10100100", "10100101", "10100001", "10100000", "10110100", "10110101", "10110001", "10110000", "11100100", "11100101", "11100001", "11100000", "11110100", "11110101", "11110001", "11110000"]

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

                ["0001100", "0001101", "0001001", "0001000", "0011100", "0011101", "0011001", "0011000", "1001100", "1001101", "1001001", "1001000", "1011100", "1011101", "1011001", "1011000"],
                ["0001110", "0001111", "0001011", "0001010", "0011110", "0011111", "0011011", "0011010", "1001110", "1001111", "1001011", "1001010", "1011110", "1011111", "1011011", "1011010"],
                ["0000110", "0000111", "0000011", "0000010", "0010110", "0010111", "0010011", "0010010", "1000110", "1000111", "1000011", "1000010", "1010110", "1010111", "1010011", "1010010"],
                ["0000100", "0000101", "0000001", "0000000", "0010100", "0010101", "0010001", "0010000", "1000100", "1000101", "1000001", "1000000", "1010100", "1010101", "1010001", "1010000"],
                ["0101100", "0101101", "0101001", "0101000", "0111100", "0111101", "0111001", "0111000", "1101100", "1101101", "1101001", "1101000", "1111100", "1111101", "1111001", "1111000"],
                ["0101110", "0101111", "0101011", "0101010", "0111110", "0111111", "0111011", "0111010", "1101110", "1101111", "1101011", "1101010", "1111110", "1111111", "1111011", "1111010"],
                ["0100110", "0100111", "0100011", "0100010", "0110110", "0110111", "0110011", "0110010", "1100110", "1100111", "1100011", "1100010", "1110110", "1110111", "1110011", "1110010"],
                ["0100100", "0100101", "0100001", "0100000", "0110100", "0110101", "0110001", "0110000", "1100100", "1100101", "1100001", "1100000", "1110100", "1110101", "1110001", "1110000"]

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

                ["001100", "001101", "001001", "001000", "011100", "011101", "011001", "011000"],
                ["001110", "001111", "001011", "001010", "011110", "011111", "011011", "011010"],
                ["000110", "000111", "000011", "000010", "010110", "010111", "010011", "010010"],
                ["000100", "000101", "000001", "000000", "010100", "010101", "010001", "010000"],
                ["101100", "101101", "101001", "101000", "111100", "111101", "111001", "111000"],
                ["101110", "101111", "101011", "101010", "111110", "111111", "111011", "111010"],
                ["100110", "100111", "100011", "100010", "110110", "110111", "110011", "110010"],
                ["100100", "100101", "100001", "100000", "110100", "110101", "110001", "110000"]

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

            FRONT_veich_structure = np.zeros((4, 8), dtype=int)
            BACK_veich_structure = [

                ["01100", "01101", "01001", "01000", "11100", "11101", "11001", "11000"],
                ["01110", "01111", "01011", "01010", "11110", "11111", "11011", "11010"],
                ["00110", "00111", "00011", "00010", "10110", "10111", "10011", "10010"],
                ["00100", "00101", "00001", "00000", "10100", "10101", "10001", "10000"]

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