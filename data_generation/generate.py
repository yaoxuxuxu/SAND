from CodeGen.modelManager import ModelManager
from CodeGen.formatParser import Parser
from data_generation.promptReader import PromptReader
import data_generation.utils as utils
import json
from CodeGen import fewshot
from CodeTest.evaluator import SandEvaluator

problem_dir="tmp/problem"
testcase_dir="tmp/testcase.py"
solution_dir="tmp/solution.py"
prompts=PromptReader('./data_generation/prompts')

class Problem:
    def __init__(self):
        self.problem_dir=problem_dir
        self.testcase_dir=testcase_dir
        self.solution_dir=solution_dir

        self.problem=utils.read_file(self.problem_dir)
        self.testcase=utils.load_module("testcase",self.testcase_dir).generate
        self.solution=utils.load_module("solution",self.solution_dir).solve
    

class ProblemGenerator:
    def __init__(self):
        self.code_dir="./data_generation"
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
            except:
                mm.history=mm.history[:-1]
        return res
    def generate_testcase(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(prompts.get("testcase_gen"))
        return self.get_markdown_retry(mm)
    def generate_solution(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(prompts.get("solution_gen"))
        return self.get_markdown_retry(mm)
    def main(self):
        problem=self.generate_problem()
        testcase=self.generate_testcase(problem)
        solution=self.generate_solution(problem)

        utils.write_file(problem_dir,problem)
        utils.write_file(testcase_dir,testcase)
        utils.write_file(solution_dir,solution)


class ProblemEvaluator:
    def __init__(self):
        #setting
        self.check_iter=int(1e5)
        self.min_data_space=int(1e3)
        self.problem=Problem()
    def check_generator_diversity(self):
        cnt={}
        for _ in range(int(self.check_iter)):
            test=self.problem.testcase()
            test=test["input"]
            test=json.dumps(test)
            cnt[test]=1
        return len(cnt)>self.min_data_space
    def check_solvable(self):
        for _ in range(self.check_iter):
            testcase=self.problem.testcase()
            stdin=testcase["input"]
            stdout=testcase["output"]

            testout=self.problem.solution(*stdin)
            if stdout!=testout:
                print("Wrong Answer on test case:",stdin,stdout,testout,sep="\n")
                return False
            
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
    """pg=ProblemGenerator()
    pg.main()
    pe=ProblemEvaluator()
    print(pe.main())
    ss=SandSolver()
    ss.main()"""
    ss=SandSolver()
    #ss.main()
    ss.test(utils.read_file("tmp/sandcode.sand"))
    