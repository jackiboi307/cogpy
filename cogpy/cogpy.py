import os
import time as _time

class _cogpyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        
        
def _err(msg):
    raise _cogpyError(msg)
    
    
class draw:
    def __init__(self, console):
        self._console = console
        
    def pixel(self, pos, pixel):
        self._console._out[pos[1]][pos[0]][1] = str(pixel)


class Console:
    def __init__(self, size, bg=" ", flags=[]):
        self._out = [[[[], bg]] * size[0]] * size[1]
        self._clear = self._out
        
        self._size = size
        self._flags = flags
                
        self.draw = draw(self)
        
    def flip(self, renderer="r"):
        out = ""
        if renderer == "r":
            for y in self._out:
                for x in range(len(y)):
                    out += "".join(y[x][0])+y[x][1]+"\033[0m"
                if x != len(y) - 1: out += "\n"
            print(out, end="\r")
            
    def clear(self):
        self._out = self._clear
        
   
class time:
    @staticmethod
    def tick(fps):
        _time.sleep(1/fps)