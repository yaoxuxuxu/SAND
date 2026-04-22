from StoneException import StoneException
from asttree import ASTnode
class Environment:
    def __init__(self):
        self.var={}
    def setValue(self,name,value):
        self.var[name]=value
        return value
    def getValue(self,name):
        if name in self.var:
            return self.var[name]
        else:
            raise StoneException("name "+str(name)+" is not defined")
    def getFatherEnv(self):
        return None
class TreeEnv(Environment):
    def __init__(self,father):
        self.var={}
        self.father=father
    def getFatherEnv(self):
        return self.father
    def whereis(self,name):
        env=self
        while name not in env.var:
            env=env.getFatherEnv()
            if env == None:
                break
        return env
    def getValue(self,name):
        env=self.whereis(name)
        if env==None:
            raise StoneException("name "+str(name)+" is not defined")
        return env.var[name]
    def setValueForce(self,name,value):
        #When create Function env, use this to set vars in self env
        self.var[name]=value
        return value
    def setValue(self, name, value):
        env=self.whereis(name)
        if env==None:
            env=self
        env.var[name]=value
        return value