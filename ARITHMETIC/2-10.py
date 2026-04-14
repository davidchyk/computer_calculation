BCD_8421 = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100',
    '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001'
}

def bin2dec(bcd_str):

    result = 0

    sign_bit = int(bcd_str[0])
    operating_bcd_str = bcd_str[2:]
    operating_bcd_str = operating_bcd_str.replace(' ', '')

    for i in range(0, len(operating_bcd_str)):

        if operating_bcd_str[-i-1] == "1": result += 2 ** i

    return result if sign_bit == 0 else -result

def dec2bin(n):
    binary = bin(n)[2:]  # Переводимо в двійковий, без '0b'
    
    # Доповнюємо провідними нулями до кратності 4
    while len(binary) % 4 != 0:
        binary = '0' + binary
    
    # Розбиваємо на групи по 4 біти
    grouped = ' '.join(binary[i:i+4] for i in range(0, len(binary), 4))
    return grouped

def to_bcd8421(n, coding_table):

    is_negative = n < 0
    digits = str(abs(n))

    if is_negative:

        digits_vector = [abs(9 - int(d)) for d in digits]
        number = int(''.join(str(d) for d in digits_vector)) + 1

        digits = str(number)

    bcd_raw = ''.join(coding_table[d] for d in digits)
    
    # Розбити на тетради по 4 біти
    bcd_grouped = ' '.join(bcd_raw[i:i+4] for i in range(0, len(bcd_raw), 4))
    
    sign_bit = '1' if is_negative else '0'
    return f"{sign_bit}.{bcd_grouped}"

def summing(a, b):

    def pretty_binary_addition(x_str, y_str, result_str):
        # Довжина для вирівнювання
        max_len = max(len(x_str), len(y_str), len(result_str))
        
        # Додаємо пропуски зліва для вирівнювання
        x_line = x_str.rjust(max_len)
        y_line = y_str.rjust(max_len)
        r_line = result_str.rjust(max_len)

        # Вивід
        print("  " + x_line)
        print("+ " + y_line)
        print("-" * (max_len + 2))
        print("  " + r_line)

    dec_a = bin2dec(a)
    dec_b = bin2dec(b)

    abs_dec_c = abs(dec_a) + abs(dec_b)

    sign_c = 0 if dec_a + dec_b >= 0 else 1

    c = f"{sign_c}.{dec2bin(abs_dec_c)}"

    print("\n\n")

    pretty_binary_addition(a, b, c)

    return f"\n\n{c}"

print(bin2dec("1.0101 1000 1001 0100"))
print(bin2dec("1.0011 1001 1000 0110"))


# Приклад виклику:
X_number = int(input("Enter X: "))
Y_number = int(input("Enter Y: "))
operation = input("Enter operation: ")

if operation == "+":

    C = X_number + Y_number

elif operation == "-":

    C = X_number - Y_number

print("Formats: 8421, 8421+delta")

format = input("Enter format: ")

if format == "8421":

    coding_table = BCD_8421.copy()
    correction_value = 6

elif format == "8421+delta":

    delta = int(input("Enter delta: "))
    BCD_8421_delta = {}

    for key, value in BCD_8421.items():
        # Додаємо delta до значення
        new_value = bin(int(value, 2) + delta)[2:]

        # Доповнюємо до 4 біт
        while len(new_value) < 4: new_value = '0' + new_value

        BCD_8421_delta[key] = new_value

    coding_table = BCD_8421_delta.copy()

    correction_value = 13

if __name__ == "__main__":

    new_X_number = to_bcd8421(X_number, coding_table)
    new_Y_number = to_bcd8421(Y_number, coding_table)

    print(f"Number X: {new_X_number}")
    print(f"Number Y: {new_Y_number}")

    x = summing(new_X_number, new_Y_number)
    print(f"df: {x}")

    print(f"bin2dec: {bin2dec("0.1001 1000 1001 1010")}")
    print(f"Absulute correct value of C: {to_bcd8421(C, coding_table)}, C = {C}")