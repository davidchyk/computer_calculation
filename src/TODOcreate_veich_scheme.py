import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib import font_manager
import numpy as np
import sys, os

# === ПАРАМЕТРИ ===
CELL_SIZE = 0.2  # Розмір клітинки
LINE_WIDTH = 1.2  # Товщина обведення
PADDING = 0.03  # Відступ усередині, щоб рамки не накладались

def resource_path(relative_path):
    """Повертає абсолютний шлях до ресурсу, працює і в .exe, і в IDE"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def draw_axis_brackets(ax, list_args: list[str]):

    normal_symbols = {"I", "J", "T", "Y"} # not add
    over_add_symbols = {"m", "M", "w", "W"}

    offer_list = []
    x_left = 0.0147
    x_right = 0.009
    y_down = 0.015

    for x in list_args:

        offer_list.append(bool((not set(x).intersection(normal_symbols) and (x.isupper() or set(x).intersection({"m", "w"})))))

    if len(list_args) == 9:

        left_offer = offer_list[5]*x_left+0.01
        left_left_offer = offer_list[3]*x_left + left_offer

        if over_add_symbols.intersection(set(list_args[3])):

            left_offer += 0.009
            left_left_offer += 0.005

            if over_add_symbols.intersection(set(list_args[3])): left_left_offer += 0.006

        down_offer = bool(offer_list[7] or set(list_args[8]).intersection(normal_symbols) or set(list_args[8]).intersection({"k", "l", "i", "j", "f"}))*y_down

        down_down_offer = down_offer + 0.03

        right_offer = bool(set(list_args[7]).intersection(over_add_symbols))*x_right
        right_right_text_offer = bool(set(list_args[1]).intersection(over_add_symbols))*0.015
        right_right_offer = right_offer + 0.03

        # Врехня, верхня, врехня дужка (X9)
        ax.plot([3.4032, 6.6032], [3.71, 3.71], color='black', linewidth=3, zorder=100, clip_on=False)
        ax.text(5.0032, 3.77, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права правіша (X8)
        ax.plot([6.77 + right_right_offer, 6.77 + right_right_offer], [1.7968, 0.2032], color='black', linewidth=3, zorder=100, clip_on=False)
        ax.text(6.84 + right_right_offer + right_right_text_offer, 1.0, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня, нижня, нижня (X7)
        ax.plot([1.8032, 3.3968], [0.06 - down_down_offer, 0.06 - down_down_offer], color='black', linewidth=3, zorder=100)
        ax.text(2.6, 0.01 - down_down_offer - 0.02, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([5.0032, 6.5968], [0.06 - down_down_offer, 0.06 - down_down_offer], color='black', linewidth=3, zorder=100)
        ax.text(5.8, 0.01 - down_down_offer - 0.02, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва_лівіша дужка (X6)
        ax.plot([0.03 - left_offer, 0.03 - left_offer], [0.9968, 0.2032], color='black', linewidth=3, zorder=100)
        ax.text(-0.04 - left_left_offer, 0.6, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.03 - left_offer, 0.03 - left_offer], [2.5968, 1.8032], color='black', linewidth=3, zorder=100)
        ax.text(-0.04 - left_left_offer, 2.2, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня_вища дужка (X5)
        ax.plot([1.0032, 1.8032], [3.57, 3.57], color='black', linewidth=3, zorder=100)
        ax.text(1.4032, 3.63, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.6032, 3.4032], [3.57, 3.57], color='black', linewidth=3, zorder=100)
        ax.text(3.0032, 3.63, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([4.2032, 5.0032], [3.57, 3.57], color='black', linewidth=3, zorder=100)
        ax.text(4.6032, 3.63, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([5.8032, 6.6032], [3.57, 3.57], color='black', linewidth=3, zorder=100)
        ax.text(6.2032, 3.63, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [1.7968, 1.4032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 1.6, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [0.9968, 0.6032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.8, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [3.3968, 3.0032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 3.2, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [2.5968, 2.2032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 2.4, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X3)
        ax.plot([0.2032, 0.5968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.0032, 1.3968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(1.2, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.8032, 2.1968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(2.0, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.6032, 2.9968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(2.8, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([3.4032, 3.7968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(3.6, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([4.2032, 4.5968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(4.4, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([5.0032, 5.3968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(5.2, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([5.8032, 6.1968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(6.0, 3.49, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)
        ax.plot([6.63, 6.63], [1.5968, 1.2032], color='black', linewidth=3, zorder=100)
        ax.text(6.7 + right_offer, 1.4, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([6.63, 6.63], [0.7968, 0.4032], color='black', linewidth=3, zorder=100)
        ax.text(6.7 + right_offer, 0.6, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([6.63, 6.63], [3.1968, 2.8032], color='black', linewidth=3, zorder=100)
        ax.text(6.7 + right_offer, 3.0, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([6.63, 6.63], [2.3968, 2.0032], color='black', linewidth=3, zorder=100)
        ax.text(6.7 + right_offer, 2.2, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4032, 0.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.2032, 1.5968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(1.4, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.0032, 2.3968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(2.2, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.8032, 3.1968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(3.0, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([3.6032, 3.9968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(3.8, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([4.4032, 4.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(4.6, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([5.2032, 5.5968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(5.4, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([6.0032, 6.3968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(6.2, 0.12 - down_offer, f"${list_args[8]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 8:

        left_offer = offer_list[4]*x_left
        left_left_offer = offer_list[2]*x_left + left_offer

        if over_add_symbols.intersection(set(list_args[3])):

            left_offer += 0.009
            left_left_offer += 0.005

            if over_add_symbols.intersection(set(list_args[2])): left_left_offer += 0.006

        down_offer = bool(offer_list[7] or set(list_args[7]).intersection(normal_symbols) or set(list_args[7]).intersection({"k", "l", "i", "j", "f"}))*y_down

        down_down_offer = down_offer + 0.03

        right_offer = bool(set(list_args[6]).intersection(over_add_symbols))*x_right
        right_right_text_offer = bool(set(list_args[0]).intersection(over_add_symbols))*0.015
        right_right_offer = right_offer + 0.03

        # Права правіша (X8)
        ax.plot([3.57 + right_right_offer, 3.57 + right_right_offer], [1.7968, 0.2032], color='black', linewidth=3, zorder=100, clip_on=False)
        ax.text(3.64 + right_right_offer + right_right_text_offer, 1.0, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня, нижня, нижня (X7)
        ax.plot([1.8032, 3.3968], [0.06 - down_down_offer, 0.06 - down_down_offer], color='black', linewidth=3, zorder=100)
        ax.text(2.6, 0.01 - down_down_offer - 0.02, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва_лівіша дужка (X6)
        ax.plot([0.03 - left_offer, 0.03 - left_offer], [0.9968, 0.2032], color='black', linewidth=3, zorder=100)
        ax.text(-0.04 - left_left_offer, 0.6, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.03 - left_offer, 0.03 - left_offer], [2.5968, 1.8032], color='black', linewidth=3, zorder=100)
        ax.text(-0.04 - left_left_offer, 2.2, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня_вища дужка (X5)
        ax.plot([1.0032, 1.8032], [3.57, 3.57], color='black', linewidth=3, zorder=100)
        ax.text(1.4032, 3.63, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.6032, 3.4032], [3.57, 3.57], color='black', linewidth=3, zorder=100)
        ax.text(3.0032, 3.63, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [1.7968, 1.4032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 1.6, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [0.9968, 0.6032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.8, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [3.3968, 3.0032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 3.2, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [2.5968, 2.2032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 2.4, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X3)
        ax.plot([0.2032, 0.5968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 3.49, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.0032, 1.3968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(1.2, 3.49, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.8032, 2.1968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(2.0, 3.49, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.6032, 2.9968], [3.43, 3.43], color='black', linewidth=3, zorder=100)
        ax.text(2.8, 3.49, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)
        ax.plot([3.43, 3.43], [1.5968, 1.2032], color='black', linewidth=3, zorder=100)
        ax.text(3.5 + right_offer, 1.4, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([3.43, 3.43], [0.7968, 0.4032], color='black', linewidth=3, zorder=100)
        ax.text(3.5 + right_offer, 0.6, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([3.43, 3.43], [3.1968, 2.8032], color='black', linewidth=3, zorder=100)
        ax.text(3.5 + right_offer, 3.0, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([3.43, 3.43], [2.3968, 2.0032], color='black', linewidth=3, zorder=100)
        ax.text(3.5 + right_offer, 2.2, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4032, 0.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.2032, 1.5968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(1.4, 0.12 - down_offer, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.0032, 2.3968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(2.2, 0.12 - down_offer, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.8032, 3.1968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(3.0, 0.12 - down_offer, f"${list_args[7]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 7:

        left_offer = offer_list[3]*x_left
        left_left_offer = offer_list[1]*x_left + left_offer

        if over_add_symbols.intersection(set(list_args[3])):

            left_offer += 0.009
            left_left_offer += 0.005

            if over_add_symbols.intersection(set(list_args[1])): left_left_offer += 0.006

        down_offer = bool(offer_list[6] or set(list_args[6]).intersection(normal_symbols) or set(list_args[6]).intersection({"k", "l", "i", "j", "f"}))*y_down

        down_down_offer = down_offer + 0.03

        right_offer = bool(set(list_args[5]).intersection(over_add_symbols))*x_right

        # Нижня, нижня, нижня (X7)
        ax.plot([1.8032, 3.3968], [0.06 - down_down_offer, 0.06 - down_down_offer], color='black', linewidth=3, zorder=100)
        ax.text(2.6, 0.01 - down_down_offer - 0.02, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва_лівіша дужка (X6)
        ax.plot([0.03 - left_offer, 0.03 - left_offer], [0.9968, 0.2032], color='black', linewidth=3, zorder=100)
        ax.text(-0.04 - left_left_offer, 0.6, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня_вища дужка (X5)
        ax.plot([1.0032, 1.8032], [1.97, 1.97], color='black', linewidth=3, zorder=100)
        ax.text(1.4032, 2.03, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.6032, 3.4032], [1.97, 1.97], color='black', linewidth=3, zorder=100)
        ax.text(3.0032, 2.03, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [1.7968, 1.4032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 1.6, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [0.9968, 0.6032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.8, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X3)
        ax.plot([0.2032, 0.5968], [1.83, 1.83], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 1.89, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.0032, 1.3968], [1.83, 1.83], color='black', linewidth=3, zorder=100)
        ax.text(1.2, 1.89, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.8032, 2.1968], [1.83, 1.83], color='black', linewidth=3, zorder=100)
        ax.text(2.0, 1.89, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.6032, 2.9968], [1.83, 1.83], color='black', linewidth=3, zorder=100)
        ax.text(2.8, 1.89, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)
        ax.plot([3.43, 3.43], [1.5968, 1.2032], color='black', linewidth=3, zorder=100)
        ax.text(3.5 + right_offer, 1.4, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([3.43, 3.43], [0.7968, 0.4032], color='black', linewidth=3, zorder=100)
        ax.text(3.5 + right_offer, 0.6, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4032, 0.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.2032, 1.5968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(1.4, 0.12 - down_offer, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.0032, 2.3968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(2.2, 0.12 - down_offer, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([2.8032, 3.1968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(3.0, 0.12 - down_offer, f"${list_args[6]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 6:

        left_offer = offer_list[2]*x_left
        left_left_offer = offer_list[0]*x_left + left_offer

        if over_add_symbols.intersection(set(list_args[2])):

            left_offer += 0.009
            left_left_offer += 0.005

            if over_add_symbols.intersection(set(list_args[0])): left_left_offer += 0.006

        down_offer = bool(offer_list[5] or set(list_args[5]).intersection(normal_symbols) or set(list_args[5]).intersection({"k", "l", "i", "j", "f"}))*y_down

        right_offer = bool(set(list_args[4]).intersection(over_add_symbols))*x_right

        # Ліва_лівіша дужка (X6)
        ax.plot([0.03 - left_offer, 0.03 - left_offer], [0.9968, 0.2032], color='black', linewidth=3, zorder=100)
        ax.text(-0.04 - left_left_offer, 0.6, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня_вища дужка (X5)
        ax.plot([1.0032, 1.8032], [1.97, 1.97], color='black', linewidth=3, zorder=100)
        ax.text(1.4032, 2.03, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [1.7968, 1.4032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 1.6, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([0.17, 0.17], [0.9968, 0.6032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.8, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X3)
        ax.plot([0.2032, 0.5968], [1.83, 1.83], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 1.89, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.0032, 1.3968], [1.83, 1.83], color='black', linewidth=3, zorder=100)
        ax.text(1.2, 1.89, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)

        ax.plot([1.83, 1.83], [1.5968, 1.2032], color='black', linewidth=3, zorder=100)
        ax.text(1.9 + right_offer, 1.4, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.83, 1.83], [0.7968, 0.4032], color='black', linewidth=3, zorder=100)
        ax.text(1.9 + right_offer, 0.6, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4032, 0.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.2032, 1.5968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(1.4, 0.12 - down_offer, f"${list_args[5]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 5:

        left_offer = offer_list[1]*x_left
        if over_add_symbols.intersection(set(list_args[1])): left_offer += 0.009

        down_offer = bool(offer_list[4] or set(list_args[4]).intersection(normal_symbols) or set(list_args[4]).intersection({"k", "l", "i", "j", "f"}))*y_down

        right_offer = bool(set(list_args[3]).intersection(over_add_symbols))*x_right

        # Верхня_вища дужка (X5)
        ax.plot([1.0032, 1.8032], [1.17, 1.17], color='black', linewidth=3, zorder=100)
        ax.text(1.4032, 1.23, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [0.9968, 0.6032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.8, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X3)
        ax.plot([0.2032, 0.5968], [1.03, 1.03], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 1.09, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.0032, 1.3968], [1.03, 1.03], color='black', linewidth=3, zorder=100)
        ax.text(1.2, 1.09, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)
        ax.plot([1.83, 1.83], [0.7968, 0.4032], color='black', linewidth=3, zorder=100)
        ax.text(1.9 + right_offer, 0.6, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4032, 0.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

        ax.plot([1.2032, 1.5968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(1.4, 0.12 - down_offer, f"${list_args[4]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 4:

        left_offer = offer_list[0]*x_left
        if over_add_symbols.intersection(set(list_args[0])): left_offer += 0.009

        down_offer = bool(offer_list[2] or set(list_args[2]).intersection(normal_symbols) or set(list_args[2]).intersection({"k", "l", "i", "j", "f"}))*y_down

        right_offer = bool(set(list_args[2]).intersection(over_add_symbols))*x_right

        # Ліва дужка (X4)
        ax.plot([0.17, 0.17], [0.9968, 0.6032], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.8, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X3)
        ax.plot([0.2032, 0.5968], [1.03, 1.03], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 1.09, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Права дужка (X2)
        ax.plot([1.03, 1.03], [0.7968, 0.4032], color='black', linewidth=3, zorder=100)
        ax.text(1.10 + right_offer, 0.6, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4032, 0.7968], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[3]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 3:

        left_offer = offer_list[0]*x_left
        if over_add_symbols.intersection(set(list_args[0])): left_offer += 0.009

        down_offer = bool(offer_list[2] or set(list_args[2]).intersection(normal_symbols) or set(list_args[2]).intersection({"k", "l", "i", "j", "f"}))*y_down

        # Ліва дужка (X3)
        ax.plot([0.17, 0.17], [0.6, 0.4], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.52, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X2)
        ax.plot([0.2, 0.6], [0.63, 0.63], color='black', linewidth=3, zorder=100)
        ax.text(0.4, 0.69, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Нижня дужка (X1)
        ax.plot([0.4, 0.8], [0.17, 0.17], color='black', linewidth=3, zorder=100)
        ax.text(0.6, 0.12 - down_offer, f"${list_args[2]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 2:

        left_offer = offer_list[0]*x_left
        if over_add_symbols.intersection(set(list_args[0])): left_offer += 0.009

        # Ліва дужка (X2)
        ax.plot([0.17, 0.17], [0.5968, 0.4046], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.52, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

        # Верхня дужка (X1)
        ax.plot([0.2032, 0.3968], [0.63, 0.63], color='black', linewidth=3, zorder=100)
        ax.text(0.3, 0.69, f"${list_args[1]}$", ha='center', va='center', fontsize=40, zorder=101)

    elif len(list_args) == 1:

        left_offer = offer_list[0]*x_left
        if over_add_symbols.intersection(set(list_args[0])): left_offer += 0.009

        # Ліва дужка (X1)
        ax.plot([0.17, 0.17], [0.5968, 0.4046], color='black', linewidth=3, zorder=100)
        ax.text(0.11 - left_offer, 0.52, f"${list_args[0]}$", ha='center', va='center', fontsize=40, zorder=101)

def draw_kmap_with_tight_rounded_boxes(kmap, groups, list_args, filename):

    """
    Малює карту Вейча та додає обведення груп із заокругленими прямокутниками.
    Тепер обведення не заходить на сусідні клітинки!
    """

    plt.rcParams['mathtext.fontset'] = 'cm'        # Computer Modern
    plt.rcParams['mathtext.rm'] = 'serif'
    plt.rcParams['font.family'] = 'serif'

    tt_prop = font_manager.FontProperties(fname=resource_path("cmuntt.ttf"))

    cell_size=CELL_SIZE

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
                f"{kmap[r, c]}",
                ha='center',
                va='center',
                fontproperties=tt_prop,  # 👈 конкретно цей шрифт
                fontsize=20
            )

    for group in groups:

        mini_groups = groups[group][0]
        color = groups[group][1]
        line_type = groups[group][2]

        for mini_group in mini_groups:

            # Визначаємо точні межі групи
            min_r = mini_group[0]
            min_c = mini_group[1]

            max_r = mini_group[2]
            max_c = mini_group[3]

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
                facecolor='none',
                linestyle=line_type  # Задаємо стиль лінії
            )
            ax.add_patch(rounded_box)

    ax.set_xticks([])
    ax.set_yticks([])

    edge_rows = {0, rows - 1}
    edge_cols = {0, cols - 1}

    # Видаляємо крайні клітинки (Rectangle)
    for patch in list(ax.patches):
        if not isinstance(patch, Rectangle):
            continue  # пропустити обведення (FancyBboxPatch та ін.)

        x, y = patch.get_xy()
        c = int(x / cell_size)
        r = rows - 1 - int(y / cell_size)

        if r in edge_rows or c in edge_cols:
            patch.remove()

    # Видаляємо крайні тексти (Text)
    for text in list(ax.texts):
        x, y = text.get_position()
        c = int(x / cell_size)
        r = rows - 1 - int(y / cell_size)

        if r in edge_rows or c in edge_cols:
            text.remove()

        ax.set_xlim(0, cols * cell_size)
        ax.set_ylim(0, rows * cell_size)

    # Скільки "ластика" залізатиме в середину (оптимально ~0.5-1 клітинки)
    fade_depth = cell_size * 0.9

    # Верхній край
    ax.add_patch(Rectangle(
        (0, rows * cell_size - fade_depth),
        cols * cell_size, fade_depth,
        facecolor='white',
        edgecolor='none',
        alpha=1.0,
        zorder=10
    ))

    # Нижній край
    ax.add_patch(Rectangle(
        (0, 0),
        cols * cell_size, fade_depth,
        facecolor='white',
        edgecolor='none',
        alpha=1.0,
        zorder=10
    ))

    # Лівий край
    ax.add_patch(Rectangle(
        (0, 0),
        fade_depth, rows * cell_size,
        facecolor='white',
        edgecolor='none',
        alpha=1.0,
        zorder=10
    ))

    # Правий край
    ax.add_patch(Rectangle(
        (cols * cell_size - fade_depth, 0),
        fade_depth, rows * cell_size,
        facecolor='white',
        edgecolor='none',
        alpha=1.0,
        zorder=10
    ))

    draw_axis_brackets(ax, list_args)

    #plt.show()
    ax.axis("off")

    #fig.set_size_inches(11.7, 8.3)  # A4 landscape у дюймах

    # Збереження у файл
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

def veich_create(filename, type, num_of_args, minimized_term_term_list, sets_number, list_args):

    def differ(s1: str, s2: str) -> bool:

        """
        Повертає True, якщо s1 і s2 не відрізняються (ідентичні)
        або відрізняються рівно на 1 символ; інакше False.
        """

        if not s1: return False

        normal_dict = {}
        index = 0

        for x in range(len(s1)):

            if s1[x] != "X": normal_dict[index] = s1[x]
            index += 1

        for key, value in normal_dict.items():

            if value != s2[key]: return False

        return True

    def find_all_neighbors(points: list, origin: tuple) -> list:

        neighbors = set()
        queue = [origin]

        while queue:
            current = queue.pop(0)
            for point in points:
                if point not in neighbors and abs(point[0] - current[0]) <= 1 and abs(point[1] - current[1]) <= 1:
                    neighbors.add(point)
                    queue.append(point)

        return list(neighbors)

    def find_min_max(points):

        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)

        return min_x, min_y, max_x, max_y

    def generate_add_coordinates(start_coord, rows, cols):

        def define_matrix(coord, rows, cols):

            x, y = coord

            if x == 0 and y == 0:

                return "left_top_corner"

            elif x == 0 and y == cols-1:

                return "right_top_corner"

            elif x == rows-1 and y == 0:

                return "left_bottom_corner"

            elif x == rows-1 and y == cols-1:

                return "right_bottom_corner"

            elif x == 0:

                return "top_side_part"

            elif x == rows-1:

                return "bottom_side_part"

            elif y == 0:

                return "left_side_part"

            elif y == cols-1:

                return "right_side_part"

            return None

        result_coords = []
        x, y = start_coord

        type_coord = define_matrix(start_coord, rows, cols)

        if type_coord == "left_top_corner":

            result_coords.append((x+rows+1, y+1))
            result_coords.append((x+rows+1, y+cols+1))
            result_coords.append((x+1, y+cols+1))

        elif type_coord == "right_top_corner":

            result_coords.append((x+rows+1, y+1))
            result_coords.append((x+rows+1, y-cols+1))
            result_coords.append((x+1, y-cols+1))

        elif type_coord == "left_bottom_corner":

            result_coords.append((x-rows+1, y+1))
            result_coords.append((x-rows+1, y+cols+1))
            result_coords.append((x+1, y+cols+1))

        elif type_coord == "right_bottom_corner":

            result_coords.append((x-rows+1, y+1))
            result_coords.append((x-rows+1, y-cols+1))
            result_coords.append((x+1, y-cols+1))

        elif type_coord == "top_side_part":

            result_coords.append((x+rows+1, y+1))

        elif type_coord == "bottom_side_part":

            result_coords.append((x-rows+1, y+1))

        elif type_coord == "left_side_part":

            result_coords.append((x+1, y+cols+1))

        elif type_coord == "right_side_part":

            result_coords.append((x+1, y-cols+1))

        return result_coords

    def get_front_group_config(group_index):

        total_colors = len(colors)
        total_linestyles = len(line_configurations)
        # Використовуємо цілу частину від ділення для визначення типу лінії
        linestyle_index = group_index // total_colors  
        # Індекс кольору – залишок від ділення
        color_index = group_index % total_colors  
        # Якщо group_idx перевищує кількість комбінацій, можна циклічно повертати значення
        linestyle_index %= total_linestyles

        return [colors[color_index], line_configurations[linestyle_index]]

    def del_one(type, FRONT, shape: tuple) -> list:

        result = []
        rows, cols = shape

        for i in np.where(np.all(FRONT == type, axis=1))[0]:

            result.append((int(i)+1, 0))
            result.append((int(i)+1, cols-1))

        for j in np.where(np.all(FRONT == type, axis=0))[0]:

            result.append((0, int(j)+1))
            result.append((rows-1, int(j)+1))

        return result

    if type: WORK_minimized_term_list = 6
    else:

        WORK_minimized_term_list = []

        for t in minimized_term_term_list:

            t = t.translate(str.maketrans("01", "10"))
            WORK_minimized_term_list.append(t)

    group_config = ()
    result = dict()
    bin_sets = []

    for set_strc in sets_number: bin_sets.append(format(int(set_strc), f'0{num_of_args}b'))

    if num_of_args == 9:

        FRONT_veich_structure = np.zeros((16, 32), dtype=int)
        BACK_veich_structure = [
            [ 12,  13,   9,   8,  28,  29,  25,  24,  76,  77,  73,  72,  92,  93,  89,  88, 268, 269, 265, 264, 284, 285, 281, 280, 332, 333, 329, 328, 348, 349, 345, 344],
            [ 14,  15,  11,  10,  30,  31,  27,  26,  78,  79,  75,  74,  94,  95,  91,  90, 270, 271, 267, 266, 286, 287, 283, 282, 334, 335, 331, 330, 350, 351, 347, 346],
            [  6,   7,   3,   2,  22,  23,  19,  18,  70,  71,  67,  66,  86,  87,  83,  82, 262, 263, 259, 258, 278, 279, 275, 274, 326, 327, 323, 322, 342, 343, 339, 338],
            [  4,   5,   1,   0,  20,  21,  17,  16,  68,  69,  65,  64,  84,  85,  81,  80, 260, 261, 257, 256, 276, 277, 273, 272, 324, 325, 321, 320, 340, 341, 337, 336],
            [ 44,  45,  41,  40,  60,  61,  57,  56, 108, 109, 105, 104, 124, 125, 121, 120, 300, 301, 297, 296, 316, 317, 313, 312, 364, 365, 361, 360, 380, 381, 377, 376],
            [ 46,  47,  43,  42,  62,  63,  59,  58, 110, 111, 107, 106, 126, 127, 123, 122, 302, 303, 299, 298, 318, 319, 315, 314, 366, 367, 363, 362, 382, 383, 379, 378],
            [ 38,  39,  35,  34,  54,  55,  51,  50, 102, 103,  99,  98, 118, 119, 115, 114, 294, 295, 291, 290, 310, 311, 307, 306, 358, 359, 355, 354, 374, 375, 371, 370],
            [ 36,  37,  33,  32,  52,  53,  49,  48, 100, 101,  97,  96, 116, 117, 113, 112, 292, 293, 289, 288, 308, 309, 305, 304, 356, 357, 353, 352, 372, 373, 369, 368],
            [140, 141, 137, 136, 156, 157, 153, 152, 204, 205, 201, 200, 220, 221, 217, 216, 396, 397, 393, 392, 412, 413, 409, 408, 460, 461, 457, 456, 476, 477, 473, 472],
            [142, 143, 139, 138, 158, 159, 155, 154, 206, 207, 203, 202, 222, 223, 219, 218, 398, 399, 395, 394, 414, 415, 411, 410, 462, 463, 459, 458, 478, 479, 475, 474],
            [134, 135, 131, 130, 150, 151, 147, 146, 198, 199, 195, 194, 214, 215, 211, 210, 390, 391, 387, 386, 406, 407, 403, 402, 454, 455, 451, 450, 470, 471, 467, 466],
            [132, 133, 129, 128, 148, 149, 145, 144, 196, 197, 193, 192, 212, 213, 209, 208, 388, 389, 385, 384, 404, 405, 401, 400, 452, 453, 449, 448, 468, 469, 465, 464],
            [172, 173, 169, 168, 188, 189, 185, 184, 236, 237, 233, 232, 252, 253, 249, 248, 428, 429, 425, 424, 444, 445, 441, 440, 492, 493, 489, 488, 508, 509, 505, 504],
            [174, 175, 171, 170, 190, 191, 187, 186, 238, 239, 235, 234, 254, 255, 251, 250, 430, 431, 427, 426, 446, 447, 443, 442, 494, 495, 491, 490, 510, 511, 507, 506],
            [166, 167, 163, 162, 182, 183, 179, 178, 230, 231, 227, 226, 246, 247, 243, 242, 422, 423, 419, 418, 438, 439, 435, 434, 486, 487, 483, 482, 502, 503, 499, 498],
            [164, 165, 161, 160, 180, 181, 177, 176, 228, 229, 225, 224, 244, 245, 241, 240, 420, 421, 417, 416, 436, 437, 433, 432, 484, 485, 481, 480, 500, 501, 497, 496],
        ]

        line_configurations = [
            "-",
            "--",
            ":",
            "-."
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803",
            "#9400D3",
            "#FF1493",
            "#FF8C00",
            "#04A08B",
            "#000000",
            "#030374",
            "#0F611AFF",
            "#5E0086",
            "#857D7D",
            "#14DC89",
            "#463E1A",
            "#00F7FF",
            "#FFD700",
            "#1E90FF",
            "#ADFF2F",
            "#FF4500",
            "#8B008B",
            "#7FFF00",
            "#FF00FF",
            "#008B8B",
            "#B22222",
            "#00008B",
            "#228B22",
            "#800000",
            "#E9967A",
            "#8FBC8F",
            "#00CED1",
            "#FF69B4",
            "#A52A2A",
            "#7B68EE",
            "#00FF7F",
            "#DA70D6",
            "#F08080",
            "#20B2AA",
            "#FA8072",
            "#778899",
            "#9932CC",
            "#00BFFF",
            "#FFE4C4",
            "#9ACD32",
            "#FF7F50",
            "#191970",
            "#B0C4DE",
            "#FFB6C1",
            "#BDB76B",
            "#DC143C",
            "#6B8E23",
            "#D2691E",
            "#993300",
            "#40E0D0",
            "#F5DEB3",
            "#A9A9A9",
            "#BA55D3",
            "#CD5C5C",
            "#3CB371",
            "#6495ED",
            "#F0E68C",
            "#BC8F8F",
            "#9370DB",
            "#2F4F4F"
        ] # 64

    elif num_of_args == 8:

        FRONT_veich_structure = np.zeros((16, 16), dtype=int)
        BACK_veich_structure = [
            [ 12,  13,   9,   8,  28,  29,  25,  24,  76,  77,  73,  72,  92,  93,  89,  88],
            [ 14,  15,  11,  10,  30,  31,  27,  26,  78,  79,  75,  74,  94,  95,  91,  90],
            [  6,   7,   3,   2,  22,  23,  19,  18,  70,  71,  67,  66,  86,  87,  83,  82],
            [  4,   5,   1,   0,  20,  21,  17,  16,  68,  69,  65,  64,  84,  85,  81,  80],
            [ 44,  45,  41,  40,  60,  61,  57,  56, 108, 109, 105, 104, 124, 125, 121, 120],
            [ 46,  47,  43,  42,  62,  63,  59,  58, 110, 111, 107, 106, 126, 127, 123, 122],
            [ 38,  39,  35,  34,  54,  55,  51,  50, 102, 103,  99,  98, 118, 119, 115, 114],
            [ 36,  37,  33,  32,  52,  53,  49,  48, 100, 101,  97,  96, 116, 117, 113, 112],
            [140, 141, 137, 136, 156, 157, 153, 152, 204, 205, 201, 200, 220, 221, 217, 216],
            [142, 143, 139, 138, 158, 159, 155, 154, 206, 207, 203, 202, 222, 223, 219, 218],
            [134, 135, 131, 130, 150, 151, 147, 146, 198, 199, 195, 194, 214, 215, 211, 210],
            [132, 133, 129, 128, 148, 149, 145, 144, 196, 197, 193, 192, 212, 213, 209, 208],
            [172, 173, 169, 168, 188, 189, 185, 184, 236, 237, 233, 232, 252, 253, 249, 248],
            [174, 175, 171, 170, 190, 191, 187, 186, 238, 239, 235, 234, 254, 255, 251, 250],
            [166, 167, 163, 162, 182, 183, 179, 178, 230, 231, 227, 226, 246, 247, 243, 242],
            [164, 165, 161, 160, 180, 181, 177, 176, 228, 229, 225, 224, 244, 245, 241, 240]
        ]

        line_configurations = [
            "-",
            "--",
            ":",
            "-."
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803",
            "#9400D3",
            "#FF1493",
            "#FF8C00",
            "#04A08B",
            "#000000",
            "#030374",
            "#0F611AFF",
            "#5E0086",
            "#857D7D",
            "#14DC89",
            "#463E1A",
            "#00F7FF",
            "#FFD700",
            "#1E90FF",
            "#ADFF2F",
            "#FF4500",
            "#8B008B",
            "#7FFF00",
            "#FF00FF",
            "#008B8B",
            "#B22222",
            "#00008B",
            "#228B22",
            "#800000",
            "#E9967A",
            "#8FBC8F",
            "#00CED1",
            "#FF69B4"
        ] # 32

    elif num_of_args == 7:

        FRONT_veich_structure = np.zeros((8, 16), dtype=int)
        BACK_veich_structure = [
            [ 12,  13,   9,   8,  28,  29,  25,  24,  76,  77,  73,  72,  92,  93,  89,  88],
            [ 14,  15,  11,  10,  30,  31,  27,  26,  78,  79,  75,  74,  94,  95,  91,  90],
            [  6,   7,   3,   2,  22,  23,  19,  18,  70,  71,  67,  66,  86,  87,  83,  82],
            [  4,   5,   1,   0,  20,  21,  17,  16,  68,  69,  65,  64,  84,  85,  81,  80],
            [ 44,  45,  41,  40,  60,  61,  57,  56, 108, 109, 105, 104, 124, 125, 121, 120],
            [ 46,  47,  43,  42,  62,  63,  59,  58, 110, 111, 107, 106, 126, 127, 123, 122],
            [ 38,  39,  35,  34,  54,  55,  51,  50, 102, 103,  99,  98, 118, 119, 115, 114],
            [ 36,  37,  33,  32,  52,  53,  49,  48, 100, 101,  97,  96, 116, 117, 113, 112]
        ]

        line_configurations = [
            "-",
            "--",
            ":",
            "-."
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803",
            "#9400D3",
            "#FF1493",
            "#FF8C00",
            "#04A08B",
            "#000000",
            "#030374",
            "#0F611AFF",
            "#5E0086",
            "#857D7D",
            "#14DC89",
            "#463E1A",
            "#00F7FF"
        ] # 16

    elif num_of_args == 6:

        FRONT_veich_structure = np.zeros((8, 8), dtype=int)
        BACK_veich_structure = [
            [12, 13,  9,  8, 28, 29, 25, 24],
            [14, 15, 11, 10, 30, 31, 27, 26],
            [ 6,  7,  3,  2, 22, 23, 19, 18],
            [ 4,  5,  1,  0, 20, 21, 17, 16],
            [44, 45, 41, 40, 60, 61, 57, 56],
            [46, 47, 43, 42, 62, 63, 59, 58],
            [38, 39, 35, 34, 54, 55, 51, 50],
            [36, 37, 33, 32, 52, 53, 49, 48]
        ]

        line_configurations = [
            "-",
            "--"
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803",
            "#9400D3",
            "#FF1493",
            "#FF8C00",
            "#04A08B",
            "#000000",
            "#030374",
            "#0F611AFF",
            "#5E0086",
            "#857D7D",
            "#14DC89",
            "#463E1A",
            "#00F7FF"
        ] # 16

    elif num_of_args == 5:

        FRONT_veich_structure = np.zeros((4, 8), dtype=int)
        BACK_veich_structure = [
            [12, 13, 9, 8, 28, 29, 25, 24],
            [14, 15,11,10, 30, 31, 27, 26],
            [6,  7, 3, 2,  22, 23, 19, 18],
            [4,  5, 1, 0,  20, 21, 17, 16]
        ]

        line_configurations = [
            "-"
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803",
            "#9400D3",
            "#FF1493",
            "#FF8C00",
            "#04A08B",
            "#000000",
            "#030374",
            "#0F611AFF",
            "#5E0086",
            "#857D7D",
            "#14DC89",
            "#463E1A",
            "#00F7FF"
        ] # 16

    elif num_of_args == 4:

        FRONT_veich_structure = np.zeros((4, 4), dtype=int)
        BACK_veich_structure = [
            [12, 13,  9,  8],
            [14, 15, 11, 10],
            [ 6,  7,  3,  2],
            [ 4,  5,  1,  0]
        ]

        line_configurations = [
            "-"
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803",
            "#9400D3",
            "#FF1493",
            "#FF8C00",
            "#04A08B",
        ] # 8

    elif num_of_args == 3:

        FRONT_veich_structure = np.zeros((2, 4), dtype=int)
        BACK_veich_structure = [
            [6, 7, 5, 4],
            [2, 3, 1, 0]
        ]

        line_configurations = [
            "-"
        ]

        colors = [
            "#DC143C",
            "#4169E1",
            "#32CD32CF",
            "#C5A803"
        ] # 4

    elif num_of_args == 2:

        FRONT_veich_structure = np.zeros((2, 2), dtype=int)
        BACK_veich_structure = [
            [3, 2],
            [1, 0]
        ]

        line_configurations = [
            "-"
        ]

        colors = [
            "#DC143C",
            "#4169E1"
        ] # 2

    elif num_of_args == 1:

        FRONT_veich_structure = np.zeros((2, 1), dtype=int)
        BACK_veich_structure = [
            [1],
            [0]
        ]

        line_configurations = [
            "-"
        ]

        colors = [
            "#DC143C"
        ] # 1

    BACK_veich_structure = np.array([[format(n, f'0{num_of_args}b') for n in row] for row in BACK_veich_structure], dtype=str) # Перетворення списку чисел в список двійкоих представлень у вигляді рядка
    initial_MAIN_coord_groups = []

    for num in bin_sets:

        row_indices, col_indices = np.where(BACK_veich_structure == num)
        row = row_indices[0]
        col = col_indices[0]
        FRONT_veich_structure[row, col] = 1

    for minimized_term in WORK_minimized_term_list:

        group = []

        for idx, val in np.ndenumerate(BACK_veich_structure):

            if differ(minimized_term, str(val)): group.append((idx[0], idx[1]))

        initial_MAIN_coord_groups.append(group)

    # initial_coord_groups --- це список, який має в собі групи, а в кожній групі є координати, які входять до мінімізаційного терму

    rows, cols = FRONT_veich_structure.shape

    updated_MAIN_coord_groups = []
    updated_EXTENDED_coord_groups = []

    NEW_FRONT_veich_structure = np.zeros((rows+2, cols+2), dtype=int)
    NEW_BACK_veich_structure = np.empty((rows+2, cols+2), dtype=object)

    """Для ФРОНТОВОЇ таблиці Вейча"""

    # Сторони
    top_side = FRONT_veich_structure[0, :]          # Верхня сторона
    bottom_side = FRONT_veich_structure[-1, :]      # Нижня сторона
    left_side = FRONT_veich_structure[:, 0]         # Ліва сторона
    right_side = FRONT_veich_structure[:, -1]       # Права сторона

    # Кути (як 1x1 матриці для узгодженості)
    top_left_corner = np.array([[FRONT_veich_structure[0, 0]]])      # Верхній лівий
    top_right_corner = np.array([[FRONT_veich_structure[0, -1]]])    # Верхній правий
    bottom_left_corner = np.array([[FRONT_veich_structure[-1, 0]]])  # Нижній лівий
    bottom_right_corner = np.array([[FRONT_veich_structure[-1, -1]]]) # Нижній правий

    # Заповнюємо верхній рядок
    NEW_FRONT_veich_structure[0, 0] = bottom_right_corner[0, 0]
    NEW_FRONT_veich_structure[0, 1:cols+1] = bottom_side
    NEW_FRONT_veich_structure[0, cols+1] = bottom_left_corner[0, 0]

    # Заповнюємо середні рядки (1–4)
    NEW_FRONT_veich_structure[1:rows+1, 1:cols+1] = FRONT_veich_structure  # Центральна частина
    NEW_FRONT_veich_structure[1:rows+1, 0] = right_side  # Ліва сторона
    NEW_FRONT_veich_structure[1:rows+1, cols+1] = left_side  # Права сторона

    # Заповнюємо нижній рядок
    NEW_FRONT_veich_structure[rows+1, 0] = top_right_corner[0, 0]
    NEW_FRONT_veich_structure[rows+1, 1:cols+1] = top_side
    NEW_FRONT_veich_structure[rows+1, cols+1] = top_left_corner[0, 0]

    """Для ЗАДНЬОЇ таблиці Вейча"""

    # Сторони
    top_side = BACK_veich_structure[0, :]          # Верхня сторона
    bottom_side = BACK_veich_structure[-1, :]      # Нижня сторона
    left_side = BACK_veich_structure[:, 0]         # Ліва сторона
    right_side = BACK_veich_structure[:, -1]       # Права сторона

    # Кути (як 1x1 матриці для узгодженості)
    top_left_corner = np.array([[BACK_veich_structure[0, 0]]], dtype=object)      # Верхній лівий
    top_right_corner = np.array([[BACK_veich_structure[0, -1]]], dtype=object)    # Верхній правий
    bottom_left_corner = np.array([[BACK_veich_structure[-1, 0]]], dtype=object)  # Нижній лівий
    bottom_right_corner = np.array([[BACK_veich_structure[-1, -1]]], dtype=object) # Нижній правий

    if bool(WORK_minimized_term_list[0]) and WORK_minimized_term_list[0].count('X') == len(WORK_minimized_term_list[0]):

        min_x, min_y = 1, 1
        max_x, max_y = FRONT_veich_structure.shape

        group_config = (NEW_FRONT_veich_structure, {1: [[(min_x, min_y, max_x, max_y)], '#4169E1', '-']}, num_of_args, list_args)

    else:

        for group in initial_MAIN_coord_groups:

            updated_MAIN_coord_groups.append([])
            updated_EXTENDED_coord_groups.append([])

            for coord in group:

                updated_MAIN_coord_groups[-1].append((coord[0]+1, coord[1]+1))

                for new_coord in generate_add_coordinates(coord, rows, cols):

                    if new_coord not in del_one(type, FRONT_veich_structure, NEW_FRONT_veich_structure.shape):

                        updated_EXTENDED_coord_groups[-1].append(new_coord)

        for group_index, group in enumerate(updated_MAIN_coord_groups):

            result[group_index + 1] = []
            added_temp = []
            temp = []

            for main_coord in group:
                neighbors = find_all_neighbors(
                    updated_MAIN_coord_groups[group_index] + updated_EXTENDED_coord_groups[group_index],
                    main_coord
                )
                if neighbors in temp: continue
                temp.append(neighbors)

            for mini_group in temp:
                added_temp.append(find_min_max(mini_group))

            result[group_index + 1].append(added_temp)

            group_front_config = get_front_group_config(group_index)
            result[group_index + 1].extend(group_front_config)

        group_config = (NEW_FRONT_veich_structure, result, num_of_args, list_args)

    kmap, forming_groups, num_of_args, list_args = group_config
    if not list_args:

        for x in range(num_of_args, 0, -1): list_args.append(f"x_{x}")

    draw_kmap_with_tight_rounded_boxes(kmap, forming_groups, list_args, filename)