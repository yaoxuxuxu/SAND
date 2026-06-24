def fun(a,b):
    a=num(a)
    b=num(b)
    if a==b:
        return "tie"
    if a-b==1 or a-b ==-2:
        return "win"
    return "lose"


def num(s):
    if s=="scissor":
        return 1
    elif s=="rock":
        return 2
    elif s=="paper":
        return 3
    return 0