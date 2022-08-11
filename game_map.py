import csv
from characters import Enemy


class MapSquare:
    def __init__(self, categ:str, name: str, desc: str, is_hidden: bool, Xval: int, Yval: int):
        """MapSquare object used to define place on the map

        Args:
            categ (str): category of object
            name (str): name of object
            desc (str): description of object
            is_hidden (bool): is given object hidden
            Xval (int): coordinates of object on x axis
            Yval (int): coordinates of object on y axis
        """
        self.categ = categ
        self.coord = [Xval, Yval]
        self.name = name
        self.desc = desc
        self.is_hidden = is_hidden

    def get_desc(self):
        """Method that returns description of class object

        Returns:
            str: description of object
        """
        return self.desc

    def is_found(self) -> bool:
        """Method that reveals hidden on map object if it was hidden

        Returns:
            bool: result of the action
        """
        if not self.is_hidden:
            return False
        self.is_hidden = False
        return True


class Location(MapSquare):
    def __init__(self, categ:str, name: str, desc: int, is_hidden: bool, Xval: int, Yval: int, loot: str):
        """Locaton class object that is child of the MapSquare class. Used to define location on map

        Args:
            categ (str): category of object
            name (str): name of object
            desc (int): descripton of object
            is_hidden (bool): is given object hidden
            Xval (int): coordinates of object on x axis
            Yval (int): coordinates of object on y axis
            loot (str): loot present at object
        """
        super().__init__(categ, name, desc, is_hidden, Xval, Yval)
        self.loot = loot

    def pickup_loot(self):
        """Method that removes loot from object if it was picked up
        """
        self.loot = "0"


class MapArea:
    def __init__(self, map_file):
        """MapArea class object. Used to store game map, locations on map and map size

        Args:
            map_file (str): name of map file
        """
        locations = self.csv_read(map_file)
        map_locations = self.generate_locations(locations)
        self.map_size = self.get_map_size(locations)
        self.game_map = self.generate_map(map_locations)

    def current_map_loactions(self):
        """Method used to create list of current map locations, used to save the game progress

        Returns:
            list: list of map locations
        """
        map_locations = []
        location_count = 1  # number used as first column of save file
        for col in self.game_map:  # for every column in map matrix
            for row in col:  # for every row in current column
                if row is not None:  
                    if isinstance(row, Location):
                        current_loc = {"nr":location_count, "category":row.categ, "level":"0", "name":row.name, "desc":row.desc, "is_hidden":str(int(row.is_hidden)), "Xval":str(row.coord[0]),  "Yval":str(row.coord[1]), "loot":row.loot}
                        map_locations.append(current_loc)
                        location_count += 1
                    elif isinstance(row, MapSquare):
                        current_loc = {"nr":location_count, "category":row.categ, "level":"0", "name":row.name, "desc":row.desc, "is_hidden":str(int(row.is_hidden)), "Xval":str(row.coord[0]),  "Yval":str(row.coord[1]), "loot":"0"}
                        map_locations.append(current_loc)
                        location_count += 1
                    elif isinstance(row, Enemy):
                        loot = row.loot
                        if loot is None:  # if enemy does not have obj.loot field 'loot' variable is set to '0' (save file format)
                            loot = "0"
                        current_loc = {"nr":location_count, "category":"enemy", "level":row.level, "name":row.name, "desc":row.desc, "is_hidden":"0", "Xval":str(row.coord[0]),  "Yval":str(row.coord[1]), "loot":loot}
                        map_locations.append(current_loc)
                        location_count += 1
        return map_locations

    def generate_map(self, locations):
        """Method used to generate game map

        Args:
            locations (list): list of locations on map

        Returns:
            list: map matrix
        """
        map_area = []
        for i in range(0, self.map_size + 1):
            map_area.append([])
            for j in range(0, self.map_size + 1):
                if self.get_location_by_coords(i, j, locations) is None:  # no object at given coordinates
                    map_area[i].append(None)
                else:
                    map_area[i].append(self.get_location_by_coords(i, j, locations))
        return map_area

    def add_dropped_loot(self, name:str, enemy_name:str, Xval, Yval):
        self.game_map[Xval][Yval] = MapSquare("item", name, f"Left after {enemy_name}", False, Xval, Yval)

    def remove_area(self, Xval, Yval):
        """Method used to remove object from game map

        Args:
            Xval (int): coordinates of object on x axis
            Yval (int): coordinates of object on y axis
        """
        self.game_map[Xval][Yval] = None

    def pickup_loot(self, Xval, Yval):
        """Method used to pick up loot that is present at object present at given coordinates

        Args:
            Xval (int): coordinates of object on x axis
            Yval (int): coordinates of object on y axis
        """
        if isinstance(self.game_map[Xval][Yval], Location):  # loot is only present at Location class objects
            return self.game_map[Xval][Yval].pickup_loot()

    @staticmethod
    def csv_read(map_file):
        """Method used to extract map locations from csv file

        Args:
            map_file (str): name of the map file

        Returns:
            list: list of items present at map
        """
        items = []
        with open(map_file) as file:
            csvfile = csv.reader(file)
            header = next(csvfile)
            for row in csvfile:
                items.append(row)
        return items

    @staticmethod
    def get_location_by_coords(x: int, y: int, locations):
        """Method that returns object that is present at given coordinates

        Args:
            x (int): coordinates of object on x axis
            y (int): coordinates of object on y axis
            locations (list): list of map locations

        Returns:
            object: object present at given coordinates
        """
        for item in locations:
            if item.coord[0] == x and item.coord[1] == y:
                return item
        return None  # no object present at given coordinates

    @staticmethod
    def generate_locations(items):
        """Method used to create given class objects of items present at map

        Args:
            items (list): list of items present on game map

        Returns:
            list: list of class objects present on map
        """
        game_map = []
        try:
            for item in items:
                if str(item[1]) == 'location':  # item is location class object
                    new_location = Location("location", item[3], item[4], bool(int(item[5])), int(item[6]), int(item[7]), item[8])
                    game_map.append(new_location)
                elif item[1] == "item":  # item is MapSquare class object
                    new_item = MapSquare("item", item[3], item[4], bool(int(item[5])), int(item[6]), int(item[7]))
                    game_map.append(new_item)
                elif item[1] == 'enemy':  # item is Enemy class object
                    enemy_level = int(item[2])
                    enemy_points = enemy_level * 2
                    if item[8] == '0':
                        enemy_item = None  # object does not carry item
                    else:
                        enemy_item = item[8]  # object carries an item
                    new_enemy = Enemy(name=item[3], health=enemy_points, level=enemy_level, xp=enemy_points,
                                      item=enemy_item, Xval=int(item[6]), Yval=int(item[7]), desc = item[4])
                    game_map.append(new_enemy)
            return game_map
        except Exception:
            print("Error creating map locations!")

    @staticmethod
    def get_map_size(map_file):
        """Method used to determine map size

        Args:
            map_file (list): list of items present on map

        Returns:
            int: map size
        """
        max_var = 0  # map size cannot be less than 0, when 0 indicates empty map
        for item in map_file:
            if int(item[6]) > int(item[7]) and int(item[6]) > max_var:
                max_var = int(item[6])
            elif int(item[6]) < int(item[7]) and int(item[7]) > max_var:
                max_var = int(item[7])
        return max_var + 1  # map size is determined by adding 1 to max value of x/y coordinates
