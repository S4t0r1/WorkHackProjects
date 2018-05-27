import sys


def getInputs(all_data=None):
    inType, inData = None, None
    all_ins = [] if not all_data else all_data
    print("'b' = step back, press ENTER to cancel")
    while True:
        if inType not in {'ma', 'fa'}:
            inType = input('\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): ")
            if inType and inType not in {'m', 'ma', 'f', 'fa'}:
                print('\n'*2)
                return getInputs(all_data=all_ins)
        if len(inType) == 0:
            break
        inData = input("Paste dataset: ") if inType in {'m', 'ma'} else input("Fname: ")
        if 'b' in inData+inType:
            print('\n'*2)
            return getInputs(all_data=all_ins)
        if len(inData) == 0:
            break
        else:
            if inType in {'f', 'fa'}:
                with open(inData, 'r', encoding='utf8') as fi:
                    inData = fi.readlines() if input("Table(t)?: ") == 't' else fi.read()
            all_ins.append(inData)
    print(all_ins)
    if len(all_ins) == 0:
        process = getInputs() if input("No data, RE?: ").lower() == "y" else sys.exit()
    return all_ins


class Datas:  

    def __init__(self, all_data=getInputs()):
        self.all_ins = all_data
        self.data_Nsets = len(self.all_ins)

x = Datas()
