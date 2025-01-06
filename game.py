import pygame as pg
import sys
from world import World
from settings import TILE_SIZE
from utils import draw_text
from camera import Camera
from hud import Hud
from resource_manager import ResourceManager
from workers import Worker


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # entities
        self.entities = []

        # resource manager
        self.resource_manager = ResourceManager()

        # hud
        self.hud = Hud(self.resource_manager, self.width, self.height)

        # world
        self.world = World(self.resource_manager, self.entities, self.hud, 50, 50, self.width, self.height)
        # for _ in range(10):
        #     worker = Worker(tile=self.world.world[25][25], world=self.world)
        #     #self.entities.append(worker)  # Add worker to entities

        # camera
        self.camera = Camera(self.width, self.height)

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
                    self.playing = False

    def update(self, dt: float):
        self.camera.update()
        # Update all entities to handle damage and other interactions
        for entity in self.entities:
            if entity.alive:
                entity.update()
        self.hud.update()
        self.world.update(self.camera, dt)  # Pass both camera and dt

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 10)
        )

        pg.display.flip()

