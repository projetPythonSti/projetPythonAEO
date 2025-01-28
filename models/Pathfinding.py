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


    #heuristic(): Uses Euclidean distance as a heuristic.
    def heuristic(self, a, b):
        # Added checks for NoneType
        if a is None or b is None:
            self.logger("heuristic called with a or b as None")
            return float('inf')  # Assign a large heuristic value
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

    #checkIfOccupied(): Checks if a given position is occupied
    def checkIfOccupied(self, position):
        return self.mapGrid[position[0]-1][position[1]-1] != 1

    #checkNeighbors(): Attempts to find an alternative goal if the target is blocked.
    def checkNeighbors(self, position):
        finalPos = None
        direction = (self.goal[0]-self.startingPoint[0], self.goal[1]-self.startingPoint[1])
        if (direction[0] < 0) and (direction[0]<0) or (direction[0] < 0) and (direction[1] > 0): # Came from northeast, searching for accurate
            self.logger("NORTHEAST or NORTHWEST or NORTH")
            finalPos = (self.goal[0],self.goal[1]-1) if self.checkIfOccupied((self.goal[0],self.goal[1]-1)) else None
            self.logger("finalPOS now", finalPos)


        elif ((direction[0] > 0) and (direction[1] < 0)) or ((direction[0] < 0) and (direction[1] < 0)) or ((direction[0]==0) and (direction[1] < 0)) : # Came from south, searching for accurate position
            self.logger("SOUTHEAST or SOUTHWEST or SOUTH")
            finalPos = (self.goal[0],self.goal[1]+1) if self.checkIfOccupied((self.goal[0],self.goal[1]+1)) else None
            self.logger("finalPOS now", finalPos)

        elif (direction[0] < 0) and (direction[1] == 0):
            self.logger("EAST")
            finalPos = (self.goal[0]-1,self.goal[1]) if self.checkIfOccupied((self.goal[0]-1,self.goal[1])) else None
            self.logger("finalPOS now", finalPos)

        elif (direction[0] > 0) and (direction[1] == 0):
            self.logger("West")
            finalPos = (self.goal[0] + 1, self.goal[1]) if self.checkIfOccupied((self.goal[0] + 1, self.goal[1])) else None
            self.logger("finalPOS now", finalPos)

        if finalPos is None:
            self.logger("Found no nearPath")
            xPos = -1
            yPos = -1
            while finalPos is None and xPos<=1 :
                finalPos = (self.goal[0] + xPos, self.goal[1] -yPos) if self.checkIfOccupied((self.goal[0]+xPos , self.goal[1]+yPos)) else None
                self.logger("Xpos val : ", xPos, "Ypos val : ", yPos, "CIO : ",self.checkIfOccupied((self.goal[0]+xPos , self.goal[1]+yPos)))
                xPos += 1
                yPos += 1
            if finalPos is None:
                self.logger("After all this search foundNoPaths")
            self.logger("avant de partir, voici finalPos à la fin de checkNeighbors",finalPos)
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
        
        if self.goal is None:
            self.logger("Goal is None. Cannot perform pathfinding.")
            return False

        if self.mapGrid[self.goal[0]][self.goal[1]]:
            self.logger("Goal position is occupied. Searching for alternative goal.")
            self.goal = self.checkNeighbors(self.goal)
            if self.goal is None:
                self.logger("No valid alternative goal found.")
                return False
            self.logger("New goal value = ", self.goal)

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

    # Corrected jump_point_search method
    def jump_point_search(self):
        """
        Implements the Jump Point Search (JPS) algorithm for pathfinding on grid-based maps.
        """
        start = tuple(self.startingPoint)
        goal = tuple(self.goal)
        if not self.checkIfOccupied(goal):
            self.logger("Goal position is occupied. Searching for alternative goal.")
            goal = self.checkNeighbors(goal)
            if goal is None:
                self.logger("No valid alternative goal found.")
                return False
            self.logger("New goal value = ", goal)
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        closed_set = set()

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            closed_set.add(current)

            for successor in self.identify_successors(current, goal):
                if successor in closed_set:
                    continue
                tentative_gscore = gscore[current] + self.heuristic(current, successor)

                if successor not in gscore or tentative_gscore < gscore[successor]:
                    came_from[successor] = current  # Corrected from came_from[current] = current
                    gscore[successor] = tentative_gscore
                    fscore[successor] = tentative_gscore + self.heuristic(successor, goal)
                    heapq.heappush(open_set, (fscore[successor], successor))

        return False  # No path found

    def identify_successors(self, current, goal):
        """
        Identify all successors from the current position for JPS.
        """
        successors = []
        neighbors = self.get_neighbors(current)
        for direction in neighbors:
            jump_point = self.jump(current, direction, goal)
            if jump_point:
                successors.append(jump_point)
        return successors

    def jump(self, current, direction, goal):
        """
        Recursively jump in the specified direction to find jump points.
        """
        x, y = current
        dx, dy = direction
        next_pos = (x + dx, y + dy)

        if not self.is_within_bounds(next_pos) or not self.checkIfOccupied(next_pos):
            return None

        if next_pos == tuple(goal):
            return next_pos

        # Check for forced neighbors
        if self.has_forced_neighbors(next_pos, direction):
            return next_pos

        # Recursively continue in the direction
        return self.jump(next_pos, direction, goal)

    def has_forced_neighbors(self, pos, direction):
        """
        Check if the current position has any forced neighbors.
        """
        x, y = pos
        dx, dy = direction
        # Define orthogonal directions to check for forced neighbors
        if dx != 0 and dy != 0:
            # Diagonal movement
            if (self.checkIfOccupied((x - dx, y + dy)) and not self.checkIfOccupied((x - dx, y))) or \
               (self.checkIfOccupied((x + dx, y - dy)) and not self.checkIfOccupied((x, y - dy))):
                return True
        else:
            # Horizontal or vertical movement
            if dx != 0:
                if self.checkIfOccupied((x + dx, y + 1)) and not self.checkIfOccupied((x, y + 1)):
                    return True
                if self.checkIfOccupied((x + dx, y - 1)) and not self.checkIfOccupied((x, y - 1)):
                    return True
            elif dy != 0:
                if self.checkIfOccupied((x + 1, y + dy)) and not self.checkIfOccupied((x + 1, y)):
                    return True
                if self.checkIfOccupied((x - 1, y + dy)) and not self.checkIfOccupied((x - 1, y)):
                    return True
        return False

    def is_within_bounds(self, pos):
        """
        Check if the position is within the grid boundaries.
        """
        x, y = pos
        return 0 <= x < self.mapGrid.shape[0] and 0 <= y < self.mapGrid.shape[1]

    def get_neighbors(self, current):
        """
        Get possible movement directions from the current node.
        """
        x, y = current
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        return directions

    def astar_or_jps(self, use_jps=False):
        """
        Choose between A* and JPS algorithms based on the parameter.
        """
        if use_jps:
            return self.jump_point_search()
        else:
            return self.astar()


#route = astar(grid, self.startingPoint, self.goal)
#route = route + [self.startingPoint]
#route = route[::-1]
#self.logger(route)
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
