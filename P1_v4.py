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
        print(self.__dict__.items)

    def inType(self):
        return self.inType
    
    def table(self):
        return self.table
    
    def inData(self):
        return self.inData
    
    def lastIn(self):
        return self.lastIn

class Data():   
    def __init__(self, tools, name=None):
        self.commands = tools.getCommandSet("mftda", 'a')
        self.all_data = []
        self.count = 0
        self.name = name
    
    def data(self):
        print("{}\n{}".format(self.all_data, self.name))
        return self.all_data
    
    def addData(self, add):
        self.all_data.append(add)
        print(self.all_data)
        return self.all_data

class InputOps(Data, InputNode):   
    def __init__(self, tools, data):
        Data.__init__(self, tools)
        self.tools = tools
        self.data = data
    
    def getInType(self):
        tools = self.tools
        if self.inType not in tools.getCommandSet("m", 'a', p=True):
            msg = '\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): "
            self.inType = tools.inputChecker(msg=msg, seq=tools.getCommandSet("mf", 'a'))
        else:
            self.inType = 'ma'
        return self.inType
    
    def getTable(self):
        tools = self.tools
        if self.table not in tools.getCommandSet("tn", 'a', p=True):
            msg = "Table?(t, ta): "
            self.table = tools.inputChecker(msg=msg, seq=tools.getCommandSet("tn", 'a'))
        else:
            self.table = 'ta'
        return self.table
    
    def getInData(self):
        tools = self.tools
        msg = "Paste Dataset: " if self.inType in tools.getCommandSet("m", 'a') else "Filename: "
        self.inData = tools.inputChecker(msg=msg)
        return self.inData

    def addNew(self, datalst):
        tools = self.tools
        if not tools.anySetter(0, "de", seq=[self.inData]):
            self.inData = self.file_mngr()
            datalst.append(self.inData)
            self.all_data = Data.addData(self, self.inData)

            print("\n{}\ndatasets count = {}\n".format(self.all_data, len(self.all_data)))
            self.lastIn = self.inData
            self.count += 1
        else:
            print(self.all_data)
            return 1
    
    def file_mngr(self, filename=None):
        tools = self.tools
        if any(self.table == c for c in tools.getCommandSet('t', 'a')):
            try:
                filename = self.inData if not filename else filename
                with open(filename, 'r', encoding='utf8') as fi:
                    self.inData = (fi.readlines() if self.table in tools.getCommandSet('t', 'a') 
                                   else fi.read())
            except FileNotFoundError:
                filename = "g_file"+str(self.count+1)+".txt"
                with open(filename, 'w', encoding='utf8') as fi:
                    fi = fi.write(self.inData)
            else:   
                return self.inData
        return self.inData 

    def del_all(self):
        if self.inData == 'da':
            print("DELETED all ({}) inputs".format(len(self.all_data)))
            self.all_data.clear()
        return self.all_data


def gatherData():
    all_data_lst = []
    d = Data(Tools())
    while True:
        print(all_data_lst)
        x = InputOps(Tools(), InputNode())
        x.getInType()
        x.getTable()
        newData = x.getInData()
        if x.del_all():
            all_data_lst.clear() 
        if newData != 1:
            x.addNew(all_data_lst)
            d.addData(newData)
        else: break
gatherData()
