from models.buildings.buildings import Building

class Stable(Building) :
  """
      25/01/2025@tahakhetib - j'ai apporté des modification sur ce que @amadou_yaya_diallo a écrit
        - Changé la définition du l'UID -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.

    """
  surface = (3, 3)  # 3x3
  def __init__(self, team) :

    uid = f"eq{team.name}b{team.get_bldCount()}"
    super().__init__(
      uid,
      name="S",
      cost={"w": 175},
      time_building=50,
      health=500,
      spawn="Horseman",
      team=team
    )
