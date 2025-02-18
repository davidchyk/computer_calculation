import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

# forming_groups: кожен елемент — список координат (row, col),
#                які належать до конкретної групи.
forming_groups = [
    [(1, 0), (1, 1)],   # Група 0
    [(1, 1), (1, 2)]   # Група 1

]


def draw_kmap_with_markers_topright(kmap, groups, cell_size=1, gap=0.05):
    """
    Відображає 2D-масив kmap у вигляді таблиці. У кожній клітинці, 
    якщо вона належить декільком групам, у правому верхньому кутку 
    малюється декілька фігур (міні-значків), які йдуть рядочком зправа наліво.
    """
    rows, cols = kmap.shape
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    fig.set_size_inches(6, 2.5)  # Можна налаштувати на свій розсуд

    # ---------------------------------------
    # 1) Малюємо сітку (прямокутники) і текст
    # ---------------------------------------
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  # 0-й рядок угорі
            
            # Рамка клітинки
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor='black',
                linewidth=1
            ))
            
            # Текст (значення в клітинці)
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
    # 2) Зберемо дані: (r, c) → [список груп], яким належить ця клітинка
    # ---------------------------------------
    cell_to_groups = {}
    for group_idx, coords_list in enumerate(groups):
        for (r, c) in coords_list:
            cell_to_groups.setdefault((r, c), []).append(group_idx)

    # ---------------------------------------
    # 3) Визначимо для кожної групи 
    #    - колір (із палітри)
    #    - форму (маркер)
    # ---------------------------------------
    # Популярні маркери: 'o' (коло), '^' (трикутник), 's' (квадрат),
    # 'D' (ромб), 'v' (трикутник вниз), '>' (трикутник вправо), '<', '*', 'X'
    marker_styles = ['o', '^', 's', 'D', '*', 'X', 'v', '>']  # про запас
    color_map = plt.cm.tab10  # Кольори з палітри tab10 (0..9)

    def get_marker_for_group(g_idx):
        return marker_styles[g_idx % len(marker_styles)]
    
    def get_color_for_group(g_idx):
        return color_map(g_idx % 10)
    
    # ---------------------------------------
    # 4) Малюємо маркери у правому верхньому куточку клітинки
    #    Якщо кілька груп, розташовуємо маркери зправа наліво
    # ---------------------------------------
    for (r, c), group_list in cell_to_groups.items():
        # Координати правого верхнього куточка клітинки (трішки відступимо)
        # Щоб не впритул до рамки, робимо margin_x, margin_y
        x_right_top = c * cell_size + (cell_size - gap) - 0.05
        y_right_top = (rows - 1 - r) * cell_size + (cell_size - gap) - 0.05
        
        # Відстань між маркерами у клітинці
        spacing = 0.12  # чим більше, тим далі розсуваються
        
        # Для зручності: малюємо зправа наліво.
        # Перший маркер -- праворуч, наступні -- лівіше.
        # group_list може мати 1, 2, 3.. елементів
        for i, g_idx in enumerate(group_list):
            # Для i-го маркера «відступимо» i * spacing ліворуч
            x_pos = x_right_top - i * spacing
            y_pos = y_right_top  # незмінний по вертикалі

            marker_style = get_marker_for_group(g_idx)
            color = get_color_for_group(g_idx)
            
            # Виводимо маркер. scatter із одним x,y — по суті одиночна точка.
            ax.scatter(
                [x_pos],
                [y_pos],
                marker=marker_style,
                c=[color],
                s=100,       # розмір
                edgecolors='black',
                linewidths=1
            )

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Міні-значки в правому верхньому куточку")
    plt.show()


# === Запуск ===
draw_kmap_with_markers_topright(veich_structure, forming_groups)
