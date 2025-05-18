import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

# === ПАРАМЕТРИ ===
CELL_SIZE = 0.2  # Розмір клітинки
GAP = 0  # Відсутність проміжку між клітинками
LINE_WIDTH = 1.2  # Товщина обведення
PADDING = 0.03  # Відступ усередині, щоб рамки не накладались

def draw_axis_brackets(ax, cell_size, rows, cols, list_args):
    """
    Малює 4 лінії (дужки) навколо таблиці та текстові позначки.
    Координати жорстко задані на основі меж таблиці.
    """

    if len(list_args) == 4:

        plt.rcParams['text.usetex'] = True
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

        # Верхня дужка (X3)
        ax.plot([0.2, 0.6], [1.03, 1.03], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 1.09, r"$x_3$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [1, 0.6], color='black', linewidth=3, zorder=100)
        ax.text(0.11, 0.8, r"$x_4$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)
        ax.plot([1.03, 1.03], [0.8, 0.4], color='black', linewidth=3, zorder=100)
        ax.text(1.10, 0.6, r"$x_2$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4, 0.8], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12, r"$x_1$", ha='center', va='center', fontsize=40, zorder=101)





def draw_kmap_with_tight_rounded_boxes(kmap, groups, list_args, filename="rounded_groups_fixed.png"):

    """
    Малює карту Карно та додає обведення груп із заокругленими прямокутниками.
    Тепер обведення не заходить на сусідні клітинки!
    """

    cell_size=CELL_SIZE
    gap = GAP

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
    #plt.show()

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

    if len(list_args) == 4:

        draw_axis_brackets(ax, cell_size, rows, cols, list_args)

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

        for x in range(num_of_args): list_args.append(f"x_{x}")

    draw_kmap_with_tight_rounded_boxes(kmap, forming_groups, list_args)