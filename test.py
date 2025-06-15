import numpy as np

BACK_veich_structure = [
                [12, 13,  9,  8],
                [14, 15, 11, 10],
                [ 6,  7,  3,  2],
                [ 4,  5,  1,  0]
            ]

num_of_args = 4

BACK_veich_structure = np.array([[format(n, f'0{num_of_args}b') for n in row] for row in BACK_veich_structure], dtype=str)

print(BACK_veich_structure)