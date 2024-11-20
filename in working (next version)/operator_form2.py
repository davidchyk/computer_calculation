def group_elements(data, m):

    def group_once(lst, m):

        if len(lst) <= m:
            
            return lst

        else:

            grouped = [lst[i:i + m] for i in range(0, len(lst), m)]

            return [group[0] if len(group) == 1 else group for group in grouped]

    grouped = group_once(data, m)

    while len(grouped) > m:grouped = group_once(grouped, m)

    return grouped

def union(lst, way, begin, in_not, out_not):

    if in_not and begin:

        term = str(lst)

        term = term[1:]
        term = term[:-1]
        term = f"not({term})"

        term = term.replace("'", "")
        term = term.replace("]", "))")

        term = term.replace("[", "not(not(")

        if way[0] in ["АБО", "АБО-НЕ"]: term = term.replace(",", " ∨")
        elif way[0] in ["І", "І-НЕ"]: term = term.replace(",", " ∧")

        return term
    
    elif out_not and not(begin):

        term = str(lst)

        term = term[1:]
        term = term[:-1]
        term = f"not({term})"

        term = term.replace("'", "")
        term = term.replace("]", "))")

        term = term.replace("[", "not(not(")

        if way[1] in ["АБО", "АБО-НЕ"]: term = term.replace(",", " ∨")
        elif way[1] in ["І", "І-НЕ"]: term = term.replace(",", " ∧")

        return term

    else:

        term = str(lst)

        term = term.replace("[", "(")
        term = term.replace("]", ")")

        term = term.replace("'", "")

        if begin:

            if way[0] == "АБО": term = term.replace(",", " ∨")
            elif way[0] == "І": term = term.replace(",", " ∧")

            return term

        else:

            if way[1] == "АБО": term = term.replace(",", " ∨")
            elif way[1] == "І": term = term.replace(",", " ∧")

            return term[1:len(term)-1]

def operator_form(class_structure, in_num, out_num):

    groups = []
    result_groups = []

    for term in class_structure.structure: groups.append(group_elements([x for x in term], in_num))

    for term in groups: result_groups.append(union(term, class_structure.way, True, class_structure.in_not, class_structure.out_not))

    result = union(group_elements(result_groups, out_num), class_structure.way, False, class_structure.in_not, class_structure.out_not)

    return result