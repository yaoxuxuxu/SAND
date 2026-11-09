import importlib
import os
from func_timeout import func_timeout,FunctionTimedOut
from pathlib import Path
home_dir="data_generation"
def load_module(name, path):
    path=os.path.join(home_dir,path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def read_file(dir):
    dir=os.path.join(home_dir,dir)
    with open(dir,"r+",encoding="utf-8") as fp:
        res=fp.read()
    return res
def write_file(dir,res):
    dir=os.path.join(home_dir,dir)
    with open(dir,"w+",encoding="utf-8") as fp:
        fp.write(res)
    return
def run_with_timeout(fun,timeout,*args):
    try:
        res=func_timeout(timeout,fun,args)
        return res
    except FunctionTimedOut:
        print(str(fun.__name__)+" timeout!")
        return "Timeout"
    except Exception as e:
        raise e   

class TrainCase:
    def __init__(self,dir:str|Path):
        if isinstance(dir,str):
            dir=Path(dir)
        self.dir=dir
        self.load_data()
    def load_data(self):
        self.problem=(self.dir/"problem").read_text(encoding="utf-8")
        self.sandcode=(self.dir/"sandcode.sand").read_text(encoding="utf-8")

class DataLoader:
    def __init__(self,dir:str|Path):
        if isinstance(dir,str):
            dir=Path(dir)
        #var
        self.dir=dir
        self.datadir=self.reload()
        #init
    def isValidDataset(self,dirname):
        #just check dirname is a number
        try:
            int(dirname)
            return True
        except:
            return False
    def reload(self):
        data=[]
        for dir in os.listdir(self.dir):
            if self.isValidDataset(dir):
                data.append(dir)
        data=sorted(data,key=lambda x:int(x))
        return data
    def _load_data(self,dir):
        return TrainCase(self.dir/dir)
    def __getitem__(self, key):
        return self._load_data(self.datadir[key])
    def __iter__(self):
        for i in self.datadir:
            yield self._load_data(i)
    def __len__(self):
        return len(self.datadir)
    