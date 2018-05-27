
import sys


def getInputs(all_data=None):
    inType, inData = None, None
    all_ins = [] if not all_data else all_data
    print("{}'b' = step back, press ENTER to cancel".format('\n'*2))
    while True:
        if inType not in {'ma', 'fa'}:
            inType = input('\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): ")
            if len(inType) > 0:
                if inType not in {'m', 'ma', 'f', 'fa'}:
                    return getInputs(all_data=all_ins)
            else:
                break
        inData = input("Paste dataset: ") if inType in {'m', 'ma'} else input("Fname: ")
        if len(inData) == 0:
            break
        if 'b' in inData+inType:
            return getInputs(all_data=all_ins)
        else:
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
