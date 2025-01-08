import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_and_gate():
    fig, ax = plt.subplots(figsize=(4, 4))

    # Рамка логічного елемента
    and_gate = patches.FancyBboxPatch(
        (0.2, 0.3), 0.4, 0.4, boxstyle="round,pad=0.1",
        edgecolor="black", facecolor="white", linewidth=2
    )
    ax.add_patch(and_gate)

    # Півколо справа
    and_arc = patches.Arc((0.6, 0.5), 0.4, 0.4, theta1=270, theta2=90, color="black", linewidth=2)
    ax.add_patch(and_arc)

    # Лінії входу
    ax.plot([0.0, 0.2], [0.4, 0.4], color="black", linewidth=2)  # Верхня лінія
    ax.plot([0.0, 0.2], [0.6, 0.6], color="black", linewidth=2)  # Нижня лінія

    # Лінія виходу
    ax.plot([0.8, 1.0], [0.5, 0.5], color="black", linewidth=2)

    # Написи
    ax.text(0.5, 0.2, "I (ANSI)", ha="center", fontsize=12, fontweight="bold")

    # Налаштування візуалізації
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")  # Прибрати осі

    plt.show()

draw_and_gate()
