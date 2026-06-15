import random
def generate():
    choice=["scissor","rock","paper"]
    res=[]
    for i in choice:
        for j in choice:
            res.append([i,j])
    return res
