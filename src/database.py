import json
import os

class Database:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load(self, filename, default=[]):
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save(self, filename, data):
        path = os.path.join(self.data_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)