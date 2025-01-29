import logging
from typing import Optional

import pygame as pg

from settings import TILE_SIZE

logger = logging.getLogger(__name__)


class Projectile(pg.sprite.Sprite):
    """
    A Projectile that travels from a start position to a target entity.
    Coordinates in 'pos' are isometric coordinates; screen coords 
    are handled by updating 'self.rect'.
    """
    def __init__(self, start_pos, target_entity, damage=10, speed=5, image=None):
        super().__init__()
        self.active = False
        self.last_active_time = 0

        # Load or assign the projectile image
        if isinstance(image, str):
            try:
                self.image = pg.image.load(image).convert_alpha()
                logger.info(f"Loaded projectile image from {image}")
            except FileNotFoundError:
                logger.error(f"Projectile image file not found: {image}")
                self.image = self._fallback_surface()
        elif isinstance(image, pg.Surface):
            self.image = image
        else:
            self.image = self._fallback_surface()
            logger.warning("Invalid image provided to Projectile. Using fallback surface.")

        self.rect = self.image.get_rect(center=start_pos)

        # Position and movement
        self.pos = pg.Vector2(start_pos)  # iso coords
        self.speed = speed
        self.damage = damage
        self.target_entity = target_entity

        # If you have a world reference for further collisions or interactions:
        self.world = None

    def _fallback_surface(self) -> pg.Surface:
        """
        Creates a simple 10x10 red surface for fallback usage.
        """
        surf = pg.Surface((10, 10), pg.SRCALPHA)
        surf.fill((255, 0, 0))
        return surf

    def activate(self, start_pos, target_entity, damage):
        """
        Resets or initializes the projectile for launch.
        """
        if isinstance(start_pos, (tuple, list, pg.Vector2)):
            self.pos = pg.Vector2(start_pos)
        else:
            logger.error("Invalid start_pos type. Must be tuple, list, or pygame.Vector2.")
            self.pos = pg.Vector2(0, 0)

        self.target_entity = target_entity
        self.damage = damage
        self.active = True
        self.last_active_time = pg.time.get_ticks()

        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if not isinstance(self.image, pg.Surface):
            logger.warning("Activated projectile has no valid image.")
        logger.info(
            f"Projectile activated at position: {self.pos}, "
            f"target: {getattr(self.target_entity, 'pos', None)}, damage: {self.damage}"
        )

    def update(self, dt: Optional[float] = None, camera=None):
        """
        Move the projectile toward the target if active. 
        Convert iso coords to screen coords for rendering/collision.
        """
        if not self.active or not self.target_entity or not self.target_entity.alive:
            self.deactivate()
            return

        # Calculate direction in iso space
        direction_vec = self.target_entity.pos - self.pos
        if direction_vec.length_squared() == 0:
            self.deactivate()
            return

        direction = direction_vec.normalize()
        movement = direction * self.speed
        if dt:
            movement *= dt

        self.pos += movement
        logger.info(f"Projectile moved to {self.pos}")

        # If we have a camera, convert iso -> screen and update rect
        if camera is not None:
            screen_x, screen_y = camera.iso_to_screen(self.pos)
            self.rect.center = (screen_x, screen_y)
        else:
            # If no camera is provided, just set rect based on iso coords
            self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Check if we hit the target (simple distance check)
        # Adjust threshold if needed
        if self.pos.distance_to(self.target_entity.pos) < 10 * TILE_SIZE:
            if hasattr(self.target_entity, "take_damage"):
                self.target_entity.take_damage(self.damage)
                logger.info(
                    f"Projectile hit {getattr(self.target_entity, 'name', 'Unknown')} "
                    f"for {self.damage} damage."
                )
            self.deactivate()

    def deactivate(self):
        """
        Deactivate and remove the projectile from all sprite groups.
        """
        self.active = False
        self.kill()

    def draw(self, screen):
        """
        Optional: if you want to individually draw the projectile
        (otherwise, rely on `Group.draw(screen)`).
        """
        screen.blit(self.image, self.rect)


class ProjectilePool:
    """
    Manages a pool of Projectile objects to avoid creating/destroying them constantly.
    """
    def __init__(self, max_projectiles, projectile_image=None):
        self.group = pg.sprite.Group()
        self.world = None  # Will be set externally if needed
        self.projectile_image = self._load_projectile_image(projectile_image)

        # Pre-create a pool of Projectiles
        for _ in range(max_projectiles):
            projectile = Projectile((0, 0), None, image=self.projectile_image)
            self.group.add(projectile)

    def _load_projectile_image(self, projectile_image):
        """
        Load the image from file or return the provided surface, 
        or fall back to a default if invalid.
        """
        if isinstance(projectile_image, str):
            try:
                loaded = pg.image.load(projectile_image).convert_alpha()
                logger.info(f"Loaded projectile image from {projectile_image}")
                return loaded
            except FileNotFoundError:
                logger.error(f"Projectile image file not found: {projectile_image}")
                return self._fallback_surface()
        elif isinstance(projectile_image, pg.Surface):
            return projectile_image
        else:
            logger.warning("Invalid projectile_image type. Using fallback surface.")
            return self._fallback_surface()

    def _fallback_surface(self):
        surf = pg.Surface((10, 10), pg.SRCALPHA)
        surf.fill((255, 0, 0))
        return surf

    def get_projectile(self, start_pos, target_entity, damage=10):
        """
        Retrieves an inactive projectile (or recycles the oldest).
        """
        for projectile in self.group:
            if not projectile.active:
                projectile.activate(start_pos, target_entity, damage)
                projectile.world = self.world
                return projectile

        # If all are active, recycle the oldest (the one with the earliest last_active_time)
        if len(self.group) > 0:
            oldest = min(self.group, key=lambda p: p.last_active_time)
            oldest.activate(start_pos, target_entity, damage)
            oldest.world = self.world
            return oldest
        else:
            # If somehow the group is empty, create a new projectile
            logger.warning("Projectile pool is empty. Creating a new projectile.")
            new_projectile = Projectile(start_pos, target_entity, damage=damage, image=self.projectile_image)
            new_projectile.activate(start_pos, target_entity, damage)
            new_projectile.world = self.world
            self.group.add(new_projectile)
            return new_projectile

    def update(self, dt: Optional[float] = None, camera=None):
        """
        Update all projectiles in the pool. Pass the camera so each projectile 
        can convert iso -> screen coords in its update method.
        """
        for projectile in self.group:
            if projectile.active:
                projectile.update(dt, camera=camera)

    def draw(self, screen):
        """
        If each projectile updates its rect correctly,
        we can draw via Group.draw(screen).
        """
        self.group.draw(screen)
