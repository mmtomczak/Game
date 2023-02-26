from game import Game


class UI:
    def __init__(self, game: Game):
        """UI class object. Used to communicate and determine actions to player

        Args:
            game (Game): played game
        """
        self.game = game

    def start_game(self):
        print(f"{'-' * 10} Welcome to the game, {self.game.player.name}! {'-' * 10}\n")

    def save_game(self):
        self.game.save_progress()
        print(f"\n{'-' * 10} GAME SAVED {'-' * 10}\n")

    def move(self, direction: str):
        direction = direction.lower()
        cases = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
        if direction in cases:
            if self.game.move(direction):
                print(f"\n\tGoing {cases[direction]}...\n")
            else:
                print("\n\tCannot move in this direction!\n")
        else:
            print(f"\n\t{direction} is an invalid direction! Please use n/s/w/e to go north/south/west/east\n")

    def attack(self):
        attack_status = self.game.attack()
        if attack_status == 0:
            print("\n\tAttack was not successful!\n")
        elif attack_status == -1:
            print("\n\tNo enemy to attack!\n")
        elif attack_status == -2:
            print("\n\tThere is nothing here...\n")
        else:
            damage = self.game.get_hit_damage()
            self.game.enemy_hit(damage)
            print(f"\n\tAttack successful! Dealt {damage} damage to {self.game.current_location().name}\n")
            if not self.game.enemy_status():
                if self.game.is_player_hit():
                    damage = self.game.current_location().attack()
                    damage_taken = self.game.player.register_hit(damage)
                    print(f"\n\t{self.game.current_location().name} attacked back!\n\t{damage_taken} damage taken!\n")
            else:
                dropped_loot = self.game.current_location().loot
                xp_gained = self.game.current_location().level*2
                self.game.enemy_is_dead()
                print(f"\n\tEnemy defeated! You gained {xp_gained} XP!\n")
                if dropped_loot is not None:
                    print(f"\n\tIt dropped {dropped_loot}!\n")

    def get_current_coordinates(self):
        print(f"\n\tYour current coordinates are [{self.game.player.coord[0]}, {self.game.player.coord[1]}]\n")

    def uncover_location(self):
        action_result = self.game.look_around()
        if action_result:
            self.game.look_around()
            print(f"\n\tYou found {self.game.current_location().name}!\n")
        else:
            print("\n\tNothing hidden here\n")

    def level_up(self):
        if self.game.player.check_xp():
            self.game.player.level_up()
            print(f"\n{'*' * 5} LEVEL UP! {'*' * 5}\n\tCurrent level: {self.game.player.level}\n")

    def pickup_item(self):
        pickup = self.game.pickup()
        if pickup is not None:
            self.game.pickup()
            print(f"\n\tPicked up {pickup}!\n")
        else:
            print("\n\tNothing to pickup here!\n")

    def player_hit(self):
        if self.game.is_player_hit():
            value = self.game.current_location().attack()
            self.game.player.register_hit(value)
            print(f"\n\tYou got hit for {value} damage!\n")

    def can_player_enter(self):
        if self.game.get_needed_item():
            print(f"\n\tTo enter this place you need {self.game.get_needed_item()}\n")
            return False
        else:
            return True

    def describe_location(self):
        if self.game.current_location() is not None:
            if self.game.is_location_class():
                if self.game.current_location().is_hidden:
                    print("\n\tI think there is something here...\n")
                else:
                    print(f"\n\tIt is {self.game.current_location().name},\n\t{self.game.current_location().desc}\n")
            elif self.game.is_mapsquare_class():
                if self.game.current_location().is_hidden:
                    print("\n\tIt seems like someone has been here...\n")
                else:
                    print(f"\n\tThere is {self.game.current_location().name} here."
                          f"\n\tIt is {self.game.current_location().desc}\n")
            elif self.game.is_enemy_class():
                print(
                    f"\n\t{self.game.current_location().name}\n\tlevel: {self.game.current_location().level}"
                    f"\n\t{self.game.current_location().desc}\n\tI better draw my weapon, it is hostile\n")
        else:
            print("\n\tNothing here...\n")

    def print_inventory(self):
        if self.game.player.inventory:
            print(f"\n\t Items in your inventory:\n\t\t{self.game.player.inventory}\n")
        else:
            print("\n\tYour inventory is empty!\n")

    def is_player_alive(self):
        if self.game.player.health <= 0:
            return False
        else:
            return True

    def heal(self):
        NOT_HEALED = 0
        HEALED = 1
        HEALTH_FULL = 2
        result = self.game.heal_player()
        if result == NOT_HEALED:
            print(f"\n\tHealing unsuccessful!\n\tCurrent HP: {self.game.player.health}\n")
        elif result == HEALED:
            print(f"\n\tHealed 1HP!\n\tCurrent HP: {self.game.player.health}\n")
        elif result == HEALTH_FULL:
            print(f"\n\tYour health is full: {self.game.player.health} HP\n")

    def print_player_health(self):
        print(
            f"\n\tCurrent level: {self.game.player.level}\n"
            f"\n\tCurrent health: {self.game.player.health} HP\n")

    @staticmethod
    def print_commands():
        print("\nAvailable commands: "
              "\n\t0. commands - to print all commands"
              "\n\t1. go - to go in the given direction"
              "\n\t2. describe - to describe current location"
              "\n\t3. examine - to uncover hidden items and location at current coordinates"
              "\n\t4. inventory - to print items in your inventory"
              "\n\t5. pickup - to pick up item that is at current location"
              "\n\t6. coordinates - to print current coordinates"
              "\n\t7. health - to get your current level and health"
              "\n\t8. attack - to attack"
              "\n\t9. heal - to heal"
              "\n\t10. save - to save"
              "\n\t11. exit - to exit"
              "\nPlease enter a number of action you desire to take\n")

    @staticmethod
    def player_death():
        print(f"{'*'*45}\n\t\tYOU ARE DEAD!\n{'*'*45}")

    @staticmethod
    def load_successful():
        print("\n\tGAME LOADED\n")
