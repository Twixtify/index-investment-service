import os

from Portfolio.config import DIR_PATH


class DataFolder:
    path = DIR_PATH['data']['base']

    def __init__(self, name):
        self.name = name
        self.path = DataFolder.path

    def create_folder(self):
        if os.path.isdir(self.path):
            path_head = os.path.join(self.path, self.name)
            try:
                os.mkdir(path_head)
                print("Created folder " + self.name + " in " + self.path)
            except FileExistsError:
                pass
        else:
            raise FileNotFoundError(self.path + " is not a directory!")
