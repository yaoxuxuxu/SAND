class Function:
    def __init__(self,args=[],astTree=None):
        self.astTree=astTree
        self.args=args
    def getArgs(self):
        return self.args
    def getASTtree(self):
        return self.astTree
    