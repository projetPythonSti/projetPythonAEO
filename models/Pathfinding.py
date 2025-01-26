import heapq

import numpy as np


class Pathfinding:
    def __init__(self, mapGrid, statingPoint, goal, debug=False):
        self.mapGrid = mapGrid
        self.startingPoint = statingPoint
        self.goal = goal
        self.debug = debug

    def logger(self,*args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def heuristic(self,a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


    ##############################################################################
    # path finding function
    ##############################################################################
        """_summary_
            self.mapGrid : map
            self.startingPoint : starting position
            self.goal : destination : position
        """
        
    def getGoal(self): return self.goal


    def checkIfOccupied(self, position):
        return self.mapGrid[position[0]][position[1]] != 1

    def checkNeighbors(self, position):
        finalPos = None
        direction = (self.goal[0]-self.startingPoint[0], self.goal[1]-self.startingPoint[1])
        if (direction[0] < 0) and (direction[0]<0) or (direction[0] < 0) and (direction[1] > 0): # Came from northeast, searching for accurate
            print("NORTHEAST or NORTHWEST or NORTH")
            finalPos = (self.goal[0],self.goal[1]-1) if self.checkIfOccupied((self.goal[0],self.goal[1]-1)) else None
            print("finalPOS now", finalPos)


        elif ((direction[0] > 0) and (direction[1] < 0)) or ((direction[0] < 0) and (direction[1] < 0)) or ((direction[0]==0) and (direction[1] < 0)) : # Came from south, searching for accurate position
            print("SOUTHEAST or SOUTHWEST or SOUTH")
            finalPos = (self.goal[0],self.goal[1]+1) if self.checkIfOccupied((self.goal[0],self.goal[1]+1)) else None
            print("finalPOS now", finalPos)

        elif (direction[0] < 0) and (direction[1] == 0):
            print("EAST")
            finalPos = (self.goal[0]-1,self.goal[1]) if self.checkIfOccupied((self.goal[0]-1,self.goal[1])) else None
            print("finalPOS now", finalPos)

        elif (direction[0] > 0) and (direction[1] == 0):
            print("West")
            finalPos = (self.goal[0] + 1, self.goal[1]) if self.checkIfOccupied((self.goal[0] + 1, self.goal[1])) else None
            print("finalPOS now", finalPos)

        if finalPos is None:
            print("Found no nearPath")
            xPos = -1
            yPos = -1
            while finalPos is None and xPos<=1 :
                finalPos = (self.goal[0] + xPos, self.goal[1] -yPos) if self.checkIfOccupied((self.goal[0]+xPos , self.goal[1]+yPos)) else None
                print("Xpos val : ", xPos, "Ypos val : ", yPos, "CIO : ",self.checkIfOccupied((self.goal[0]+xPos , self.goal[1]+yPos)))
                xPos += 1
                yPos += 1
            if finalPos is None:
                print("After all this search foundNoPaths")
            print("avant de partir, voici finalPos à la fin de checkNeighbors",finalPos)
            return finalPos
        return finalPos

    def astar(self):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # ,(1,1),(1,-1),(-1,1),(-1,-1)]
        close_set = set()
        came_from = {}
        gscore = {self.startingPoint: 0}
        fscore = {self.startingPoint: self.heuristic(self.startingPoint, self.goal)}
        oheap = []
        heapq.heappush(oheap, (fscore[self.startingPoint], self.startingPoint))
        if self.mapGrid[self.goal[0]][self.goal[1]]:
            print("VALUE NOT SHEKED")
            self.goal = self.checkNeighbors(self.goal)
            print("new goal value = ", self.goal)

        while oheap:

            current = heapq.heappop(oheap)[1]
            if current == self.goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)

                if 0 <= neighbor[0] < self.mapGrid.shape[0]:
                    if 0 <= neighbor[1] < self.mapGrid.shape[1]:
                        if self.mapGrid[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        # self.mapGrid bound y walls
                        continue
                else:
                    # self.mapGrid bound x walls
                    continue
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

        return False

    def maxfinding(self): #returns a list of tuples, calls astar if problem
        ()

#route = astar(grid, self.startingPoint, self.goal)
#route = route + [self.startingPoint]
#route = route[::-1]
#print(route)
##############################################################################
# plot the path
##############################################################################

# extract x and y coordinates from route list
x_coords = []
y_coords = []
'''for i in (range(0, len(route))):
    x = route[i][0]
    y = route[i][1]
    x_coords.append(x)
    y_coords.append(y)'''

# plot map and path
