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

    def move(self, direction: str):
        direction = direction.lower()
        cases = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
        if direction in cases:
            if self.game.move(direction):
                print('-' * 25)
                print(f"\tGoing {cases[direction]}...\n")
            else:
                print("\tCannot move in this direction!\n")
        else:
            print(f"\t{direction} is an invalid direction! Please use n/s/w/e to go north/south/west/east")

    def attack(self):
        attack_status = self.game.attack()
        if attack_status == 0:
            print("\tAttack was not successful!")
        elif attack_status == -1:
            print("\tNo enemy to attack!")
        elif attack_status == -2:
            print("\tThere is nothing here...")
        else:
            damage = self.game.get_hit_damage()
            self.game.enemy_hit(damage)
            print(f"\tAttack successful! Dealt {damage} damage to {self.game.current_location().name}")
            if not self.game.enemy_status():
                if self.game.is_player_hit():
                    damage = self.game.current_location().attack()
                    damage_taken = self.game.player.is_hit(damage)
                    print(f"\n\t{self.game.current_location().name} attacked back!\n\t{damage_taken} damage taken!")
            else:
                dropped_loot = self.game.current_location().loot
                xp_gained = self.game.current_location().level*2
                self.game.enemy_is_dead()
                print(f"\tEnemy deafeated! You gained {xp_gained} XP!")
                if dropped_loot is not None:
                    print(f"\tIt dropped {dropped_loot}!")

    def get_current_coordinates(self):
        print(f"\tYour current coordinates are [{self.game.player.coord[0]}, {self.game.player.coord[1]}]")

    def uncover_location(self):
        action_result = self.game.look_around()
        if action_result:
            self.game.look_around()
            print(f"\tYou found {self.game.current_location().name}!")
        else:
            print("\tNothing hidden here")

    def level_up(self):
        if self.game.player.check_xp():
            self.game.player.level_up()
            print(f"{'*' * 5} LEVEL UP! {'*' * 5}\n\tCurrent level: {self.game.player.level}")

    def pickup_item(self):
        pickup = self.game.pickup()
        if pickup is not None:
            self.game.pickup()
            print(f"\tPicked up {pickup}!")
        else:
            print("\tNothing to pickup here!")

    def player_hit(self):
        if self.game.is_player_hit():
            value = self.game.current_location().attack()
            self.game.player.is_hit(value)
            print(f"\tYou got hit for {value} damage!")

    def can_player_enter(self):
        if self.game.get_needed_item():
            print(f"\tTo enter this place you need {self.game.get_needed_item()}")
            return False
        else:
            return True

    def describe_location(self):
        if self.game.current_location() is not None:
            if self.game.is_location_class():
                if self.game.current_location().is_hidden:
                    print("\tI think there is something here...")
                else:
                    print(f"\t{self.game.current_location().desc}")
            elif self.game.is_mapsquare_class():
                if self.game.current_location().is_hidden:
                    print("\tIt seems like someone has been here...")
                else:
                    print(f"\tThere is {self.game.current_location().name} here."
                          f"\n\tIt is {self.game.current_location().desc}")
            elif self.game.is_enemy_class():
                print(
                    f"\t{self.game.current_location().desc}\n\tI better draw my weapon, it is hostile "
                    f"{self.game.current_location().name}")
        else:
            print("\tNothing here...")

    def print_inventory(self):
        if self.game.player.inventory:
            print(f"\t Items in your inventory:\n\t\t{self.game.player.inventory}")
        else:
            print("\tYour inventory is empty!")

    def is_player_alive(self):
        if self.game.player.health <= 0:
            return False
        else:
            return True

    def print_player_health(self):
        print(f"Current health: {self.game.player.health}")

    @staticmethod
    def print_commands():
        print("Available commands: "
              "\n\t0. commands - to print all commands"
              "\n\t1. go - to go in the given direction"
              "\n\t2. describe - to describe current location"
              "\n\t3. examine - to uncover hidden items and location at current coordinates"
              "\n\t4. inventory - to print items in your inventory"
              "\n\t5. pickup - to pick up item that is at current location"
              "\n\t6. coordinates - to print current coordinates"
              "\n\t7. health - to get your current health"
              "\n\t8. attack - to attack"
              "\n\t9. save - to save"
              "\n\t10. exit - to exit"
              "\nYou can enter either number or name of action you desire to take")

    @staticmethod
    def player_death():
        print(f"{'*'*30}\n\t\tYOU ARE DEAD!\n{'*'*30}")
