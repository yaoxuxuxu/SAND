import random
def generate():
    res=[[0],[1],[2],[3],[9999]]
    for i in range(10):
        res.append([random.randint(3,int(1e4))])
    return res