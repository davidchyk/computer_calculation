import numpy as np
from creating_diagram import process

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

term_list = ['01X', '0X1', '100']
term_list = ['10', '01']

num_of_args = len(term_list[0])

sets_number = [1, 2]
bin_sets = []

for set in sets_number: bin_sets.append(format(int(set), f'0{num_of_args}b'))

if num_of_args == 4:

    veich_structure = np.zeros((4, 4), dtype=int)
    back_veich_structure = [

        ["1100", "1101", "1001", "1000"],
        ["1110", "1111", "1011", "1010"],
        ["0110", "0111", "0011", "0010"],
        ["0100", "0101", "0001", "0000"]

    ]

elif num_of_args == 3:

    veich_structure = np.zeros((2, 4), dtype=int)

    back_veich_structure = [

        ["110", "111", "101", "100"],
        ["010", "011", "001", "000"]

    ]

elif num_of_args == 2:

    veich_structure = np.zeros((2, 2), dtype=int)

    back_veich_structure = [

        ["11", "10"],
        ["01", "00"]

    ]

elif num_of_args == 1:

    veich_structure = np.zeros((2, 1), dtype=int)
    back_veich_structure = [

        ["1"],
        ["0"]

    ]

else:

    ...

back_veich_structure = np.array(back_veich_structure, dtype=str)
forming_groups = []

for num in bin_sets:

    row_indices, col_indices = np.where(back_veich_structure == num)
    row = row_indices[0]
    col = col_indices[0]
    veich_structure[row, col] = 1

for term in term_list:

    group = []

    for idx, val in np.ndenumerate(back_veich_structure):
        
        val = str(val)
        if differ(term, val): group.append((idx[0], idx[1]))

    forming_groups.append(group)

print(f"veich_structure:\n{veich_structure}")
print(f"forming_groups:\n{forming_groups}")

process(veich_structure, forming_groups)