import csv
from characters import Enemy


class MapSquare:
    def __init__(self, name: str, desc: str, is_hidden: bool,Xval: int, Yval: int):
        self.coord = [Xval, Yval]
        self.name = name
        self.desc = desc
        self.is_hidden = is_hidden
    
    def get_desc(self):
        return self.desc

    def is_found(self) -> bool:
        if self.is_hidden:
            self.is_hidden = False
            return True
        else:
            return False


class Location(MapSquare):
    def __init__(self, name: str, desc: int, is_hidden: bool,Xval: int, Yval: int, loot: str, special: str):
        super().__init__(name, desc, is_hidden,Xval, Yval)
        self.loot = loot
        self.special = special

    def get_special(self):
        return self.special


class Map:
    def __init__(self, map_file):
        locations = self.csv_read(map_file)
        self.game_map = self.generate_locations(locations)

    def csv_read(self, map_file):
        items = []
        try:
            with open("map.txt") as file:
                csvfile = csv.reader(file)
                header = next(csvfile)
                for row in csvfile:
                    items.append(row) 
        except FileNotFoundError:
            print("Map file not found!")
        except:
            print("Unknown error!")
        return items

    def generate_locations(self, items):
        game_map = []
        try:
            for item in items:
                if str(item[1]) == 'location':
                    if item[9] == '0':
                        special = None 
                    else:
                        special = item[9]
                    new_location = Location(item[3], item[4], bool(int(item[5])), int(item[6]), int(item[7]), item[8], special)
                    game_map.append(new_location)
                elif item[1] == "item":
                    new_item = MapSquare(item[3], item[4], bool(int(item[5])), int(item[6]), int(item[7]))
                    game_map.append(new_item)
                elif item[1] == 'enemy':
                    enemy_level = int(item[2])
                    enemy_points = enemy_level*2
                    if item[8] == '0':
                        enemy_item = None
                    else:
                        enemy_item = item[8]
                    new_enemy = Enemy(name=item[3], health=enemy_points, level = enemy_level, xp = enemy_points, item = enemy_item, Xval = int(item[6]), Yval = int(item[7]))
                    game_map.append(new_enemy)
            return game_map
        except:
            print("Error creating map locations!")
