from models.buildings.buildings import Building

class House(Building):
    """
        25/01/2025@tahakhetib - j'ai apporté des modification sur ce que @amadou_yaya_diallo a écrit
          - Changé la définition du l'UID -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.

      """
    surface = (2, 2)  # 2x2
    def __init__(self, team):

        uid = f"eq{team.name}b{team.get_bldCount()}"
        super().__init__(
            uid,
            name="H",
            cost={"w": 25},
            time_building=25,
            health=200,
            population=5,
            team=team
        )
