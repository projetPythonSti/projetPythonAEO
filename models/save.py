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

    def save(self, world):
        datas = [world]
        file = open(self.save_path + "\\save", 'wb')
        pickle.dump(datas, file)
        file.close()

    def load(self):
        try:
            file = open(self.save_path + "\\save", 'rb')
        except FileNotFoundError:
            print("No save found")
            return None
        datas = pickle.load(file)
        file.close()
        return datas

    def hasload(self):
        return os.path.exists(self.save_path + "\\save")


if __name__ == "__main__":
    save = Save()
    print(save.save_path)