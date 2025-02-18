import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

# forming_groups: кожен елемент — список координат (r, c),
#                що належать до однієї групи.
forming_groups = [
    [(1, 0), (1, 1)],
    [(1, 1), (1, 2)]
]

def draw_kmap_colored(kmap, groups, cell_size=0.2, gap=0):
    rows, cols = kmap.shape

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    fig.set_size_inches(6, 2.5)

    # --- 1) Малюємо «рамочки» клітинок та числа ---
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  # 0-й рядок угорі

            # Клітинка (прямокутник без заливки)
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor='black',
                linewidth=1
            ))
            
            # Текст (значення з kmap[r,c])
            val = str(kmap[r, c])
            ax.text(
                x + (cell_size - gap) / 2,
                y + (cell_size - gap) / 2,
                val,
                ha='center',
                va='center',
                fontsize=12
            )

    # --- 2) Зафарбовуємо клітинки згідно з групами ---
    #    Якщо клітинка належить двом групам, кольори просто «накладуться».
    #    Колір для кожної групи візьмемо з plt.cm.tab10()
    for group_idx, group_coords in enumerate(groups):
        color = plt.cm.tab10(group_idx % 10)   # колір із палітри
        for (r, c) in group_coords:
            x = c * cell_size
            y = (rows - 1 - r) * cell_size

            # Прямокутник із заливкою (напівпрозорою)
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=True,
                facecolor=color, 
                edgecolor=None,
                alpha=0.4  # Прозорість (0…1)
            ))

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Напівпрозоре зафарбовування клітинок, де групи перетинаються")
    plt.show()


# Запуск:
draw_kmap_colored(veich_structure, forming_groups)
