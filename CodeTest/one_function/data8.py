import random
def generate():
    res=[[4],[100],[1900],[2016],[2000]]
    for i in range(10):
        res.append([random.randint(3,int(1e6))])
    return res