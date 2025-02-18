import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

forming_groups = [
    [(1, 0), (1, 1)],
    [(1, 1), (1, 2)]
]

def draw_kmap_with_offsets(kmap, groups, cell_size=0.2, gap=0):
    rows, cols = kmap.shape
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    fig.set_size_inches(6, 2.5)  # Фіксований розмір прикладу

    # 1) Спочатку малюємо всю сітку й текст у клітинках
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  # 0-й рядок зверху
            # Рамка клітинки
            rect = Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor='black',
                linewidth=1
            )
            ax.add_patch(rect)
            # Текст (число в клітинці)
            val = str(kmap[r, c])
            ax.text(
                x + (cell_size - gap)/2,
                y + (cell_size - gap)/2,
                val,
                ha='center', va='center', fontsize=12
            )

    # 2) Зібрати дані про належність клітинок до груп:
    #    key = (r, c), value = список індексів груп, до яких належить клітинка
    cell_to_groups = {}
    for group_idx, group_coords in enumerate(groups):
        for (r, c) in group_coords:
            cell_to_groups.setdefault((r, c), []).append(group_idx)

    # 3) Для кожної клітинки, яка входить у групи, малюємо по прямокутнику з відступом
    offset_step = 0.08  # Наскільки відступати кожен наступний прямокутник
    for (r, c), group_list in cell_to_groups.items():
        # Сортуємо групи, щоб послідовно малювати
        # (можна не сортувати, це просто для визначеної послідовності)
        group_list = sorted(group_list)
        for i, g_idx in enumerate(group_list):
            color = plt.cm.tab10(g_idx % 10)
            # Кожен наступний прямокутник зміщуємо всередину на offset_step*i
            off = offset_step * i
            # Координати так само, як і для сітки:
            x = c * cell_size + off/2
            y = (rows - 1 - r) * cell_size + off/2
            # Але ширину/висоту зменшуємо, щоб "поле" залишалось
            width = (cell_size - gap) - off
            height = (cell_size - gap) - off

            rect = Rectangle(
                (x, y), width, height,
                fill=False,
                edgecolor=color,
                linewidth=2
            )
            ax.add_patch(rect)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Обведення клітинок з урахуванням кількох груп")
    plt.show()


# Запускаємо приклад
draw_kmap_with_offsets(veich_structure, forming_groups)
