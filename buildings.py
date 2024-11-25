
import pygame as pg



class Building:
    def __init__(self, pos, name, image_path, size):
        self.name = name  
        self.pos = pos
        if isinstance(image_path, str):
            #print(f"Loading image from path: {image_path}")
            self.image = pg.image.load(image_path).convert_alpha()  # Load the image here
        elif isinstance(image_path, pg.Surface):
            #print("Using pre-loaded surface")
            self.image = image_path  # Use the pre-loaded surface directly
        else:
            raise ValueError("Invalid image_path: Must be a file path or a pygame.Surface object") # Load the image here
        self.name = name
        #self.rect = self.image_path.get_rect(topleft=pos)
        #self.resource_manager = resource_manager
        #self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()
        #self.resource_type = resource_type  # The resource this building generates
        
        # Additional attributes for buildings
        #self.cost = cost  # Cost to build (e.g., {"Wood": 100})
       # self.build_time = build_time  # Time it takes to build in seconds
        #self.hp = hp  # Health Points of the building
        self.size = size  # Size of the building in tiles (e.g., "2x2")

        self.grid_x = None  # To be set when placed in the world
        self.grid_y = None

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

    def update(self):
        now = pg.time.get_ticks()
        #if now - self.resource_cooldown > 2000:  # 2-second cooldown to generate resource
            #self.resource_manager.resources[self.resource_type] += 1
            #self.resource_cooldown = now

    

class TownCentre(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Town Centre",
            image_path="assets/graphics/town_centre.png",
            resource_type="villagers",
            cost={"Wood": 350},
            build_time=150,
            hp=1000,
            size="4x4"
        )

class House(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="House",
            image_path="assets/graphics/house.png",
            resource_type="population",
            cost={"Wood": 25},
            build_time=25,
            hp=200,
            size="2x2"
        )

class Camp(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Camp",
            image_path="assets/graphics/camp.png",
            resource_type="resources",
            cost={"Wood": 100},
            build_time=25,
            hp=200,
            size="2x2"
        )

class Farm(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Farm",
            image_path="assets/graphics/farm.png",
            resource_type="food",
            cost={"Wood": 60},
            build_time=10,
            hp=100,
            size="2x2"
        )

class Barracks(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Barracks",
            image_path="assets/graphics/barracks.png",
            resource_type="swordsmen",
            cost={"Wood": 175},
            build_time=50,
            hp=500,
            size="3x3"
        )

class Stable(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Stable",
            image_path="assets/graphics/stable.png",
            resource_type="horsemen",
            cost={"Wood": 175},
            build_time=50,
            hp=500,
            size="3x3"
        )

class ArcheryRange(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Archery Range",
            image_path="assets/graphics/archery_range.png",
            resource_type="archers",
            cost={"Wood": 175},
            build_time=50,
            hp=500,
            size="3x3"
        )

class Keep(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            resource_manager=resource_manager,
            name="Keep",
            image_path="assets/graphics/keep.png",
            resource_type="defense",
            cost={"Wood": 35, "Gold": 125},
            build_time=80,
            hp=800,
            size="1x1",
            attack=5,
            range=8
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


