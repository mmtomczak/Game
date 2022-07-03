import random


class Character():
    def __innit__(self, name: str, health: int, level: int, xp: int):
        self.name = name
        self.health = health
        self.level = level
        self.xp = xp

    def attack(self) -> int:
        return random.randrange(self.level / 2, self.level)

    def check_xp(self) -> bool:
        if self.xp >= level * 2:
            xp = xp - level * 2
            level += 1
            return True
        else:
            return False

    def heal(self) -> bool:
        if random.randint(0, 1) == 1:
            health += 1
            return True
        else:
            return False


class Player(Character):
    def __innit__(self, name: str, health: int, level: int, xp: int):
        super().__innit__(name, health, level, xp)
        self.inventory = []
