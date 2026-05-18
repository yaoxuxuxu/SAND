import importlib
import os
import inspect
from .StoneException import LibException
from .function import NativeFunctionManager,NativeFunction
from .environment import Environment,TreeEnv
from .StoneException import StoneException

class StandardLibrary:
    def __init__(self):
        self.description="A BuiltIn Library"
    def raise_exception(self,message):
        raise LibException(self.description,message)
    def check_args(self,args,minn,maxx):
        if len(args)<minn or len(args)>maxx:
            self.raise_exception("Wrong number of arguments")
    def check_types(self,args,types):
        for i in range(len(args)):
            if types[i]=="any":
                continue
            if not isinstance(args[i],types[i]):
                self.raise_exception("Wrong type of arguments")
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
    def isMethod(self,name,method):
        if '_' in name:
            return False
        if not inspect.ismethod(method):
            return False
        return True
    def returnAllMethod(self):
        funlist=[]
        for name,method in inspect.getmembers(self.module):
            if self.isMethod(name,method):
                funlist.append((name,method))
        return funlist
class BuiltInLibraryManager:
    def __init__(self):
        self.libs_dir=os.path.abspath("SAND/sandlib")
        self.libs=[]
        self.nowlibs={}
        self.generate_list()
    def isFileLibrary(self,dir):
        if ".py" in dir:
            return True
        return False
    def generate_list(self):
        for dir in os.listdir(self.libs_dir):
            if self.isFileLibrary(dir):
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