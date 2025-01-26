# from resource_manager import ResourceManager
import timeit
from utils.setup import TILE_SIZE
from views.camera import Camera
from views.world import World_GUI
from views.menu import PlayPauseMenu
# from views.hud import Hud
import pygame as pg
import sys


class Game:

    def __init__(self, screen, clock, game_manager, players=None):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.entities = list()
        self.players = players if players else []
        self.game_manager = game_manager #maybe deleted, à revoir
        # self.resource_manager = ResourceManager() #have to be deleted
        # self.hud = Hud(self.resource_manager, self.width, self.height)
        # self.world = World(self.resource_manager, self.entities, self.hud, 50, 50, self.width, self.height)
        self.camera = Camera(self.width, self.height)
        self.world = World_GUI(self.entities, self.game_manager.world.width, self.game_manager.world.height, self.width, self.height, self.game_manager.world)
        self.BLACK, self.WHITE, self.RED = (0, 0, 0), (255, 255, 255), (255,  70,  70)
        self.playPauseMenu = PlayPauseMenu(self)
        self.playing = True      
           
    def run(self):
        self.playing = True
        while self.playing:
            for a in self.players:
                a.playTurn()
            self.game_manager.checkUnitsToMove()
            self.game_manager.tick = timeit.default_timer()
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
                    self.playing = False
                    self.game_manager.html_generator()
                    self.playPauseMenu.run()
                

    def update(self, dt: float):
        self.camera.update()
        
        # self.hud.update()
        self.world.update(self.screen, self.camera, dt=dt)  # Pass both camera and dt

    def draw(self):
        self.screen.fill((0, 0, 0))
        #self.world.draw(self.screen, self.camera)
        self.world.draw(self.screen, self.camera)
        # self.draw_entities(self.screen , self.camera)
            
        # self.world.draw_buildings(self.screen, self.camera)
        #     # self.draw_large_image(self.screen, self.(0,0), pg.image.load("assets/images/buildings/T.png").convert_alpha(), camera)
        #     # self.draw_buildings(self.screen  , self.camera)
        # self.world.draw_hp_score(self.screen , self.camera)
        # self.world.draw_projectiles(self.screen  , self.camera)
        # # self.world.draw_grass_tiles(self.screen, self.camera)
        # self.world.draw_on_map(self.screen, (0, 0), pg.image.load("assets/images/buildings/K.png"), self.camera, (0.8,0.8))
        # self.world.draw_on_map(self.screen, 0, 1, pg.image.load("assets/images/sable.png"), self.camera)
        # self.world.draw_on_map(self.screen, (1, 119), pg.image.load("assets/images/sable.png"), self.camera)
        
        
        # self.hud.draw(self.screen)
        # for x in range(self.world.grid_width):
        #     for y in range(self.world.grid_height):
        #         # sq = self.world.world[(x,y)]["cart_rect"]
        #         # rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE, TILE_SIZE)
        #         # pg.draw.rect(self.screen, (0,0,255), rect, 1)
                
        #         sq = self.world.world[(x,y)]["iso_poly"]
        #         sq = [(x + self.width/2, y + self.height/4) for x, y in sq]
        #         pg.draw.polygon(self.screen, (0,0,255), sq, 1)
                
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
        

