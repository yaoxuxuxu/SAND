from Token import Token
class ASTnode:
    def __init__(self):
        self.child=[]
        self.exp_type=""
        self.value=None
    def getToken(self):
        return None
    def getChild(self):
        return self.child
    def getValue(self):
        return self.value
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
        if type(nownode) == ASTfruit:
            res+=" value : "+str(nownode.getValue())   
        res+="\n"     
        for i in nownode.getChild():
            res+=self.printtree(i,depth+1)
        return res
class ASTfruit(ASTnode):
    def __init__(self,token):
        super().__init__()
        self.token=token
    def getToken(self):
        return self.token
    def getValue(self):
        return self.token.getValue()
    
    

        