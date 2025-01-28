from models.buildings.buildings import Building
import logging
logger = logging.getLogger(__name__)
from .projectile import  ProjectilePool  # Ensure Projectile and ProjectilePool are imported

class Keep(Building) :
  """
      25/01/2025@tahakhetib - j'ai apporté des modification sur ce que @amadou_yaya_diallo a écrit
        - Changé la définition du l'UID -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.

    """
  surface = (1, 1)  # 1x1
  def __init__(self, team) :

    uid = f"eq{team.name}b{team.get_bldCount()}"
    super().__init__(
      uid,
      name="K",
      cost={"w": 35, "g": 125},
      time_building=80,
      health=800,
      team=team
    )
    self.damage = 5
    self.visibility = 80
    self.projectile_speed = 0.5
    self.projectile_pool=ProjectilePool(6, cooldown=4.0)

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