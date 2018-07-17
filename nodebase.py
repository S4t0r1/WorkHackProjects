import re

Rvrs = type("Rvrs", (), {'getrev': print(' '.join(input("Write a sentence !: ").split()[::-1]))})


class Nodebase:
    def __init__(self, *data):
        self.all_data = {}
    
    def getFile(fname):
        
        with open(fname, 'r', encoding='utf-8') as fi:
            datitem = fi.read()
        
    
    def getNode(datitem, mode='s', name=None):
        if mode == 's':
            continue
        elif mode == 'f':
            fname, ftype = datitem.split('.')
            with open(fname, 'r', encoding='utf-8') as fi:
                datitem = fi.read()
        elif mode == 'u':
            

    def getNodes(self, data):
        for datitem in [data]:
            pass
            

def setNode():
    cls = type(str(nodename), (Nodebase), {'dtype': dtype, 'ops': ops, ''})
    Nodebase.addNode(cls)
