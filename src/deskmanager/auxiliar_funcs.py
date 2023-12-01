class AuxiliarFunctions():
    def __init__(self):
        pass

    def adjust_sufix(self, sufix):
        if len(sufix) == 5:
            new_sufix = "0" + sufix
        elif len(sufix) == 4:
            new_sufix = "00" + sufix
        elif len(sufix) == 3:
            new_sufix = "000" + sufix
        elif len(sufix) == 2:
            new_sufix = "0000" + sufix
        elif len(sufix) == 1:
            new_sufix = "00000" + sufix
        else:
            new_sufix = "000000"
        return new_sufix
