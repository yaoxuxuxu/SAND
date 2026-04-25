from environment import TreeEnv
class Function:
    def __init__(self,funname="fun",args=[],astTree=None,env=None):
        self.funname=funname
        self.astTree=astTree
        self.args=args
        self.env=env
    def getArgs(self):
        return self.args
    def getASTtree(self):
        return self.astTree
    def getEnv(self):
        return self.env
    def setEnv(self,env):
        self.env=env