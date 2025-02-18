import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Приклад даних
veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

# forming_groups: кожен елемент — це список координат (row, col)
# що належать до певної групи.
forming_groups = [
    [(1, 0), (1, 1)],    # перша група
    [(1, 1), (1, 2)]     # друга група
]

def draw_kmap_hatching(kmap, groups, cell_size=0.2, gap=0):
    rows, cols = kmap.shape
    
    # Палітра візерунків (hatches). Якщо груп більше, можна додати ще.
    # Наприклад, `"/"`, `"\"`, `"|"`, `"-"`, `"+"`, `"x"`, `"o"`, `"."`, `"*"`
    hatch_styles = ["/", "\\", "x", "+", "."]

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    fig.set_size_inches(6, 2.5)
    
    # ---------------------------------------
    # 1) Спочатку промалюємо "рамки" клітинок і текст
    # ---------------------------------------
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  # 0-й рядок угорі

            # Звичайний прямокутник без заливки: щоб бачили сітку
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor="black",
                linewidth=1
            ))

            # Виводимо значення (0 чи 1) у центр клітинки
            val = str(kmap[r, c])
            ax.text(
                x + (cell_size - gap)/2,
                y + (cell_size - gap)/2,
                val,
                ha='center',
                va='center',
                fontsize=12
            )
    
    # ---------------------------------------
    # 2) За допомогою штрихування вказуємо групи
    # ---------------------------------------
    # Ідея: для кожної групи вибираємо hatch_style, потім "заливаємо" клітинки
    #       прямокутниками з hatch=..., але з facecolor='none' або напівпрозорим,
    #       щоб було видно базове значення клітинки.
    for group_idx, group_coords in enumerate(groups):
        # Виберемо візерунок по індексу групи. Якщо груп більше, ніж hatch_styles,
        # можна взяти hatch_styles[group_idx % len(hatch_styles)].
        hatch_pattern = hatch_styles[group_idx % len(hatch_styles)]
        
        # Кожну клітинку, що належить групі, заштриховуємо
        for (r, c) in group_coords:
            x = c * cell_size
            y = (rows - 1 - r) * cell_size
            # Прямокутник зі штрихуванням
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=True,
                facecolor='none',       # фон незафарбований (прозорий)
                hatch=hatch_pattern,    # сюди передаємо стилі: '/', '\', 'x', ...
                edgecolor='black',      # колір ліній
                linewidth=1,
                alpha=1.0               # при бажанні можна додати прозорість < 1
            ))

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Приклад заштрихованих візерунків (hatching) для позначення груп")
    plt.show()

draw_kmap_hatching(veich_structure, forming_groups)