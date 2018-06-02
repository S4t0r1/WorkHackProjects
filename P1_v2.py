
import sys

class BadInputError(Exception): pass

def getCommandSet(s, char, p=False):
    return set(','.join(c1+c2 if p else ','.join((c1, c1+c2)) 
               for c1, c2 in zip(s, char*len(s))).split(','))

commandsSet = getCommandSet("mftd", 'a')

def anySetter(*conditions, seq=None):
    return any((len(txt) == conditions[0] if type(conditions[0]) == int 
           else len(txt) == txt.count(conditions[0])) if len(conditions) == 1 
           else len(txt) in {txt.count(ch) for ch in conditions[1]} for txt in seq)

def inputChecker(msg):
    allcommandsSet = commandsSet
    inpt = input(msg)
    if len(inpt) in {inpt.count(c) for c in "bde"}:
        allcommandsSet = allcommandsSet | {c*len(inpt) for c in "bde"}
    return inpt if inpt in allcommandsSet else inputChecker("\nERROR: Bad Input!\n{}".format(msg))

def getInputs(all_data=None, inType=None, table=None, inData=None, msg=''):
    all_ins = [] if not all_data else all_data
    if len(all_ins) == 0 or inData == 'del':
        print("\n\n{} \nb = step back \nd*N = delete \npress ENTER to cancel".format(msg))
    while True:
        if not inType:
            inType = inputChecker('\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): ")
        avalSettings = [d for d in (inType, table, inData) if d != None]
        if anySetter(0, "de", seq=avalSettings):
            break
        if anySetter('b', seq=avalSettings):
            return getInputs(all_ins, None)
        ((all_ins if any(inData==c for c in (None, 'del')) else all_ins.append(inData)) 
                   if avalSettings[-1] != 'da' else print("0 INPUTS", all_ins.clear()))
        print(all_ins)
        if table in getCommandSet('t', 'a'):
            table = None if table == 't' else table
            inData = input("Paste Dataset: " if inType in {'m', 'ma'} else "Fname: ")
            inType = None if inType not in getCommandSet("mf", 'a', p=True) else inType
            return getInputs(all_ins, inType, table, inData)
        else:
            return getInputs(all_ins, inType, inputChecker("Table?(t, ta): "))
        
        if inType in {'f', 'fa'}:
            with open(inData, 'r', encoding='utf8') as fi:
                inData = fi.readlines() if input("Table(t)?: ") == 't' else fi.read()
    if len(all_ins) == 0 or any(len(d)==d.count('e') for d in avalSettings if len(d)>0):
        process = getInputs(all_ins) if input("No data, exit?: " if avalSettings[-1] != 'e' 
                                         else "Exit?: ").lower() != "y" else sys.exit()
    for inpt in avalSettings:
        if len(inpt) > 0 and inpt.count('d') == len(inpt):
            for n in range(len(inpt)):
                del all_ins[-1]
            return getInputs(all_ins, inType, table, 'del', "\ndeleted {} dataset{}".format(
                                                  len(inpt), '' if len(inpt) == 1 else 's'))
    if anySetter(0, seq=avalSettings):
        return all_ins


class Datas:  

    def __init__(self, all_data=getInputs()):
        self.all_ins = all_data
        self.data_Nsets = len(self.all_ins)
    
    def printAll(self):
        print("\n\nall data\n{}\n\nnumber of datasets\n{}\n".
                      format(self.all_ins, self.data_Nsets))
    
    def compareDatasets(self):
        for dataset in self.all_ins:
            print(dataset)
            print(len(dataset))

x = Datas()
x.printAll()
x.compareDatasets()
