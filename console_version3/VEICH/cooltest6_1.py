import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

forming_groups = [
    [(1, 0), (1, 1)],   # Група 0
    [(1, 1), (1, 2)]    # Група 1
]

def draw_kmap_with_markers_topright_save(kmap, groups, cell_size=1, gap=0.05, filename="kmap_result.png"):
    """
    Відображає 2D-масив kmap у вигляді таблиці та зберігає результат у PNG-файл.
    У кожній клітинці, якщо вона належить декільком групам, 
    у правому верхньому кутку малюється декілька фігур (міні-значків).
    """
    rows, cols = kmap.shape
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    fig.set_size_inches(9, 5)  # Можна налаштувати інші розміри

    # (1) Малюємо сітку та значення в клітинках
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  
            
            ax.add_patch(Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor='black',
                linewidth=1
            ))
            
            val = str(kmap[r, c])
            ax.text(
                x + (cell_size - gap)/2,
                y + (cell_size - gap)/2,
                val,
                ha='center',
                va='center',
                fontsize=12
            )
    
    # (2) Зберемо дані про групи для кожної клітинки
    cell_to_groups = {}
    for group_idx, coords_list in enumerate(groups):
        for (r, c) in coords_list:
            cell_to_groups.setdefault((r, c), []).append(group_idx)

    # (3) Визначимо кольори та форми маркерів
    marker_styles = ['o', '^', 's', 'D', '*', 'X', 'v', '>']
    color_map = plt.cm.tab10
    
    def get_marker_for_group(g_idx):
        return marker_styles[g_idx % len(marker_styles)]
    
    def get_color_for_group(g_idx):
        return color_map(g_idx % 10)
    
    # (4) Малюємо маркери у правому верхньому куточку
    for (r, c), group_list in cell_to_groups.items():
        x_right_top = c * cell_size + (cell_size - gap) - 0.05
        y_right_top = (rows - 1 - r) * cell_size + (cell_size - gap) - 0.05
        
        spacing = 0.12  # Відстань між маркерами
        
        for i, g_idx in enumerate(group_list):
            x_pos = x_right_top - i * spacing
            y_pos = y_right_top
            
            marker_style = get_marker_for_group(g_idx)
            color = get_color_for_group(g_idx)
            
            ax.scatter(
                [x_pos],
                [y_pos],
                marker=marker_style,
                c=[color],
                s=100,
                edgecolors='black',
                linewidths=1
            )

    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()

    # Замість plt.show() - зберігаємо у файл (PNG за замовчуванням)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)  # Закриваємо фігуру, щоб не залишалась у пам'яті

# Приклад виклику
draw_kmap_with_markers_topright_save(
    veich_structure,
    forming_groups,
    filename="example_output.png"
)
print("Зображення збережено у файл 'example_output.png'")
