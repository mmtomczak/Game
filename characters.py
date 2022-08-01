import random


class Character:
    def __init__(self, name: str, health: int, level: int, xp: int, Xval: int, Yval: int):
        """Init method of Character class object

        Args:
            name (str): name of the class object
            health (int): health of the class object
            level (int): level of the class object
            xp (int): xp of the class object
            Xval (int): coordinates on map on x axis
            Yval (int): coordinates on map on y axis
        """
        self.coord = [Xval, Yval]
        self.name = name
        self.health = health
        self.level = level
        self.xp = xp

    def heal(self) -> bool:
        """Method healing character class object by 1 unit by random

        Returns:
            bool: result of action
        """
        if random.randint(0, 1) == 1:
            self.health += 1
            return True
        else:
            return False

    def is_hit(self, value: int):
        """Method that decreases hp ob character class object by given amount

        Args:
            value (int): damage taken
        """
        self.health -= value

    def is_dead(self) -> bool:
        """Method that indicates if class object hp is less or equal 0

        Returns:
            bool: result of action
        """
        return self.health <= 0

    def get_level(self) -> int:
        """Method that returns class object level

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
            Xval (int): coordinates on map on x axis
            Yval (int): coordinates on map on y axis
        """
        super().__init__(name, health, level, xp, Xval, Yval)
        self.loot = item
        self.desc = desc

    def __repr__(self):
        return "Enemy('{}', {}, {}, {}, {}, {}, {}, {})".format(self.name, self.health, self.level, self.xp, self.item,
                                                                self.coord[0], self.coord[1])

    def attack(self) -> int:
        """Method used to determine damage that class object inflicted 

        Returns:
            int: determined attack damage
        """
        return random.randrange(self.level, self.level*2)


class Player(Character):
    def __init__(self, name: str, health: int, level: int, xp: int, Xval: int, Yval: int, inventory):
        """Init method of child class Player object

        Args:
            name (str): name of the class obejct
            health (int): helath of the class obejct
            level (int): level of the class obejct
            xp (int): xp of the class obejct
            Xval (int): coordinates on map on x axis
            Yval (int): coordinates on map on y axis
            inventory (_type_): inventory of the class obejct
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

    def pickup_item(self, item: str):
        """Method used to add picked up item to class object inventory

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
        self.health += self.level * 2

    def check_xp(self) -> bool:
        """Method used to check if class object has enough xp to increase level

        Returns:
            bool: result of action
        """
        if self.xp >= self.level*2:
            return True
        else:
            return False

    def attack(self) -> int:
        """Method used to determine attack value

        Returns:
            int: attack value
        """
        if "Sword" in self.inventory:
            power = self.level + 10
        else:
            power = self.level
        return random.randrange(power, 2*power)

    def is_hit(self, value: int):
        """Method that determines damage taken by class object

        Args:
            value (int): damage taken

        Returns:
            int: value substracted from class object hp
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
