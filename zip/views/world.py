from models.buildings.buildings import Building 
from collections import defaultdict
from utils.setup import TILE_SIZE
from models.World import World
from models.Position import Position
from views.camera import Camera
import pygame as pg
import random
import noise
#from buildings import Building, TownCentre, House, Camp, Farm, Barracks, Stable, ArcheryRange, Keep, ProjectilePool, Projectile
import logging
logging.basicConfig(level=logging.DEBUG)  # Changed from INFO to DEBUG
logger = logging.getLogger(__name__)


class World_GUI:
    def __init__(self, entities, grid_width, grid_height, width, height, world:World):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.entities = entities
        self.height = height
        self.width = width
        self.hud = None
        self.world_model = world
        self.world = {}
        self.perlin_scale = grid_width / 2
        self.grid = [[None] * self.grid_width for _ in range(self.grid_height)]
        self.grass_tiles = pg.Surface((self.grid_width * TILE_SIZE * 2, self.grid_height * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tile_images = defaultdict(None) 
        self.all_withouth_ressources  = {**self.world_model.villages[0].population(), **self.world_model.villages[1].population()}  # Removed self.world_model.ressources
        self.all= {**self.world_model.villages[0].population(), **self.world_model.villages[1].population(), **self.world_model.ressources}
        #logger.debug(f"World_GUI: all entities: {self.all}")
        self.load_images()
        self.create_world()
        self.world_grid = self.world_model.filled_tiles
        self.i = 0
        self.keeps=[kv for k,v in self.all.items() for kv in v.values() if isinstance(kv, Building) and kv.name == "K"]
        
                
    def create_world(self):
        for grid_x in range(self.grid_width):
            for grid_y in range(self.grid_height):
                world_tile = self.grid_to_world(grid_x, grid_y)
                self.world[(grid_x, grid_y)] = world_tile
                render_pos = world_tile["render_pos"]
                tile = self.tile_images["grass"] if world_tile["tile"] != "eau" and world_tile["tile"] != "sable" else \
                    self.tile_images[world_tile["tile"]]
                self.grass_tiles.blit(tile, (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        
        # If you want to keep a return value, you can return self.world here
        # return self.world

    def grid_to_world(self, grid_x, grid_y):
        rect = [(grid_x * TILE_SIZE, grid_y * TILE_SIZE),
                (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
                (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
                (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min(x for x, _ in iso_poly)
        miny = min(y for _, y in iso_poly)

        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)

        if "w" in self.world_model.ressources and "g" in self.world_model.ressources:
            if (perlin >= 15) or (perlin <= -35):
                tile = "w"
            else:
                if r == 1:
                    tile = "F"
                elif r == 2:
                    tile = "eau"
                elif r == 3:
                    tile = "g"
                else:
                    tile = ""
        else:
            tile = ""
            
        
            
        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True,
            "projectiles": []  # Track projectiles on this tile
        }
        
        return out
  
    def load_images(self):
        # village1, village2 = self.world_model.villages
        # ressources = self.world_model.ressources
        
        for key, values in self.all.items():
            if len(values) > 0:
                self.load_image(key, list(values.values())[0])
        self.tile_images["grass"] = pg.image.load("assets/images/tilegraphic.png").convert_alpha()
        self.tile_images["eau"] = pg.image.load("assets/images/eau.png").convert_alpha()
        self.tile_images["K"] = pg.image.load("assets/images/buildings/K.png")
        self.tile_images["S"] = pg.image.load("assets/images/buildings/S.png")
        self.tile_images["A"] = pg.image.load("assets/images/buildings/A.png")
        self.tile_images["F"] = pg.image.load("assets/images/buildings/F.png")
        self.tile_images["projectile"] = pg.image.load("assets/images/buildings/projectile.png")
        self.tile_images["H"] = pg.image.load("assets/images/buildings/H.png").convert_alpha()
        self.tile_images["C"]= pg.image.load("assets/images/buildings/C.png")  # Added default image
        #self.tile_images["default"] = pg.image.load("assets/images/default.png").convert_alpha()  # Added default image
        # self.tile_images["sable"] = pg.image.load("assets/images/sable.png").convert_alpha()
        # self.tile_images["block"] = pg.image.load("assets/images/block.png").convert_alpha()
        # self.tile_images["tree"] = pg.image.load("assets/images/graphics/tree.png").convert_alpha()
        # self.tile_images["rock"] = pg.image.load("assets/images/graphics/rock.png").convert_alpha()
        
        
    def load_image(self, key, value):
        if key not in self.tile_images:
                try:
                    self.tile_images[key] = pg.image.load(value.image).convert_alpha()
                except FileNotFoundError:
                    print(f"No such file : {value.image}")
            

    def compute_screen_position(self, grid_x, grid_y):
        """
        Compute the screen position for a building based on grid position.
        """
        # Convert grid position to cartesian coordinates
        cart_x = grid_x * TILE_SIZE
        cart_y = grid_y * TILE_SIZE

        # Convert cartesian to isometric coordinates
        iso_x, iso_y = self.cart_to_iso(cart_x, cart_y)

        # Center the map
        screen_x = iso_x + self.grass_tiles.get_width() / 2
        screen_y = iso_y
        return screen_x, screen_y

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def iso_to_cart(self, iso_x, iso_y):
        cart_x = (2 * iso_y + iso_x) / 2
        cart_y = (2 * iso_y - iso_x) / 2
        return int(cart_x), int(cart_y)

    def is_entity_collision(self, grid_x, grid_y, size):
        size_x, size_y = size
        for entity in self.entities:
            if isinstance(entity, Building) and entity.alive:
                for (ox, oy) in entity.tiles_occupied:
                    for dx in range(size_x):
                        for dy in range(size_y):
                            if (grid_x + dx, grid_y + dy) == (ox, oy):
                                return True
        return False

    # def can_place_building(self, grid_x, grid_y, size):
    #     """Check if a building of given size can be placed at the grid position."""
    #     size_x, size_y = size
    #     if grid_x + size_x > self.grid_width or grid_y + size_y > self.grid_height:
    #         return False

    #     for dx in range(size_x):
    #         for dy in range(size_y):
    #             if not self.is_tile_available(grid_x + dx, grid_y + dy):
    #                 return False  # Tile is not available

    #     if self.is_entity_collision(grid_x, grid_y, size):
    #         return False  # Collision with existing entity

    #     return True
    def can_place_building(self, occupied_tiles, position, surface):
        return all(tile not in set(self.world_model.filled_tiles.values()) for tile in occupied_tiles) and surface[0] + position[0] <= self.grid_width and surface[1] + position[1] <= self.grid_height

    # def is_tile_available(self, x, y):
    #     if (x, y) not in self.world:
    #         return False
        
    #     # Check if there's already a building here
    #     if (x, y) in self.buildings:
    #         return False

    #     # Check if the tile is marked as a collision in the world (e.g., tree, rock)
    #     if self.world[(x, y)]["collision"]:
    #         return False

    #     return True

    def is_tile_available(self, position):
        if position not in self.world or position in self.world_model.filled_tiles:
            return False
        
        return True
    
    def select_tile(self, grid_pos):
        """Select a tile to place a worker or examine."""
        print(f"Selected tile: {grid_pos}")
        self.selected_tile = grid_pos

        # You can add further logic here, like placing a worker on the selected tile
        if self.hud and self.selected_tile:
            # ...existing code...
            pass

    def handle_tile_examination(self, mouse_pos, camera, mouse_action):
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera)
        if self.can_place_tile(grid_pos):
            building = self.buildings.get((grid_pos[0], grid_pos[1]))
            if mouse_action[0] and building is not None:
                self.examine_tile = grid_pos
                if self.hud:
                    self.hud.examined_tile = building

    def handle_mouse_right_click(self, mouse_action):
        if mouse_action[2]:
            self.examine_tile = None
            if self.hud:
                self.hud.examined_tile = None

    def handle_tile_selection(self, mouse_pos, camera, mouse_action):
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera)
        if self.can_place_tile(grid_pos):
            self.prepare_temp_tile(grid_pos)
            if mouse_action[0] and not self.world[grid_pos[0], grid_pos[1]]["collision"]:
                self.place_building(grid_pos)

    def prepare_temp_tile(self, grid_pos):
        img = self.hud.selected_tile["image"].copy()
        img.set_alpha(100)

        render_pos = self.world[grid_pos[0], grid_pos[1]]["render_pos"]
        iso_poly = self.world[grid_pos[0], grid_pos[1]]["iso_poly"]
        collision = self.world[grid_pos[0], grid_pos[1]]["collision"]

        self.temp_tile = {
            "image": img,
            "render_pos": render_pos,
            "iso_poly": iso_poly,
            "collision": collision
        }

    def can_place_tile(self, grid_pos):
        """Check if the tile can be placed and a building is selected."""
        if (0 <= grid_pos[0] < self.grid_width and
                0 <= grid_pos[1] < self.grid_height):
            if self.hud and self.hud.selected_tile is None:
                return False

            selected_building_name = self.hud.selected_tile["name"]
            if selected_building_name in self.hud.building_classes:
                building_info = self.hud.building_classes[selected_building_name]
                size_x, size_y = building_info["size"]
                return self.can_place_building(grid_pos[0], grid_pos[1], size=(size_x, size_y))
        return False

    def draw_grass_tiles(self, screen, camera):
        """Draw the grass tiles in the background."""
        scaled_grass_tiles = pg.transform.scale(
            self.grass_tiles,
            (
                int(self.grass_tiles.get_width() * camera.zoom),
                int(self.grass_tiles.get_height() * camera.zoom)
            )
        )
        # Adjust position according to zoom and scroll
        screen.blit(
            scaled_grass_tiles,
            (camera.scroll.x * camera.zoom, camera.scroll.y * camera.zoom)
        )

    # def draw_world_tiles(self, screen, camera):
    #     for x in range(self.grid_width):
    #         for y in range(self.grid_height):
    #             render_pos = self.world[x, y]["render_pos"]
    #             self.draw_world_tile(screen, render_pos, x, y, camera)

    # def draw_element(self, screen, camera, element):
    #     position = element.get_position()
    #     self.draw_world_tile(screen, self.world[position]["render_pos"], position, camera)
    
    # def draw_world_tile(self, screen, render_pos, position, camera):
    #     """Draw a single world tile at the specified position."""
    #     tile = self.world[position]["tile"]
    #     if tile != "":
    #         # Scale the tile image
    #         try:
    #             scaled_tile = pg.transform.scale(
    #                 self.tile_images[tile],
    #                 (
    #                     int(self.tile_images[tile].get_width() * camera.zoom),
    #                     int(self.tile_images[tile].get_height() * camera.zoom)
    #                 )
    #             )
    #             # Adjust position according to zoom and scroll
    #             screen.blit(
    #                 scaled_tile,
    #                 (
    #                     (render_pos[0] + self.grass_tiles.get_width() / 2) * camera.zoom + camera.scroll.x * camera.zoom,
    #                     (render_pos[1] - (self.tile_images[tile].get_height() - TILE_SIZE)) * camera.zoom + camera.scroll.y * camera.zoom
    #                 )
    #             )
    #         except KeyError:
    #             print("Clé non trouvé !")

    def draw(self, screen, camera):
            """Render the world, including buildings."""
            self.draw_grass_tiles(screen, camera)
            self.draw_entities(screen, camera)
            self.draw_buildings(screen, camera)
            # self.draw_large_image(screen, (0,0), pg.image.load("assets/images/buildings/T.png").convert_alpha(), camera)
            #self.draw_buildings(screen, camera)
            self.draw_hp_score(screen, camera)
            self.draw_projectiles(screen, camera)
            # for k in self.world_model.filled_tiles.keys():
            #     self.draw_on_map(screen, k, pg.image.load("assets/images/sable.png").convert_alpha(), camera)



    def draw_building(self, screen, building, camera, surf=None):
        """Single entry point to render buildings."""
        image = self.tile_images[building.get_name()]
        #logger.debug(f"Drawing building {building.get_name()} at position: {building.getTPosition()}") 
        self.draw_on_map(screen, building.getTPosition(), image, camera, surf)

    def draw_buildings(self, screen, camera):
        """Draw all the buildings in the world."""
        buildings_keys = {"A", "B", "C", "F", "H", "K", "S", "T"}
        buildings1 = {k: v for k, v in self.world_model.villages[0].population().items() if k in buildings_keys}
        buildings2 = {k: v for k, v in self.world_model.villages[1].population().items() if k in buildings_keys}
        
        # Draw first village's buildings
        for key1, group1 in buildings1.items():
            for b1 in group1.values():
                if issubclass(b1.__class__, Building):
                    #print(f"Drawing building {b1.name} at position: {b1.getTPosition()}")  # Added debug statement
                    self.draw_building(screen, b1,  camera, b1.surface)

        # Draw second village's buildings
        for key2, group2 in buildings2.items():
            for b2 in group2.values():
                if issubclass(b2.__class__, Building):
                    self.draw_building(screen, b2, camera, b2.surface)
    
    def draw_entities(self, screen, camera):
        unity_keys = {"a", "h", "s", "v"}
        units1 = {k:v for k, v in self.world_model.villages[0].population().items() if k in unity_keys}
        units2 = {k:v for k, v in self.world_model.villages[1].population().items() if k in unity_keys}
        
        for (k, ressources) in self.world_model.get_ressources().items():
            for (_, ressource) in ressources.items():
                if ressource:
                    image_key= ressource.get_name()
                    image = self.tile_images[image_key]
                    #print(f"Drawing ressource {image_key} at position: {ressource.getTPosition()}")  # Added debug statement
                    self.draw_on_map(screen, ressource.getTPosition(), image, camera)
        for k, h in units1.items():
            surface = 1 if k in "ah" else (2,2)
            for _, v in h.items():
                if h:
                    image_key = v.get_name()
                    image = self.tile_images[image_key] #Changed "default" to "grass"
                    self.draw_on_map(screen, v.getTPosition(), image, camera, surface)
        
        for k, h in units2.items():
            surface = 1 if k in "ah" else (2,2)
            for _, v in h.items():
                if h:
                    image_key = v.get_name()
                    image = self.tile_images[image_key]  # Changed "default" to "grass"
                    self.draw_on_map(screen, v.getTPosition(), image, camera, surface)
            
    
    def draw_on_map(self, screen, position, image, camera, surface=1, p=0):
        # ...existing code...
        #print(f"Rendering entity at position: {position}")  # Added debug statement
        
        # Scale grid positions by TILE_SIZE to convert to pixel coordinates
        cart_x = position[0] * TILE_SIZE  # Added scaling
        cart_y = position[1] * TILE_SIZE  # Added scaling
        
        # Convert scaled cartesian coordinates to isometric coordinates
        iso_x, iso_y = self.cart_to_iso(cart_x, cart_y)  # Use scaled coordinates
        minx = iso_x
        miny = iso_y
        render_pos = [minx, miny]
        
        if render_pos:
            # ...existing code...
            if surface == 1 or surface is None:
                scaled_image = pg.transform.scale(
                    image,
                    (
                        int(image.get_width() * camera.zoom),
                        int(image.get_height() * camera.zoom)
                    )
                )
            else:
                scaled_image = pg.transform.scale(
                    image,
                    (
                        int(image.get_width() * surface[0] * camera.zoom),
                        int(image.get_height() * surface[1] * camera.zoom)
                    )
                )
                
            # Adjust position according to zoom and scroll
            screen.blit(
                scaled_image,
                (
                    (render_pos[0] + self.grass_tiles.get_width() / 2) * camera.zoom + camera.scroll.x * camera.zoom,
                    (render_pos[1] - (image.get_height() - TILE_SIZE)) * camera.zoom + camera.scroll.y * camera.zoom
                )
            )
            # ...existing code...
        else:
            print("This position is out of the map")

    def draw_on_map_p(self, screen, position, image, camera, surface=1):
        cart_x = position[0] * TILE_SIZE
        cart_y = position[1] * TILE_SIZE

         # Convert cartesian to isometric coordinates
        iso_x, iso_y = self.cart_to_iso(cart_x, cart_y)
        render_pos = [iso_x, iso_y]
        
        if render_pos:
            # Scale the image if necessary (e.g., based on camera zoom)
            if surface == 1 or None:
                scaled_image = pg.transform.scale(
                    image,
                    (
                        int(image.get_width() * camera.zoom),
                        int(image.get_height() * camera.zoom)
                    )
                )
            else:
                #logger.debug(f"Scaling image {image.get_width} to surface: {surface}, camrera.zoom: {camera.zoom}")
                scaled_image = pg.transform.scale(
                    image,
                    (
                        int(image.get_width() * surface[0] * camera.zoom),
                        int(image.get_height() * surface[1]* camera.zoom)
                    )
                )
                
            # Adjust position according to zoom and scroll
            screen.blit(
                scaled_image,
                (
                    (render_pos[0] + self.grass_tiles.get_width() / 2) * camera.zoom + camera.scroll.x * camera.zoom,
                    (render_pos[1] - (image.get_height() - TILE_SIZE)) * camera.zoom + camera.scroll.y * camera.zoom
                )
            )
        else:
            print("This position is out of the map")

    def update(self, screen, camera, dt):
        """Update the world and its entities."""
        # self.draw(screen, camera)
        #self.update_projectiles(dt=dt)
        self.update_projectiles(dt=dt)
        # first_key, first_value = next(iter(self.world_model.filled_tiles.items()))
        # print(f"Key: {first_key}, Value: {first_value}")
        # print(f"type_key: {type(first_key)} , type_value: {type(first_value)}")
 
    def iso_to_grid(self, iso_x, iso_y):
        """Helper to convert iso coords back to grid coords."""
        cart_y = (2 * iso_y - iso_x) / 2
        cart_x = cart_y + iso_x
        return int(cart_x // TILE_SIZE), int(cart_y // TILE_SIZE)

    def find_closest_target(self, position: tuple[int, int], team: str):
        """
        Find the closest enemy entity with health to the given position using QuadTree.

        Parameters:
            position (tuple[int, int]): The (x, y) position of the searching entity.
            team (str): The team of the searching entity.

        Returns:
            Entity or None: The closest enemy entity or None if no enemy is found.
        """
        closest_entity, closest_dist = self.world_model.quad_tree.nearest_neighbor(position, team)
        #logger.debug(f"Closest entity: {closest_entity}, distance: {closest_dist}")
        if hasattr(closest_entity, "is_build") and not closest_entity.is_build:
            if hasattr(closest_entity, 'health') and closest_entity.health > 0:
                return closest_entity
        
        if not hasattr(closest_entity, "is_build") and hasattr(closest_entity, 'health') and closest_entity.health > 0:
            return closest_entity

        
    def remove_projectile_from_tile(self, projectile, old_grid_pos):
        """Remove a projectile from its old tile."""
        if old_grid_pos in self.world:
            tile_data = self.world[old_grid_pos]
            if projectile in tile_data["projectiles"]:
                tile_data["projectiles"].remove(projectile)

    def draw_projectiles(self, screen, camera):
        """
        Draw all active projectiles using their current positions.
        Ensure projectiles are within world boundaries and account for zoom.
        """
        for keep in self.keeps:
            for projectile in keep.projectile_pool.projectiles:
                if projectile.active:
                    self.draw_on_map_p(screen, projectile.position.toTuple(), projectile.image, camera, surface=(0.25, 0.25))
                    logger.debug(f"Draw projectile at position: {projectile.position.toTuple()}")
                    # # Check if projectile is within grid boundaries
                    # if (0 <= projectile.position.getX() < self.grid_width * TILE_SIZE and
                    #     0 <= projectile.position.getY() < self.grid_height * TILE_SIZE):
                    #     # Convert projectile's grid/world position to screen coords
                    #     screen_pos = self.compute_screen_position(
                    #         projectile.position.getX(),
                    #         projectile.position.getY()
                    #     )
                        
                    #     # Adjust for camera zoom & scroll
                    #     adjusted_x = (screen_pos[0] + camera.scroll.x) * camera.zoom
                    #     adjusted_y = (screen_pos[1] + camera.scroll.y) * camera.zoom

                    #     # Center the projectile image
                    #     projectile_rect = projectile.image.get_rect(center=(int(adjusted_x), int(adjusted_y)))
                        
                    #     screen.blit(projectile.image, projectile_rect)
                    #     logger.debug(f"Draw projectile at ({adjusted_x}, {adjusted_y})")
                    # else:
                    #    logger.debug(f"Projectile out of bounds: position={projectile.position}")

    def update_projectiles(self, dt: float):
        """Update all active projectiles and activate new ones towards closest targets."""
        for building in self.keeps:
            target = self.find_closest_target(building.position.toTuple(), building.team)
            if target:
                projectile = building.projectile_pool.get_projectile()
                if projectile and not projectile.active:
                    projectile.activate(
                        start_pos=building.position,
                        target_entity=target,
                        damage=building.damage,
                        speed=building.projectile_speed,
                        team=building.team,
                        image=self.tile_images["projectile"]
                    )
                    logger.debug(f"Projectile activated from {building.name} towards target {target}")
            building.projectile_pool.update(dt)  # Update cooldown timer and projectiles


    def create_collision_matrix(self):
        """Create a matrix for pathfinding where 1 indicates blocked tiles."""
        collision_matrix = []
        for x in range(self.grid_width):
            row = []
            for y in range(self.grid_height):
                # 1 if tile is collision, else 0
                row.append(1 if self.world[x, y]["collision"] else 0)
            collision_matrix.append(row)
        print("Collision Matrix:")
        for row in collision_matrix:
            print(row)
        return collision_matrix
    def mouse_to_grid(self, x, y, camera):
        """Convert mouse position to grid coordinates, accounting for zoom."""
        adjusted_x = (x - camera.scroll.x * camera.zoom - (self.grass_tiles.get_width() / 2) * camera.zoom) / camera.zoom
        adjusted_y = (y - camera.scroll.y * camera.zoom) / camera.zoom
        world_x = adjusted_x
        world_y = adjusted_y
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def place_building(self, grid_pos):
        """Place a building at the specified grid position if possible."""
        if self.hud and self.hud.selected_tile:
            selected_building_name = self.hud.selected_tile["name"]
            if selected_building_name in self.hud.building_classes:
                building_class = self.hud.building_classes[selected_building_name]["class"]
                # Pass the projectile image from ResourceManager
                if building_class.__name__ == "Keep":
                    building = building_class(
                        pos=self.world[grid_pos[0], grid_pos[1]]["render_pos"],
                        resource_manager=self.resource_manager,
                        world=self,
                        projectile_image=self.resource_manager.images.get("projectile")  # Added projectile_image
                    )
                else:
                    building = building_class(
                        pos=self.world[grid_pos[0], grid_pos[1]]["render_pos"],
                        resource_manager=self.resource_manager,
                        world=self
                    )
                print(f"Placing {building.name} at position: {building.pos}")  # Debug statement
                # Log grid and screen positions
                #logger.info(f"Placing {building.name} at grid position: {grid_pos}, screen position: {building.pos}")
                # Set grid_x and grid_y
                building.grid_x = grid_pos[0]
                building.grid_y = grid_pos[1]
                size_x, size_y = building.size
                print(f"Attempting to place {building.name} at ({grid_pos[0]}, {grid_pos[1]}) with size ({size_x}, {size_y})")  # Debug statement

                if self.can_place_building(grid_pos[0], grid_pos[1], size=building.size):
                    # Add the building to entities
                    self.entities.append(building)
                    building.update_tiles_occupied()

                    # Update the grid and collision status
                    for dx in range(size_x):
                        for dy in range(size_y):
                            self.buildings[(grid_pos[0] + dx, grid_pos[1] + dy)] = building  # Register occupied tiles
                            self.world[(grid_pos[0] + dx, grid_pos[1] + dy)]["collision"] = True
                    self.hud.selected_tile = None
                    print(f"Placed {building.name} successfully!")  # Debug statement
                    if isinstance(building, Keep):
                        logger.info(f"Keep {building.name} placed with projectile pool.")
                        # Remove the following line as we no longer add ProjectilePool to self.projectiles
                        # self.add_projectile_to_world(building.projectile_pool)
                else:
                    print(f"Cannot place {building.name} at ({grid_pos[0]}, {grid_pos[1]}): Collision or out of bounds.")  # Debug statement
        else:
            # Handle the case where hud is None or no tile is selected
            print("HUD is not initialized or no tile is selected.")

    def remove_building(self, building):
        """Remove a destroyed building from the world."""
        if building in self.entities:
            self.entities.remove(building)
            # Remove building from all occupied tiles
            for tile in building.tiles_occupied:
                if tile in self.buildings:
                    del self.buildings[tile]
                # Optionally, reset the collision status
                self.world[tile]["collision"] = False
            print(f"{building.name} has been removed from the world.")
        else:
            print(f"Error: {building.name} not found in entities.")

    def draw_hp_score(self, screen, camera):
            for category, entities in self.all_withouth_ressources.items():
                for b in entities.values():
                    if b.health > 0 and b.health < b.hp_max:
                        # Same positioning logic as in draw_building
                        building_render_pos = self.compute_screen_position(b.position.getX(), b.position.getY())
                        building_render_pos = (
                            (building_render_pos[0] + camera.deplacement.x) * camera.get_zoom(),
                            (building_render_pos[1] + camera.deplacement.y) * camera.get_zoom()
                        )
                        
                        # Retrieve the image Surface from tile_images using the building's name
                        image_key = b.name.lower()
                        image = self.tile_images.get(image_key, self.tile_images.get("grass"))
                        
                        offset_x = image.get_width() * camera.get_zoom()
                        offset_y = image.get_height() * camera.get_zoom()
                        building_render_pos = (
                            building_render_pos[0] - offset_x,
                            building_render_pos[1] - offset_y
                        )
                        
                        # Draw a simple HP bar
                        hp_ratio = b.health / b.hp_max  # Ensure correct attribute names
                        bar_width = 50
                        bar_height = 6
                        current_width = int(bar_width * hp_ratio)
                        bar_x = building_render_pos[0] + offset_x / 2 - bar_width / 2
                        bar_y = building_render_pos[1] - 10
                        pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                        pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_width, bar_height))

if __name__ == "__main__":
    pass
    pass