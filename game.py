from characters import Player, Enemy
from game_map import MapArea, MapSquare, Location
import random


class Game:
    def __init__(self, map_file, health, level, xp, Xval, Yval, inventory):
        self.map = MapArea(map_file)
        self.player = Player("Player", health, level, xp, Xval, Yval, inventory)

    def attack(self) -> int:
        player_location = self.current_location()
        if player_location is not None:
            if isinstance(player_location, Enemy):
                if random.randrange(0, 2):
                    damage = self.player.attack()
                    player_location.is_hit(damage)
                    return damage
                return 0
            return -1
        return -2

    def current_location(self):
        return self.map.game_map[self.player.coord[0]][self.player.coord[1]]

    def look_around(self):
        player_location = self.current_location()
        if isinstance(player_location, MapSquare):
            if player_location.is_hidden is True:
                player_location.is_found()
                return True
            return False
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
        if direction == 0:  # north
            if self.player.coord[1] + 1 <= self.map.map_size:
                self.player.coord[1] += 1
                return True
            else:
                return False
        elif direction == 1:  # east
            if self.player.coord[0] + 1 <= self.map.map_size:
                self.player.coord[0] += 1
                return True
            else:
                return False
        elif direction == 2:  # south
            if self.player.coord[1] - 1 >= 0:
                self.player.coord[1] -= 1
                return True
            else:
                return False
        elif direction == 3:  # west
            if self.player.coord[0] - 1 >= 0:
                self.player.coord[0] -= 1
                return True
            else:
                return False

