from .llm_interface import ModelManager,fewshot
import json
from pathlib import Path
class DiversityMaker:
    def __init__(self):
        pass
    def generate_prefix(self):
        prefix=""
        prefix+=problemlister.prompt()

        return prefix
    def generate_suffix(self):
        pass


class ProblemLister:
    def __init__(self):
        #setting
        self.savefile=Path("data_generation/problemlist.txt")
        #var
        self.problemlist=[]
        if self.savefile.exists():
            self.read
    def write(self):
        with open(self.savefile,"w+",encoding="utf-8") as fp:
            json.dump(self.problemlist,fp)
    def read(self):
        with open(self.savefile,"r",encoding="utf-8") as fp:
            self.problemlist=json.load(fp)
    def add(self,problem:str):
        problem="please summarize this problem in a few of words.\n\n"+problem
        problem=ModelManager().send(problem)
        self.problemlist.append(problem)
        self.write()
    def prompt(self):
        return "do not generate a similar problem in this list: "+str(self.problemlist)+"\n\n\n"




problemlister=ProblemLister()
diversity_maker=DiversityMaker()
    
    
