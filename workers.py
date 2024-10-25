import pygame as pg
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.node import GridNode  # Import GridNode directly

class Worker:
    def __init__(self, tile, world):
        self.world = world
        self.world.entities.append(self)  # Add worker to world entities list
        image = pg.image.load("assets/graphics/worker.png").convert_alpha()
        self.name = "worker"
        self.image = pg.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.tile = tile  # Current tile the worker occupies

        # Pathfinding initialization
        self.world.workers[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()  # Timer for movement delay
        self.path = []  # Initialize path to be empty
        self.path_index = 0  # Initialize path index

        self.create_path()  # Generate path on initialization

    def create_path(self):
        """Generates a new path for the worker to follow."""
        searching_for_path = True
        while searching_for_path:
            # Choose a random destination tile within the grid
            x = random.randint(0, self.world.grid_length_x - 1)
            y = random.randint(0, self.world.grid_length_y - 1)
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:  # Check if the destination is not blocked
                self.grid = Grid(matrix=self.world.collision_matrix)  # Create grid for pathfinding
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])  # Start at current tile
                self.end = self.grid.node(x, y)  # End at random destination

                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)  # A* pathfinder with no diagonal movement
                self.path, runs = finder.find_path(self.start, self.end, self.grid)  # Find path between start and end

                if self.path:  # Ensure the path is found
                    self.path_index = 0  # Reset path index
                    searching_for_path = False  # Exit the loop when a valid path is found

    def change_tile(self, new_tile):
        """Change the worker's tile to a new one after moving."""
        #print(f"self.tile['grid']: {self.tile['grid']}, type: {type(self.tile['grid'])}, length: {len(self.tile['grid'])}")
        #print(f"new_tile: {new_tile}, type: {type(new_tile)}")

        # Check if new_tile is a GridNode and extract its coordinates
        if isinstance(new_tile, GridNode):  # Directly check GridNode
            new_tile = [new_tile.x, new_tile.y]
            #print(f"Extracted coordinates from GridNode: {new_tile}")

        # Ensure current tile and new tile are valid 2-element lists or tuples
        if not isinstance(self.tile["grid"], (list, tuple)) or len(self.tile["grid"]) != 2:
            raise TypeError("self.tile['grid'] must be a list or tuple with 2 elements")
        if not isinstance(new_tile, (list, tuple)) or len(new_tile) != 2:
            raise TypeError("new_tile must be a list or tuple with 2 elements")

        # Update the world to reflect the worker's new position
        self.world.workers[self.tile["grid"][0]][self.tile["grid"][1]] = None  # Clear old tile
        self.world.workers[new_tile[0]][new_tile[1]] = self  # Set worker at the new tile
        self.tile = self.world.world[new_tile[0]][new_tile[1]]  # Update current tile reference

    def update(self):
        """Update worker's position on the grid at each time step."""
        now = pg.time.get_ticks()
        if now - self.move_timer > 1000 and self.path:  # If enough time has passed and path exists
            new_pos = self.path[self.path_index]  # Get next position in the path
            self.change_tile(new_pos)  # Move worker to the next tile
            self.path_index += 1  # Move to the next step in the path
            self.move_timer = now  # Reset move timer

            if self.path_index >= len(self.path):  # If the worker reaches the destination
                self.create_path()  # Generate a new path
