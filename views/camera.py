import pygame as pg
from utils.setup import TILE_SIZE
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

pg.init()
class Camera:
    def __init__(self, largeur_fenetre, hauteur_fenetre):
        self.largeur = largeur_fenetre
        self.hauteur = hauteur_fenetre

        self.deplacement = pg.Vector2(0, 0)
        self.zoom = 1.0
        self.zoom_speed = 0.1
        self.vitesse = 15  # speed for panning (edge-scrolling or keyboard)

        # Internal dx/dy used each frame
        self.dx = 0
        self.dy = 0

    @property
    def scroll(self):
        """
        Returns camera displacement for compatibility with older code.
        """
        return self.deplacement

    def update(self):
        """
        - Edge-based scrolling (move if mouse near screen edges).
        - WASD-based movement (Q, D, S, Z in French keyboard).
        - Zoom in/out with UP/DOWN keys.
        """
        self.zoom_me()
        mouse_x, mouse_y = pg.mouse.get_pos()

        # Edge scrolling logic
        if mouse_x > self.largeur * 0.97:  # Right edge
            self.dx = -self.vitesse
        elif mouse_x < self.largeur * 0.03:  # Left edge
            self.dx = self.vitesse
        else:
            self.dx = 0

        if mouse_y > self.hauteur * 0.97:  # Bottom edge
            self.dy = -self.vitesse
        elif mouse_y < self.hauteur * 0.03:  # Top edge
            self.dy = self.vitesse
        else:
            self.dy = 0

        # Keyboard movement
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:  # left
            self.dx -= self.vitesse
        elif keys[pg.K_d]:  # right
            self.dx += self.vitesse
        if keys[pg.K_s]:   # down
            self.dy -= self.vitesse
        elif keys[pg.K_z]: # up
            self.dy += self.vitesse

        # Apply displacement
        self.deplacement.x += self.dx
        self.deplacement.y += self.dy

        logger.info(f"Camera displacement: {self.deplacement}, zoom: {self.zoom}")

    def zoom_me(self):
        """
        Zoom in/out with arrow keys. Clamp zoom between 0.1 and 3.0.
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.zoom *= (1.0 + self.zoom_speed)
        if keys[pg.K_DOWN]:
            self.zoom /= (1.0 + self.zoom_speed)
        self.zoom = max(0.1, min(3.0, self.zoom))

    def get_zoom(self) -> float:
        return self.zoom

    def iso_to_screen(self, iso_pos: pg.Vector2) -> tuple:
        """
        Convert isometric coordinates to screen coordinates, applying:
         - Isometric transform
         - Zoom
         - Camera displacement
         - Center offset (width/2, height/2)
        """
        # Apply diamond isometric transform first
        screen_x = (iso_pos.x - iso_pos.y) * (TILE_SIZE / 2)
        screen_y = (iso_pos.x + iso_pos.y) * (TILE_SIZE / 4)

        # Then apply zoom
        screen_x *= self.zoom
        screen_y *= self.zoom

        # Then add camera offset and center
        screen_x += self.deplacement.x + (self.largeur / 2)
        screen_y += self.deplacement.y + (self.hauteur / 2)

        # Convert to int for Pygame
        screen_x = int(screen_x)
        screen_y = int(screen_y)

        logger.info(
            f"iso_to_screen called with iso_pos: {iso_pos}, "
            f"Result => ({screen_x}, {screen_y})"
        )
        return (screen_x, screen_y)

    def screen_to_iso(self, screen_pos: tuple) -> pg.Vector2:
        """
        Inverse of iso_to_screen. 
        """
        sx = screen_pos[0] - (self.largeur / 2) - self.deplacement.x
        sy = screen_pos[1] - (self.hauteur / 2) - self.deplacement.y
        sx /= (TILE_SIZE / 2) * self.zoom
        sy /= (TILE_SIZE / 2) * self.zoom

        # diamond iso math
        iso_x = (sx + sy) / 2
        iso_y = (sy - sx) / 2

        return pg.Vector2(iso_x, iso_y)
