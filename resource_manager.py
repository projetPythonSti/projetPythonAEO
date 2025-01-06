import pygame as pg

class ResourceManager:
    def __init__(self):
        # resources
        self.resources = {
            "Wood": 50000,
            "Stone": 10000,
            "Gold": 10000
        }

        #costs
        self.costs = {
            "Town Centre": {"Wood": 350},
            "House": {"Wood": 25},
            "Camp": {"Wood": 100},
            "Farm": {"Wood": 60},
            "Barracks": {"Wood": 175},
            "Stable": {"Wood": 175},
            "Archery Range": {"Wood": 175},
            "Keep": {"Wood": 35, "Gold": 125},
        }
        
        self.images = self.load_images()  # Initialize the images attribute

    def load_images(self):
        """Load all necessary game images and store them in a dictionary."""
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
            images["projectile"] = pg.image.load("assets/graphics/projectile.png").convert_alpha()  # Add projectile image
            images["Worker"] = pg.image.load("assets/graphics/worker.png").convert_alpha()  # Add Worker image
            print("Projectile image loaded successfully.")
            # Add any additional images as needed
        except FileNotFoundError as e:
            print(f"Error loading image: {e}")
        return images

    def apply_cost_to_resource(self, building):
        """Deduct the cost of building from available resources."""
        if building in self.costs:
            for resource, cost in self.costs[building].items():
                self.resources[resource] -= cost
        else:
            print(f"Error: Building {building} does not have defined costs.")

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable  # Fixed to return the correct affordability status

