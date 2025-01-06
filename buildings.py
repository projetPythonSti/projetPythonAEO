import pygame as pg
from settings import TILE_SIZE  # Add this import
from projectile import Projectile, ProjectilePool  # Import Projectile classes
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import pygame as pg
from settings import TILE_SIZE

class Projectile:
    def __init__(self, start_pos, target_pos, speed=5):
        self.pos = pg.Vector2(start_pos)
        self.target = pg.Vector2(target_pos)
        self.speed = speed
        self.active = False

    def update(self):
        if not self.active:
            return

        # Move towards the target
        direction = (self.target - self.pos).normalize()
        self.pos += direction * self.speed

        # Deactivate if close to the target
        if self.pos.distance_to(self.target) < 5:
            self.active = False

    def draw(self, screen):
        if self.active:
            pg.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 5)

class ProjectilePool:
    def __init__(self, max_projectiles):
        self.pool = [Projectile((0, 0), (0, 0)) for _ in range(max_projectiles)]

    def get_projectile(self, start_pos, target_pos):
        for projectile in self.pool:
            if not projectile.active:
                projectile.pos = pg.Vector2(start_pos)
                projectile.target = pg.Vector2(target_pos)
                projectile.active = True
                return projectile
        return None  # No available projectile

    def update(self):
        for projectile in self.pool:
            if projectile.active:
                projectile.update()

    def draw(self, screen):
        for projectile in self.pool:
            projectile.draw(screen)


class Building:
<<<<<<< HEAD
    def __init__(
        self,
        pos,             # iso coords
        name,
        image,
        size,
        resource_manager=None,
        world=None,
        resource_type=None,
        cost=None,
        build_time=None,
        hp=None,
        attack_power=None,
        range_=None
    ):
        self.name = name
        self.pos = pg.Vector2(pos)  # iso coords
        # Ensure position is non-negative
        self.pos.x = max(self.pos.x, 0)
        self.pos.y = max(self.pos.y, 0)
        # Log initial position
        logger.info(f"Building {self.name} initialized at position: {self.pos}")
        if not isinstance(image, pg.Surface):
=======
    def __init__(self, pos, name, image, size, resource_manager=None, resource_type=None, cost=None, build_time=None, hp=None, attack_power=None, range_=None):
        self.name = name  
        self.pos = pg.Vector2(pos)
        if isinstance(image, pg.Surface):
            self.image = image  # Use the pre-loaded surface directly
        else:
>>>>>>> fabf5e0e59423b8c00684cd8858b44aa6406cf36
            raise ValueError("Invalid image: Must be a pygame.Surface object")
        self.image = image
        
        self.size = size
        self.grid_x = None
        self.grid_y = None
        self.tiles_occupied = []

        self.resource_manager = resource_manager
        self.resource_type = resource_type
        self.cost = cost
        self.build_time = build_time
        self.hp = hp
<<<<<<< HEAD
        self.max_hp = hp
        self.attack_power = attack_power
=======
        self.attack_power = attack_power  # Renamed from attack
>>>>>>> fabf5e0e59423b8c00684cd8858b44aa6406cf36
        self.range = range_
        self.world = world
        self.alive = True  # Track if the building is active

        # Scale the building image to fit the tile size if needed
        building_width = self.size[0] * TILE_SIZE
        building_height = self.size[1] * TILE_SIZE
        self.image = pg.transform.scale(self.image, (building_width, building_height))

    def update_tiles_occupied(self):
<<<<<<< HEAD
        """
        Update which tiles in the grid are occupied by this building, 
        based on (grid_x, grid_y) and (size).
        """
        if self.grid_x is None or self.grid_y is None:
            return
        self.tiles_occupied = [
            (self.grid_x + dx, self.grid_y + dy)
            for dx in range(self.size[0])
            for dy in range(self.size[1])
        ]
=======
        """Met à jour les cases occupées par ce bâtiment dans la grille."""
        if self.grid_x is not None and self.grid_y is not None:
            self.tiles_occupied = [
                (self.grid_x + dx, self.grid_y + dy)
                for dx in range(self.size[0])
                for dy in range(self.size[1])
            ]
            print(f"{self.name} occupies tiles: {self.tiles_occupied}")

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
>>>>>>> fabf5e0e59423b8c00684cd8858b44aa6406cf36

    def update(self):
        """
        By default, buildings might not do much here. 
        Derived classes can override or extend.
        """
        pass



    def take_damage(self, damage):
        """Apply damage to the building and handle its destruction."""
        self.hp -= damage
        self.hp = max(self.hp, 0)  # Prevent HP from going negative
        print(f"{self.name} took {damage} damage. Remaining HP: {self.hp}")  # Debug statement
        if self.hp == 0:
            print(f"{self.name} has been destroyed!")  # Debug statement
            self.destroy()

    def destroy(self):
        """Handle the destruction of the building."""
        # Notify the world to remove this building
        if self.world:
            self.world.remove_building(self)
        self.alive = False  # Mark the building as destroyed
        # Additional cleanup if necessary


