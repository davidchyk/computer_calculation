import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

def process(data1, data2):

    veich_structure = data1
    forming_groups = data2

    # === ПАРАМЕТРИ ===
    CELL_SIZE = 0.2  # Розмір клітинки
    GAP = 0  # Відсутність проміжку між клітинками
    LINE_WIDTH = 1.2  # Товщина обведення
    PADDING = 0.03  # Відступ усередині, щоб рамки не накладались

    def draw_kmap_with_tight_rounded_boxes(kmap, groups, cell_size=CELL_SIZE, gap=GAP, filename="rounded_groups_fixed.png"):
        """
        Малює карту Карно та додає обведення груп із заокругленими прямокутниками.
        Тепер обведення не заходить на сусідні клітинки!
        """
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
                    fontsize=8
                )

        # 2) Обведення групи без виходу за межі
        color_map = ["#640000", "#4A7023"]  # Червоне, Зелене

        for group_idx, group_cells in enumerate(groups):

            color = color_map[group_idx % len(color_map)]

            # Визначаємо точні межі групи
            min_r = min(c[0] for c in group_cells)
            max_r = max(c[0] for c in group_cells)
            min_c = min(c[1] for c in group_cells)
            max_c = max(c[1] for c in group_cells)

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
                facecolor='none'
            )
            ax.add_patch(rounded_box)

        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

        # **Збереження у файл**
        plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        print(f"Зображення збережено у файл: {filename}")

    draw_kmap_with_tight_rounded_boxes(veich_structure, forming_groups)