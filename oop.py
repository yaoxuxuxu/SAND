from asttree import ASTnode
from environment import TreeEnv
class Class:
    def __init__(self,name:str,asttree:ASTnode,father_env):
        self.classname=name
        self.asttree=asttree
        self.env=TreeEnv(father_env)
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
        
    
    
    
    
