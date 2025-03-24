# math matrix

import numpy as np

def generate_add_coordinates(start_coord, C):
    x, y = start_coord  # Розпаковуємо початкову координату
    coords = []
    
    # Проходимо по 3 можливим значенням для x: 0, C, 2C
    for i in range(3):
        new_x = x + i * C
        # Проходимо по 3 можливим значенням для y: 1, 1+C, 1+2C
        for j in range(3):
            new_y = y + j * C
            coords.append((new_x, new_y))
    
    return coords

# Початкова матриця 4x4
kmap = np.array([
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 0]
])

forming_groups = [[(0, 1), (3, 1)]]
new_forming_groups = []
new_main_groups = []

rows, cols = kmap.shape
print(rows, cols)

C = 4
K = 4

new_kmap = np.zeros((rows*3, cols*3), dtype=int)

for row in range(rows*3):

    row_row = row % rows

    for col in range(cols*3):

        col_col = col % cols
        new_kmap[row, col] = kmap[row_row, col_col]

for group in forming_groups:

    new_forming_groups.append([])

    for coord in group:

        for new_coord in generate_add_coordinates(coord, C):

            new_forming_groups[-1].append(new_coord)

for group in forming_groups:

    new_main_groups.append([])

    for coord in group:

        new_main_groups[-1].append((coord[0]+C, coord[1]+K))

print(kmap)
print(new_kmap)
print(new_forming_groups)
print(new_main_groups)