import random
def generate():
    res=[[1,9],[4,7],[8,12],[125,15]]
    for i in range(10):
        res.append([random.randint(1,1e6),random.randint(1,1e6)])
    return res