import pygame as pg
from settings import TILE_SIZE  # Add this import

class Building:
    def __init__(self, pos, name, image, size, resource_manager=None, resource_type=None, cost=None, build_time=None, hp=None, attack=None, range_=None):
        self.name = name  
        self.pos = pos
        if isinstance(image, pg.Surface):
            self.image = image  # Use the pre-loaded surface directly
        else:
            raise ValueError("Invalid image: Must be a pygame.Surface object")
        self.size = size  # Ensure size is a tuple of integers

        # Correct the image scaling to match the building's size
        building_width = self.size[0] * TILE_SIZE
        building_height = self.size[1] * TILE_SIZE

        self.image = pg.transform.scale(self.image, (building_width, building_height))
        
        self.grid_x = None  # To be set when placed in the world
        self.grid_y = None
        self.tiles_occupied = []
        self.resource_manager = resource_manager
        self.resource_type = resource_type
        self.cost = cost
        self.build_time = build_time
        self.hp = hp
        self.attack = attack
        self.range = range_

    def update_tiles_occupied(self):
        """Met à jour les cases occupées par ce bâtiment dans la grille."""
        if self.grid_x is not None and self.grid_y is not None:
            self.tiles_occupied = [
                (self.grid_x + dx, self.grid_y + dy)
                for dx in range(self.size[0])
                for dy in range(self.size[1])
            ]
            print(f"{self.name} occupies tiles: {self.tiles_occupied}")

<<<<<<< HEAD
        # Attack-related attributes for defensive buildings like "Keep"
        #self.attack = attack  # Attack power (if the building can attack)
        self.range = range  # Attack range in tiles (if the building can attack)
        self.tiles_occupied = []


    
    def update_tiles_occupied(self):
        """Update the list of tiles occupied by this building based on grid_x and grid_y."""
        if self.grid_x is not None and self.grid_y is not None:
            self.tiles_occupied = [
                (self.grid_x + dx, self.grid_y + dy)
                for dx in range(self.size[0])
                for dy in range(self.size[1])
            ]
=======
>>>>>>> c9d4631 (Fixed size renderring and zoom working)

    def update(self):
        now = pg.time.get_ticks()
        # Uncomment and integrate resource management if needed
        # if now - self.resource_cooldown > 2000:  # 2-second cooldown to generate resource
        #     self.resource_manager.resources[self.resource_type] += 1
        #     self.resource_cooldown = now

    

class TownCentre(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/town_centre.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Town Centre",
            image=image,
            size=(4, 4),
            resource_manager=resource_manager,
            resource_type="villagers",
            cost={"Wood": 350},
            build_time=150,
            hp=1000
        )

class House(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/house.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="House",
            image=image,
            size=(2, 2),
            resource_manager=resource_manager,
            resource_type="population",
            cost={"Wood": 25},
            build_time=25,
            hp=200
        )

class Camp(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/camp.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Camp",
            image=image,
            size=(2, 2),
            resource_manager=resource_manager,
            resource_type="resources",
            cost={"Wood": 100},
            build_time=25,
            hp=200
        )

class Farm(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/farm.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Farm",
            image=image,
            size=(2, 2),
            resource_manager=resource_manager,
            resource_type="food",
            cost={"Wood": 60},
            build_time=10,
            hp=100
        )

class Barracks(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/barracks.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Barracks",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            resource_type="swordsmen",
            cost={"Wood": 175},
            build_time=50,
            hp=500
        )

class Stable(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/stable.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Stable",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            resource_type="horsemen",
            cost={"Wood": 175},
            build_time=50,
            hp=500
        )

class ArcheryRange(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/archery_range.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Archery Range",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            resource_type="archers",
            cost={"Wood": 175},
            build_time=50,
            hp=500
        )

class Keep(Building):
    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/keep.png").convert_alpha()
        super().__init__(
            pos=pos,
            name="Keep",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            resource_type="defense",
            cost={"Wood": 35, "Gold": 125},
            build_time=80,
            hp=800,
            attack=5,
            range_=8
        )


class Lumbermill:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/building01.png")
        self.image = image
        self.name = "lumbermill"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["wood"] += 1
            self.resource_cooldown = now



class Stonemasonry:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("assets/graphics/building02.png")
        self.image = image
        self.name = "stonemasonry"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["stone"] += 1
            self.resource_cooldown = now


