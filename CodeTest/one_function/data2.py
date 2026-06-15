import random
def generate():
    res=[[[5]],[[2,4,3,1]]]
    for _ in range(5):
        length=random.randint(20,100)
        tmp=[]
        for _ in range(length):
            tmp.append(random.randint(100,10000))
        res.append([tmp])
    return res