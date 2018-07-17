import re

Rvrs = type("Rvrs", (), {'getrev': print(' '.join(input("Write a sentence !: ").split()[::-1]))})


class Nodebase:
    def __init__(self, *data):
        self.all_data = {}
    
    def getFile(fname):
        strdata = ''
        with open(fname, 'r', encoding='utf-8') as fi:
            strdata = fi.read()
        return strdata

    def getNode(datitem, mode='s', name=None):
        if mode == 's' and not name:
            name = len(self.all_data.keys())
        elif mode == 'f':
            fname, mode = datitem.split('.')
            datitem = self.getFile(fname)
            if not name:
                name = fname
        return datitem, mode, name
            

def setNode():
    cls = type(str(nodename), (Nodebase), {'dtype': dtype, 'ops': ops, ''})
    Nodebase.addNode(cls)
