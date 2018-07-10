import importlib
import sys
print(globals())

exec("from math import log")
print(globals())

tst = input("Operation: ")
def parseTxt(parsetxt):
    newtxt = []
    for i, value in enumerate(parsetxt):
        start = None
        objlen = 0
        for y, e in enumerate(value):
            if e.isalpha() or e == '_':
                if e.isalnum() or e == '_':
                    objlen += 1
                if not start:
                    start = y
        newtxt.append(parsetxt[start:objlen+1])
    newtxt = ' '.join(newtxt)
            
    print('\n'+newtxt+'\n')
    
    for txtblock in parsetxt:
        if '.' in txtblock:
            module = txtblock[:txtblock.index('.')]
            method = txtblock[txtblock.index('.') + 1:txtblock.index('(')]
            arg = txtblock[txtblock.index('(') + 1:-1]
            if method not in globals():
                globals()[module+'.'+method] = getattr(importlib.import_module(module), method)
            txtblock = "globals()['{}']({})".format(module+'.'+method, arg)
            del (module, method, arg)
    print(locals())
    print(' '.join(parsetxt))
    return txtblock
parsed = print(parseTxt(tst))

tst = "math.sqrt(4)"
parsed = parseTxt(tst)
exec("d = {}".format(parsed))
print(d)
print(globals())
