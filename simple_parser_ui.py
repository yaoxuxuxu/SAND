import os
from parser import Parser
def cls():
    os.system("cls")
def pause():
    os.system("pause")
def main():
    cls()
    base_dir="./sand_code"
    codes=[]
    cnt=0
    for dir in os.listdir(base_dir):
        cnt+=1
        codes.append(os.path.join(base_dir,dir))
        print(str(cnt)+"\t"+dir)
    op=input()
    try:
        op=int(op)
        dir=codes[op-1]
    except:
        print("op out of range")
        pause()
        main()
        return
    print(dir)
    with open(dir,"r+") as fp:
        code=fp.read()
    parser=Parser(code)
    for i in parser.parse():
        print(i)
main()

