import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle

veich_structure = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0]
])

forming_groups = [
    [(1, 0), (1, 1)],   # Група 0
    [(1, 1), (1, 2)]    # Група 1
]

def draw_kmap_pie(kmap, groups, cell_size=0.2, gap=0):
    """
    Відображає 2D-масив kmap та ділить клітинки на сектори «пирога»,
    якщо клітинка належить одразу кільком групам.
    """
    rows, cols = kmap.shape
    
    # 1) Зберемо інформацію про те, які групи належать до якої клітинки:
    #    key = (r, c), value = список індексів груп
    cell_to_groups = {}
    for group_idx, coords_list in enumerate(groups):
        for (r, c) in coords_list:
            cell_to_groups.setdefault((r, c), []).append(group_idx)

    # 2) Палітра кольорів (наприклад, tab10)
    #    При потребі збільшуйте або змінюйте
    def get_group_color(g_idx):
        return plt.cm.tab10(g_idx % 10)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    fig.set_size_inches(6, 2.5)

    # 3) Малюємо базову сітку: прямокутники + числа
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = (rows - 1 - r) * cell_size  # 0-й рядок угорі
            
            # Рамка клітинки (прямокутник без заливки)
            rect = Rectangle(
                (x, y),
                cell_size - gap,
                cell_size - gap,
                fill=False,
                edgecolor="black",
                linewidth=1
            )
            ax.add_patch(rect)

            # Текст (число в клітинці)
            val = str(kmap[r, c])
            ax.text(
                x + (cell_size - gap)/2,
                y + (cell_size - gap)/2,
                val,
                ha='center',
                va='center',
                fontsize=12
            )
    
    # 4) Тепер малюємо «пироги» (в тому разі, якщо в клітинці є одна чи більше груп)
    for (r, c), group_list in cell_to_groups.items():
        # Центр "пирога" — центр клітинки
        center_x = c * cell_size + (cell_size - gap)/2
        center_y = (rows - 1 - r) * cell_size + (cell_size - gap)/2
        
        # Радіус (приблизний) — щоб "пиріг" вмістився в клітинку
        radius = (cell_size - gap)/2
        
        # Якщо клітинка належить n групам, ділимо «коло» на n секторів
        n = len(group_list)
        angle_step = 360 / n
        
        # Малюємо кожен сектор
        for i, g_idx in enumerate(group_list):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            
            wedge = Wedge(
                center=(center_x, center_y),
                r=radius,
                theta1=start_angle,
                theta2=end_angle,
                facecolor=get_group_color(g_idx),
                edgecolor="black",
                linewidth=1,
                alpha=0.6  # Напівпрозорість, щоб було видно число під пирогом
            )
            ax.add_patch(wedge)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Клітинки, розділені на сектори («пироги») за групами")
    plt.show()

# Запуск
draw_kmap_pie(veich_structure, forming_groups)