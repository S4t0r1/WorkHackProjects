import sys



class BadInputError(Exception): pass
class Tools():
    def inpt_node_args(self):
        return {k: None for k in "inType;table;inData;lastIn"}
    
    def getCommandSet(self, s, char, p=False):
        return set(','.join(c1+c2 if p else ','.join((c1, c1+c2)) 
                   for c1, c2 in zip(s, char*len(s))).split(','))
    
    def anySetter(self, *conds, seq=None):
        if len(conds) == 1:
            return any(len(txt) == conds[0] if type(conds[0]) == int
                  else len(txt) == txt.count(conds[0]) for txt in seq)
        return any(len(txt) == conds[0] 
                or len(txt) in {txt.count(ch) for ch in conds[1]} for txt in seq)

    def inputChecker(self, msg, seq=None, anyfiltr=None):
        inpt = input(msg)
        if not seq:
            return '' if anyfiltr else inpt
        if len(inpt) in {inpt.count(c) for c in "bde"}:
            seq = seq | {c*len(inpt) for c in "bde"}
        if inpt not in list(seq):
            print("\nERROR: Bad Input!")
            return self.inputChecker(msg, seq)
        return inpt


class InputNode(Tools):
    def __init__(self):
        inpt_specs = Tools.inpt_node_args(self)
        self.__dict__.update({k: None for k in inpt_specs})

    def inType(self):
        return self.inType
    
    def table(self):
        return self.table
    
    def inData(self):
        return self.inData

    def lastIn(self):
        return self.lastIn


class InputOps(InputNode, Tools):   
    def __init__(self, tools, data):
        tools.__init__()
        InputNode.__init__(self)
        self.tools = tools
        self.data = data
    
    def getInType(self):
        tools = self.tools
        if self.inType not in tools.getCommandSet("m", 'a', p=True):
            msg = '\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): "
            self.inType = tools.inputChecker(msg=msg, seq=tools.getCommandSet("mf", 'a'))
        else:
            self.inType = 'ma'
        self.lastIn = self.inType
        return self.inType
    
    def getTable(self):
        tools = self.tools
        if self.table not in tools.getCommandSet("tn", 'a', p=True):
            msg = "Table?(t, ta): "
            self.table = tools.inputChecker(msg=msg, seq=tools.getCommandSet("tn", 'a'))
        else:
            self.table = 'ta'
        self.lastIn = self.table
        return self.table
    
    def getInData(self):
        tools = self.tools
        msg = "Paste Dataset: " if self.inType in tools.getCommandSet("m", 'a') else "Filename: "
        self.inData = tools.inputChecker(msg=msg)
        self.lastIn = self.inData
        return self.inData
    
    def file_mngr(self, datalist=None, filename=None):
        tools, count = self.tools, len(datalist)
        if any(self.table == c for c in tools.getCommandSet('t', 'a')):
            try:
                filename = self.inData if not filename else filename
                with open(filename, 'r', encoding='utf8') as fi:
                    self.inData = (fi.readlines() if self.table in tools.getCommandSet('t', 'a') 
                                   else fi.read())
            except FileNotFoundError:
                filename = "g_file"+str(count+1)+".txt"
                with open(filename, 'w', encoding='utf8') as fi:
                    fi = fi.write(self.inData)
            else:   
                return self.inData
        return self.inData 
    
    def addNew(self, datalst=None):
        tools = self.tools
        self.inData = self.getInData()
        if not tools.anySetter(0, "de", seq=[self.inData]):
            self.inData = self.file_mngr(datalist=datalst)
            self.all_data = Data(tools).addData(self.inData)
            self.lastIn = self.inData
            return self.inData
        else:
            print(self.all_data)
            return 1
    
    def del_all(self):
        return True if self.lastIn == 'da' else False

class Data(InputOps):   
    def __init__(self, tools, name=None):
        tools.__init__(), InputNode().__init__()
        self.tools = tools
        self.commands = tools.getCommandSet("mftda", 'a')
        self.all_data = []
        self.count = 0
        self.name = name
    
    def allData(self):
        print("{}\n{}".format(self.all_data, self.name))
        return self.all_data
    
    def addData(self, add):
        self.all_data.append(add)
        self.count = len(self.all_data)
        print("\n{}\ndatapackage{}= {}".format(self.all_data, 
                              's' if self.count>1 else '', self.count))
    
    def del_allData(self):
        if self.inData == 'da':
            print("DELETED all ({}) inputs".format(len(self.all_data)))
            self.all_data.clear()
        return self.all_data


def gatherData():
    d = Data(Tools())
    while True:
        x = InputOps(Tools(), InputNode())
        x.getInType()
        x.getTable()
        newData = x.getInData()
        d.addData(newData)
gatherData()
