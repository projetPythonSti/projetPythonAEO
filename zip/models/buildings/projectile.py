import logging
from typing import Optional

import pygame as pg
import numpy as np
from models.Position import Position  # Added import
TILE_SIZE=32

logger = logging.getLogger(__name__)


class Projectile(pg.sprite.Sprite):
    """
    A Projectile that travels from a start position to a target entity.
    Coordinates in 'pos' are isometric coordinates; screen coords 
    are handled by updating 'self.rect'.
    """
    def __init__(self, start_pos: Position, target_entity, damage=10, speed=3, image: Optional[pg.Surface] = None):
        super().__init__()
        self.active = False
        self.damage = damage
        self.speed = speed
        self.target_entity = target_entity
        self.position = start_pos if start_pos else Position(0, 0)
        self.start_position = start_pos  # Added start_position
        self.team = None  # To be set when activated
        self.velocity_x = 0  # Added velocity_x
        self.velocity_y = 0  # Added velocity_y
        self.long_range_limit = None  # Added long_range_limit

        if image:
            self.image = image.copy()  # Use the provided image
            logger.debug(f"Projectile received external image: {type(self.image)}")
        else:
            self.image = self._fallback_surface()
            logger.warning("No image provided to Projectile. Using fallback surface.")
            logger.debug(f"Fallback surface assigned: {type(self.image)}")
        
        self.rect = self.image.get_rect(center=self.position.toTuple())
        logger.debug(f"Projectile rect initialized: {self.rect}")

    def _fallback_surface(self) -> pg.Surface:
        surface = pg.Surface((10, 10), pg.SRCALPHA)
        pg.draw.circle(surface, (255, 0, 0), (5, 5), 5)
        return surface
    
    
    def getTPosition(self):
        return self.position.toTuple()

    def activate(self, start_pos: Position, target_entity, damage, speed, team, image: Optional[pg.Surface] = None):
        if not isinstance(start_pos, Position):
            logger.error("Invalid start_pos provided to Projectile.activate(). Must be an instance of Position.")
            self.deactivate()
            return
        
        if start_pos.getX() is None or start_pos.getY() is None:
            logger.error("start_pos contains invalid coordinates.")
            self.deactivate()
            return

        self.position = Position(start_pos.getX(), start_pos.getY())  # Ensure position is a Position instance
        self.target_entity = target_entity
        self.damage = damage
        self.speed = speed        
        self.team = team
        self.active = True
        self.rect.center = self.position.toTuple()
        self.start_position = start_pos  # Added start_position
        
        if image:
            if isinstance(image, pg.Surface):
                self.image = image.copy()
                self.rect = self.image.get_rect(center=self.position.toTuple())
                logger.debug("Projectile image updated with external image.")
            else:
                logger.error(f"Provided image is not a Pygame Surface: {type(image)}. Using fallback surface.")
                self.image = self._fallback_surface()
                self.rect = self.image.get_rect(center=self.position.toTuple())
        else:
            logger.warning("No external image provided during activation. Using current image.")
        
        # Calculate velocity based on direction to target
        dx = self.target_entity.position.getX() - self.position.getX()
        dy = self.target_entity.position.getY() - self.position.getY()
        distance = np.hypot(dx, dy)
        self.long_range_limit = target_entity.position.distance_to(self.position) * 1.25
        if distance != 0:
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
            logger.debug(f"Projectile velocity set to ({self.velocity_x}, {self.velocity_y})")
        else:
            self.velocity_x = 0
            self.velocity_y = 0

        logger.info(f"Projectile activated: start_pos={self.position.toTuple()}, target_entity={target_entity}, damage={damage}, speed={speed}, team={team}, ")

    def move(self):
        if not self.active or self.target_entity is None:
            logger.debug("Projectile move called but inactive or no target.")
            return

        # Update position using velocity
        self.position.setX(self.position.getX() + self.velocity_x)
        self.position.setY(self.position.getY() + self.velocity_y)
        self.rect.center = self.position.toTuple()  # Update rect position
        logger.debug(f"Projectile moved to position {self.position.toTuple()}")

        # Removed life_time decrement from here
        # self.life_time -= 1 / self.speed  # Removed this line

        # if self.life_time <= 0:
        #     logger.info("Projectile life_time expired.")
        #     self.deactivate()
            
        # Check if projectile has crossed max range
        if self.position.distance_to(self.start_position) > self.long_range_limit:
            logger.info("Projectile exceeded long range limit.")
            self.deactivate()

        if self._has_reached_target():
            self.apply_damage()
            self.deactivate()



    def _has_reached_target(self):
        if self.target_entity.position is None:
            logger.debug("Projectile has no target.")
            return False
        reached = np.isclose(self.position.getX(), self.target_entity.position.getX(), atol=self.speed) and \
                  np.isclose(self.position.getY(), self.target_entity.position.getY(), atol=self.speed)
        #logger.debug(f"Checking if projectile has reached target: {reached}")
        return reached

    def apply_damage(self):

        if  self.target_entity.position  and not self.target_entity.is_destroyed() :  # Now valid for both Buildings and Unities
            self.target_entity.health -= self.damage
            logger.info(f"Projectile hit {self.target_entity.name}: Damage={self.damage}, Remaining Health={self.target_entity.health}")
            if self.target_entity.health <= 0:
                logger.warning(f"Target {self.target_entity.name} destroyed by projectile.")
                self.target_entity.destroy()  # Call the destroy method
        else:
            logger.warning("Projectile tried to apply damage but target is invalid or already destroyed.")

    def update(self, dt: Optional[float] = None, camera=None):
        if self.active:
            self.move()
            if dt:
                # self.life_time -= dt  # Decrement life_time based on delta time
                # logger.debug(f"Projectile life_time decreased by dt to {self.life_time}")
                # if self.life_time <= 0:
                if self.position.distance_to(self.start_position) > self.long_range_limit:
                    self.deactivate()
                    logger.info("Projectile deactivated due to long range limit.")
        # else:
        #     logger.debug("Updating inactive projectile.")

    def deactivate(self):
        self.active = False
        logger.info("Projectile deactivated.")

    def draw(self, screen, camera):
        """
        Removed the draw method to centralize drawing within World_GUI.
        """
        pass  # Drawing is handled by World_GUI.draw_projectiles

    def get_rect(self):
        """Returns the rect of the projectile."""
        return self.rect


