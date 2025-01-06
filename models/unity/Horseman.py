from unity.Unity import Unity

class Horseman(Unity):
    """
        22/12/2024@tahakhetib : J'ai apporté des modifications à ce fichier sur ce que @amadou_yaya_diallo a écrit
            - Changé la définition de l'UID du Horseman -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.
    """
    def __init__(self, team):
        community = team.get_community().get('h')
        # uid = len(community) if community else 0 # 0 if it doesn't exist yet
        villageName = team.get_name()
        uid = f"eq{villageName}p{len(community) if community else 0}"  # 0 if
        super().__init__(uid, "h", { "f" : 80, "g" : 20}, 30, 45, 4, 1.2, 1, team=team)
