
import os
import csv
import numpy as np

class DatasetLoader:
    def __init__(self, file_path = './persistance/data'):
        self.file_path = file_path

    def load_dataset(self):
        asin_values = []
        for filename in os.listdir(self.file_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(self.file_path, filename)
                with open(file_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    if 'ASIN' not in reader.fieldnames:
                        print(f"ASIN column not found in {filename}")
                        continue
                    for row in reader:
                        asin_values.append(row['ASIN'])
        
        return asin_values