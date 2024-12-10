import pygame as pg
import random
import noise
from settings import TILE_SIZE
from buildings import Building, TownCentre, House, Camp, Farm, Barracks, Stable, ArcheryRange, Keep
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

    def can_place_building(self, grid_x, grid_y, size):
        """Check if a building of given size can be placed at the grid position."""
        size_x, size_y = size
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
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera)
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
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera)
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

    def can_place_tile(self, grid_pos):
        """Check if the tile can be placed and a building is selected."""
        if (0 <= grid_pos[0] < self.grid_length_x and
                0 <= grid_pos[1] < self.grid_length_y):
            if self.hud.selected_tile is None:
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
                render_pos = self.world[x][y]["render_pos"]
                self.draw_world_tile(screen, render_pos, x, y, camera)

                # Debug grid lines
                cart_rect = self.world[x][y]["cart_rect"]
                iso_poly = [self.cart_to_iso(c[0], c[1]) for c in cart_rect]
                iso_poly_screen = [(int(c[0] + camera.scroll.x + self.grass_tiles.get_width() / 2),
                                    int(c[1] + camera.scroll.y)) for c in iso_poly]
                pg.draw.polygon(screen, (255, 0, 0), iso_poly_screen, 1)

    def draw_world_tile(self, screen, render_pos, x, y, camera):
        """Draw a single world tile at the specified position."""
        tile = self.world[x][y]["tile"]
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

    def draw_building(self, screen, building, camera):
        """Draw the building using its isometric position."""
        # Compute the screen position
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

    def update(self, camera):
        """Update the game world state, handle input for building placement and examination."""
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

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

        # Remove redundant entity updates
        # for entity in self.entities:
        #     entity.update()
        
        # Debugging: Log the update call
        # print("World update called")

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
        collision_matrix = [[1 if not self.world[x][y]["collision"] else 0 for y in range(self.grid_length_y)]
                            for x in range(self.grid_length_x)]
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

    def load_images(self):
        images = {}
        try:
            images["tree"] = pg.image.load("assets/graphics/tree.png").convert_alpha()
            images["rock"] = pg.image.load("assets/graphics/rock.png").convert_alpha()
            images["block"] = pg.image.load("assets/graphics/block.png").convert_alpha()
        except FileNotFoundError as e:
            print(f"Error loading image: {e}")
        return images

    def draw(self, screen, camera):
        """Render the world, including buildings."""
        self.draw_grass_tiles(screen, camera)
        self.draw_world_tiles(screen, camera)
        self.draw_buildings(screen, camera)


    def draw_buildings(self, screen, camera):
        """Draw all the buildings in the world."""
        for building in self.entities:
            if isinstance(building, Building):
                # Ensure the building is placed at its top-left grid position
                if building.grid_x is not None and building.grid_y is not None:
                    self.draw_building(screen, building, camera)

    def place_building(self, grid_pos):
        """Place un bâtiment à l'emplacement spécifié si possible."""
        selected_building_name = self.hud.selected_tile["name"]
        if selected_building_name in self.hud.building_classes:
            building_class = self.hud.building_classes[selected_building_name]["class"]
            building = building_class(
                pos=self.world[grid_pos[0]][grid_pos[1]]["render_pos"],
                resource_manager=self.resource_manager
            )
            building.grid_x = grid_pos[0]
            building.grid_y = grid_pos[1]

            size_x, size_y = building.size
            print(f"Attempting to place {building.name} at ({grid_pos[0]}, {grid_pos[1]}) with size ({size_x}, {size_y})")

            if self.can_place_building(grid_pos[0], grid_pos[1], size=building.size):
                # Ajout du bâtiment aux entités
                self.entities.append(building)
                building.update_tiles_occupied()

                # Mettre à jour la grille et le statut de collision
                for dx in range(size_x):
                    for dy in range(size_y):
                        self.buildings[grid_pos[0] + dx][grid_pos[1] + dy] = building
                        self.world[grid_pos[0] + dx][grid_pos[1] + dy]["collision"] = True

                self.hud.selected_tile = None
                print(f"Placed {building.name} successfully!")
            else:
                print(f"Cannot place {building.name} at ({grid_pos[0]}, {grid_pos[1]}): Collision or out of bounds.")
