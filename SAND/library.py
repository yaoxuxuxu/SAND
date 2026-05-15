import importlib
import os
import inspect
from .function import NativeFunctionManager,NativeFunction
from .environment import Environment,TreeEnv
from .StoneException import StoneException

class BuiltInLibrary:
    def __init__(self,module):
        self.name=""
        self.module=module
        self.env=Environment()
    def importFunByName(self,name):
        try:
            return getattr(self.module,name)
        except:
            raise StoneException("No function called"+name)
        
    def returnAllMethod(self):
        return inspect.getmembers(self.module)
class BuiltInLibraryManager:
    def __init__(self):
        self.libs_dir=os.path.abspath("SAND/sandlib")
        self.libs=[]
        self.nowlibs={}
        self.generate_list()
    def generate_list(self):
        for dir in os.listdir(self.libs_dir):
            self.libs.append(dir.replace(".py",""))    
    def importLib(self,name):
        if name in self.nowlibs:
            return self.nowlibs[name]
        dir= ".sandlib."+name
        module=importlib.import_module(dir,package=__package__)
        module=getattr(module,name)()
        self.nowlibs[name]=BuiltInLibrary(module)
        return self.nowlibs[name]
    def isBuiltInLibrary(self,name):
        return name in self.libs