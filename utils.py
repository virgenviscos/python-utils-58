import json
import random
from typing import List, Dict, Any

class GameDataHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'Error loading data: {e}')
            return []

    def save_data(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_random_game(self) -> Dict[str, Any]:
        if self.data:
            return random.choice(self.data)
        return {}  

    def add_game(self, game: Dict[str, Any]) -> None:
        self.data.append(game)
        self.save_data()

    def find_game_by_name(self, name: str) -> List[Dict[str, Any]]:
        return [game for game in self.data if game.get('name') == name]

# Example of usage
# handler = GameDataHandler('games.json')
# handler.add_game({'name': 'Super Adventure', 'genre': 'RPG'})
# print(handler.get_random_game())
# print(handler.find_game_by_name('Super Adventure'))