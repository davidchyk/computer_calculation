import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

forming_groups = [
    [(1, 0), (1, 1)],  # Група 0 (червоне обведення)
    [(1, 1), (1, 2)]   # Група 1 (зелене обведення)
]

def draw_kmap_with_rounded_boxes(kmap, groups, cell_size=0.2, gap=0, filename="rounded_groups.png"):
    """
    Малює карту Карно та додає обведення груп із заокругленими прямокутниками.
    """
    rows, cols = kmap.shape
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    fig.set_size_inches(6, 2.5)

    # 1) Малюємо таблицю (сітку)
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  # 0-й рядок угорі
            
            # Прямокутник сітки
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor='black',
                linewidth=1
            ))

            # Текст (значення у клітинці)
            val = str(kmap[r, c])
            ax.text(
                x + (cell_size - gap) / 2,
                y + (cell_size - gap) / 2,
                val,
                ha='center',
                va='center',
                fontsize=12
            )
    
    # 2) Обведення групи єдиним "округленим" прямокутником
    color_map = ["#640000", "#4A7023"]  # Червоне, Зелене (можна додати більше)

    for group_idx, group_cells in enumerate(groups):
        color = color_map[group_idx % len(color_map)]

        # Визначимо межі (мін/макс координати групи)
        min_r = min(c[0] for c in group_cells)
        max_r = max(c[0] for c in group_cells)
        min_c = min(c[1] for c in group_cells)
        max_c = max(c[1] for c in group_cells)

        # Обчислюємо позицію та розмір прямокутника
        x_rect = min_c * cell_size
        y_rect = (rows - 1 - max_r) * cell_size  # верхня межа
        width = (max_c - min_c + 1) * cell_size - gap
        height = (max_r - min_r + 1) * cell_size - gap

        # Додаємо заокруглений прямокутник (обведення групи)
        rounded_box = FancyBboxPatch(
            (x_rect, y_rect),
            width, height,
            boxstyle="round,pad=0.1",
            edgecolor=color,
            linewidth=3,
            facecolor='none'
        )
        ax.add_patch(rounded_box)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Заокруглені обведення груп клітинок")

    plt.show()

    # Збереження у файл
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print(f"Зображення збережено у файл: {filename}")

# Виклик функції
draw_kmap_with_rounded_boxes(veich_structure, forming_groups)