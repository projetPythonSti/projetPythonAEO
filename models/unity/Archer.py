from models.unity.Unity import Unity

class Archer(Unity):
    """
        22/12/2024@tahakhetib : J'ai apporté des modifications à ce fichier sur ce que @amadou_yaya_diallo a écrit
            - Changé la définition de l'UID d'Archer -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.
    """
    def __init__(self, team):
        community = team.get_pplCount()
        villageName = team.get_name()
        uid = f"eq{villageName}p{community}"
        super().__init__(uid, "A", { "wood" : 25, "gold" : 45}, 35, 30, 4, 1, 4, team = team)
        
