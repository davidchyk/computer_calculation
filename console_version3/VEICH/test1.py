import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

# === ДАНІ ===
veich_structure = np.array([
    [1, 0, 0, 1],
    [1, 0, 0, 1]
])

colors = []

forming_groups = [
    [(0, 0), (0, 3), (1, 0), (1, 3)]  # Група має переходити через край
]

# === ПАРАМЕТРИ ===
CELL_SIZE = 0.2  # Розмір клітинки
GAP = 0  # Відсутність проміжку між клітинками
LINE_WIDTH = 1.5  # Товщина обведення
PADDING = 0.02  # Відступ усередину рамки
BOLD_LINE_WIDTH = 3  # Товщина жирних ліній
BOLD_LINE_LENGTH = 0.5  # Довжина жирних ліній (як частка ширини таблиці)
VERTICAL_LINE_LENGTH = 0.7  # Довжина вертикальної лінії (як частка висоти таблиці)

def draw_kmap_with_shorter_borders(kmap, groups, cell_size=CELL_SIZE, gap=GAP, filename="kmap_with_fixed_lines.png"):
    """
    Малює карту Карно та додає:
    1) Округлені обведення груп
    2) Скорочені жирні горизонтальні та вертикальні лінії
    3) Позначення змінних X₁, X₂, X₃
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
            y = (rows - 1 - r) * cell_size
            
            ax.add_patch(Rectangle(
                (x, y),
                cell_size,
                cell_size,
                fill=False,
                edgecolor='black',
                linewidth=0.8
            ))

            ax.text(
                x + cell_size / 2,
                y + cell_size / 2,
                str(kmap[r, c]),
                ha='center',
                va='center',
                fontsize=8
            )

    # 2) Додаємо коротші жирні лінії
    total_width = cols * cell_size
    total_height = rows * cell_size

    line_half_length = total_width * BOLD_LINE_LENGTH / 2  # Половина довжини горизонтальної лінії
    vertical_half_length = total_height * VERTICAL_LINE_LENGTH / 2  # Половина довжини вертикальної лінії

    # Горизонтальна лінія зверху
    ax.plot(
        [total_width / 2 - line_half_length, total_width / 2 + line_half_length],
        [total_height + 0.05, total_height + 0.05],
        'k', linewidth=BOLD_LINE_WIDTH
    )

    # Горизонтальна лінія знизу
    ax.plot(
        [total_width / 2 - line_half_length, total_width / 2 + line_half_length],
        [-0.05, -0.05],
        'k', linewidth=BOLD_LINE_WIDTH
    )

    # Вертикальна лінія зліва
    ax.plot(
        [-0.1, -0.1],
        [total_height / 2 - vertical_half_length, total_height / 2 + vertical_half_length],
        'k', linewidth=BOLD_LINE_WIDTH
    )

    # 3) Додаємо змінні X₁, X₂, X₃ біля коротших ліній
    ax.text(total_width / 2, total_height + 0.1, r'$X_2$', fontsize=12, ha='center', va='bottom')  # Верхня змінна
    ax.text(-0.15, total_height / 2, r'$X_3$', fontsize=12, ha='right', va='center', rotation=90)  # Ліва змінна
    ax.text(total_width / 2, -0.15, r'$X_1$', fontsize=12, ha='center', va='top')  # Нижня змінна

    # 4) Малюємо округлені обведення груп
    color_map = ["#640000"]  # Червоне обведення
    for group_idx, group_cells in enumerate(groups):
        color = color_map[group_idx % len(color_map)]

        left_block = [(r, c) for r, c in group_cells if c < cols // 2]
        right_block = [(r, c) for r, c in group_cells if c >= cols // 2]

        for segment in [left_block, right_block]:
            if not segment:
                continue

            min_r = min(c[0] for c in segment)
            max_r = max(c[0] for c in segment)
            min_c = min(c[1] for c in segment)
            max_c = max(c[1] for c in segment)

            x_rect = min_c * cell_size + PADDING
            y_rect = (rows - 1 - max_r) * cell_size + PADDING
            width = (max_c - min_c + 1) * cell_size - 2 * PADDING
            height = (max_r - min_r + 1) * cell_size - 2 * PADDING

            rounded_box = FancyBboxPatch(
                (x_rect, y_rect),
                width, height,
                boxstyle=f"round,pad={PADDING}",
                edgecolor=color,
                linewidth=LINE_WIDTH,
                facecolor='none'
            )
            ax.add_patch(rounded_box)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Карта Карно з короткими жирними лініями")

    plt.show()

    # **Збереження у файл**
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close(fig)
    print(f"Зображення збережено у файл: {filename}")

# Виклик функції
draw_kmap_with_shorter_borders(veich_structure, forming_groups)
