import codecs
import csv
import os

from pandas import DataFrame

from StockApplications.Portfolio.config import ENCODING


class CSVFile:
    def __init__(self, file_name, folder_path):
        self.file_name = file_name
        self.folder_path = folder_path
        if os.path.isdir(self.folder_path):
            self.file_path = os.path.join(self.folder_path, self.file_name)
        else:
            raise FileNotFoundError("No such folder: " + self.folder_path)

    def write_row(self, msg):
        with codecs.open(self.file_path, 'w', encoding=ENCODING) as file:
            writer = csv.writer(file)
            if msg:
                writer.writerow(msg)
                print("Success! " + self.file_name + ": ", msg)
            else:
                pass

    def write_rows(self, msg):
        with codecs.open(self.file_path, 'w', encoding=ENCODING) as file:
            writer = csv.writer(file)
            if msg:
                writer.writerows(msg)
                print("Success! Rows written to " + self.file_name)
            else:
                pass

    def append_row(self, msg):
        with codecs.open(self.file_path, 'a', encoding=ENCODING) as file:
            writer = csv.writer(file)
            writer.writerow(msg)
            print("Success! " + self.file_name + ": ", msg)

    def append_rows(self, msg):
        with codecs.open(self.file_path, 'a', encoding=ENCODING) as file:
            writer = csv.writer(file)
            if msg:
                writer.writerows(msg)
                print("Success! " + self.file_name + ": ", msg)
            else:
                pass

    def read_rows(self):
        rows = []
        with open(self.file_path, 'r', newline='\n', encoding=ENCODING) as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)
        return rows

    def read_csv_column(self, col, header_in_file):
        column = []
        with codecs.open(self.file_path, 'r', encoding=ENCODING) as file:
            reader = csv.reader(file)
            if header_in_file:
                next(reader, None)
            for row in reader:
                column.append(row[col])
        return column

    def get_items_row_index(self, items):
        col_index = []
        for i, item in enumerate(items):
            if isinstance(item, str):
                items[i] = item.lower()
        with open(self.file_path, 'r', newline='\n', encoding=ENCODING) as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                for row_item in row:
                    if isinstance(row_item, str):
                        row_item = row_item.lower()
                    for item in items:
                        if item in row_item:
                            col_index.append(index)
        return col_index

    def sort_csv_file(self, id_col, header_in_file):
        with codecs.open(self.file_path, 'r', encoding=ENCODING) as unsorted_file:
            reader = csv.reader(unsorted_file, delimiter=',')
            if header_in_file:
                header = next(reader, None)
            sorted_csv_file = sorted(reader, key=lambda row: self.extract_type(row[id_col]))
        if header_in_file:
            return [header, *sorted_csv_file]
        else:
            return [*sorted_csv_file]

    def extract_type(self, csv_entry):
        if self.isfloat(csv_entry):
            return float(csv_entry)
        elif csv_entry.isdigit():
            return int(csv_entry)
        else:
            return csv_entry

    def pprint_self(self):
        rows = self.read_rows()
        print(DataFrame(rows))

    @staticmethod
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
