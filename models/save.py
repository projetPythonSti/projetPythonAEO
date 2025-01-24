import os
import pickle
import platform


class Save:
    def __init__(self):
        self.generate_default_path()

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    # def save(self, world, path=None):
    #     self.generate_default_path()
    #     datas = [world]
    #     if path: self.save_path = path
    #     file = open(self.save_path + "/save", 'wb')
    #     pickle.dump(datas, file)
    #     file.close()
    
    def save(self, game, path=None):
        self.generate_default_path()
        datas = [game]
        if path: self.save_path = path
        file = open(self.save_path + "/save", 'wb')
        pickle.dump(datas, file)
        file.close()

    def generate_default_path(self):
        system = platform.system()
        self.save_path = os.getcwd()
        if system == "Windows":
            self.save_path += "\\assets\\data\\saves"
        else:
            self.save_path += "/assets/data/saves"
            
    """
        pay attention to load à saved file, note a file of another extention
    """
    def load(self, path=None):
        self.generate_default_path()
        if path: 
            self.save_path = path
        else:
            self.save_path += "/save"
        if self.backup_exist(self.save_path):
            file = open(self.save_path, 'rb')
            datas = pickle.load(file)
            file.close()
            return datas

    def backup_exist(self, path=None):
        if path: self.save_path = path
        else:
            self.save_path += "/save"
        return os.path.exists(self.save_path)

if __name__ == "__main__":
    save = Save()
    print(save.save_path)