class Keep(Building):
    def __init__(self, pos, resource_manager, world, projectile_image=None):
        image = resource_manager.images["Keep"]  
        super().__init__(
            pos=pos,
            name="Keep",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            world=world,
            resource_type=None,
            cost={"Wood": 35, "Gold": 125},
            build_time=80,
            hp=800,
            attack_power=30,
            range_=8
        )
        print(f"Keep initialized at position: {self.pos}")  # Debug statement
        self.attack_cooldown = 1000  # in ms
        self.last_attack_time = pg.time.get_ticks()  # Initialize to current time
        
        if projectile_image is not None and isinstance(projectile_image, pg.Surface):
            self.projectile_pool = ProjectilePool(30, projectile_image)
            print("ProjectilePool initialized with a valid image.")
        else:
            self.projectile_pool = ProjectilePool(30, None)
            print("Warning: Invalid projectile image provided. ProjectilePool initialized without an image.")
        
        # Assign the world reference to ProjectilePool
        self.projectile_pool.world = world  # Ensure ProjectilePool can access 'world'

    def attack(self, target):
        logger.info(f"{self.name} at position {self.pos} is attacking target {target.name} at position {target.pos}")
        now = pg.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = now
            projectile = self.projectile_pool.get_projectile(
                start_pos=self.pos,
                target_entity=target,
                damage=self.attack_power
            )
            if projectile:
                logger.info(f"Projectile launched from {self.pos} towards {target.pos}")
                # Ensure the projectile is properly activated
                projectile.activate(self.pos, target, self.attack_power)
            else:
                print(f"{self.name} could not fire a projectile: Pool is full.")

    def update(self, dt=None):
        pass

    def find_closest_target(self):
        """
        Example target-search logic. 
        We search in self.world.entities for the nearest building that isn't a Keep.
        """
        closest = None
        min_dist = float("inf")
        for entity in self.world.entities:
            # skip self & other keeps
            if entity is self or isinstance(entity, Keep):
                continue
            # measure distance in iso space (approx)
            dist = self.pos.distance_to(entity.pos)
            if dist < (self.range * TILE_SIZE) and dist < min_dist:
                closest = entity
                min_dist = dist
        if closest:
            # Debugging statement
            print(f"{self.name} found target {closest.name} at distance {min_dist}")
        else:
            print(f"{self.name} found no targets within range.")
        return closest

<<<<<<< HEAD
=======
class Keep(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            pos=pos,
            name="Keep",
            image=pg.image.load("assets/graphics/keep.png").convert_alpha(),
            size=(3, 3),
            resource_manager=resource_manager,
            resource_type=None,
            cost={"Wood": 35, "Gold": 125},
            build_time=80,
            hp=800,
            attack_power=5,  # Updated attribute name
            range_=8
        )
        self.attack_cooldown = 12 * 1000  # 5 attacks per minute
        self.last_attack_time = 0
        self.projectile_pool = ProjectilePool(10)

    def attack(self, target_pos):
        now = pg.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = now
            projectile = self.projectile_pool.get_projectile(
                start_pos=self.pos,
                target_pos=target_pos
            )
            if projectile:
                print(f"{self.name} fires a projectile at {target_pos}")

    def update(self):
        super().update()
        self.projectile_pool.update()

    def draw(self, screen):
        super().draw(screen)
        self.projectile_pool.draw(screen)

    def find_closest_target(self, entities):
        closest = None
        min_distance = float('inf')
        for entity in entities:
            if entity != self and not isinstance(entity, Keep):
                distance = self.pos.distance_to(entity.pos)
                if distance < self.range * TILE_SIZE and distance < min_distance:
                    closest = entity
                    min_distance = distance
        return closest
>>>>>>> fabf5e0e59423b8c00684cd8858b44aa6406cf36

class TownCentre(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["Town Centre"]
        super().__init__(
            pos=pos,
            name="Town Centre",
            image=image,
            size=(4, 4),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="villagers",
            cost={"Wood": 350},
            build_time=150,
            hp=1000
        )

class House(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["House"]
        super().__init__(
            pos=pos,
            name="House",
            image=image,
            size=(2, 2),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="population",
            cost={"Wood": 25},
            build_time=20,
            hp=200
        )

class Camp(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["Camp"]  # Use centralized image
        super().__init__(
            pos=pos,
            name="Camp",
            image=image,
            size=(2, 2),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="resources",
            cost={"Wood": 100},
            build_time=25,
            hp=200
        )

class Farm(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["Farm"]  # Use centralized image
        super().__init__(
            pos=pos,
            name="Farm",
            image=image,
            size=(2, 2),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="food",
            cost={"Wood": 60},
            build_time=10,
            hp=100
        )

class Barracks(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["Barracks"]  # Use centralized image
        super().__init__(
            pos=pos,
            name="Barracks",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="swordsmen",
            cost={"Wood": 175},
            build_time=50,
            hp=500
        )

class Stable(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["Stable"]  # Use centralized image
        super().__init__(
            pos=pos,
            name="Stable",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="horsemen",
            cost={"Wood": 175},
            build_time=50,
            hp=500
        )

class ArcheryRange(Building):
    def __init__(self, pos, resource_manager, world):
        image = resource_manager.images["Archery Range"]  # Use centralized image
        super().__init__(
            pos=pos,
            name="Archery Range",
            image=image,
            size=(3, 3),
            resource_manager=resource_manager,
            world=world,  # Pass world reference
            resource_type="archers",
            cost={"Wood": 175},
            build_time=50,
            hp=500
<<<<<<< HEAD
        )
=======
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
>>>>>>> fabf5e0e59423b8c00684cd8858b44aa6406cf36
