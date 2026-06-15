import random
def generate():
    res=[[[5]],[[1,2,3,4]]]
    for _ in range(10):
        length=random.randint(20,1000)
        tmp=[]
        for _ in range(length):
            tmp.append(random.randint(100,10000))
        res.append([tmp])
    return res