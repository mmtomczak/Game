class Location:
    def __init__(self, name: str, desc: int, level: int, loot: str, is_hidden: bool, special: str):
        self.name = name
        self.desc = desc
        self.level = level
        self.loot = loot
        self.is_hidden = is_hidden
        self.special = special

    def get_desc(self):
        return self.desc

    def is_found(self) -> bool:
        if self.is_hidden:
            self.is_hidden = 0
            return True
        else:
            return False

    def get_special(self):
        return self.special


