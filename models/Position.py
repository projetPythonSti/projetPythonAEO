class Position:
    """
        26/12/2024@tahakhetib : j'ai apporté des modifs sur ce que @amadou_yaya_diallo a écrit
            - Ajout d'une méthode toTuple() pour faciliter la conversion des positions en tuple

    """
    def __init__(self, x = 0, y = 0):
        self._x = x
        self._y = y
    
    def setX(self, x) : self._x = x
    def setY(self, y) : self._y = y
    
    def getX(self): return self._x
    def getY(self): return self._y
    def toTuple(self): return (self._x, self._y)
    def __repr__(self):
            return f"({self._x}, {self._y})"
    def __eq__(self, other): return self.getX() == other.getX() and self.getY() == other.getY()
    
    def __ne__(self, other): return self.getX() != other.getX() or self.getY() != other.getY()