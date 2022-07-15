import csv
from characters import Enemy


class MapSquare:
    def __init__(self, categ:str, name: str, desc: str, is_hidden: bool, Xval: int, Yval: int):
        self.categ = categ
        self.coord = [Xval, Yval]
        self.name = name
        self.desc = desc
        self.is_hidden = is_hidden

    def get_desc(self):
        return self.desc

    def is_found(self) -> bool:
        self.is_hidden = False



class Location(MapSquare):
    def __init__(self, categ:str, name: str, desc: int, is_hidden: bool, Xval: int, Yval: int, loot: str, special: str):
        super().__init__(categ, name, desc, is_hidden, Xval, Yval)
        self.loot = loot
        self.special = special

    def get_special(self):
        return self.special

    def pickup_loot(self):
        self.loot = "0"


class MapArea:
    def __init__(self, map_file):
        locations = self.csv_read(map_file)
        map_locations = self.generate_locations(locations)
        self.map_size = self.get_map_size(locations)
        self.game_map = self.generate_map(map_locations)

    def generate_map(self, locations):
        map_area = []
        for i in range(0, self.map_size + 1):
            map_area.append([])
            for j in range(0, self.map_size + 1):
                if self.get_location_by_coords(i, j, locations) is None:
                    map_area[i].append(None)
                else:
                    map_area[i].append(self.get_location_by_coords(i, j, locations))
        return map_area

    def remove_area(self, Xval, Yval):
        self.game_map[Xval][Yval] = None

    def pickup_loot(self, Xval, Yval):
        if isinstance(self.game_map[Xval][Yval],"Location"):
            self.game_map[Xval][Yval].pickup_loot()

    @staticmethod
    def csv_read(map_file):
        items = []
        try:
            with open("map.txt") as file:
                csvfile = csv.reader(file)
                header = next(csvfile)
                for row in csvfile:
                    items.append(row)
        except FileNotFoundError:
            print("Map file not found!")
        except Exception:
            print("Unknown error!")
        return items

    @staticmethod
    def get_location_by_coords(x: int, y: int, locations):
        for item in locations:
            if item.coord[0] == x and item.coord[1] == y:
                return item
        return None

    @staticmethod
    def generate_locations(items):
        game_map = []
        try:
            for item in items:
                if str(item[1]) == 'location':
                    if item[9] == '0':
                        special = None
                    else:
                        special = item[9]
                    new_location = Location("location", item[3], item[4], bool(int(item[5])), int(item[6]), int(item[7]), item[8],
                                            special)
                    game_map.append(new_location)
                elif item[1] == "item":
                    new_item = MapSquare("item", item[3], item[4], bool(int(item[5])), int(item[6]), int(item[7]))
                    game_map.append(new_item)
                elif item[1] == 'enemy':
                    enemy_level = int(item[2])
                    enemy_points = enemy_level * 2
                    if item[8] == '0':
                        enemy_item = None
                    else:
                        enemy_item = item[8]
                    new_enemy = Enemy(name=item[3], health=enemy_points, level=enemy_level, xp=enemy_points,
                                      item=enemy_item, Xval=int(item[6]), Yval=int(item[7]))
                    game_map.append(new_enemy)
            return game_map
        except Exception:
            print("Error creating map locations!")

    @staticmethod
    def get_map_size(map_file):
        max_var = 0
        for item in map_file:
            if int(item[6]) > int(item[7]) and int(item[6]) > max_var:
                max_var = int(item[6])
            elif int(item[6]) < int(item[7]) and int(item[7]) > max_var:
                max_var = int(item[7])
        return max_var + 1
