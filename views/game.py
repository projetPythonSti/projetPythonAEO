# from resource_manager import ResourceManager
import timeit
from utils.setup import TILE_SIZE
from views.camera import Camera
from views.world import World_GUI
from views.menu import PlayPauseMenu
import pygame as pg
import sys


class Game:

    def __init__(self, screen, clock, game_manager, players=None):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.entities = list()
        self.players = players if players else []
        self.game_manager = game_manager
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
                if event.key == pg.K_TAB:
                    self.playing = False
                    self.playPauseMenu.run()
                

    def update(self):
        self.camera.update()
        

    def draw(self):
        self.screen.fill((0, 0, 0))
        #self.world.draw(self.screen, self.camera)
        self.world.draw(self.screen, self.camera)
        
                
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
        

