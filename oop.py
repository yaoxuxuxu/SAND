from asttree import ASTnode
from environment import TreeEnv
class Class:
    def __init__(self,name:str,asttree:ASTnode,env:TreeEnv):
        self.classname=name
        self.asttree=asttree
        self.env=env
    def getName(self):
        return self.classname
    def getAsttree(self):
        return self.asttree
    def getEnv(self):
        return self.env
    def getFatherEnv(self):
        return self.env.getFatherEnv()
    
class ClassInstance:
    def __init__(self,env):
        self.env=env
    def getEnv(self):
        return self.env
        
    
    
    
    
