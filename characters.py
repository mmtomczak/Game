import random


class Character:
    def __init__(self, name: str, health: int, level: int, xp: int, Xval: int, Yval: int):
        """Init method of Character class object

        Args:
            name (str): name of the class object
            health (int): health of the class object
            level (int): level of the class object
            xp (int): xp of the class object
            Xval (int): coordinates on map on x-axis
            Yval (int): coordinates on map on y-axis
        """
        self.coord = [Xval, Yval]
        self.name = name
        self.health = health
        self.level = level
        self.xp = xp

    def register_hit(self, value: int):
        """Decreases hp ob character class object by given amount

        Args:
            value (int): damage taken
        """
        self.health -= value

    def is_dead(self) -> bool:
        """Indicates if class object hp is less or equal 0

        Returns:
            bool: result of action
        """
        return self.health <= 0

    def get_level(self) -> int:
        """Returns class object level

        Returns:
            int: level of the object
        """
        return self.level


class Enemy(Character):
    def __init__(self, name: str, health: int, level: int, xp: int, item: str, Xval: int, Yval: int, desc: str):
        """Init method of child class Enemy object 

        Args:
            name (str): name of the class object
            health (int): health of the class object
            level (int): level of the class object
            xp (int): xp of the class object
            item (str): item held by the class object
            Xval (int): coordinates on map on x-axis
            Yval (int): coordinates on map on y-axis
        """
        super().__init__(name, health, level, xp, Xval, Yval)
        self.loot = item
        self.desc = desc

    def __repr__(self):
        return "Enemy('{}', {}, {}, {}, {}, {}, {}, {})".format(self.name, self.health, self.level, self.xp, self.item,
                                                                self.coord[0], self.coord[1], self.desc)

    def attack(self) -> int:
        """Used to determine damage that class object inflicted

        Returns:
            int: determined attack damage
        """
        return random.randrange(self.level, self.level*2)

    def get_object_data(self) -> dict:
        """Used to get Enemy class object information for save file

        Returns:
            dict: object information in save file formatting
        """
        loot = '0' if self.loot is None else self.loot
        return {"nr": None, "category": "enemy", "level": self.level, "name": self.name,
                                       "desc": self.desc, "is_hidden": "0", "Xval": str(self.coord[0]),
                                       "Yval": str(self.coord[1]), "loot": loot}


class Player(Character):
    def __init__(self, name: str, health: int, level: int, xp: int, Xval: int, Yval: int, inventory):
        """Init method of child class Player object

        Args:
            name (str): name of the class object
            health (int): health of the class object
            level (int): level of the class object
            xp (int): xp of the class object
            Xval (int): coordinates on map on x-axis
            Yval (int): coordinates on map on y-axis
            inventory (_type_): inventory of the class object
        """
        super().__init__(name, health, level, xp, Xval, Yval)
        self.inventory = inventory

    def __repr__(self):
        return "Player('{}', {}, {}, {}, {}, {}, {})".format(self.name, self.health, self.level, self.xp, self.coord[0],
                                                             self.coord[1], self.inventory)

    def __str__(self):
        return "'{}', level: {}".format(self.name, self.level)

    def gain_xp(self, xp: int):
        """Method increasing class object xp

        Args:
            xp (int): amount of xp that will be added to class object xp

        Returns:
            bool: result of action
        """
        if xp is None:
            return False

        self.xp += xp
        return True

    def heal(self) -> int:
        """Method healing player class object by 1 unit by random

        Returns:
            int: result of action
        """

        NOT_HEALED = 0
        HEALED = 1
        HEALTH_FULL = 2

        if self.health < self.level*2:
            if random.randint(0, 1) == 1:
                self.health += 1
                return HEALED
            else:
                return NOT_HEALED
        else:
            return HEALTH_FULL

    def pickup_item(self, item: str):
        """Add picked up item to class object inventory

        Args:
            item (str): picked up item

        Returns:
            bool: result of action
        """
        if item is None:
            return False
        self.inventory.append(item)
        return True

    def level_up(self):
        """Method used to increase class object level
        """
        self.xp -= self.level * 2
        self.level += 1
        self.health = self.level * 2

    def check_xp(self) -> bool:
        """Checks if class object has enough xp to increase level

        Returns:
            bool: result of action
        """
        if self.xp >= self.level*2:
            return True
        else:
            return False

    def attack(self) -> int:
        """Determines attack value

        Returns:
            int: attack value
        """
        if "Sword" in self.inventory:
            power = self.level + 10
        else:
            power = self.level
        return random.randrange(power, 2*power)

    def register_hit(self, value: int):
        """Determines damage taken by class object

        Args:
            value (int): damage taken

        Returns:
            int: value subtracted from class object hp
        """
        if "Armor" in self.inventory:
            self.health -= int(value / 5)  # Armor divides taken damage by 5
            return int(value / 5)
        elif "Shield" in self.inventory:
            self.health -= int(value / 2)  # Shield divides taken damage by 2
            return int(value / 2)
        else:
            self.health -= value
            return value
