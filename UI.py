from game import Game

class UI:
    def __init__(self, game: Game):
        self.game = game

    def start_game(self):
        print(f"{'-'*10} Welcome to the game, {self.game.player.name}! {'-'*10}\n")

    def move(self, direction: str):
        direction = direction.lower()
        cases = {'n': 'north', 's':'south', 'e':'east', 'w':'west'}
        if direction in cases:
            if self.game.move(direction):
                print('-'*25)
                print(f"Going {cases[direction]}...\n")
            else:
                print("Cannot move in this direction!\n")
        else:
            print(f"{direction} is an invalid direction! Please use n/s/w/e to go north/south/west/east")

    def attack(self):
        pass

    def uncover_location(self):
        pass

    def level_up(self):
        pass

    def pickup_item(self):
        pass

    def end_game(self):
        pass
