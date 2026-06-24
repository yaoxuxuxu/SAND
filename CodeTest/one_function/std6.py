def fun(a,b):
    return a if b==0 else fun(b,a%b)
