# This file contains the Villager class which is a subclass of Unity
# This file contains the Villager class which is a subclass of Unity
from models.unity.Unity import Unity


class Villager(Unity):

    """
        22/12/2024@tahakhetib : J'ai apporté des modifications à ce fichier sur ce que @amadou_yaya_diallo a écrit
            - Changé la définition de l'UID du villageois -> Passage à une string basé sur le numéro d'équipe + la taille de la communauté.
    """
    def __init__(self, team):
        community = team.get_pplCount()
        villageName = team.get_name()
        uid = f"eq{villageName}p{community}" # 0 if
        super().__init__(uid,"V", {"fo" : 50}, 25, 40, 4, 0.8, 1, team=team)
        self.carry_max = 25
        # self.buildingSpeed = buildingSpeed,
        self.ressources_dict = {
            "fo" : 0,
            "w" : 0,
            "g" : 0,
        }
        
    def __repr__(self):
        return f"Villageois ID  : {self.uid} - Position {self.position}"
    """
        droping ressources in the village drop point
    """
    def collect(self, ressource):
        all_collected = sum(self.ressources_dict.values())
        # quantity_to_collect = ressource.get_quantity()
        rest = self.carry_max - all_collected
        quantity_to_collect = rest if rest < ressource.get_quantity() else ressource.get_quantity()
        
        if all_collected >= self.carry_max:
            self.drop_ressources()
        else:
            ressource.extract(quantity_to_collect)
            self.ressources_dict[ressource.get_name().lower()] += quantity_to_collect
            if all_collected + quantity_to_collect == self.carry_max: # if the villager is full
                self.drop_ressources()
            else:
                #he has to do other things
                pass
        if ressource.get_quantity() == 0:
            ressource.remove()
        else:
            #he has to come back to the ressource to finish collecting
            # self.move(ressource.get_position())
            self.collect(ressource)
    
    def drop_ressources(self):
        for key, quantity in self.ressources_dict.items():
            self.team.add_ressources(key, quantity)
            self.ressources_dict[key] = 0
    """
        droping ressources in the village drop point
    """
    
    def build(self):
        return 0
