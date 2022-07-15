import random


class Character:
    def __init__(self, name: str, health: int, level: int, xp: int, Xval: int, Yval: int):
        self.coord = [Xval, Yval]
        self.name = name
        self.health = health
        self.level = level
        self.xp = xp

    def heal(self) -> bool:
        if random.randint(0, 1) == 1:
            self.health += 1
            return True
        else:
            return False

    def is_hit(self, value: int):
        self.health -= value

    def is_dead(self) -> bool:
        return self.health <= 0

    def get_level(self) -> int:
        return self.level


class Enemy(Character):
    def __init__(self, name: str, health: int, level: int, xp: int, item: str, Xval: int, Yval: int):
        super().__init__(name, health, level, xp, Xval, Yval)
        self.loot = item

    def attack(self) -> int:
        return random.randrange(int(self.level / 2), self.level)


class Player(Character):
    def __init__(self, name: str, health: int, level: int, xp: int, Xval: int, Yval: int, inventory = []):
        super().__init__(name, health, level, xp, Xval, Yval)
        self.inventory = inventory

    def gain_xp(self, xp: int):
        self.xp += xp
        return True

    def pickup_item(self, item:str):
        self.inventory.append(item)
        return True

    def check_xp(self) -> bool:
        if self.xp >= self.level * 2:
            self.xp -= self.level * 2
            self.level += 1
            self.health += self.level*2
            return True
        else:
            return False

    def attack(self) -> int:
        if "Sword" in self.inventory:
            power = self.level + 10
        else:
            power = self.level
        return random.randrange(int(power / 2), power)

    def is_hit(self, value: int):
        if "Armor" in self.inventory:
            self.health -= int(value/5)
        elif "Shield" in self.inventory:
            self.health -= int(value/2)
