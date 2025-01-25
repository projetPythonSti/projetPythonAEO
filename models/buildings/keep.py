from models.buildings.buildings import Building
from typing import Optional
import pygame as pg
import logging
import numpy as np
from .projectile import  ProjectilePool  # Ensure Projectile and ProjectilePool are imported
import logging
logger = logging.getLogger(__name__)
class Keep(Building) :
  surface = (1, 1)  # 1x1
  def __init__(self, team) :
    community = team.get_community().get('K')
    uid = len(community) if community else 0 # 0 if it doesn't exist yet
    super().__init__(
      uid,
      name="K",
      cost={"w": 35, "g": 125},
      time_building=80,
      health=800,
      team=team,

    )

    self.range=8
    self.damage = 5
    self.visibility = 8
    self.projectile_speed = 0.5
    self.projectile_pool=ProjectilePool(1, cooldown=5.0)  
    logger.debug(f"Keep {self.uid} initialized for team {team} with position {self.position}")

  def attack(self, target):
    """Activate a projectile towards the target."""
    logger.debug(f"Keep {self.uid} at position {self.position} attacking target {target}")
    projectile = self.projectile_pool.get_projectile()
    if projectile and not projectile.active:
        projectile.activate(
            start_pos=self.position,  # Use Position instance
            target_entity=target,
            damage=self.damage,
            speed=self.projectile_speed,
            team=self.team
        )
        logger.debug(f"Projectile activated with start_pos={self.position} towards target={target}")
    else:
        logger.warning("No available projectile to activate or pool is in cooldown.")

# import logging
# from typing import Optional

# import pygame as pg
# import numpy as np

# TILE_SIZE=32

# logger = logging.getLogger(__name__)


# class Projectile(pg.sprite.Sprite):
#     """
#     A Projectile that travels from a start position to a target entity.
#     Coordinates in 'pos' are isometric coordinates; screen coords 
#     are handled by updating 'self.rect'.
#     """
#     def __init__(self, start_pos, target_entity, damage=10, speed=5, image=None):
#         super().__init__()
#         self.active = False
#         self.damage = damage
#         self.speed = speed
#         self.target_entity = target_entity
#         self.origin_pos = start_pos
#         self.position = start_pos
#         self.team = None  # To be set when activated

#         if image:
#             self.image = image
#         else:
#             self.image = self._fallback_surface()
#         self.rect = self.image.get_rect(center=self.position)
#         logger.debug(f"Initialized Projectile: origin={start_pos}, target={target_entity}, damage={damage}, speed={speed}")

#     def _fallback_surface(self) -> pg.Surface:
#         surface = pg.Surface((10, 10), pg.SRCALPHA)
#         pg.draw.circle(surface, (255, 0, 0), (5, 5), 5)
#         return surface

#     def activate(self, start_pos, target_entity, damage, speed, team):
#         self.position = start_pos
#         self.target_entity = target_entity
#         self.damage = damage
#         self.speed = speed
#         self.team = team
#         self.active = True
#         self.rect.center = self.position
#         logger.info(f"Projectile activated: start_pos={start_pos}, target_entity={target_entity}, damage={damage}, speed={speed}, team={team}")
#         logger.debug(f"Projectile activated towards {self.target_entity} from {self.origin_pos}")

#     def move(self):
#         if not self.active or self.target_entity is None:
#             logger.debug("Projectile move called but inactive or no target.")
#             return

#         dx = self.target_entity.position[0] - self.position[0]
#         dy = self.target_entity.position[1] - self.position[1]
#         distance = np.hypot(dx, dy)

#         if distance == 0:
#             self.apply_damage()
#             self.deactivate()
#             return

#         dx /= distance
#         dy /= distance

#         self.position = (self.position[0] + dx * self.speed, self.position[1] + dy * self.speed)
#         self.rect.center = self.position
#         logger.debug(f"Projectile moved to position {self.position}")

#         if self._has_reached_target():
#             logger.info(f"Projectile reached target: {self.target_entity}")
#             self.apply_damage()
#             self.deactivate()

