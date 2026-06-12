import re
def getNumberFromStr(s):
    match=re.search(r"\d+",s)
    if match:
        num=match.group()
        return int(num)
    return 0