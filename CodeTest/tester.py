from CodeGen import formatParser
class Tester:
    def __init__(self,model=None):
        #setting
        self.result_dir="./test_result.txt"
        #var
        self.model=model
        self.datasets=self.read_dataset()
        #status
        self.test_id=0
    def test(self,model):
        self.test_id=0
        self.model=model
        result=[]
        for test in self.datasets:
            res=self.test_once(test)
            result.append(res)
            self.test_id+=1
        with open(self.result_dir,"w+",encoding="utf-8") as fp:
            fp.write(str(result))
        return result
    def parse_markdown(self,mode,code):
        res=formatParser.Parser().parse(mode,code)
        return res
    def read_dataset(self):
        raise NotImplementedError("This method should be implemented in a subclass.")
    def test_once(self,test):
        raise NotImplementedError("This method should be implemented in a subclass.")
    
        
