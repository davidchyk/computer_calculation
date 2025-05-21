import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

# === ПАРАМЕТРИ ===
CELL_SIZE = 0.2  # Розмір клітинки
LINE_WIDTH = 1.2  # Товщина обведення
PADDING = 0.03  # Відступ усередині, щоб рамки не накладались

def draw_axis_brackets(ax, list_args):

    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

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

def draw_kmap_with_tight_rounded_boxes(kmap, groups, list_args, filename="rounded_groups_fixed.png"):

    """
    Малює карту Вейча та додає обведення груп із заокругленими прямокутниками.
    Тепер обведення не заходить на сусідні клітинки!
    """

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
                str(kmap[r, c]),
                ha='center',
                va='center',
                fontsize=15
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

    draw_axis_brackets(ax, list_args)

    plt.show()

    #TODO

    # **Збереження у файл**
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    print(f"Зображення збережено у файл: {filename}")

def paint(data: tuple):

    kmap, forming_groups, num_of_args, list_args = data

    print("input kmap:")
    print(kmap)

    if not list_args:

        for x in range(num_of_args, 0, -1): list_args.append(f"x_{x}")

    print(list_args)

    draw_kmap_with_tight_rounded_boxes(kmap, forming_groups, list_args)