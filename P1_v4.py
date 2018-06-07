
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
        forbidden_or_allowed = {c for c in "bde"}
        if not seq:
            return inpt
        seq = seq | forbidden_or_allowed
        if inpt not in list(seq):
            print("\nERROR: Bad Input!")
            return self.inputChecker(msg, seq)
        return inpt


class InputNode(Tools):
    def __init__(self):
        inpt_specs = Tools.inpt_node_args(self)
        self.__dict__.update(inpt_specs)

    def inType(self):
        return self.inType
    
    def table(self):
        return self.table
    
    def inData(self):
        return self.inData


class InputOps(InputNode, Tools):   
    def __init__(self, tools, data):
        tools.__init__()
        InputNode.__init__(self)
        self.tools = tools

    def getInType(self):
        tools = self.tools
        if self.inType not in tools.getCommandSet("mf", 'a', p=True):
            msg = '\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): "
            self.inType = tools.inputChecker(msg=msg, seq=tools.getCommandSet("mf", 'a'))
        return self.inType
    
    def getTable(self):
        tools = self.tools
        if self.table not in tools.getCommandSet("tn", 'a', p=True):
            msg = "Table?(t, ta): "
            self.table = tools.inputChecker(msg=msg, seq=tools.getCommandSet("tn", 'a'))
        return self.table
    
    def getInData(self, cnum):
        tools = self.tools
        msg = ("Paste Dataset: " if self.inType in tools.getCommandSet("m", 'a') 
               else "Filename: ")
        self.inData = tools.inputChecker(msg=msg, filtr=True)
        self.inData = self.file_mngr(count=cnum)
        return self.inData
    
    def file_mngr(self, count=None, filename=None):
        tools = self.tools
        if any(self.table == c for c in tools.getCommandSet('tf', 'a')):
            try:
                filename = self.inData if not filename else filename
                with open(filename, 'r', encoding='utf8') as fi:
                    self.inData = (fi.readlines() if self.table in tools.getCommandSet('t', 'a') 
                                   else fi.read())
            except (FileNotFoundError, OSError):
                filename = "g_file"+str(count+1)+".txt"
                with open(filename, 'w', encoding='utf8') as fi:
                    fi = fi.write(self.inData)
            else:   
                return self.inData
        return self.inData 


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
    
    def addData(self, newdata):
        if type(newdata) == str:
            self.all_data.append(newdata)
            self.count = len(self.all_data)
            print("\n{}\ndatapackage{}= {}".format(self.all_data, 
                                    's' if self.count>1 else '', self.count))
            return self.all_data
    
    def dellData(self, count):
        for i in range(count):
            del self.all_data[-1]
        print("..deleted {} datablocks".format(count))
        return self.all_data

    def del_allData(self):
        print("DELETED all ({}) inputs".format(len(self.all_data)))
        self.all_data.clear()
        return self.all_data


def gatherData(datarealm=None):         
    tools = Tools()
    _D = Data(tools) if not datarealm else datarealm
    data = _D.allData()
    inpt = 'n/a'
    x = InputOps(tools, InputNode())
    while not (tools.anySetter("bde", seq=[inpt])) and inpt != "da":
        print(data)
        inpt = x.getInType()
        inpt = x.getTable()
        inpt = x.getInData(len(data))
        if tools.anySetter("bde", seq=[inpt]):
            print(inpt)
        data = _D.addData(inpt)

    print("woo")    
    count = len(inpt)
    if inpt == "da":
        data = _D.del_allData()
        return gatherData(datarealm=_D)
    elif tools.anySetter("d", seq=[inpt]):
        data = _D.dellData(count)
        return gatherData(datarealm=_D)
    elif inpt == 'b':
        return gatherData(datarealm=_D)
    else:
        return sys.exit()
        
gatherData()
