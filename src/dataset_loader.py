
# import os
# import csv
# import numpy as np
# import pandas as pd

# class DatasetLoader:
#     def __init__(self, file_path = './persistance/data'):
#         self.file_path = file_path

#     def load_dataset(self):
#         with open(self.file_path, 'r', newline='') as csvfile:
#             if self.file_path.endswith('xlsx'):
#                 df =  pd.DataFrame(pd.read_excel(self.file_path)) 
#             else:
#                 df = pd.read_csv(self.file_path)
#         return df['ASIN']

import redis
import pandas as pd

class DatasetLoader:
    def __init__(self, csv_path, priority, redis_host='localhost', redis_port=6379, redis_db=0, batch_size=10):
        """Initialize Redis connection, batch size, and CSV file path."""
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        self.batch_size = batch_size
        self.csv_path = csv_path
        self.priority = priority

    def load_dataset_from_csv(self):
        """Load ASINs from the specified CSV file."""
        try:
            df = pd.read_csv(self.csv_path)
            print(self.csv_path)
            if 'ASIN' not in df.columns:
                raise ValueError("CSV file does not contain 'ASIN' column.")
            return df['ASIN'].dropna().tolist()  # Drop missing values
        except FileNotFoundError:
            # Handle file not found error
            return []
        except Exception as e:
            # Handle any other exceptions during loading
            return []

    def push_to_redis(self, items):
        """Push a list of ASINs to Redis with the specified priority."""
        for item in items:
            self.redis_client.zadd('asin_queue', {item: self.priority})

    def load_dataset(self):
        """Load ASINs from the CSV and push them to Redis."""
        asin_list = self.load_dataset_from_csv()
        if asin_list:
            self.push_to_redis(asin_list)
        print(f"Pushed {len(asin_list)} ASINs to Redis with priority {self.priority}.")

    def load_dataset_from_redis(self):
        """Load ASINs from Redis sorted set in batches."""
        print(f"Loading ASINs from Redis with priority {self.priority}...")
        asin_batch = self.redis_client.zrange('asin_queue', 0, self.batch_size - 1)
        return asin_batch