import pygame as pg
from utils import draw_text
from buildings import Building

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

        # Load images and define buildable buildings
        self.images = self.load_images()
        self.buildings = self.create_buildings()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None

    def create_surface(self, width, height, pos):
        """Helper method to create HUD surfaces."""
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill(self.hud_colour)
        surface_rect = surface.get_rect(topleft=pos)
        return surface, surface_rect


    def create_build_hud(self):
        """Creates the build HUD icons for buildings that have images."""
        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5
        tiles = []

        for image_name, image in self.images.items():
            building = self.buildings.get(image_name)
            if building:
                image_scaled = self.scale_image(image.copy(), w=object_width)
                rect = image_scaled.get_rect(topleft=render_pos.copy())
                tiles.append({
                    "name": image_name,
                    "icon": image_scaled,
                    "image": image,
                    "rect": rect,
                    "affordable": True  # No resource check yet
                })
                render_pos[0] += image_scaled.get_width() + 10

        return tiles
    
    def load_images(self):
        images = {}
        try:
            images["tree"] = pg.image.load("assets/graphics/tree.png").convert_alpha()
            images["rock"] = pg.image.load("assets/graphics/rock.png").convert_alpha()
            images["block"] = pg.image.load("assets/graphics/block.png").convert_alpha()
            images["Town Centre"] = pg.image.load("assets/graphics/town_centre.png").convert_alpha()
            images["House"] = pg.image.load("assets/graphics/house.png").convert_alpha()
            images["Camp"] = pg.image.load("assets/graphics/camp.png").convert_alpha()
            images["Farm"] = pg.image.load("assets/graphics/farm.png").convert_alpha()
            images["Barracks"] = pg.image.load("assets/graphics/barracks.png").convert_alpha()
            images["Stable"] = pg.image.load("assets/graphics/stable.png").convert_alpha()
            images["Archery Range"] = pg.image.load("assets/graphics/archery_range.png").convert_alpha()
            images["Keep"] = pg.image.load("assets/graphics/keep.png").convert_alpha()
        except FileNotFoundError as e:
            print(f"Error loading image: {e}")
        return images
    

    def update(self):
        """Allow selection of buildings without checking resources."""
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None  # Reset selection

        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:  # Left click
                    self.selected_tile = tile

    def draw(self, screen):
        """Draw the HUD and the selected building information."""
        screen.blit(self.resources_surface, (0, 0))  # Draw resources HUD
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))  # Draw build HUD

        if self.examined_tile:
            img_scaled = self.scale_image(self.examined_tile.image.copy(), h=self.select_rect.height * 0.7)
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            screen.blit(img_scaled, (self.width * 0.35 + 10, self.height * 0.79 + 40))
            draw_text(screen, self.examined_tile.name, 40, (255, 255, 255), self.select_rect.topleft)

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
        """Defines all the available buildings with their properties."""
        return {
            "Town Centre": Building(pos=(0, 0),  name="Town Centre",
                                    image_path="assets/graphics/town_centre.png", 
                                    size="4x4"),
            "House": Building(pos=(0, 0),  name="House",
                              image_path="assets/graphics/house.png", 
                               size="2x2"),
            "Camp": Building(pos=(0, 0),  name="Camp",
                             image_path="assets/graphics/camp.png", 
                              size="2x2"),
            "Farm": Building(pos=(0, 0),  name="Farm",
                             image_path="assets/graphics/farm.png", 
                              size="2x2"),
            "Barracks": Building(pos=(0, 0),  name="Barracks",
                                 image_path="assets/graphics/barracks.png", 
                                  size="3x3"),
            "Stable": Building(pos=(0, 0),  name="Stable",
                               image_path="assets/graphics/stable.png", 
                                size="3x3"),
            "Archery Range": Building(pos=(0, 0),  name="Archery Range",
                                      image_path="assets/graphics/archery_range.png", 
                                       size="3x3"),
            "Keep": Building(pos=(0, 0),  name="Keep",
                             image_path="assets/graphics/keep.png", 
                              size="1x1")
        }
