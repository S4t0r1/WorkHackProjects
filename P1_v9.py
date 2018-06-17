
import sys


class BadInputError(Exception): pass

class Tools():  
    def getCommandSet(self, seq1=None, char=None, p=False):
        return set(';'.join(c1+c2 if p else ';'.join((c1, c1+c2)) 
                   for c1, c2 in zip(seq1, char*len(seq1))).split(';'))
    
    def anySetter(self, *args, var_seq=None):
        conds, isTrue = False, False
        if '^' in args:
            start_or = args.index('^')
        for cond in args:    
            if '^' == cond:
                conds = True
                continue
            isTrue = any(len(txt) == cond if type(cond) == int
                else txt == cond if (len(cond) > 1 and cond[0] != cond[1])
                else len(txt) == txt.count(cond) if len(cond) == 1 
                else len(txt) in {txt.count(ch) for ch in cond 
                  if len(txt) >= 1} for txt in var_seq)
            if conds:
                if isTrue and cond in args[start_or + 1:]:
                    break
            else:
                if not isTrue:
                    break
        return isTrue


    def inputChecker(self, msg, seq=None, filtr=None):
        inpt = input(msg)
        if len(inpt) == 0:
            return self.inputChecker(msg, seq, filtr)
        if filtr:
            if self.anySetter('^', *filtr, var_seq=[inpt]):
                return inpt, len(inpt)
        if seq:
            if inpt not in list(seq):
                print("\nERROR: Bad Input!")
                return self.inputChecker(msg, seq, filtr)               
        return inpt
    
    def getCmndSeqs(self, seq):
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
    
    def getInputOp(self, x, dnum, off=False):
        return (self.getInType(off) if x == 0 
          else self.getTable(off) if x == 1 
          else self.getInData(off, data_pos=dnum))
    
    def getInput(self, *args, **kwargs):
        msg, inptvar, data_cmnds, off = args
        inpt_cmnds, condition, data_pos = kwargs.values()
        if not off:
            if type(condition) == set:
                if inptvar not in condition:
                    inptvar = self.inputChecker(msg, inpt_cmnds, filtr=data_cmnds)
                return inptvar
            elif condition == tuple:
                inptvar = self.inputChecker(msg, None, data_cmnds)
                if type(inptvar) != condition:
                    inptvar = self.file_mngr(inptvar, dnum=data_pos)
                return inptvar

    def getInType(self, off):
        inpt_cmnds, condition = self.i_cmndset, self.getCommandSet("mf", 'a', p=True)
        msg = "\nINPUT\nmanually(m/all=ma)\n    file(f/all=fa): "
        self.inType = self.getInput(msg, self.inType, self.d_cmndset, off,
            inpt_cmnds=inpt_cmnds, condition=condition, data_pos=None)
        return self.inType
    
    def getTable(self, off):
        inpt_cmnds, condition = self.i_cmndset, self.getCommandSet("tn", 'a', p=True)
        self.table = self.getInput("Table?(t, ta): ", self.table, self.d_cmndset, off, 
                      inpt_cmnds=inpt_cmnds, condition=condition, data_pos=None)
        return self.table
    
    def getInData(self, off, data_pos=None):
        prev_cmnds = self.getCommandSet("m", 'a')
        inpt_cmnds, condition = None, tuple
        msg = ("Paste Dataset: " if self.inType in prev_cmnds else "Filename: ")        
        self.inData = self.getInput(msg, self.inData, self.d_cmndset, off, 
            inpt_cmnds=inpt_cmnds, condition=condition, data_pos=data_pos)
        return self.inData

    def file_mngr(self, indata, dnum=None, filename=None):
        if any(self.table == c for c in self.getCommandSet('tf', 'a')):
            try:
                filename = indata if not filename else filename
                with open(filename, 'r', encoding='utf8') as fi:
                    indata = (fi.readlines() if self.table in self.getCommandSet('t', 'a') 
                                   else fi.read())
            except (FileNotFoundError, OSError):
                filename = "g_file" + str(dnum + 1 )+ ".txt"
                with open(filename, 'w', encoding='utf8') as fi:
                    fi = fi.write(indata)
            else:   
                return indata
        return indata 


class Data(InputNode, Tools):   
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
    
    def dellData(self, slen):
        self.all_data = self.all_data[:-slen]
        print("\n..deleted {} datablocks\n{}".format(slen, self.print_allData()))

    def del_allData(self):
        delcount = len(self.all_data)
        self.all_data.clear()
        print("\n..deleted all inputs({})\n{}".format(delcount, self.print_allData()))
    
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
                specs = "{}.{}".format(len(self.all_data), '.'.join(specs))
                self.datadict[specs] = inpt
        return self.all_data

    
d = Data(seq="mftn;bde", name="TEST 99999")
datarealm = d.getInputs()
