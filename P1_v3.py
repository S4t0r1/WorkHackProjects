
import sys

class BadInputError(Exception): pass

def getCommandSet(s, char, p=False):
    return set(','.join(c1+c2 if p else ','.join((c1, c1+c2)) 
               for c1, c2 in zip(s, char*len(s))).split(','))

commandsSet = getCommandSet("mftd", 'a')

def anySetter(*conds, seq=None):
    return any((len(txt) == conds[0] if type(conds[0]) == int 
           else len(txt) == txt.count(conds[0])) if len(conds) == 1 
           else len(txt) in {txt.count(ch) for ch in conds[1]} for txt in seq)

def inputChecker(msg, seq=commandsSet):
    inpt = input(msg)
    if len(inpt) in {inpt.count(c) for c in "bde"}:
        seq = seq | {c*len(inpt) for c in "bde"}
    if inpt not in seq:
        print("\nERROR: Bad Input!")
        return inputChecker(msg, seq)
    return inpt 

def getInputs(*args):
    all_data, inType, table, inData, msg, num, lastIn = args
    all_ins = [] if not all_data else all_data
    if len(all_ins) == 0 or any(d in {'del', 'b'} for d in (inType, table, inData)):
        print("\n\n{} \nb = step back \nd*N = delete \npress ENTER to cancel".format(msg))
    while True:
        if not inType:
            inType = inputChecker('\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): ")
            lastIn = inType
            
        avalSettings = [d for d in (inType, table, inData) if d is not None]
        if anySetter(0, "de", seq=avalSettings):
            num -= 1
            break
        if anySetter('b', seq=avalSettings):
            return getInputs(all_ins, None, None, None, '', num-1, None)
        
        ((all_ins if any(inData==c for c in (None, 'del')) else all_ins.append(inData)) 
                   if avalSettings[-1] != 'da' else print("0 INPUTS", all_ins.clear()))
        print(all_ins, num)
       
        if table in getCommandSet('tx', 'a'):
            table = None if table in "tx" else table
            inData = input("Paste Dataset: " if inType in {'m', 'ma'} else "Fname: ")
            inType = None if inType not in getCommandSet("mf", 'a', p=True) else inType
            return getInputs(all_ins, inType, table, inData, msg, num+1, inData)
        else:
            table = inputChecker("Table?(t, ta): ", seq=getCommandSet('tx', 'a'))
            return getInputs(all_ins, inType, table if len(table) > 0 else 'x', None, '', num, table)
        
        if inType in {'f', 'fa'}:
            with open(inData, 'r', encoding='utf8') as fi:
                inData = fi.readlines() if input("Table(t)?: ") == 't' else fi.read()

    if len(all_ins) == 0 or any(len(d)==d.count('e') for d in avalSettings if len(d)>0):
        num = 0 if len(all_ins) == 0 else num
        getInputs(all_ins, None, None, None, '', num, lastIn) if input("No data, exit?: " 
                          if lastIn != 'e' else "Exit?: ").lower() != "y" else sys.exit()
    
    if len(lastIn) > 0 and lastIn.count('d') == len(lastIn):
        n = len(lastIn) if len(lastIn) <= len(all_ins) else len(all_ins)
        i = 0
        while i < n:
            del all_ins[-1]
            i += 1
        return getInputs(all_ins, inType, table, 'del', "\ndeleted {} dataset{}".format(
                                               n, '' if n == 1 else 's'), num-n, lastIn)
    if len(lastIn) == 0:
        return all_ins


class Datas:  

    def __init__(self, all_data=getInputs(*[None for i in range(5)], 0, None)):
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
