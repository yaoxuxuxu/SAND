from .asttree import ASTnode
from .environment import TreeEnv
class Class:
    def __init__(self,name:str,init_astTree:list,father):
        self.classname=name
        self.asttree=[]
        if isinstance(father,Class):
            self.asttree=list(father.getAsttree())
            self.env=TreeEnv(father.getEnv())
        else:
            self.env=TreeEnv(father)
        self.asttree+=init_astTree
        
    def getName(self):
        return self.classname
    def getAsttree(self):
        return self.asttree
    def getEnv(self):
        return self.env
    def getFatherEnv(self):
        return self.env.getFatherEnv()
    def createInstance(self):
        pass
class ClassInstance:
    def __init__(self,father_env):
        self.env=TreeEnv(father_env)
    def getEnv(self):
        return self.env
    def getFatherEnv(self):
        return self.env.getFatherEnv()
        
    
    
    
    
