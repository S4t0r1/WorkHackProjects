
import sys
from itertools import permutations


def getInputs(all_data=None, dataType=None, msg=''):
    inType, inData = dataType, ''
    all_ins = [] if not all_data else all_data
    print("\n\n{} \nb = step back \nd*N = delete \npress ENTER to cancel".format(msg))
    while True:
        if inType not in {'ma', 'fa'}:
            inType = input('\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): ")
            if len(inType) == 0:
                break
            if inType not in {'m', 'ma', 'f', 'fa', 'b', 'd'*len(inType)}:
                return getInputs(all_ins)
        if 'd' not in inType:
            inData = input("Paste dataset: ") if inType in {'m', 'ma'} else input("Fname: ")
            if len(inData) == 0:
                break
        if 'b' in inData + inType:
            return getInputs(all_ins)
        for inpt in (inType, inData):
            if inpt.count('d') == len(inpt):
                for n in range(len(inpt)):
                    del all_ins[-1]
                return getInputs(all_ins, inType, "\ndeleted {} dataset{}".
                          format(len(inpt), '' if len(inpt) == 1 else 's'))
        if inType in {'f', 'fa'}:
            with open(inData, 'r', encoding='utf8') as fi:
                inData = fi.readlines() if input("Table(t)?: ") == 't' else fi.read()
        all_ins.append(inData)
    if len(all_ins) == 0:
        process = getInputs() if input("No data, RE?: ").lower() == "y" else sys.exit()
    return all_ins


class Datas:  

    def __init__(self, all_data=getInputs()):
        self.all_ins = all_data
        self.data_Nsets = len(self.all_ins)
    
    def printAll(self):
        print("\n\nall data\n{}\n\nnumber of datasets\n{}\n".
                      format(self.all_ins, self.data_Nsets))

x = Datas()
x.printAll()
