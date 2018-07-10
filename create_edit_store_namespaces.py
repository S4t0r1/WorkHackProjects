
import re
import collections

class Operations:
    def __init__(self, name="Ops"):
        self.name = name
        self.all_logic = {}
    
    def get_all(self, namespace, console=False):
        Optypes = collections.namedtuple("Optypes", "funcs super_locals")
        
        """
        while console:
            inpt = input("Write/paste logic (Enter=Cancel):", '\n')
            if 'def' in inpt:
                funcs = 
            if "ext" in inpt:
                break
        """
        if console == "ext":
            self.all_logic.update(namespace)
    
    def prnt(self, target=None):
        target = self.all_logic.items() if not target else [(target, self.all_logic[target])]
        for item in target:
            print(item)

def testing():
    tst1 = Operations("Test1")
    tst1.prnt()
    def abecede():
        c = 20 + 11
        return c
    tst1.get_all(locals(), "ext")
    tst1.prnt("abecede")

testing()
