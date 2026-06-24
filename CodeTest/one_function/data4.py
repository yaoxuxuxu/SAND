import random
def random_capital_letter():
    return chr(random.randint(ord("A"),ord("Z")))
def random_small_letter():
    return chr(random.randint(ord("a"),ord("z")))
def random_name():
    len1=random.randint(2,10)
    len2=random.randint(2,10)
    s=random_capital_letter()
    for _ in range(len1):
        s+=random_small_letter()
    s+=" "+random_capital_letter()
    for _ in range(len2):
        s+=random_small_letter()
    return s
def generate():
    res=[[14,"Mike",80],[15,"David",60]]
    for _ in range(10):
        age=random.randint(10,100)
        name=random_name()
        score=random.randint(0,100)
        res.append([age,name,score])
    return res

def test(param):
    code=f"""
import sys,os
sys.path.insert(0, os.getcwd())
sys.modules.pop("testcode", None)
sys.modules.pop("stdcode", None)
import testcode
import stdcode
test=testcode.fun({param})
std=stdcode.fun({param})
a=test.age==std.age
b=test.name==std.name
c=test.score==std.score
result = a and b and c
    """
    return code