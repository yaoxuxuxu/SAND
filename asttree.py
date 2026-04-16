class ASTnode:
    def __init__(self):
        self.child=[]
        self.exp_type=""
    def get_child(self):
        return self.child
    def __str__(self):
        linechar="-"
        line=linechar*20
        res=line+"AST_TREE_START"+line+"\n"
        res+=self.printtree(self)
        res+=line+linechar+"AST_TREE_END"+linechar+line
        return res
    def printtree(self,nownode,depth=0):
        res=depth*" "*4
        res+="type : "+nownode.exp_type
        if type(nownode) == ASTleaf:
            res+=" value : "+str(nownode.value)   
        res+="\n"     
        for i in nownode.get_child():
            res+=self.printtree(i,depth+1)
        return res
class ASTleaf(ASTnode):
    def __init__(self,value):
        super().__init__()
        self.value=value
        

class ASTstem:
    pass