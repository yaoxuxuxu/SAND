from environment import TreeEnv
class Function:
    def __init__(self,args=[],astTree=None,father_env=None):
        self.env=TreeEnv(father_env)
        self.astTree=astTree
        self.args=args
    def getArgs(self):
        return self.args
    def getEnv(self):
        return self.env
    def getASTtree(self):
        return self.astTree
    