import os
import CodeTest.utils as utils
from CodeGen import fewshot,formatParser
from .stressTest import StressTester
class Tester:
    def __init__(self,test_dir):
        self.tests=self.getTests(test_dir)
        try:
            os.mkdir("./CodeTest/temp")
            print("made a 'temp' file")
        except:
            pass
        print("Test Start")
    def getTests(self,test_dir):
        prompts=[]
        stds=[]
        datas=[]
        for dir in os.listdir(test_dir):
            if "prompt" in dir:
                prompts.append(dir)
            elif "std" in dir:
                stds.append(dir)
            elif "data" in dir:
                datas.append(dir)
        prompts.sort(key=utils.getNumberFromStr)
        stds.sort(key=utils.getNumberFromStr)
        datas.sort(key=utils.getNumberFromStr)
        tests=[]
        for i in range(len(prompts)):
            #get prompt
            prompt=os.path.join(test_dir,prompts[i])
            with open(prompt,"r+") as fp:
                prompt=fp.read()
            #get std
            if i<len(stds):
                std=os.path.join(test_dir,stds[i])
                with open(std,"r+") as fp:
                    std=fp.read()
            else:
                std=None
            #get data
            if i<len(datas):
                data=os.path.join(test_dir,datas[i])
            else:
                data=None
            tests.append({"prompt":prompt,"std":std,"data":data})
        return tests
    def test_all_tests(self,model):
        count={"ok":0,"syntax_error":0,"runtime_error":0,"performance_error":0}
        result=[]
        codes=[]
        test_id=1
        for test in self.tests:
            print(f"Test {test_id}: start")
            res,code=self.test_once(test,model,str(test_id))
            #codes.append(code)
            if "OK" in res:
                status="ok"
            elif "Syntax" in res:
                status="syntax_error"
            elif "Runtime" in res:
                status="runtime_error"
            elif "Performance" in res:
                status="performance_error"
            else:
                raise Exception(res+"bad status")
            
            count[status]+=1
            result.append(status)
            print(f"Test {test_id}: {status}")
            test_id+=1
            
        print(count)
        print(result)
        return count,result
    def test_once(self,test,model,test_id=""):
        model=model()
        model.user_add(test['prompt'])
        sys_prompt="You can only use Programming language python." \
        "complete the code,We will test your code by calling `fun(xxxxxxx)`."\
        "You must provide a top-level function named `fun`."\
        "do not put it inside a class"\
        "do not write test or debug code for it." \
        "output as markdown format with name python"
        while 1:
            try:
                code=model.send(sys_prompt)
                if code==None:
                    print("Code Not Found")
                    continue
                code=formatParser.Parser().parse("python",code)
                break
            except Exception as e:
                print(str(e))
                print("code generation bug occur!! retrying")
        with open("./CodeTest/temp/generate"+test_id+".sand","w+") as fp:
            fp.write(code)
        try:
            self.run_test(code,test["std"],test["data"])
            return "OK!",code
        except Exception as e:
            return str(e),code
    def test_once_with_std(self,test,model,test_id=""):
        code=test["std"]
        with open("./CodeTest/temp/generate"+test_id+".sand","w+") as fp:
            fp.write(code)
        try:
            self.run_test(code,test["std"],test["data"])
            return "OK!",code
        except Exception as e:
            return str(e),code
    def test_format(self,code):
        try:
            compile(code, "<string>", "exec")
        except Exception as e:
            raise Exception("Syntax Error\n"+str(e))
        try:
            exec(code)
        except Exception as e:
            raise Exception("Runtime Error(before test)\n"+str(e))
    def run_test(self,code,std,data):
        self.test_format(code)
        try:
            result=StressTester(code,std,data).test()
        except:
            raise Exception("Runtime Error(when test)\n")
        if result!="Accepted":
            raise Exception("Performance not Correct"+result)

if __name__ == "__main__":
    test=Tester("CodeTest/one_function")
    result=test.test_all_tests(fewshot.perfect_document)

"""if __name__ == "__main__":
    test=Tester("CodeTest/one_function")
    result=test.test_once_with_std(test.tests[0],fewshot.baseline)
    print(result)"""