
def graph_func(peak_name, amount_of_peaks):
    state_coding = {}
    order_of_codes = []
    indecies = {}
    print("Введіть кодування вершин")
    for i in range(amount_of_peaks):
        print(f"Кодування вершини {peak_name}[{i}]:")
        state_coding[peak_name+str(i)] = input()
    print(state_coding)
    print("Запишіть як поєднанні вершини. Формат 000>001>010>011")
    temp  = input().replace(">", "  >  ")
    order_of_codes = temp.split(" ")
    print(f"Порядок кодування вершин{order_of_codes}")
    temp = temp.replace(">", "")
    temp = temp.replace(" ", "")
    for i in range(enumerate(order_of_codes)):
        indecies[order_of_codes].update(state_coding[order_of_codes[i]])
    
    
    print(f"indecies: {indecies}")





if __name__ == '__main__':
    graph_func("Z",3)
