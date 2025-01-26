import pygame as pg
from utils import draw_text
from buildings import Building, TownCentre, House, Camp, Farm, Barracks, Stable, ArcheryRange, Keep

class Hud:
    def __init__(self, resource_manager, width, height):
        self.resource_manager = resource_manager
        self.width = width
        self.height = height

        self.hud_colour = (198, 155, 93, 175)

        # HUD surfaces
        self.resources_surface, self.resources_rect = self.create_surface(width, height * 0.02, (0, 0))
        self.build_surface, self.build_rect = self.create_surface(width * 0.15, height * 0.25, (self.width * 0.84, self.height * 0.74))
        self.select_surface, self.select_rect = self.create_surface(width * 0.3, height * 0.2, (self.width * 0.35, self.height * 0.79))

        # Define buildable buildings
        self.create_buildings()
        self.tiles = self.create_build_hud()  # Assign the returned value to self.tiles

        self.selected_tile = None
        self.examined_tile = None

    def create_surface(self, width, height, pos):
        """Helper method to create HUD surfaces."""
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill(self.hud_colour)
        surface_rect = surface.get_rect(topleft=pos)
        return surface, surface_rect


    def create_build_hud(self):
        """Creates HUD icons for buildings."""
        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5
        tiles = []
        cols = 3
        col_count = 0
        row_count = 0
        space = 10

        for building_name, building_info in self.building_classes.items():
            # Use resource_manager's images instead of loading again
            image = self.resource_manager.images.get(building_name)
            if image:
                image_scaled = self.scale_image(image.copy(), w=object_width)
                tile_x = render_pos[0] + col_count * (image_scaled.get_width() + space)
                tile_y = render_pos[1] + row_count * (image_scaled.get_height() + space)
                rect = image_scaled.get_rect(topleft=(tile_x, tile_y))
                tiles.append({
                    "name": building_name,
                    "icon": image_scaled,
                    "image": image,
                    "rect": rect,
                    "affordable": True  # No resource check yet
                })
                col_count += 1
                if col_count >= cols:
                    col_count = 0
                    row_count += 1

        return tiles  # Return the list of tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            print("Resetting selection")
            self.selected_tile = None

        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:  # Left click
                    self.selected_tile = tile
                    print(f"Selected building: {tile['name']} with size {tile['image'].get_width()}x{tile['image'].get_height()}")

    def draw(self, screen):
        """Draw the HUD and the selected building information."""
        screen.blit(self.resources_surface, (0, 0))  # Draw resources HUD
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))  # Draw build HUD

        if self.examined_tile:
            img_scaled = self.scale_image(self.examined_tile.image.copy(), h=self.select_rect.height * 0.7)
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            screen.blit(img_scaled, (self.width * 0.35 + 10, self.height * 0.79 + 40))
            draw_text(screen, self.examined_tile.name, 40, (255, 255, 255), (self.width * 0.35 + 10, self.height * 0.79))

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"].topleft)

    def scale_image(self, image, w=None, h=None):
        """Scale an image to the given width or height."""
        if not w and not h:
            return image  # No scaling provided
        if w and not h:
            scale = w / image.get_width()
            h = scale * image.get_height()
        elif h and not w:
            scale = h / image.get_height()
            w = scale * image.get_width()
        return pg.transform.scale(image, (int(w), int(h)))


    def create_buildings(self):
        """Stores references to building classes and their sizes."""
        self.building_classes = {
            "Town Centre": {
                "class": TownCentre,
                "size": (4, 4)
            },
            "House": {
                "class": House,
                "size": (2, 2)
            },
            "Camp": {
                "class": Camp,
                "size": (2, 2)
            },
            "Farm": {
                "class": Farm,
                "size": (2, 2)
            },
            "Barracks": {
                "class": Barracks,
                "size": (3, 3)
            },
            "Stable": {
                "class": Stable,
                "size": (3, 3)
            },
            "Archery Range": {
                "class": ArcheryRange,
                "size": (3, 3)
            },
            "Keep": {
                "class": Keep,
                "size": (3, 3)
            }
        }

    def load_image_for_building(self, building_name):
        try:
            image = pg.image.load(f"assets/graphics/{building_name.lower().replace(' ', '_')}.png").convert_alpha()
            self.images[building_name] = image
            return image
        except FileNotFoundError as e:
            print(f"Error loading image for {building_name}: {e}")
            return None
