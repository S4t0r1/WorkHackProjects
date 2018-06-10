
import sys


class BadInputError(Exception): pass

class Tools():  
    def getCommandSet(self, seq=None, char=None, p=False):
        return set(';'.join(c1+c2 if p else ';'.join((c1, c1+c2)) 
                   for c1, c2 in zip(seq, char*len(seq))).split(';'))
    
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
        if len(inpt) == 0:
            return self.inputChecker(msg, seq, filtr)
        if filtr:
            if len(inpt) > 1:
                filtr = filtr | {c*len(inpt) for c in filtr if len(c) == 1}
            if inpt in filtr:
                return inpt, len(inpt)
        if seq:
            if inpt not in list(seq):
                print("\nERROR: Bad Input!")
                return self.inputChecker(msg, seq, filtr)               
        return inpt
    
    def getCmndSeqs(self, seq, slen=None):
        assert ';' in seq, "divide inpt_cmnds & data_cmnds by ';'"
        seq = seq.split(';')
        i_cmnds, d_cmnds = seq
        i_cmnds = self.getCommandSet(i_cmnds, 'a')
        d_cmnds = self.getCommandSet(d_cmnds, 'a') - {'ea'}
        a_cmnds = i_cmnds | d_cmnds
        print("{a_cmnds}\n{i_cmnds}\n{d_cmnds}\n".format(**locals()))
        return a_cmnds, i_cmnds, d_cmnds


class InputNode(Tools):
    def __init__(self, inType=None, table=None, inData=None, seq=None, off=False):
        Tools.__init__(self)
        self.a_cmndset, self.i_cmndset, self.d_cmndset = self.getCmndSeqs(seq)     
        self.inType = inType
        self.table = table
        self.inData = inData
    
    def getInputOp(self, x, cnum, off=False):
        return self.getInType(off) if x == 0 else self.getTable(off) if x == 1 else self.getInData(cnum, off)

    def getInType(self, off):
        if not off:
            if self.inType not in self.getCommandSet("mf", 'a', p=True):
                msg = '\n'+"INPUT"+'\n'+"manually(m/all=ma)"+'\n'+"    file(f/all=fa): "
                self.inType = self.inputChecker(msg=msg, seq=self.getCommandSet("mf", 'a'),                                                                            filtr=self.d_cmndset)
            return self.inType
    
    def getTable(self, off):
        if not off:
            if self.table not in self.getCommandSet("tn", 'a', p=True):
                msg = "Table?(t, ta): "
                self.table = self.inputChecker(msg=msg, seq=self.getCommandSet("tn", 'a'),
                                                                     filtr=self.d_cmndset)
            return self.table
    
    def getInData(self, cnum, off):
        if not off:
            msg = ("Paste Dataset: " if self.inType in self.getCommandSet("m", 'a') else "Filename: ")
            self.inData = self.inputChecker(msg=msg, filtr=self.d_cmndset)
            if type(self.inData) != tuple:
                self.inData = self.file_mngr(count=cnum)
            return self.inData
    
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
    def __init__(self, seq=None, name=None):
        Tools.__init__(self)
        InputNode.__init__(self, seq=seq)
        self.seq = seq
        self.name = name
        self.a_cmnds, self.i_cmnds, self.d_cmnds = self.getCmndSeqs(seq)
        self.datadict = {}
        self.all_data = list(self.datadict.values())
        self.count = len(self.all_data)
        self.ext = None

    def print_allData(self):
        return "\n{}\n{}".format(self.name, self.all_data)         
    
    def back_startmenu(self):
        InputNode.__init__(self, seq=self.seq, off=False)
        return self.getInputs()
    
    def exit_adding(self):
        self.ext = True
        return self.getInputs()

    def addData(self, newdata):
        self.all_data.append(newdata)
        print("\n{}\n{}\ndatapackage{} = {}".format(self.name, self.all_data, 
                  's' if len(self.all_data) > 1 else '', len(self.all_data)))
    
    def dellData(self, count):
        self.all_data = self.all_data[:-count]
        print("\n..deleted {} datablocks\n{}".format(count, self.print_allData()))

    def del_allData(self):
        prevcount = self.count
        self.all_data.clear()
        print("\n..deleted all inputs({})\n{}".format(prevcount, self.print_allData()))
    
    def getDataOp(self, inpt, slen):
        return (self.back_startmenu() if 'b' in inpt
              else self.del_allData() if 'da' == inpt
              else self.dellData(slen) if 'd' in inpt
              else self.exit_adding())

    def getInputs(self):
        while not self.ext:
            specs = []
            for n in range(3):
                inpt = self.getInputOp(n, self.count, off=False)
                if type(inpt) == tuple:
                    inpt, slen = inpt
                    self.getDataOp(inpt, slen)
                    break
                if n < 2:
                    specs.append(inpt)
            else:
                self.addData(inpt)
                specs = "{}.{}".format(self.count, '.'.join(specs))
                self.datadict[specs] = inpt
        return self.all_data

    
d = Data(seq="mftn;bde", name="TEST 99999")
datarealm = d.getInputs()
