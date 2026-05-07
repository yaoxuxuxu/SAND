import os
from parser import Parser
from interpreter import Interpreter
import argparse
def read_file(dir):
    try:
        with open(dir,"r+") as fp:
            code=fp.read()
        return code
    except:
        print("No such file!!!")
        return -1
def showASTtree(parser):
    for i in parser.parse():
        print(i)
    return
def debug(result):
    asttree=result.getASTtree()
    print(asttree)
def main():
    console_parser=argparse.ArgumentParser()
    console_parser.add_argument("file")
    console_parser.add_argument("--tokenize", action="store_true")
    console_parser.add_argument("--asttree", action="store_true")
    console_parser.add_argument("--debug", action="store_true",help="Debug return each value of all the statement.")
    args=console_parser.parse_args()
    
    dir=args.file

    code=read_file(dir)
    if code==-1:
        return
    parser=Parser(code)
    itpt=Interpreter()

    if args.tokenize:
        tokens=parser.lexer.tokens
        for token in tokens:
            print(token)
        return
    if args.asttree:
        showASTtree(parser)
        return
    if args.debug:
        for i in parser.parse():
            result=itpt.eval(i)
            debug(result)
            print(result)
        return
    
    for i in parser.parse():
        itpt.eval(i)
main()

