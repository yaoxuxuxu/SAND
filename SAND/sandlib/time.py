import time
from ..library import StandardLibrary
class Time(StandardLibrary):
    def __init__(self):
        super().__init__()
        
    def time(self):
        return time.time()
    def date_stamp(self):
        date=""
        lt=time.localtime()
        date+=str(lt.tm_year)+"-"
        date+=str(lt.tm_mon)+"-"
        date+=str(lt.tm_mday)+" "

        date+=str(lt.tm_hour)+":"
        date+=str(lt.tm_min)+":"
        date+=str(lt.tm_sec)
        return date