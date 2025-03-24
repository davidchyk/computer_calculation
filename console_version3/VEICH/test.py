# math matrix

import numpy as np

def define_matrix(coord):

    x, y = coord

    if x == 0 and y == 0:

        return "left_top_corner"

    elif x == 0 and y == K-1:

        return "right_top_corner"

    elif x == C-1 and y == 0:

        return "left_bottom_corner"

    elif x == C-1 and y == K-1:

        return "right_bottom_corner"

    elif x == 0:

        return "top_side_part"

    elif x == C-1:

        return "bottom_side_part"

    elif y == 0:

        return "left_side_part"

    elif y == K-1:

        return "right_side_part"

    return None

def generate_add_coordinates(start_coord, C, K):

    result_coords = []
    x, y = start_coord

    type_coord = define_matrix(start_coord)

    if type_coord == "left_top_corner":

        result_coords.append((x+C+1, y+1))
        result_coords.append((x+C+1, y+K+1))
        result_coords.append((x+1, y+K+1))

    elif type_coord == "right_top_corner":

        result_coords.append((x+C+1, y+1))
        result_coords.append((x+C+1, y-K+1))
        result_coords.append((x+1, y-K+1))

    elif type_coord == "left_bottom_corner":

        result_coords.append((x-C+1, y+1))
        result_coords.append((x-C+1, y+K+1))
        result_coords.append((x+1, y+K+1))

    elif type_coord == "right_bottom_corner":

        result_coords.append((x-C+1, y+1))
        result_coords.append((x-C+1, y-K+1))
        result_coords.append((x+1, y-K+1))

    elif type_coord == "top_side_part":

        result_coords.append((x+C+1, y+1))

    elif type_coord == "bottom_side_part":

        result_coords.append((x-C+1, y+1))

    elif type_coord == "left_side_part":

        result_coords.append((x+1, y+K+1))

    elif type_coord == "right_side_part":

        result_coords.append((x+1, y-K+1))

    return result_coords

# Початкова матриця 4x4
kmap = np.array([
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

rows, cols = kmap.shape
C, K = rows, cols

forming_groups = [[(1,1)]]
new_forming_groups = []
new_main_groups = []

# Сторони
top_side = kmap[0, :]          # Верхня сторона
bottom_side = kmap[-1, :]      # Нижня сторона
left_side = kmap[:, 0]         # Ліва сторона
right_side = kmap[:, -1]       # Права сторона

# Кути (як 1x1 матриці для узгодженості)
top_left_corner = np.array([[kmap[0, 0]]])      # Верхній лівий
top_right_corner = np.array([[kmap[0, -1]]])    # Верхній правий
bottom_left_corner = np.array([[kmap[-1, 0]]])  # Нижній лівий
bottom_right_corner = np.array([[kmap[-1, -1]]]) # Нижній правий

new_kmap = np.zeros((C+2, K+2), dtype=int)

# Заповнюємо верхній рядок
new_kmap[0, 0] = bottom_right_corner
new_kmap[0, 1:K+1] = bottom_side
new_kmap[0, K+1] = bottom_left_corner

# Заповнюємо середні рядки (1–4)
new_kmap[1:C+1, 1:K+1] = kmap  # Центральна частина
new_kmap[1:C+1, 0] = right_side  # Ліва сторона
new_kmap[1:C+1, K+1] = left_side  # Права сторона

# Заповнюємо нижній рядок
new_kmap[C+1, 0] = top_right_corner
new_kmap[C+1, 1:K+1] = top_side
new_kmap[C+1, K+1] = top_left_corner

for group in forming_groups:

    new_forming_groups.append([])

    for coord in group:

        for new_coord in generate_add_coordinates(coord, C, K):

            new_forming_groups[-1].append(new_coord)

for group in forming_groups:

    new_main_groups.append([])

    for coord in group:

        new_main_groups[-1].append((coord[0]+1, coord[1]+1))

print(kmap)
print(new_kmap)
print(new_forming_groups)
print(new_main_groups)