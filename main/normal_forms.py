class NormalForm:

    def __init__(self, structure, type, way):

        self.structure = structure
        self.type = type
        self.way = way

        self.in_sign = None
        self.out_sign = None
        self.in_not = None
        self.out_not = None

        self.reverse = None

    def define(self):

        if self.type == 1:

            if self.way == ('І', 'АБО'):

                self.in_sign = '∧'
                self.out_sign = '∨'
                self.in_not = False
                self.out_not = False

            elif self.way == ('І-НЕ', 'І-НЕ'):

                self.in_sign = '∧'
                self.out_sign = '∧'
                self.in_not = True
                self.out_not = True

            elif self.way == ('АБО', 'І-НЕ'):

                self.in_sign = '∨'
                self.out_sign = '∧'
                self.in_not = False
                self.out_not = True

                self.reverse = True

            elif self.way == ('АБО-НЕ', 'АБО'):
                
                self.in_sign = '∨'
                self.out_sign = '∨'
                self.in_not = True
                self.out_not = False

                self.reverse = True

        else:

            if self.way == ('АБО', 'І'):

                self.in_sign = '∨'
                self.out_sign = '∧'
                self.in_not = False
                self.out_not = False

            elif self.way == ('АБО-НЕ', 'АБО-НЕ'):

                self.in_sign = '∨'
                self.out_sign = '∨'
                self.in_not = True
                self.out_not = True

            elif self.way == ('І', 'АБО-НЕ'):

                self.in_sign = '∧'
                self.out_sign = '∨'
                self.in_not = False
                self.out_not = True

                self.reverse = True

            elif self.way == ('І-НЕ', 'І'):

                self.in_sign = '∧'
                self.out_sign = '∧'
                self.in_not = True
                self.out_not = False

                self.reverse = True

        if self.reverse:

            new_structure = []

            for term in self.structure:

                term = term.replace("1", "_")
                term = term.replace("0", "1")
                term = term.replace("_", "0")

                new_structure.append(term)

            self.structure = new_structure

    def __str__(self):

        str_form = ""

        for set in self.structure:

            term_str = ""

            for e in set: term_str += f"{e} {self.in_sign} "

            term_str = term_str.rstrip(f" {self.in_sign} ")
            term_str = f"({term_str})"
            if self.in_not: term_str = f"not{term_str}"
            str_form += f"{term_str} {self.out_sign} "

        str_form = str_form.rstrip(f" {self.out_sign} ")
        if self.out_not: str_form = f"not({str_form})"

        return str_form

def basic(sets_number, type, num_of_args):

    db = []
    result = ""

    if type == 1:

        for set in sets_number: db.append(format(int(set), f'0{num_of_args}b'))

        for set in db:

            new_set = ""

            for e in set: new_set += f"{e} ∧ "
    
            new_set = new_set.rstrip(' ∧ ')
            result += f"({new_set}) ∨ "

        result = result.rstrip(' ∨ ')

    else:

        time_db = []

        sets_number_new = [x for x in range(2**num_of_args) if x not in sets_number]
        for set in sets_number_new: time_db.append(format(int(set), f'0{num_of_args}b'))

        for set in time_db:

            set = set.replace("1", "_")
            set = set.replace("0", "1")
            set = set.replace("_", "0")

            db.append(set)

        for set in db:

            new_set = ""

            for e in set: new_set += f"{e} ∨ "

            new_set = new_set.rstrip(' ∨ ')
            result += f"({new_set}) ∧ "

        result = result.rstrip(' ∧ ')

    return (result, type, db)

def normal(sets_number, type_of, num_of_args, basis, mini):

    output = []

    if mini:

        normal_form = NormalForm(sets_number, type_of, basis)
        normal_form.define()

    else:

        output.append(f"{basic(sets_number, 1, int(num_of_args))[0]}") #ДДНФ
        output.append(f"{basic(sets_number, 0, int(num_of_args))[0]}") #ДКНФ

        basic_result = basic(sets_number, type_of, int(num_of_args))

        normal_form = NormalForm(basic_result[2], type_of, basis)
        normal_form.define()

        output.append(f"{normal_form}")

    return output, normal_form