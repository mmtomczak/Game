import random


class Character:
    def __init__(self, name: str, health: int, level: int, xp: int):
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
    def __init__(self, name: str, health: int, level: int, xp: int, item: str):
        super().__init__(name, health, level, xp)
        self.loot = item

    def attack(self) -> int:
        return random.randrange(int(self.level / 2), self.level)


class Player(Character):
    def __init__(self, name: str, health: int, level: int, xp: int):
        super().__init__(name, health, level, xp)
        self.inventory = []

    def gain_xp(self, xp: int):
        self.xp += xp

    def check_xp(self) -> bool:
        if self.xp >= self.level * 2:
            self.xp -= self.level * 2
            self.level += 1
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
