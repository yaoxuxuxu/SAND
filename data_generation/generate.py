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
class Problem:
    def __init__(self):
        self.problem_dir=problem_dir
        self.testcase_dir=testcase_dir
        self.solution_dir=solution_dir

        self.problem=utils.read_file(self.problem_dir)
        self.testcase=utils.load_module("testcase",self.testcase_dir).generate
        self.solution=utils.load_module("solution",self.solution_dir).solve
    def generate_testcase(self):
        return self.testcase()
    

class ProblemGenerator:
    def __init__(self):
        self.code_dir="./data_generation"
        self.prompts=PromptReader('./data_generation/prompts')
    def generate_problem(self):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(self.prompts.get("fun_completion"))
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
        mm.user_add(self.prompts.get("testcase_gen"))
        return self.get_markdown_retry(mm)
    def generate_solution(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(self.prompts.get("solution_gen"))
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
            test=self.problem.generate_testcase()
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
        if not self.check_generator_diversity():
            print("data is too easy")
            return False
        if not self.check_solvable():
            print("problem can not be solved")
            return False
        return True

class SandSolver():
    
    def __init__(self,problem=Problem()):
        #setting
        self.tmp_code_dir="tmp/sandcode.sand"
        self.check_iter=int(1e5)

        self.sandmodel=fewshot.patched_document
        self.problem=problem

    def main(self):
        model=self.sandmodel()
        model.user_add(self.problem.problem)
        while True:
            try:
                code=Parser().parse("sand",model.send(""))
                break
            except:
                print("format not correct from model!")
        utils.write_file(self.tmp_code_dir,code)
        se=SandEvaluator(code)
        for _ in range(self.check_iter):
            testcase=self.problem.testcase()
            testcase["funname"]="solve"
            status,message=se.check_all(mode="inout",args=testcase)
            if status != "pass":
                print("Wrong Answer",message,sep="\n")
                return False
        print("Accepted")
        return True

if __name__ == "__main__":
    pg=ProblemGenerator()
    pe=ProblemEvaluator()
    ss=SandSolver()
    pg.main()
    print(pe.main())
    ss.main()
    