class ProjectilePool:
    """
    Manages a pool of Projectile objects to avoid creating/destroying them constantly.
    """
    def __init__(self, max_projectiles, cooldown=5.0):
        self.projectiles = pg.sprite.Group()
        self.max_projectiles = max_projectiles
        self.cooldown = cooldown  # Cooldown period in seconds
        self.cooldown_timer = 0.0  # Timer to track cooldown
        self.active_projectiles = 0  # Track the number of active projectiles

        for _ in range(max_projectiles):
            projectile = Projectile(start_pos=None, target_entity=None)
            projectile.active = False
            self.projectiles.add(projectile)
            logger.debug("Added new projectile to pool.")

    def get_projectile(self) -> Optional[Projectile]:
        if self.cooldown_timer > 0:
            #logger.debug("ProjectilePool is in cooldown.")
            return None  # Prevent firing new projectiles during cooldown

        for projectile in self.projectiles:
            if not projectile.active:
                self.active_projectiles += 1
                if self.active_projectiles >= self.max_projectiles:
                    self.cooldown_timer = self.cooldown  # Start cooldown
                    self.active_projectiles = 0  # Reset active projectiles count
                return projectile
        return None  # No available projectiles

    def update(self, dt: Optional[float] = None, camera=None):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt  # Decrease cooldown timer
            if self.cooldown_timer < 0:
                self.cooldown_timer = 0  # Ensure timer doesn't go negative
        self.projectiles.update(dt=dt, camera=camera)
