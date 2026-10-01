from CodeGen.modelManager import ModelManager
from CodeGen.formatParser import Parser
from data_generation.promptReader import PromptReader
import data_generation.utils as utils
import json
from CodeGen import fewshot
from CodeTest.evaluator import SandEvaluator
import os

if not os.path.exists("data_generation/tmp"):
    os.mkdir("data_generation/tmp")

problem_dir="tmp/problem"
testcase_dir="tmp/testcase.py"
solution_dir="tmp/solution.py"
cornercase_dir="tmp/cornercase.json"
prompts=PromptReader('./data_generation/prompts')

class Problem:
    def __init__(self,problem=None,testcase=None,solution=None,cornercase=None):
        self._problem=problem
        self._testcase=testcase
        self._solution=solution
        self._cornercase=cornercase
    @property
    def problem(self):
        if self._problem==None:
            return utils.read_file(problem_dir)
        return self._problem
    @problem.setter
    def problem(self,problem):
        self._problem=problem
    @property
    def testcase(self):
        if self._testcase==None:
            return utils.load_module("testcase",testcase_dir).generate
        return self._testcase
    @testcase.setter
    def testcase(self,testcase):
        self._testcase=testcase
    @property
    def solution(self):
        if self._solution==None:
            return utils.load_module("solution",solution_dir).solve
        return self._solution
    @solution.setter
    def solution(self,solution):
        self._solution=solution
    @property
    def cornercase(self):
        return self._cornercase
    @cornercase.setter
    def cornercase(self,cornercase):
        self._cornercase=cornercase
class ProblemGenerator:
    def __init__(self,isGenerateCornerCase=True):
        self.code_dir="./data_generation"
        self.isGenerateCornerCase=isGenerateCornerCase
    def generate_problem(self):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(prompts.get("fun_completion"))
        res=mm.send("")
        return res
    def get_markdown_retry(self,mm,mode="python"):
        while True:
            try:
                res=mm.send("")
                res=Parser().parse(mode,res)
                break
            except KeyboardInterrupt:
                exit(0)
            except:
                mm.history=mm.history[:-1]
        return res
    def generate_testcase(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(prompts.get("testcase_gen"))
        return self.get_markdown_retry(mm)
    def generate_cornercase(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(prompts.get("corner_case_gen"))
        cornercase=self.get_markdown_retry(mm,mode="json")
        return cornercase
    def generate_solution(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(prompts.get("solution_gen"))
        return self.get_markdown_retry(mm)
    def main(self):
        print("Generating problem ...")
        problem=self.generate_problem()
        testcase=self.generate_testcase(problem)
        solution=self.generate_solution(problem)
        cornercase=None

        utils.write_file(problem_dir,problem)
        utils.write_file(testcase_dir,testcase)
        utils.write_file(solution_dir,solution)
        if self.isGenerateCornerCase:
            cornercase=self.generate_cornercase(problem)
            utils.write_file(cornercase_dir,json.dumps(cornercase))

        testcase=utils.load_module("testcase",testcase_dir).generate
        solution=utils.load_module("solution",solution_dir).solve
        p=Problem(problem,testcase,solution,cornercase)
        print("Problem generated!")
        return p

class ProblemEvaluator:
    def __init__(self,problem=None):
        #setting
        self.check_iter=int(300)
        self.min_data_space=int(15)
        self.problem=Problem() if problem==None else problem
        

    def check_generator_diversity(self):
        cnt={}
        for _ in range(int(self.check_iter)):
            test=self.problem.testcase()
            test=test["input"]
            test=json.dumps(test)
            cnt[test]=1
        return len(cnt)>self.min_data_space
    def check_testcase(self,testcase):
        stdin=testcase["input"]
        stdout=testcase["output"]
        
        testout=self.problem.solution(*stdin)
        if stdout!=testout:
            print("Wrong Answer on test case:",stdin,stdout,testout,sep="\n")
            return False
        return True
    def check_solvable(self):
        if self.problem.cornercase!=None:
            for testcase in self.problem.cornercase:
                if not self.check_testcase(testcase):
                    return False
            print("corner case passed!")

        for _ in range(self.check_iter):
            testcase=self.problem.testcase()
            if not self.check_testcase(testcase):
                return False
        print("normal testcase passed!")

            
        return True            
    def main(self):
        print("start diversity data checking")
        if not self.check_generator_diversity():
            print("data is too easy")
            return False
        print("start solvable checking")
        if not self.check_solvable():
            print("problem can not be solved")
            return False
        return True

class SandSolver():
    
    def __init__(self,problem=None):
        if problem==None:
            self.problem=Problem()
        else:
            self.problem=problem
            
        #setting
        self.tmp_code_dir="tmp/sandcode.sand"
        self.check_iter=int(1e3)

        self.sandmodel=fewshot.patched_document
    def test(self,code):
        se=SandEvaluator(code)
        if self.problem.cornercase!=None:
            for testcase in self.problem.cornercase:
                testcase["funname"]='solve'
                status,message=se.check_all(mode="inout",args=testcase)
                if status != "pass":
                    print("Wrong Answer",message,sep="\n")
                    return False,message
        for _ in range(self.check_iter):
            testcase=self.problem.testcase()
            testcase["funname"]="solve"
            status,message=se.check_all(mode="inout",args=testcase)
            if status != "pass":
                print("Wrong Answer",message,sep="\n")
                return False,message
        print("Accepted")
        return True,"Accepted"
    def generate(self,model=None):
        if model == None:
            model=self.sandmodel()
        model.user_add(self.problem.problem)
        while True:
            try:
                code=Parser().parse("sand",model.send(prompts.get("sand_solver")))
                break
            except KeyboardInterrupt:
                exit(0)
            except:
                print("format not correct from model!")
        utils.write_file(self.tmp_code_dir,code)
        return code
    def main(self):
        return self.pass_k_enhance(5)
    def pass_k(self,k):
        while k:
            code=self.generate()
            status,message=self.test(code)
            if status:
                return code
            k-=1
        return None
    def pass_k_enhance(self,k):
        model=self.sandmodel()
        while k:
            code=self.generate(model)
            status,message=self.test(code)
            if status:
                return True,code
            print(message)
            model.user_add(str(message))
            k-=1
        return False,message
        

if __name__ == "__main__":
    pe=ProblemEvaluator()
    pe.main()
    