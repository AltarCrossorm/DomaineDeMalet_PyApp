"""
# cppy.py
###### [Deprecated]

A decorator system to declare functions outside of the class, C++ style

```
@class_declaration
class My_Class:
    def __init__(self):
        pass
        
@class_definition(My_Class)
def __init__(My_class.self):
    ... # Complete the init function here
```
"""

import inspect
import types
from typing import TypeVar, Type

class_lib:dict[str,list[str]] = {}

C = TypeVar('C') # généricité
def class_declaration(cls: type[C]):
    """
    decorator who build the `CpPy` environnement\n
    builds up the global variable to store
    """
    
    # Obtenir tous les attributs de la classe
    attributs = dir(cls)

    # Obtenir les attributs des classes de base
    attributs_de_base:set[str] = set()
    for base in cls.__bases__:
        attributs_de_base.update(dir(base))

    # Filtrer pour ne garder que les méthodes explicitement déclarées dans la classe    
    class_lib[cls.__name__] = [
        attr
        for attr in attributs
        if callable(getattr(cls, attr))
        and (
            attr not in attributs_de_base
            or getattr(cls, attr) != getattr(cls.__bases__[0], attr, None)
        )
        and not "sub" in attr
    ]
    
    return cls

def class_definition(cls : Type[C]):
    """
    calls up the directory to find if a class exists in the CpPy scope\n
    raise exceptions if the compared methods (on the class and on the method checked) don't mach (name match and signature match)
    
    ```
    @class_declaration
    class My_Class:
        def My_Func(self,foo):
            pass
            
    @class_definition(My_Class)
    def My_Func(self,bar):
        ... # Exception : signatures don't match
        
    @class_definition(My_Class)
    def My_Func1(self,foo):
        ... # Exception : 'My_Class' don't have that function registered 
    ```
    """
    def method_wrapper(method:types.FunctionType):
        if (method.__name__ in class_lib[cls.__name__]):
            method_signatures:list[str] = [name for name, parameter in inspect.signature(getattr(cls,method.__name__)).parameters.items()] # type: ignore
            base_signatures:list[str] = [name for name, parameter in inspect.signature(method).parameters.items()] # type: ignore
            
            if method_signatures == base_signatures:
                cls.method = method  # type: ignore
            else:
                raise Exception(f"Method '{method.__name__}' does not match the signature of the original one\nYours are : {method_signatures}\nBase are : {base_signatures}")
        else:
            raise Exception(f"Method '{method.__name__}' does not exists in '{cls.__name__}' class")
    
    if cls.__name__ in class_lib.keys():
        return method_wrapper
    else:
        raise Exception(f"Class '{cls.__name__}' is not implemented")
    