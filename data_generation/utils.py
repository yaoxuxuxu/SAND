import importlib
import os
import multiprocessing as mp
from func_timeout import func_timeout,FunctionTimedOut

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
    except Exception as e:
        raise e   

