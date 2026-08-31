from CodeGen.modelManager import ModelManager
import json
import os
from CodeGen.formatParser import Parser
import importlib
class ProblemGenerator:
    def __init__(self):
        self.code_dir="./data_generation"
        self.prompts=self.read_prompts("prompts")
    def read_prompts(self,dir):
        dir=os.path.join(self.code_dir,dir)
        try:
            with open(dir,"r+",encoding="utf-8") as fp:
                prompt=json.load(fp)
        except Exception as e:
            print("Can not read prompts\n",e)
        return prompt
    def generate_problem(self):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(self.prompts["fun_completion"])
        res=mm.send("")
        return res
    def generate_testcase(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(self.prompts["test_case_gen"])
        while True:
            try:
                res=mm.send("")
                res=Parser().parse("python",res)
                break
            except:
                mm.history=mm.history[:-1]
        return res
    def generate_solution(self,problem):
        mm=ModelManager("gemma-4-31b-it")
        mm.user_add(problem)
        mm.user_add(self.prompts["test_case_solve"])
    def testcase_generate(self):
        spec = importlib.util.spec_from_file_location("testcase", os.path.join(self.work_dir,"testcase.py"))
        testcase = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(testcase)
        return testcase.Generator().main()
    def write_file(self,dir,res):
        dir=os.path.join(self.code_dir,dir)
        with open(dir,"w+",encoding="utf-8") as fp:
            fp.write(res)
    def main(self):
        problem=self.generate_problem()
        testcase=self.generate_testcase(problem)

        self.write_file("problem",problem)
        self.write_file("testcase.py",testcase)
        
if __name__ == "__main__":
    pg=ProblemGenerator()
    pg.main()