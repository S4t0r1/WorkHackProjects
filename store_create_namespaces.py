
dict1 = {k: v for k,v in zip("abc", [1, 2, 3])}
dict2 = {k: v for k,v in zip("a_.b_.c_.".split('.'), [10, 20, 30])}

locals2 = {k: v for k, v in zip({'dict1', 'dict2'}, [dict1, dict2])}
tst_cls = type('Tst_cls', (object, ), {k: v for k, v in locals2.items()})


cls_name = input("Class name: ")
base = input("Namespace base: ")
namespaces, namespace = {}, ''
while True:
    namespace = input("Namespaces(as dicts) to include: ")
    if len(namespace) == 0:
        break
    var_dict = (eval(base)[namespace] if type(eval(base)) == dict 
          else getattr(eval(base), namespace))
    namespaces.update({namespace: var_dict})
cls_name = type(cls_name, (object, ), {k: v for k, v in namespaces.items()})
new = cls_name()

for k, v in cls_name.__dict__.items():
    try:
        if type(v) == dict:
            print("{} : {}".format(k, v))
    except (TypeError, NameError):
        continue

