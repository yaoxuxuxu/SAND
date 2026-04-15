
class ASTnode:
    def __init__(self):
        self.child=[]
        self.exp_type=""
    def get_child(self):
        return self.child
    def __str__(self):
        res=self.printtree(self)
        return "--ASTREE--"
    def printtree(self,nownode,depth=0):
        res=depth*" "*4
        res+="type : "+nownode.exp_type
        if type(nownode) == ASTleaf:
            res+=" value : "+str(nownode.value)
        print(res)
        for i in nownode.get_child():
            self.printtree(i,depth+1)
class ASTleaf(ASTnode):
    def __init__(self,value):
        super().__init__()
        self.value=value
        

class ASTstem:
    pass