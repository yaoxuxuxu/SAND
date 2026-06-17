import time
from ..library import StandardLibrary
class Time(StandardLibrary):
    def __init__(self):
        super().__init__()
        
    def time(self):
        return time.time()