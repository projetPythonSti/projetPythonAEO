import pygame as pg
import random
import noise
from settings import TILE_SIZE
from buildings import Building, TownCentre, House, Camp, Farm, Barracks, Stable, ArcheryRange, Keep, ProjectilePool, Projectile
from workers import Worker  
from resource_manager import ResourceManager


import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class World:
    def __init__(self, resource_manager: ResourceManager, entities, hud, grid_length_x, grid_length_y, width, height):
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(grid_length_y)] for _ in range(grid_length_x)]

        self.perlin_scale = grid_length_x / 2

        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.resource_manager.images
        # Define self.world as an empty dictionary first
        self.world = {}
        self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = {}
        self.workers = {}
        # self.projectiles = []  # Remove this line as it's no longer needed

        self.temp_tile = None
        self.examine_tile = None

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

        # Log the transformation details
        logger.info(f"compute_screen_position called with grid_x: {grid_x}, grid_y: {grid_y}")
        logger.info(f"Cartesian coordinates: ({cart_x}, {cart_y}), Isometric coordinates: ({iso_x}, {iso_y})")
        logger.info(f"Screen coordinates: ({screen_x}, {screen_y})")

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

    def can_place_building(self, grid_x, grid_y, size):
        """Check if a building of given size can be placed at the grid position."""
        size_x, size_y = size
        if grid_x + size_x > self.grid_length_x or grid_y + size_y > self.grid_length_y:
            return False

        for dx in range(size_x):
            for dy in range(size_y):
                if not self.is_tile_available(grid_x + dx, grid_y + dy):
                    return False  # Tile is not available

        if self.is_entity_collision(grid_x, grid_y, size):
            return False  # Collision with existing entity

        return True

    def is_tile_available(self, x, y):
        if (x, y) not in self.world:
            return False

        # Check if there's already a building here
        if (x, y) in self.buildings:
            return False

        # Check if the tile is marked as a collision in the world (e.g., tree, rock)
        if self.world[(x, y)]["collision"]:
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
        if (0 <= grid_pos[0] < self.grid_length_x and
                0 <= grid_pos[1] < self.grid_length_y):
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
        # Scale the grass tiles surface
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

    def draw_world_tiles(self, screen, camera):
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x, y]["render_pos"]
                self.draw_world_tile(screen, render_pos, x, y, camera)

                # Debug grid lines
                cart_rect = self.world[x, y]["cart_rect"]
                iso_poly = [self.cart_to_iso(c[0], c[1]) for c in cart_rect]
                iso_poly_screen = [(int(c[0] + camera.scroll.x + self.grass_tiles.get_width() / 2),
                                    int(c[1] + camera.scroll.y)) for c in iso_poly]

                if self.world[x, y]["collision"]:
                    color = (255, 0, 0)  # Red outline if colliding
                else:
                    color = (0, 255, 0)  # Green outline if free

                pg.draw.polygon(screen, color, iso_poly_screen, 1)

    def draw_world_tile(self, screen, render_pos, x, y, camera):
        """Draw a single world tile at the specified position."""
        tile = self.world[x, y]["tile"]
        if tile != "":
            # Scale the tile image
            scaled_tile = pg.transform.scale(
                self.tiles[tile],
                (
                    int(self.tiles[tile].get_width() * camera.zoom),
                    int(self.tiles[tile].get_height() * camera.zoom)
                )
            )
            # Adjust position according to zoom and scroll
            screen.blit(
                scaled_tile,
                (
                    (render_pos[0] + self.grass_tiles.get_width() / 2) * camera.zoom + camera.scroll.x * camera.zoom,
                    (render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE)) * camera.zoom + camera.scroll.y * camera.zoom
                )
            )



    def update(self, camera, dt: float):
        """Update the game world state, handle input for building placement and examination."""
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        # Handle right-click to reset examined tile and HUD selection
        self.handle_mouse_right_click(mouse_action)
        
        # Reset temporary tile before handling new interactions
        self.temp_tile = None
        
        # If a building is selected in the HUD, handle its placement
        if self.hud and self.hud.selected_tile:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera)
            if self.can_place_tile(grid_pos):
                self.place_building(grid_pos)
        else:
            # Handle cases when HUD is None or no tile is selected
            pass  # Add any necessary logic here

        # Update buildings with delta time
        for entity in self.entities:
            if entity.alive and  isinstance(entity, Keep):
                entity.projectile_pool.update(dt, camera=camera)
                target = entity.find_closest_target()
                if target and target.alive:
                    #logger.info(f"{entity.name} at position {entity.pos} found target {target.name} at position {target.pos}.")
                    entity.attack(target)
                else:
                    logger.info(f"{entity.name} at position {entity.pos} found no valid targets to attack.")



    def find_closest_target(self, building):
        """
        Find the closest target for the given building.
        """
        closest = None
        min_distance = float('inf')
        for entity in self.entities:
            if not entity.alive:
                continue  # Skip inactive entities
            # Remove any exclusion; all entities can be targeted
            distance = building.pos.distance_to(entity.pos)
            if distance < building.range * TILE_SIZE and distance < min_distance:
                closest = entity  # Set the closest entity
                min_distance = distance  # Update the minimum distance
        if closest:
            print(f"{building.name} found target {closest.name} at distance {min_distance}")  # Debug statement
        else:
            print(f"{building.name} found no targets within range.")  # Debug statement
        return closest

    def create_world(self):
        # Fill the existing self.world dictionary
        for grid_x in range(self.grid_length_x):
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                self.world[(grid_x, grid_y)] = world_tile
                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        # If you want to keep a return value, you can return self.world here
        # return self.world

    def grid_to_world(self, grid_x, grid_y):
        rect = [(grid_x * TILE_SIZE, grid_y * TILE_SIZE),
                (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
                (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
                (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min(x for x, y in iso_poly)
        miny = min(y for x, y in iso_poly)

        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)

        if (perlin >= 15) or (perlin <= -35):
            tile = "tree"
        else:
            if r == 1:
                tile = "rock"
            elif r == 2:
                tile = "block"
            else:
                tile = ""

        return {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True,
            "projectiles": []  # Track projectiles on this tile
        }

    def remove_projectile_from_tile(self, projectile, old_grid_pos):
        """Remove a projectile from its old tile."""
        if old_grid_pos in self.world:
            tile_data = self.world[old_grid_pos]
            if projectile in tile_data["projectiles"]:
                tile_data["projectiles"].remove(projectile)

    def iso_to_grid(self, iso_x, iso_y):
        """Helper to convert iso coords back to grid coords."""
        cart_y = (2 * iso_y - iso_x) / 2
        cart_x = cart_y + iso_x
        return int(cart_x // TILE_SIZE), int(cart_y // TILE_SIZE)

    def draw_projectiles(self, screen, camera):
        """Draw all active projectiles with proper screen positioning."""
        for building in self.entities:
            if isinstance(building, Keep):
                building.projectile_pool.draw(screen)

    def update_projectiles(self, dt: float):
        """Update all active projectiles."""
        for building in self.entities:
            if isinstance(building, Keep):
                building.projectile_pool.update(dt)

    def create_collision_matrix(self):
        """Create a matrix for pathfinding where 1 indicates blocked tiles."""
        collision_matrix = []
        for x in range(self.grid_length_x):
            row = []
            for y in range(self.grid_length_y):
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

    # def draw(self, screen, camera):
    #     """Render the world, including buildings."""
    #     try:
    #         images["tree"] = pg.image.load("assets/graphics/tree.png").convert_alpha()
    #         images["rock"] = pg.image.load("assets/graphics/rock.png").convert_alpha()
    #         images["block"] = pg.image.load("assets/graphics/block.png").convert_alpha()
    #     except FileNotFoundError as e:
    #         print(f"Error loading image: {e}")
    #     return images

    def draw(self, screen, camera):
        """Render the world, including buildings."""
        self.draw_grass_tiles(screen, camera)
        self.draw_world_tiles(screen, camera)
        #print("Drawing buildings")
        self.draw_buildings(screen, camera)
        self.draw_hp_score(screen, camera)
        self.draw_projectiles(screen, camera)



    def draw_building(self, screen, building, camera):
        """Draw the building using its isometric position."""

        building_render_pos = self.compute_screen_position(building.grid_x, building.grid_y)

        # Apply camera displacement and zoom
        building_render_pos = (
            (building_render_pos[0] + camera.deplacement.x) * camera.get_zoom(),
            (building_render_pos[1] + camera.deplacement.y) * camera.get_zoom()
        )

        # Adjust for the building image size
        building_render_pos = (
            building_render_pos[0] - (building.image.get_width() * camera.get_zoom()),
            building_render_pos[1] - (building.image.get_height() * camera.get_zoom())
        )

        # Double the building image size and apply zoom
        doubled_building_image = pg.transform.scale(
            building.image,
            (
                int(building.image.get_width() * 2 * camera.get_zoom()),
                int(building.image.get_height() * 2 * camera.get_zoom())
            )
        )

        # Draw the doubled building image at the adjusted position
        screen.blit(doubled_building_image, building_render_pos)

        # ...existing code...

        # Render projectiles if the building has a projectile pool
        if hasattr(building, 'projectile_pool') and building.projectile_pool:
            logger.info(f"Drawing projectiles for {building.name}")
            building.projectile_pool.draw(screen)
            logger.info(f"Finished drawing projectiles for {building.name}")
        # ...existing code...
        

    def draw_buildings(self, screen, camera):
        """Draw all the buildings in the world."""
        for building in self.entities:
            if isinstance(building, Building):
                self.draw_building(screen, building, camera)


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
                logger.info(f"Placing {building.name} at grid position: {grid_pos}, screen position: {building.pos}")
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
        for b in self.entities:
            if isinstance(b, Building) and b.alive and b.hp < b.max_hp:
                # Same positioning logic as in draw_building
                building_render_pos = self.compute_screen_position(b.grid_x, b.grid_y)
                building_render_pos = (
                    (building_render_pos[0] + camera.deplacement.x) * camera.get_zoom(),
                    (building_render_pos[1] + camera.deplacement.y) * camera.get_zoom()
                )
                # Adjust for the building image dimensions
                offset_x = b.image.get_width() * camera.get_zoom()
                offset_y = b.image.get_height() * camera.get_zoom()
                building_render_pos = (
                    building_render_pos[0] - offset_x,
                    building_render_pos[1] - offset_y
                )
                # Draw a simple HP bar
                hp_ratio = b.hp / b.max_hp
                bar_width = 50
                bar_height = 6
                current_width = int(bar_width * hp_ratio)
                bar_x = building_render_pos[0] + offset_x / 2 - bar_width / 2
                bar_y = building_render_pos[1] - 10
                pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_width, bar_height))
        print("Drawing HP bars")