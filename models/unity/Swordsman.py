from models.unity.Unity import Unity
# from model import Model

class Swordsman(Unity):
    """
        22/12/2024@tahakhetib : J'ai apporté des modifications à ce fichier sur ce que @amadou_yaya_diallo a écrit
            - Changé la définition de l'UID du Swordsman -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.
    """
    def __init__(self, team):
        community = team.get_community().get('s')
        # uid = len(community) if community else 0 # 0 if 
        villageName = team.get_name()
        uid = f"eq{villageName}p{len(community) if community else 0}"
        super().__init__(uid, "s", { "f" : 50, "g" : 20}, 20, 40, 4, 0.9, 1, team=team)