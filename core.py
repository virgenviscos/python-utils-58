import json
from collections import defaultdict

class DataHandler:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self.data, default=str)

    def group_by(self, key):
        grouped_data = defaultdict(list)
        for item in self.data:
            grouped_data[item[key]].append(item)
        return dict(grouped_data)

    def flatten(self, key):
        flat_list = []
        for item in self.data:
            flat_list.append(item[key])
        return flat_list

if __name__ == '__main__':
    sample_data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Alice', 'age': 30, 'city': 'Chicago'},
    ]
    handler = DataHandler(sample_data)
    print(handler.to_json())
    print(handler.group_by('name'))
    print(handler.flatten('city'))