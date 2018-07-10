import importlib
import sys
print(globals())


tst = input("Operation: ")
def parseTxt(*parsetxt):
    for txtblock in parsetxt:
        if '.' in txtblock:
            module = txtblock[:txtblock.index('.')]
            method = txtblock[txtblock.index('.') + 1:txtblock.index('(')]
            arg = txtblock[txtblock.index('(') + 1:-1]
            if method not in globals():
                globals()[module+'.'+method] = getattr(importlib.import_module(module), method)
            txtblock = "globals()['{}']({})".format(module+'.'+method, arg)
        print(locals())
    del (module, method, arg)
    return txtblock

tst = "math.sqrt(4)"
parsed = parseTxt(tst)
exec("d = {}".format(parsed))
print(d)
print(globals())
