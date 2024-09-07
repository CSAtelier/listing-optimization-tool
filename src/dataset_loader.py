
import os
import csv
import numpy as np
import pandas as pd

class DatasetLoader:
    def __init__(self, file_path = './persistance/data'):
        self.file_path = file_path

    def load_dataset(self):
        with open(self.file_path, 'r', newline='') as csvfile:
            if self.file_path.endswith('xlsx'):
                df =  pd.DataFrame(pd.read_excel(self.file_path)) 
            else:
                df = pd.read_csv(self.file_path)
        return df['ASIN']
