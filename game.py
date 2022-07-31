from characters import Player, Enemy
from game_map import MapArea, MapSquare, Location
import random


class Game:
    def __init__(self, map_file='map.txt', health=10, level=1, xp=0, Xval=None, Yval=None, inventory=[]):
        """Game class. Creates game map from given file and player character.

        Args:
            map_file (str, optional): Map file in .txt format used to create game map. Defaults to 'map.txt'.
            health (int, optional): Player health. Defaults to 10.
            level (int, optional): Player level. Defaults to 1.
            xp (int, optional): Player xp. Defaults to 0.
            Xval (int, optional): Player position on X axis. Defaults to None.
            Yval (int, optional): Player position on Y axis. Defaults to None.
            inventory (list, optional): Player inventory. Defaults to [].
        """
        self.file = map_file
        self.map = MapArea(map_file)
        if Xval is None and Yval is None:  # if arguments Xval and Yval are not declared, player is placed at the middle of the map
            Xval = Yval = int(self.map.map_size / 2)
        self.player = Player("Player", health, level, xp, Xval, Yval, inventory)

    def __repr__(self):
        return "Game('{}', {}, {}, {}, {}, {}, {})".format(self.file, self.player.health, self.player.level,
                                                           self.player.xp, self.player.coord[0], self.player.coord[1],
                                                           self.player.inventory)

    def get_hit_damage(self):
        """Method that returns damage that player will deal given enemy hit

        Returns:
            int: Hit damage value
        """
        return self.player.attack()

    def enemy_hit(self, damage):
        """Method that is responsible for dealing damage to enemy

        Args:
            damage (int): damage dealt to enemy 
        """
        player_location = self.current_location()
        player_location.is_hit(damage)
        return True

    def attack(self) -> int:
        """Method that determines if on current player position enemy that can be attacked is present and if attack is successful 


        Returns:
            int: Status of unsuccessful attack (-2, -1, 0) or successful attack (1)
        """
        player_location = self.current_location()
        if player_location is not None:
            if isinstance(player_location, Enemy):
                if random.randrange(0, 2):
                    return 1
                return 0  # attack not successful
            return -1  # no enemy at player location
        return -2  # current player location is empty

    def current_location(self):
        """Method thet returns current player coordinates 

        Returns:
            None, Enemy class, MapSquare class, Location class: Returns object that is present at current player location
        """
        return self.map.game_map[self.player.coord[0]][self.player.coord[1]]

    def get_needed_item(self):
        """Returns item that is needed to perform actions on current location (special item)

        Returns:
            _type_: _description_
        """
        player_location = self.current_location()
        if isinstance(player_location, Location) and player_location.special:
            return player_location.special  # if there is special item needed, its name will be returned 
        else:
            return False  # if special item is not necessary at current location nothing will be returned

    def is_location_class(self):
        """Method that checks if at current player location there is present Location class object

        Returns:
            bool: boolean value of result
        """
        return isinstance(self.current_location(), Location)

    def is_enemy_class(self):
        """Method that checks if at current player location there is present Enemy class object

        Returns:
            bool: boolean value of result
        """
        return isinstance(self.current_location(), Enemy)

    def is_mapsquare_class(self):
        """Method that checks if at current player location there is present MapSquare class object

        Returns:
            bool: boolean value of result
        """
        return isinstance(self.current_location(), MapSquare)

    def can_enter(self):
        """Method that checks if player can enter Location class object at current location (if class object requires Special Item method checks if said item is present in player inventory)

        Returns:
            bool: result
        """
        player_location = self.current_location()
        if isinstance(player_location, Location):
            if player_location.special:
                if player_location.special in self.player.inventory:
                    return True  # Location class object requires special item to enter and said item is present in player inventory
                return False  # Location class object requires special item to enter and said item is NOT present in player inventory
            return True  # Location class object doesn't require special item to enter
        return False  # At current player location there is no Location class object

    def look_around(self):
        """Method that uncovers hidden items/locatin at current player position

        Returns:
            bool: result of the action
        """
        player_location = self.current_location()
        if isinstance(player_location, MapSquare):
            if player_location.is_hidden is True:
                player_location.is_found()
                return True  # hidden item/location uncovered
            return False  # no hidden item/location at current player position
        return False  # at current position there is no object present that can be hidden

    def is_player_hit(self):
        """Method that determines if player has been hit by the Enemy, if it is present at current player location

        Returns:
            bool: random result
        """
        if isinstance(self.current_location(), Enemy):
            if random.randrange(0, 2):
                return True  # there is Enemy at player current location and player is hit
            else:
                return False  # there is Enemy at player current location but player is NOT hit
        else:
            return False  # there is no Enemy at current player location

    def pickup(self):
        """Method that checks if at current player location there is item that can be picked up. If yes, picks up that item

        Returns:
            str: picked up item name
        """
        player_location = self.current_location()
        if isinstance(player_location, MapSquare):
            if player_location.is_hidden is False:
                if player_location.categ == "item":
                    self.player.pickup_item(player_location.name)
                    self.map.remove_area(self.player.coord[0], self.player.coord[1])
                    return player_location.name  # picked up item
                elif player_location.categ == "location":
                    if player_location.loot != "0":
                        loot = player_location.loot
                        self.player.pickup_item(loot)
                        self.map.pickup_loot(self.player.coord[0], self.player.coord[1])
                        return loot  # picked up item that was hidden in Location class object
                return None  # nothing was picked up
            return None  # location is hidden
        return None  # no object that can store item is present

    def get_desc(self):
        """Returns description of object present at current player location

        Returns:
            str: description of location
        """
        player_location = self.current_location()
        if player_location is not None:
            return player_location.desc

    def move(self, direction):
        """Method that, if possible, moves player character in given direction on the map

        Args:
            direction (str): direction in which player is to be moved

        Returns:
            bool: result of the action
        """
        if direction == 'n':  # move north
            if self.player.coord[1] + 1 <= self.map.map_size:
                self.player.coord[1] += 1
                return True
            else:
                return False
        elif direction == 'e':  # move east
            if self.player.coord[0] + 1 <= self.map.map_size:
                self.player.coord[0] += 1
                return True
            else:
                return False
        elif direction == 's':  # move south
            if self.player.coord[1] - 1 >= 0:
                self.player.coord[1] -= 1
                return True
            else:
                return False
        elif direction == 'w':  # move west
            if self.player.coord[0] - 1 >= 0:
                self.player.coord[0] -= 1
                return True
            else:
                return False