#     def _has_reached_target(self):
#         reached = np.isclose(self.position[0], self.target_entity.position[0], atol=self.speed) and \
#                   np.isclose(self.position[1], self.target_entity.position[1], atol=self.speed)
#         logger.debug(f"Checking if projectile has reached target: {reached}")
#         return reached

#     def apply_damage(self):
#         if self.target_entity and not self.target_entity.is_destroyed():
#             self.target_entity.health -= self.damage
#             logger.info(f"Projectile hit {self.target_entity.name}: Damage={self.damage}, Remaining Health={self.target_entity.health}")
#             if self.target_entity.health <= 0:
#                 logger.warning(f"Target {self.target_entity.name} destroyed by projectile.")
#                 self.target_entity.destroy()
#         else:
#             logger.warning("Projectile tried to apply damage but target is invalid or already destroyed.")

#     def update(self, dt: Optional[float] = None, camera=None):
#         if self.active:
#             logger.debug("Updating active projectile.")
#             self.move()
#         else:
#             logger.debug("Updating inactive projectile.")

#     def deactivate(self):
#         self.active = False
#         logger.info("Projectile deactivated.")

#     def draw(self, screen):
#         """
#         Optional: if you want to individually draw the projectile
#         (otherwise, rely on `Group.draw(screen)`).
#         """
#         screen.blit(self.image, self.rect)


# class ProjectilePool:
#     """
#     Manages a pool of Projectile objects to avoid creating/destroying them constantly.
#     """
#     def __init__(self, max_projectiles):
#         self.group = pg.sprite.Group()
#         self.world = None  # Will be set externally if needed
#         self.projectile_image = self._load_projectile_image("../assets/images/buildings/projectile.png")

#         # Pre-create a pool of Projectiles
#         for _ in range(max_projectiles):
#             projectile = Projectile((0, 0), None, image=self.projectile_image)
#             self.group.add(projectile)

#     def _load_projectile_image(self, projectile_image):
#         """
#         Load the image from file or return the provided surface, 
#         or fall back to a default if invalid.
#         """
#         if isinstance(projectile_image, str):
#             try:
#                 loaded = pg.image.load(projectile_image).convert_alpha()
#                 logger.info(f"Loaded projectile image from {projectile_image}")
#                 return loaded
#             except FileNotFoundError:
#                 logger.error(f"Projectile image file not found: {projectile_image}")
#                 return self._fallback_surface()
#         elif isinstance(projectile_image, pg.Surface):
#             return projectile_image
#         else:
#             logger.warning("Invalid projectile_image type. Using fallback surface.")
#             return self._fallback_surface()

#     def _fallback_surface(self):
#         surf = pg.Surface((10, 10), pg.SRCALPHA)
#         surf.fill((255, 0, 0))
#         return surf

#     def get_projectile(self, start_pos, target_entity, damage=10):
#         """
#         Retrieves an inactive projectile (or recycles the oldest).
#         """
#         for projectile in self.group:
#             if not projectile.active:
#                 projectile.activate(start_pos, target_entity, damage)
#                 projectile.world = self.world
#                 return projectile

#         # If all are active, recycle the oldest (the one with the earliest last_active_time)
#         if len(self.group) > 0:
#             oldest = min(self.group, key=lambda p: p.last_active_time)
#             oldest.activate(start_pos, target_entity, damage)
#             oldest.world = self.world
#             return oldest
#         else:
#             # If somehow the group is empty, create a new projectile
#             logger.warning("Projectile pool is empty. Creating a new projectile.")
#             new_projectile = Projectile(start_pos, target_entity, damage=damage, image=self.projectile_image)
#             new_projectile.activate(start_pos, target_entity, damage)
#             new_projectile.world = self.world
#             self.group.add(new_projectile)
#             return new_projectile

#     def update(self, dt: Optional[float] = None, camera=None):
#         """
#         Update all projectiles in the pool. Pass the camera so each projectile 
#         can convert iso -> screen coords in its update method.
#         """
#         for projectile in self.group:
#             if projectile.active:
#                 projectile.update(dt, camera=camera)

#     def draw(self, screen):
#         """
#         If each projectile updates its rect correctly,
#         we can draw via Group.draw(screen).
#         """
#         self.group.draw(screen)

