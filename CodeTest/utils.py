import re
import importlib.util
def getNumberFromStr(s):
    match=re.search(r"\d+",s)
    if match:
        num=match.group()
        return int(num)
    return 0
def loadModuleFromPythonFile(file):
    spec = importlib.util.spec_from_file_location( "_tmp_module", file) 
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module