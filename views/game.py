# from resource_manager import ResourceManager
from utils.setup import TILE_SIZE
# from views.camera import Camera
# from views.world import World
# from views.hud import Hud
import pygame as pg
import sys


class Game:

    def __init__(self, screen, clock, game_manager):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.entities = list()
        self.game_manager = game_manager #maybe deleted, à revoir
        # self.resource_manager = ResourceManager() #have to be deleted
        # self.hud = Hud(self.resource_manager, self.width, self.height)
        # self.world = World(self.resource_manager, self.entities, self.hud, 50, 50, self.width, self.height)
        # self.camera = Camera(self.width, self.height)
        self.BLACK, self.WHITE, self.RED = (0, 0, 0), (255, 255, 255), (255,  70,  70)

    
    
    def run(self):
        self.playing = True
        while self.playing:
            dt = self.clock.tick(60) / 1000.0  # Calculate delta time in seconds
            self.events()
            self.update(dt)  # Pass delta time to update
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game_manager.pause()
                    self.game_manager.html_generator()
                    #temporaires
                    pg.quit()
                    sys.exit()
                

    def update(self, dt: float):
        return
        self.camera.update()
        # Update all entities to handle damage and other interactions
        for entity in self.entities:
            if entity.alive:
                entity.update()
        self.hud.update()
        self.world.update(self.camera, dt)  # Pass both camera and dt

    def draw(self):
        self.screen.fill((0, 0, 0))
        # self.world.draw(self.screen, self.camera)
        # self.hud.draw(self.screen)

        self.draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            self.WHITE
        )
        pg.display.flip()
    
    def draw_text(self, screen, text, size, colour, position=None):
        font = pg.font.SysFont(None, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        if position:
            text_rect.center = (position[0], position[1])
        screen.blit(text_surface, text_rect)
        

