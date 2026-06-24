def one_function_testcode(param):
    code=f"""
import sys,os
sys.path.insert(0, os.getcwd())
sys.modules.pop("testcode", None)
sys.modules.pop("stdcode", None)
import testcode
import stdcode
result=testcode.fun({param})==stdcode.fun({param})
"""
    return code