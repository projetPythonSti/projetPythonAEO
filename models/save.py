import time
from os import killpg

# self.path mettre
from blessed import Terminal
import pickle
import platform
import os


class Save:
    def __init__(self):
        pass
        """
        self.generate_default_path()

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)"""

    def save(self, game,file_name, path=None):
        self.generate_default_path()
        datas = [game.world,game.gm, game.players, game.game_duration]
        if path: self.save_path = path
        file = open(self.save_path + file_name, 'wb')
        pickle.dump(datas, file)
        file.close()

    def generate_default_path(self):
        system = platform.system()
        self.save_path = os.getcwd()
        if system == "Windows":
            self.save_path += "\\assets\\data\\saves\\"
        else:
            self.save_path += "/assets/data/saves/"

    """
        pay attention to load à saved file, note a file of another extention
    """

    """
    def load(self,file_name, path=None):
        self.generate_default_path()
        if path:
            self.save_path = path
        else:
            self.save_path += "/save"
        if self.backup_exist():
            file = open(self.save_path, 'rb')
            datas = pickle.load(file)
            file.close()
            return datas
    
    def backup_exist(self, path=None):
        if path: self.save_path = path
        return os.path.exists(self.save_path + "/save") 
    """

    def load(self, file_name, path=None):
        #Juste besoin d'une fonction ultra naïve pas sûr que les lignes suivantes soient nécessaire
        self.generate_default_path()
        if path:
            self.save_path = path
        else:
            self.save_path += "/save"

        file = open(self.save_path + file_name, 'rb')
        datas = pickle.load(file)
        file.close()
        print(datas)
        return datas


    """
    Partie de Save et Load pour terminal
    """

    def save_term(self, game,term):
        os.system('cls' if os.name == 'nt' else 'clear')
        file_name = new_input("Veuillez choisir le nom de votre sauvegarde :",term)
        print(f"{file_name} , est-ce bien le nom que vous voulez ?")
        if not confirmation(term) :
            file_name = new_input("Veuillez choisir le nom de votre sauvegarde :", term)
            print(f"{file_name} , est-ce bien le nom que vous voulez ?")

        if file_name:
            if os.path.exists("assets/data/saves/" + file_name):
                print("Il y a déjà une sauvegarde de ce nom. Si vous voulez garder ce nom pour cette sauvegarde, l'ancienne sauvegarde du même non sera écrasé. \nVoulez vous vraiment continuer ?\n")
                if confirmation(term) :
                    self.save(game, file_name, "assets/data/saves/")
                    print(f"Vous avez enregistre votre sauvegarde sous le nom : {file_name} \n")
                    time.sleep(2)

                else:
                    print("Rien n'a été sauvegarder.")
                    time.sleep(2)
                    return None
            else:
                print("bizarre")
                self.save(game, file_name, "assets/data/saves/")

    def list_files_in_directory(self, directory):
        """Affiche les fichiers dans le répertoire spécifié."""
        liste_fichier = []
        # Liste tout le contenu du dossier
        for entry in os.listdir(directory):
            # Vérifie si c'est un fichier
            if os.path.isfile(os.path.join(directory, entry)):
                liste_fichier.append(entry)
                print(entry)
        return liste_fichier

    def list_files_in_directory_printless(self, directory):
        """Affiche les fichiers dans le répertoire spécifié."""
        liste_fichier = []
        # Liste tout le contenu du dossier
        for entry in os.listdir(directory):
            # Vérifie si c'est un fichier
            if os.path.isfile(os.path.join(directory, entry)):
                liste_fichier.append(entry)
                #print(entry)
        return liste_fichier

    def load_term (self,term):
        q = False
        list_save = self.list_files_in_directory_printless("assets/data/saves/")
        string1 = "Voici la liste des fichiers de sauvegarde :"
        for i in range(0,len(list_save)):
            string1 += "\n" + list_save[i]

        string1 += "\n\nVeuillez selectionner une des sauvegarde disponible :"
        chosen_save = new_input( string1 ,term)
        string2 = "Entrer invalide! Vérifiez que vous avez écrit correctement le nom de la sauvegarde de votre choix. Il faut respect les minuscules et les majuscules.\nEntrer la lettre q pour sortir du menu de charge.\n" + string1
        while chosen_save not in list_save:
            chosen_save = new_input(string2 , term)
            if chosen_save == "q" :
                q = True
                break
        if q :
            return None 
        else :
            data = self.load(chosen_save, "assets/data/saves/")
            return data




    """
    Quick_save et Quick_load
    """

    def quick_save (self,game) :
        self.save(game,"quick_save", "assets/data/saves/")

    def quick_load (self,game) :
        data = self.load("quick_save", "assets/data/saves/")
        game.swap_to_load(data)


"""
Je sais pas où mettre ces fonctions mais j'en ai besoin et elles sont statique mais pas particulièrement propre à la classe save
"""


def new_input(str, term):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str)
        with term.cbreak():
            str_tab = []
            val = ''
            val = term.inkey()
            str_tab.append(val.lower())
            os.system('cls' if os.name == 'nt' else 'clear')
            print(str, end='')
            print(str_tab[0])

            while val.name != 'KEY_ENTER':
                val = term.inkey()
                if val.name == 'KEY_BACKSPACE':
                    if len(str_tab) > 0:
                        del str_tab[-1]
                else:
                    str_tab.append(val.lower())

                os.system('cls' if os.name == 'nt' else 'clear')
                print(str, end='')
                for i in range(0, len(str_tab)):
                    print(str_tab[i], end='')
                print()
        string = ''
        for i in range(0, len(str_tab)-1):
            string += str_tab[i]
        return string

def confirmation(term):
    print("Appuyez sur o pour valider ou sur n pour annuler")
    with term.cbreak():
        val= ''
        while val.lower() != 'o' or val.lower() != 'n' :
            val = term.inkey()
            if val.lower() == 'o':
                return True
            elif val.lower() == 'n':
                return False

if __name__ == "__main__":

    save = Save()
    liste = save.list_files_in_directory("../assets/data/saves")
    print (liste)