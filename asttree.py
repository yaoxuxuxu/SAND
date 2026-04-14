
class ASTnode:
    def __init__(self):
        self.child=[]
        self.exp_type=""
        
    def get_child(self):
        return self.child

class ASTleaf:
    def __init__(self):
        super.__init__()
        self.value=""
        

class ASTstem:
    pass