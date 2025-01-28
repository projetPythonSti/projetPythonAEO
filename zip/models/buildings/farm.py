from models.buildings.buildings import Building
from models.ressources.ressources import Food

class Farm(Building):
  """
      25/01/2025@tahakhetib - j'ai apporté des modification sur ce que @amadou_yaya_diallo a écrit
        - Changé la définition du l'UID -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.

    """
  surface = (2, 2)  # 2x2
  def __init__(self, team):

    uid = f"eq{team.name}b{team.get_bldCount()}"
    super().__init__(
      uid,
      name = "F",
      cost = {"w": 60},
      time_building = 10,
      health = 100,
      dropPoint = True,
      team = team
    )
    self.team = team
    self.contains = []
    self.max_capacity = 300
    
  def add_food(self, food):
    if len(self.contains) < self.max_capacity:
      self.contains.append(food)
      return True
    return False
