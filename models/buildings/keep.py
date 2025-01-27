from models.buildings.buildings import Building

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
    self.visibility = 8
