import os
import codecs

from StockApplications.Portfolio.config import ENCODING


class TextFile:
    def __init__(self, file_name, folder_path):
        self.file_name = file_name
        self.folder_path = folder_path
        if os.path.isdir(self.folder_path):
            self.file_path = os.path.join(self.folder_path, self.file_name)
        else:
            raise FileNotFoundError("No such folder: " + self.folder_path)

    def read_rows(self):
        rows = []
        with codecs.open(self.file_path, 'r', encoding=ENCODING) as file:
            for row in file:
                rows.append(row.strip())
        return rows
