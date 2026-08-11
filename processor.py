import json
import random

class Processor:
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        if not data:
            raise ValueError("Data cannot be empty")
        self.data = data

    def process_data(self):
        results = []
        for item in self.data:
            try:
                result = self._process_item(item)
                results.append(result)
            except (TypeError, ValueError) as e:
                results.append(f"Error processing item {item}: {str(e)}")
        return results

    def _process_item(self, item):
        if not isinstance(item, int):
            raise TypeError("Item must be an integer")
        return item ** 2  # Example processing: squaring the item

if __name__ == '__main__':
    input_data = [1, 2, 'three', 4, None]
    processor = Processor(input_data)
    output = processor.process_data()
    print(json.dumps(output, indent=2))
