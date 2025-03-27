# math matrix

import numpy as np

def differ(s1: str, s2: str) -> bool:

    """
    Повертає True, якщо s1 і s2 не відрізняються (ідентичні)
    або відрізняються рівно на 1 символ; інакше False.
    """

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

def forming_paint_dict():

    result = dict()

    def define_matrix(coord, K, C):

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
    Afront_kmap = np.array([
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ])

    back_kmap = np.array([

        ["1100", "1101", "1001", "1000"],
        ["1110", "1111", "1011", "1010"],
        ["0110", "0111", "0011", "0010"],
        ["0100", "0101", "0001", "0000"]

    ], dtype=object)

    rows, cols = Afront_kmap.shape
    C, K = rows, cols

    forming_groups = [[(0,1), (3, 1)]]
    new_forming_groups = []
    new_main_groups = []

    """Для ФРОНТОВОЇ таблиці Вейча"""

    # Сторони
    top_side = Afront_kmap[0, :]          # Верхня сторона
    bottom_side = Afront_kmap[-1, :]      # Нижня сторона
    left_side = Afront_kmap[:, 0]         # Ліва сторона
    right_side = Afront_kmap[:, -1]       # Права сторона

    # Кути (як 1x1 матриці для узгодженості)
    top_left_corner = np.array([[Afront_kmap[0, 0]]])      # Верхній лівий
    top_right_corner = np.array([[Afront_kmap[0, -1]]])    # Верхній правий
    bottom_left_corner = np.array([[Afront_kmap[-1, 0]]])  # Нижній лівий
    bottom_right_corner = np.array([[Afront_kmap[-1, -1]]]) # Нижній правий

    new_front_kmap = np.zeros((C+2, K+2), dtype=int)

    # Заповнюємо верхній рядок
    new_front_kmap[0, 0] = bottom_right_corner
    new_front_kmap[0, 1:K+1] = bottom_side
    new_front_kmap[0, K+1] = bottom_left_corner

    # Заповнюємо середні рядки (1–4)
    new_front_kmap[1:C+1, 1:K+1] = Afront_kmap  # Центральна частина
    new_front_kmap[1:C+1, 0] = right_side  # Ліва сторона
    new_front_kmap[1:C+1, K+1] = left_side  # Права сторона

    # Заповнюємо нижній рядок
    new_front_kmap[C+1, 0] = top_right_corner
    new_front_kmap[C+1, 1:K+1] = top_side
    new_front_kmap[C+1, K+1] = top_left_corner

    """Для ЗАДНЬОЇ таблиці Вейча"""

    # Сторони
    top_side = back_kmap[0, :]          # Верхня сторона
    bottom_side = back_kmap[-1, :]      # Нижня сторона
    left_side = back_kmap[:, 0]         # Ліва сторона
    right_side = back_kmap[:, -1]       # Права сторона

    # Кути (як 1x1 матриці для узгодженості)
    top_left_corner = np.array([[back_kmap[0, 0]]], dtype=object)      # Верхній лівий
    top_right_corner = np.array([[back_kmap[0, -1]]], dtype=object)    # Верхній правий
    bottom_left_corner = np.array([[back_kmap[-1, 0]]], dtype=object)  # Нижній лівий
    bottom_right_corner = np.array([[back_kmap[-1, -1]]], dtype=object) # Нижній правий

    new_back_kmap = np.empty((C+2, K+2), dtype=object)

    # Заповнюємо верхній рядок
    new_back_kmap[0, 0] = bottom_right_corner[0, 0]
    new_back_kmap[0, 1:K+1] = bottom_side
    new_back_kmap[0, K+1] = bottom_left_corner[0, 0]

    # Заповнюємо середні рядки (1–4)
    new_back_kmap[1:C+1, 1:K+1] = back_kmap  # Центральна частина
    new_back_kmap[1:C+1, 0] = right_side  # Ліва сторона
    new_back_kmap[1:C+1, K+1] = left_side  # Права сторона

    # Заповнюємо нижній рядок
    new_back_kmap[C+1, 0] = top_right_corner[0, 0]
    new_back_kmap[C+1, 1:K+1] = top_side
    new_back_kmap[C+1, K+1] = top_left_corner[0, 0]

    for group in forming_groups:

        new_forming_groups.append([])

        for coord in group:

            for new_coord in generate_add_coordinates(coord, C, K):

                new_forming_groups[-1].append(new_coord)

    for group in forming_groups:

        new_main_groups.append([])

        for coord in group:

            new_main_groups[-1].append((coord[0]+1, coord[1]+1))

    print(Afront_kmap)
    print(new_front_kmap)

    print(back_kmap)
    print("\n")
    print(new_back_kmap)

    print(new_forming_groups)
    print(new_main_groups)

    num_count_of_groups = 0

    for group in new_main_groups:

        result[num_count_of_groups+1] = []
        temp = []
        added_temp = []

        for main_coord in group:

            neighbors = find_all_neighbors(new_main_groups + new_forming_groups, main_coord)
            if neighbors in temp: continue

            temp.append(neighbors)

        for mini_group in temp:

            added_temp.append(find_min_max(mini_group))

        result[num_count_of_groups+1].append(added_temp)

        color_index = group_index % num_colors




        



            







if __name__ == "__main__":

    forming_paint_dict()