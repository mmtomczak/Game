from characters import Player, Enemy
from game_map import MapArea, MapSquare, Location
import random


class Game:
    def __init__(self, map_file, health, level, xp, Xval, Yval, inventory):
        self.file = map_file
        self.map = MapArea(map_file)
        self.player = Player("Player", health, level, xp, Xval, Yval, inventory)

    def __repr__(self):
        return "Game('{}', {}, {}, {}, {}, {}, {})".format(self.file, self.player.health, self.player.level,
                                                           self.player.xp, self.player.coord[0], self.player.coord[1],
                                                           self.player.inventory)

    def get_hit_damage(self):
        return self.player.attack()

    def enemy_hit(self, damage):
        player_location = self.current_location()
        player_location.is_hit(damage)
        return True

    def attack(self) -> int:
        player_location = self.current_location()
        if player_location is not None:
            if isinstance(player_location, Enemy):
                if random.randrange(0, 2):
                    return 1
                return 0  # attack not successful
            return -1  # no enemy at player location
        return -2  # current player location is empty

    def current_location(self):
        return self.map.game_map[self.player.coord[0]][self.player.coord[1]]

    def get_needed_item(self):
        player_location = self.current_location()
        if isinstance(player_location, Location) and player_location.special:
            return player_location.special
        else:
            return False

    def is_location_class(self):
        return isinstance(self.current_location(), Location)

    def is_enemy_class(self):
        return isinstance(self.current_location(), Enemy)

    def is_mapsquare_class(self):
        return isinstance(self.current_location(), MapSquare)

    def can_enter(self):
        player_location = self.current_location()
        if isinstance(player_location, Location):
            if player_location.special:
                if player_location.special in self.player.inventory:
                    return True
                return False
            return True
        return False

    def look_around(self):
        player_location = self.current_location()
        if isinstance(player_location, MapSquare):
            if player_location.is_hidden is True:
                player_location.is_found()
                return True
            return False
        return False

    def is_player_hit(self):
        if isinstance(self.current_location(), Enemy):
            if random.randrange(0, 2):
                return True
            else:
                return False
        else:
            return False

    def pickup(self):
        player_location = self.current_location()
        if isinstance(player_location, MapSquare):
            if player_location.is_hidden is False:
                if player_location.categ == "item":
                    self.player.pickup_item(player_location.name)
                    self.map.remove_area(self.player.coord[0], self.player.coord[1])
                    return player_location.name
                elif player_location.categ == "location":
                    if player_location.loot != "0":
                        loot = player_location.loot
                        self.player.pickup_item(loot)
                        self.map.pickup_loot(self.player.coord[0], self.player.coord[1])
                        return loot
                return None
            return None
        return None

    def get_desc(self):
        player_location = self.current_location()
        if player_location is not None:
            return player_location.desc

    def move(self, direction):
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
