import pygame as pg
import random
import noise
from settings import TILE_SIZE
from buildings import Building
from workers import Worker  


class World:
    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):
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
        self.tiles = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.temp_tile = None
        self.examine_tile = None

    def compute_screen_position(self, render_pos, object_height, camera):
        """Compute the screen position of a tile or object based on camera position and object height."""
        return (
            render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
            render_pos[1] - (object_height - TILE_SIZE) + camera.scroll.y
        )

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def iso_to_cart(self, iso_x, iso_y):
        cart_x = (2 * iso_y + iso_x) / 2
        cart_y = (2 * iso_y - iso_x) / 2
        return int(cart_x), int(cart_y)

    def can_place_building(self, grid_x, grid_y, building):
        size_x, size_y = map(int, building.size.split('x'))
        if grid_x + size_x > self.grid_length_x or grid_y + size_y > self.grid_length_y:
            return False

        for dx in range(size_x):
            for dy in range(size_y):
                if not self.is_tile_available(grid_x + dx, grid_y + dy):
                    return False
        return True
    
    

    def is_tile_available(self, x, y):
        return (0 <= x < self.grid_length_x) and (0 <= y < self.grid_length_y) and self.grid[x][y] is None



    
    def select_tile(self, grid_pos):
        """Select a tile to place a worker or examine."""
        print(f"Selected tile: {grid_pos}")
        self.selected_tile = grid_pos

        # You can add further logic here, like placing a worker on the selected tile
        # Example:
        if self.selected_tile:
            worker = Worker(tile=self.world[grid_pos[0]][grid_pos[1]], world=self)
            self.workers[grid_pos[0]][grid_pos[1]] = worker

    def handle_tile_examination(self, mouse_pos, camera, mouse_action):
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if self.can_place_tile(grid_pos):
            building = self.buildings[grid_pos[0]][grid_pos[1]]
            if mouse_action[0] and building is not None:
                self.examine_tile = grid_pos
                self.hud.examined_tile = building

    def handle_mouse_right_click(self, mouse_action):
        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

    def handle_tile_selection(self, mouse_pos, camera, mouse_action):
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if self.can_place_tile(grid_pos):
            self.prepare_temp_tile(grid_pos)
            if mouse_action[0] and not self.world[grid_pos[0]][grid_pos[1]]["collision"]:
                self.place_building(grid_pos)

    def prepare_temp_tile(self, grid_pos):
        img = self.hud.selected_tile["image"].copy()
        img.set_alpha(100)

        render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
        iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
        collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]

        self.temp_tile = {
            "image": img,
            "render_pos": render_pos,
            "iso_poly": iso_poly,
            "collision": collision
        }



    def draw(self, screen, camera):
        """Render the world, including buildings."""
        #print("Drawing the world and buildings...")
        
        # Drawing grass tiles
        #print(f"Blitting grass tiles at camera scroll position ({camera.scroll.x}, {camera.scroll.y})")
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))
        
        drawn_buildings = set()  # To track drawn buildings

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]

                # Draw world tiles
                #print(f"Drawing world tile at grid ({x}, {y}) at render position {render_pos}")
                self.draw_world_tile(screen, render_pos, x, y, camera)

                # Draw buildings if they exist and haven't been drawn yet
                building = self.buildings[x][y]
                if building is not None and building not in drawn_buildings:
                    size_x, size_y = map(int, building.size.split('x'))

                    # Only draw the building once, at its top-left grid corner
                    if (x == building.grid_x and y == building.grid_y):
                        building_render_pos = self.compute_screen_position(render_pos, building.image.get_height(), camera)
                        
                        # Debugging: Print the render position and building details
                        print(f"Rendering {building.name} at grid ({x}, {y}) with size {building.size}. Screen position: {building_render_pos}")
                        
                        screen.blit(building.image, building_render_pos)

                        # Mark the building as drawn to prevent re-rendering
                        drawn_buildings.add(building)

                        # Print out that the building has been marked as drawn
                        print(f"{building.name} at grid ({x}, {y}) has been marked as drawn.")
                        
                        # Draw outline if examining the building
                        if self.examine_tile is not None and (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            print(f"Drawing outline for {building.name} at grid ({x}, {y})")
                            self.draw_building_outline(screen, building, render_pos, camera)
                    else:
                        print(f"Skipping drawing for building {building.name} at ({x}, {y}), not its top-left corner.")



    def draw_grass_tiles(self, screen, camera):
        """Draw the grass tiles in the background."""
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

    def draw_world_tile(self, screen, render_pos, x, y, camera):
        """Draw a tile at the given render position."""
        tile = self.world[x][y]["tile"]
        if tile != "":
            screen.blit(self.tiles[tile],
                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                        render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
            


    def draw_building(self, screen, building, render_pos, camera):
        """Draw the building at its render position."""
        building_render_pos = (
            render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
            render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y
        )
        screen.blit(building.image, building_render_pos)

    def draw_building_outline(self, screen, building, render_pos, camera):
        """Draw an outline around the building if it is being examined."""
        mask = pg.mask.from_surface(building.image).outline()
        mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y) for x, y in mask]
        pg.draw.polygon(screen, (255, 255, 255), mask, 1000)

    def update(self, camera):
        """Update the game world state, handle input for building placement and examination."""
        mouse_pos = pg.mouse.get_pos()  # Get the current mouse position
        mouse_action = pg.mouse.get_pressed()  # Check for mouse clicks (left, right, etc.)

        # Handle right-click to reset examined tile and HUD selection
        self.handle_mouse_right_click(mouse_action)
        
        # Reset temporary tile before handling new interactions
        self.temp_tile = None
        
        # If a building is selected in the HUD, handle its placement
        if self.hud.selected_tile:
            self.handle_tile_selection(mouse_pos, camera, mouse_action)
        else:
            # No building selected, handle examination of existing tiles
            self.handle_tile_examination(mouse_pos, camera, mouse_action)

        # Update all entities (buildings, workers, etc.)
        for entity in self.entities:
            entity.update()


    def create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        return world

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
                tile = "tree"
            elif r == 2:
                tile = "rock"
            else:
                tile = ""

        return {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True
        }

    def create_collision_matrix(self):
        return [[1 if not self.world[x][y]["collision"] else 0 for y in range(self.grid_length_y)] for x in range(self.grid_length_x)]

    def mouse_to_grid(self, x, y, scroll):
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def load_images(self):
        images = {}
        try:
            images["tree"] = pg.image.load("assets/graphics/tree.png").convert_alpha()
            images["rock"] = pg.image.load("assets/graphics/rock.png").convert_alpha()
            images["block"] = pg.image.load("assets/graphics/block.png").convert_alpha()
        except FileNotFoundError as e:
            print(f"Error loading image: {e}")
        return images

    def can_place_tile(self, grid_pos):
        """Check if the tile can be placed (e.g., no collision)."""
        if (0 <= grid_pos[0] < self.grid_length_x and
                0 <= grid_pos[1] < self.grid_length_y):
            tile = self.world[grid_pos[0]][grid_pos[1]]
            return not tile["collision"]
        return False



    def place_building(self, grid_pos):
        """Place the selected building at the specified grid position."""
        selected_building_name = self.hud.selected_tile["name"]

        if selected_building_name in self.hud.buildings:
            building_data = self.hud.buildings[selected_building_name]

            # Create the Building object
            ent = Building(
                pos=self.world[grid_pos[0]][grid_pos[1]]["render_pos"],
                name=building_data.name,
                image_path=building_data.image,
                size=building_data.size
            )

            # Set grid_x and grid_y for the building's top-left corner position
            ent.grid_x = grid_pos[0]
            ent.grid_y = grid_pos[1]

            # Debugging: Print the grid position and size of the building
            print(f"Attempting to place building {building_data.name} of size {building_data.size} at {grid_pos}")

            # Get the size of the building
            size_x, size_y = map(int, building_data.size.split('x'))

            # Check if we can place the building
            if self.can_place_building(grid_pos[0], grid_pos[1], building_data):
                self.entities.append(ent)

                # Mark all the tiles that the building occupies as "collision"
                for dx in range(size_x):
                    for dy in range(size_y):
                        if grid_pos[0] + dx < self.grid_length_x and grid_pos[1] + dy < self.grid_length_y:
                            self.buildings[grid_pos[0] + dx][grid_pos[1] + dy] = ent
                            self.world[grid_pos[0] + dx][grid_pos[1] + dy]["collision"] = True
                            print(f"Marking tile at ({grid_pos[0] + dx}, {grid_pos[1] + dy}) as occupied.")

                # Debugging: Confirm successful placement
                print(f"Successfully placed {building_data.name} at ({grid_pos[0]}, {grid_pos[1]})")

                # Reset the HUD after placement
                self.hud.selected_tile = None
            else:
                print(f"Cannot place {building_data.name} at {grid_pos}, collision detected or not enough space.")
