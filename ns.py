
def graph_func(peak_name, amount_of_peaks):
    state_coding = {}
    order_of_codes = []
    print("Введіть кодування вершин")
    for i in range(amount_of_peaks):
        print(f"Кодування вершини {peak_name}[{i}]:")
        state_coding[peak_name+str(i)] = input()
    print("Запишіть як поєднанні вершини. Формат 000>001>010>011")
    temp  = input().replace(">", "  >  ")
    order_of_codes = temp.split(" ")
    print(f"Порядок кодування вершин{order_of_codes}")
    temp = temp.replace(">", "")
    temp = temp.replace(" ", "")
    order_of_codes = temp.split(" ")
    print(f"Порядок кодування вершин{order_of_codes}")
    indecies = []
    for i in amount_of_peaks:
        temp = state_coding.get(peak_name + str(i))
         for j in range(order_of_codes):
             if temp == order_of_codes:
                 indecies.append(i)
    print(f"indecies: {indecies}")





if __name__ == '__main__':
    graph_func("Z",3)
