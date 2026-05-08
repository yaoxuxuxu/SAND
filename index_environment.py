from StoneException import StoneException
class EnvironmentManager:
    def __init__(self):
        self.env=[]
    def getValue(self,depth,index):
        pass
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
    def __str__(self):
        return "global_environment"
    
