class TestTranslator:
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
    s="what is book"
    index=tt.findStrRear(s,"is")
    print(index,s[index])
    