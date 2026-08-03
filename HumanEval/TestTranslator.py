import ast

class NodeTranslator(ast.NodeVisitor):
    def __init__(self,funname,testid):
        self.tests=[]
        self.testid=testid
        self.funname=funname
    def auto_dispatch(self,child):
        name=type(child).__name__
        fun=getattr(self,"translate_"+name,self.translate_default)
        return fun(child)
    def visit_Assert(self, node):
        child=node.test
        if self.has_candidate_call(child):
            #here need try except after test
            res=self.auto_dispatch(child)
            self.tests.append(res)
    def translate_Compare(self,node):
        left=node.left
        ops=node.ops
        comparators=node.comparators
        if len(ops)>1:
            raise Exception("lots of compare")
        ops=self.ops_translate(ops[0])
        comparators=comparators[0]
        return self.auto_dispatch(left)+ops+self.auto_dispatch(comparators)
    
    def translate_Call(self,node):
        func=node.func
        args=node.args
        keywords=node.keywords
        if len(keywords) > 0:
            raise Exception("keyword argument is not allowed")
        res=self.funname+'('
        for i in args:
            res+=self.auto_dispatch(i)
            res+=","
        if res[-1]==",":
            res=res[:-1]
        res+=")"

        return res
    def translate_UnaryOp(self,node):
        op=node.op
        operand=node.operand
        match op:
            case ast.USub():
                return "-"+self.auto_dispatch(operand)
            case ast.UAdd():
                return "+"+self.auto_dispatch(operand)
            case _:
                raise Exception("UnaryOp not define")
    def translate_BinOp(self,node):
        left=node.left
        op=node.op
        right=node.right
        match op:
            case ast.Add():
                return self.auto_dispatch(left)+"+"+self.auto_dispatch(right)
            case ast.Sub():
                return self.auto_dispatch(left)+"-"+self.auto_dispatch(right)
            case ast.Mult():
                return self.auto_dispatch(left)+"*"+self.auto_dispatch(right)
            case ast.Div():
                return self.auto_dispatch(left)+"/"+self.auto_dispatch(right)
            case _:
                raise Exception("BinOp not define")   
    def translate_Tuple(self,node):
        return self.translate_List(node)
    def translate_List(self,node):
        items=node.elts
        res='['
        for i in items:
            res+=self.auto_dispatch(i)
            res+=","
        if res[-1]==",":
            res=res[:-1]
        res+="]"
        return res
    def translate_Constant(self,node):
        value=node.value
        match value:
            case str():
                return '"'+value+'"'
            case bool():
                if value:
                    return "true"
                else:
                    return "false"
            case int():
                return str(value)
            case float():
                tmp=str(value)
                if 'e' in tmp:
                    return str(format(value,"f"))
                return tmp
            case _:
                raise Exception("Type not define")
    def ops_translate(self,ops):
        cmp_map = {
                    ast.Lt: "<",
                    ast.LtE: "<=",
                    ast.Gt: ">",
                    ast.GtE: ">=",
                    ast.Eq: "==",
                    ast.NotEq: "!=",
                    ast.Is: "=="
        }
        if type(ops) not in cmp_map:
            raise Exception("Failed to translate a operator")
        return cmp_map[type(ops)]
    def has_candidate_call(self,node):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                if isinstance(sub.func, ast.Name) and sub.func.id == "candidate":
                    return True               
        return False
    def translate_default(self,node):
        print(node,self.testid)
        print(ast.dump(node))
        raise NotImplementedError(type(node).__name__+" is not translated")
class TestTranslator:
    def __init__(self):
        pass
    def translate(self,test):
        self.tests=[]
        test_code=test["test"]
        asttree=ast.parse(test_code)
        nt=NodeTranslator(test["entry_point"],test["task_id"])
        nt.visit(asttree)
        if len(nt.tests)==0:
            pass
        test["test"]=nt.tests
        return test







class NaiveTestTranslator:
    def __init__(self):
        pass
    def translate(self,test):
        test_code=test["test"]
        tests=[]
        i=test_code.find("assert")
        j=0
        while True:
            j=test_code.find("assert",i+len("assert"))
            if j==-1:
                tests.append(self.parse_assert_statement(test_code[i:]))
                break
            tests.append(self.parse_assert_statement(test_code[i:j]))
            i=j
        test["test"]=tests
        return test
    def parse_assert_statement(self,statement):
        res={"input":None,"op":"==","output":None}
        #remove \n
        statement=statement.replace("\n","")
        index=self.findStrRear(statement,"assert candidate")
        if index!=-1:
            l,r=self.parse_input(statement,index)
            res["input"]=self.varTranslate(statement[l+1:r])
            res["op"],r=self.parse_op(statement,r+1)
            res["output"]=self.varTranslate(statement[r:])
        else:
            raise Exception("Not normal test")
        
        return res
    def parse_input(self,statement,start):
        l=r=start
        length=len(statement)
        if statement[l]!="(":
            raise Exception("Bad bracket")
        
        matched=0
        while r<length:
            if statement[r]=="(":
                matched+=1
            if statement[r]==")":
                matched-=1
            if matched==0:
                break
            r+=1
        if matched==0:
            return l,r
        else:
            raise Exception("bracket can not match")
    def parse_op(self,statement,start):
        operators=["=","<",">","!"]
        op=""
        index=start
        while index<len(statement):
            if statement[index]==" ":
                index+=1
            elif statement[index] in operators:
                op+=statement[index]
                index+=1                    
            else:
                break
        return op,index            


    @staticmethod
    def findStrRear(string,pattern,start=0):
        #return next char right behind the pattern string
        index=string.find(pattern,start)
        if index==-1:
            return -1
        return index+len(pattern)

    @staticmethod
    def varTranslate(string):
        string=string.replace("'",'"')
        string=string.replace("True","true")
        string=string.replace("False","false")
        return string

if __name__ == "__main__":
    tt=TestTranslator()
    