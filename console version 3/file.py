number = 10
bits = 4

bit_string = ', '.join(list(format(number, f'0{bits}b')))

print(bit_string)