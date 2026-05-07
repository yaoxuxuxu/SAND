import time
def fib(x):
    if x<2:
        return x
    return fib(x-1)+fib(x-2)
t=time.time()
print(fib(33))
print(time.time()-t)
