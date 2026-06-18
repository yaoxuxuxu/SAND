import random
def generate():
    res=[[0],[1],[2],[3],[99999]]
    for i in range(10):
        res.append([random.randint(3,int(1e6))])
    return res