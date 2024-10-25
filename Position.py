

class Position:
    
    def __init__(self, x = 0, y = 0):
        self._x = x
        self._y = y
    
    def setX(self, x) : self._x = x
    def serY(self, y) : self._y = y
    
    def getX(self): return self._x
    def getY(self): return self._y