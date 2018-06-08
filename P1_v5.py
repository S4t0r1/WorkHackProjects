
import sys


class BadInputError(Exception): pass

class Tools():
    def inpt_node_args(self):
        return {k: None for k in "inType;table;inData".split(';')}
    
    def getCommandSet(self, s, char, p=False):
        return set(','.join(c1+c2 if p else ','.join((c1, c1+c2)) 
                   for c1, c2 in zip(s, char*len(s))).split(','))
    
    def anySetter(self, cond1=None, cond2=None, seq=None):
        if not cond2:
            return any(len(txt) == cond1 if type(cond1) == int
                  else len(txt) == txt.count(cond1) if len(cond1) == 1 
                  else len(txt) in {txt.count(ch) for ch in cond1 if len(txt) >= 1} for txt in seq)
        else:
            return any(len(txt) == cond1
                or len(txt) in {txt.count(ch) for ch in cond2 if len(txt) >= 1} for txt in seq)

    def inputChecker(self, msg, seq=None, filtr=None):
        inpt = input(msg)
        forbidden_or_allowed = {c for c in "bde"} | {'da'}
        if not seq:
            if self.anySetter("bde", seq=[inpt]) or inpt == 'da':
                return inpt, len(inpt)
        else:
            seq = seq | forbidden_or_allowed
            if inpt not in list(seq):
                print("\nERROR: Bad Input!")
                return self.inputChecker(msg, seq)
        return inpt


class InputNode(Tools):
    def __init__(self, inType=None, table=None, inData=None):
        Tools.__init__(self)
        self.inType = inType
        self.table = table
        self.inData = inData

    def getInType(self):
        if self.inType not in self.getCommandSet("mf", 'a', p=True):
            msg = '\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): "
            self.inType = self.inputChecker(msg=msg, seq=self.getCommandSet("mf", 'a'))
        return self.inType
    
    def getTable(self):
        if self.table not in self.getCommandSet("tn", 'a', p=True):
            msg = "Table?(t, ta): "
            self.table = self.inputChecker(msg=msg, seq=self.getCommandSet("tn", 'a'))
        return self.table
    
    def getInData(self, cnum):
        msg = ("Paste Dataset: " if self.inType in self.getCommandSet("m", 'a') 
               else "Filename: ")
        self.inData = self.inputChecker(msg=msg)
        return self.file_mngr(count=cnum) if len(list(self.inData)) == 1 else self.inData
    
    def file_mngr(self, count=None, filename=None):
        if any(self.table == c for c in self.getCommandSet('tf', 'a')):
            try:
                filename = self.inData if not filename else filename
                with open(filename, 'r', encoding='utf8') as fi:
                    self.inData = (fi.readlines() if self.table in self.getCommandSet('t', 'a') 
                                   else fi.read())
            except (FileNotFoundError, OSError):
                filename = "g_file"+str(count+1)+".txt"
                with open(filename, 'w', encoding='utf8') as fi:
                    fi = fi.write(self.inData)
            else:   
                return self.inData
        return self.inData 


class Data(InputNode):   
    def __init__(self, name=None):
        InputNode.__init__(self)
        self.name = name
        self.commands = Tools.getCommandSet(self, "mftda", 'a')
        self.all_data = []
        self.actionsD = {}
        self.count = 0
    
    def print_allData(self):
        return "\n{}\n{}".format(self.name, self.all_data)         
    
    def back_startmenu(self, inpt):
        self.actionsD[inpt] = InputNode.__init__(self), self.getInputs()
        return self.actionsD[inpt]
    
    def exit_adding(self, inpt):
        self.actionsD[inpt] = "ext"
        return "ext"

    def addData(self, newdata):
        self.all_data.append(newdata)
        print("\n{}\n{}\ndatapackage{} = {}".format(self.name, self.all_data, 
                  's' if len(self.all_data) > 1 else '', len(self.all_data)))
    
    def dellData(self, inpt, count):
        self.actionsD[inpt] = self.all_data[:-count]
        self.all_data = self.actionsD[inpt]
        print("..deleted {} datablocks\n{}".format(count, self.print_allData()))

    def del_allData(self, inpt, count):
        self.actionsD[inpt] = self.all_data.clear()
        print("..deleted all inputs({})\n{}".format(count, self.print_allData()))
    
    def getOperation(self, inpt, count):
        return (self.back_startmenu(inpt) if 'b' in inpt
           else self.del_allData(inpt, count) if 'da' == inpt
           else self.dellData(inpt, count) if 'd' in inpt
           else self.exit_adding(inpt))

    def getInputs(self):
        exit_datarealm = None
        while not exit_datarealm:
            print(self.actionsD)
            for inpt in (self.getInType(), self.getTable(), self.getInData(self.count)):
                if type(inpt) == tuple:
                    inpt, count = inpt
                    operation = self.getOperation(inpt, count)
                    exit_datarealm = operation if operation == 'ext' else exit_datarealm
                    self.actionsD.get(inpt, operation)
                    break
            else:
                self.addData(inpt)
        return self.all_data

d = Data("TEST 99999")
datarealm = d.getInputs()
