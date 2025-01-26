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
    def __init__(self, start_pos: Position, target_entity, damage=10, speed=5, image=None):
        super().__init__()
        self.active = False
        self.damage = damage
        self.speed = speed
        self.target_entity = target_entity
        self.position = start_pos if start_pos else Position(0, 0)
        self.team = None  # To be set when activated

        if image:
            self.image = image
        else:
            self.image = self._fallback_surface()
        self.rect = self.image.get_rect(center=self.position.toTuple())
        logger.debug(f"Initialized Projectile: position={self.position}, target={self.target_entity}, damage={damage}, speed={speed}")

    def _fallback_surface(self) -> pg.Surface:
        surface = pg.Surface((10, 10), pg.SRCALPHA)
        pg.draw.circle(surface, (255, 0, 0), (5, 5), 5)
        return surface

    def activate(self, start_pos: Position, target_entity, damage, speed, team):
        self.position = Position(start_pos.getX(), start_pos.getY())
        self.target = target_entity
        self.damage = damage
        self.speed = speed
        self.team = team
        self.active = True
        # Initialize movement towards target
        self.calculate_velocity()

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
        logger.info(f"Projectile activated: start_pos={self.position.toTuple()}, target_entity={target_entity}, damage={damage}, speed={speed}, team={team}, target_pos={target_entity.position.toTuple()}")

    def calculate_velocity(self):
        """Calculate the velocity vector towards the target entity."""
        if not self.target_entity:
            logger.error("No target entity to calculate velocity.")
            self.deactivate()
            return

        target_pos = self.target_entity.position
        dx = target_pos.getX() - self.position.getX()
        dy = target_pos.getY() - self.position.getY()
        distance = np.hypot(dx, dy)

        if distance == 0:
            logger.debug("Projectile is already at the target position.")
            self.velocity = (0, 0)
            return

        # Normalize the direction vector and multiply by speed
        self.velocity = (dx / distance * self.speed, dy / distance * self.speed)
        logger.debug(f"Calculated velocity: {self.velocity}")

    def move(self):
        if not self.active or self.target_entity is None:
            logger.debug("Projectile move called but inactive or no target.")
            return

        if not hasattr(self, 'velocity'):
            logger.error("Velocity not calculated. Calling calculate_velocity.")
            self.calculate_velocity()
            if not hasattr(self, 'velocity'):
                return  # Cannot move without velocity

        new_x = self.position.getX() + self.velocity[0]
        new_y = self.position.getY() + self.velocity[1]
        self.position.setX(new_x)
        self.position.setY(new_y)
        self.rect.center = self.position.toTuple()
        logger.debug(f"Projectile moved to position {self.position}")

        if self._has_reached_target():
            logger.info(f"Projectile reached target: {self.target_entity}")
            self.apply_damage()
            self.deactivate()

    def _has_reached_target(self):
        reached = np.isclose(self.position.getX(), self.target_entity.position.getX(), atol=self.speed) and \
                  np.isclose(self.position.getY(), self.target_entity.position.getY(), atol=self.speed)
        #logger.debug(f"Checking if projectile has reached target: {reached}")
        return reached

    def apply_damage(self):
        if self.target_entity and not self.target_entity.is_destroyed():  # Now valid for both Buildings and Unities
            self.target_entity.health -= self.damage
            logger.info(f"Projectile hit {self.target_entity.name}: Damage={self.damage}, Remaining Health={self.target_entity.health}")
            if self.target_entity.health <= 0:
                logger.warning(f"Target {self.target_entity.name} destroyed by projectile.")
                self.target_entity.destroy()  # Call the destroy method
        else:
            logger.warning("Projectile tried to apply damage but target is invalid or already destroyed.")

    def update(self, dt: Optional[float] = None, camera=None):
        if self.active:
            #logger.debug("Updating active projectile.")
            self.move()
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

        self.projectiles.update(dt, camera)

    def draw(self, screen):
        for projectile in self.projectiles:
            if projectile.active:
                projectile.draw(screen)
