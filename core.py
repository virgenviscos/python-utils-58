import time
import random

class Game:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.running = True

    def play_round(self):
        start_time = time.time()
        outcome = random.choice([True, False])
        if outcome:
            self.score += 10
            print('Round won!')
        else:
            print('Round lost!')
        elapsed_time = time.time() - start_time
        print(f'Time taken for round: {elapsed_time:.2f} seconds')
        self.update_high_score()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            print('New high score!')

    def reset_game(self):
        print('Resetting game...')
        self.score = 0

    def start(self):
        while self.running:
            self.play_round()
            if input('Play another round? (y/n): ').lower() != 'y':
                self.running = False
        print(f'Final score: {self.score}, High score: {self.high_score}')