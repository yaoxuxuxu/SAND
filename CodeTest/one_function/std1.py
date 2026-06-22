def fun(n):
    if n<2:
        return n
    pre=0
    now=1
    n-=1
    while n:
        pre,now=now,pre+now
        n-=1
    return now
