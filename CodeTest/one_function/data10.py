import random
def generate():
    return [""]
def test(param):
    code=f"""
import sys,os
sys.path.insert(0, os.getcwd())
sys.modules.pop("testcode", None)
sys.modules.pop("stdcode", None)
import testcode
testcode.fun()
if os.path.exists("output.txt"):
    with open("output.txt","r") as fp:
        res=fp.read()
        if res=="hello world":
            result=True
        else:
            result=False
    os.remove("output.txt")
else:
    result=False
    """
    return code