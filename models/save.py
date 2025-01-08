import os
import pickle
import platform


class Save:
    def __init__(self):
        system = platform.system()
        self.save_path = os.getcwd()
        if system == "Windows":
            self.save_path += "\\assets\\data\\saves"
        else:
            self.save_path += "/assets/data/saves"

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def save(self, world, path=None):
        datas = [world]
        if path: self.save_path = path
        file = open(self.save_path + "/save", 'wb')
        pickle.dump(datas, file)
        file.close()

    """
        pay attention to load à saved file, note a file of another extention
    """
    def load(self, path=None):
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

if __name__ == "__main__":
    save = Save()
    print(save.save_path)