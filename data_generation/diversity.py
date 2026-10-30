from .llm_interface import ModelManager,fewshot
import json
from pathlib import Path
class DiversityMaker:
    def __init__(self):
        self.algorithm=problemlister
    def generate_prefix(self):
        prefix=""
        prefix+=self.algorithm.prefix()
        return prefix
    def generate_suffix(self):
        suffix=""
        suffix+=self.algorithm.suffix()
        return suffix
    def gonext(self,problem):
        self.algorithm.gonext(problem)

class ElementsMultiplier:
    def __init__(self):
        pass
class DocumentBase:
    def __init__(self):
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
    def prefix(self):
        return "do not generate a similar problem in this list: "+str(self.problemlist)+"\n\n\n"
    def suffix(self):
        return ""
    def gonext(self,problem):
        self.add(problem)
        self.write()
        return



problemlister=ProblemLister()
diversity_maker=DiversityMaker()
    
    
