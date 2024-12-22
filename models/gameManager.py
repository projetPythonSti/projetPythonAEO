from collections import defaultdict
from datetime import datetime

from pygame.examples.music_drop_fade import starting_pos

from models.Pathfinding import Pathfinding
from models.World import World
from models.unity.Unity import Unity


class GameManager:
        tick = datetime.today()
        unitToMove = defaultdict()
        '''
            Syntaxe du dictionnaire
            { 
                idUnité | idGroup : {
                            group : [idUnité1, idUnité2, idUnité3, idUnité4, idUnité5, idUnité6] // Si nous sommes dans le cadre d'un groupe d'unité à déplacer
                            moveQueue : [(0,1),  (0,2),  (1,2)] // représente la file des positions à suivre pour atteindre la destination
                            nextTile : (0,2) // représente la prochaine tuile dans laquelle doit se trouver le personnage (nécessaire car les personnages se déplacent à moins d'une tuile par seconde
                            currentPos : (0,2) // Représente la position actuelle
                           }
            } 
                    
        '''
        def __init__(self, speed, world: World ):
            self.gameSpeed = speed
            self.world = world

        def moveUnit(self):
            pass

        def checkUnitsToMove(self):
            for k in self.unitToMove:
                print(k.key)

        def addUnitToMoveDict(self, unit : Unity, destination):
            grid = self.world.convertMapToGrid()
            pathFinding  = Pathfinding(mapGrid=grid, statingPoint= (unit.position.getX(), unit.position.getY()), goal=(40,40))
            path = pathFinding.astar()
            if path.__class__ == bool:
                print("Found no short path")
            path = path + [pathFinding.startingPoint]
            path = path[::-1]
            self.unitToMove |= {unit.uid : path}



if __name__ == "__main__":
    pass

