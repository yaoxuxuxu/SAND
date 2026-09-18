from data_generation.generate import ProblemGenerator,ProblemEvaluator,SandSolver
import subprocess as sp
import time
import os
class DatesetGenerator:
    def __init__(self):
        #setting
        self.problem_dir="data_generation/tmp"
        self.output_dir="data_generation/dataset/"
        self.testcase_cnt=1

        self.directory_init()
    def directory_init(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
            return
        for dir in os.listdir(self.output_dir):
            try:
                count=int(dir)
            except:
                continue
            self.testcase_cnt=max(self.testcase_cnt,count)
        return
    def copy_testcase(self):
        patience=5
        while True:
            if patience==0:
                raise Exception("Failed to do some file operation")
            result=sp.run(["cp","-r",self.problem_dir,self.output_dir+str(self.testcase_cnt)])
            if result.returncode==0:
                break
            time.sleep(0.1)
            patience-=1
    def main(self):
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
                self.copy_testcase()
                print("problem generated id: "+str(self.testcase_cnt))
            except Exception as e:
                print("bug occured:",e,sep="\n")
                continue
    def debug(self):
        ss=SandSolver()
        ss.main()


if __name__ =="__main__":
    dg=DatesetGenerator()
    dg.main()