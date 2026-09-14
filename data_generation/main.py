from data_generation.generate import ProblemGenerator,ProblemEvaluator,SandSolver
import subprocess as sp
import time
import os
class DatesetGenerator:
    def __init__(self):
        #setting
        self.problem_dir="data_generation/tmp"
        self.output_dir="data_generation/dataset/"

        self.directory_init()
    def directory_init(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
    def copy_testcase(self,testid):
        patience=5
        while True:
            if patience==0:
                raise Exception("Failed to do some file operation")
            result=sp.run(["cp","-r",self.problem_dir,self.output_dir+str(testid)])
            if result.returncode==0:
                break
            time.sleep(0.1)
            patience-=1
    def main(self):
        problem_id=1
        while True:
            try:
                pg=ProblemGenerator()
                pg.main()
                pe=ProblemEvaluator()
                if not pe.main():
                    continue
                ss=SandSolver()
                status,message=ss.main()
                if not status:
                    continue
                self.copy_testcase(problem_id)
                print("problem generated id: "+str(problem_id))
            except:
                print("bug occured")
                continue
    def debug(self):
        ss=SandSolver()
        ss.main()


if __name__ =="__main__":
    dg=DatesetGenerator()
    dg.main()