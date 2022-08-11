from typing import Type
from UI import UI
from game import Game
import csv


def welcome_message():
    print(f"\nPlease type number of action you want to take:"
          f"\n\t1. New game"
          f"\n\t2. Load game"
          f"\n\t3. Exit")

def load_character():
    items = []
    try:
        with open("character_save.txt") as file:
            csvfile = csv.reader(file)
            header = next(csvfile)
            for row in csvfile:
                item = row
            return item
    except FileNotFoundError:
        print("\nCharacter save file not found!\n")
    except Exception:
        print("Unknown error!")

def load_game() -> UI:
    character = load_character()
    try:
        inventory = character[5]
        if inventory != '':
            inventory = inventory.split(';')
        else:
            inventory = []
        try: 
            GAME = UI(Game("map_save.txt", int(character[0]), int(character[1]), int(character[2]), int(character[3]), int(character[4]), inventory))
            return GAME
        except FileNotFoundError:
            print(f"{'-'*40}\nSAVE FILE NOT FOUND\n{'-'*40}")
            return UI(Game())
    except TypeError:
        GAME = UI(Game("map_save.txt"))
        return GAME
    except Exception:
        print("Cant load the game")
    

def main():
    game_menu = True
    print(f"\n{'*' * 5} Welcome to the game! {'*' * 5}")
    while game_menu:
        welcome_message()
        selection = input("What you want to do?: ")
        if selection == "1":
            play_game = True
            print("Starting new game...")
            try:
                GAME = UI(Game())
                GAME.start_game()
                GAME.print_commands()
            except FileNotFoundError:
                print("NO MAP FILE FOUND!")
                play_game = False
        elif selection == "2":
            play_game = True
            try:
                GAME = load_game()
                GAME.start_game()
                GAME.print_commands()
            except AttributeError:
                print("NO MAP FILE FOUND!")
                play_game = False
        elif selection == "3":
            print("Closing the game...")
            play_game = False
            game_menu = False
        else:
            play_game = False
            print("INVALID INPUT!")
        while play_game:
            if GAME.is_player_alive():
                GAME.level_up()
                player_input = input("What you want to do?: ")
                if player_input == "0":
                    GAME.print_commands()
                elif player_input == "1":
                    direction = input("\tIn what direction? (n/s/w/e): ")
                    GAME.move(direction)
                elif player_input == "2":
                    GAME.describe_location()
                elif player_input == "3":
                    GAME.uncover_location()
                elif player_input == "4":
                    GAME.print_inventory()
                elif player_input == "5":
                    GAME.pickup_item()
                elif player_input == "6":
                    GAME.get_current_coordinates()
                elif player_input == "7":
                    GAME.print_player_health()
                elif player_input == "8":
                    GAME.attack()
                elif player_input == "9":
                    GAME.save_game()
                elif player_input == "10":
                    print("\tThanks for playing!\n\tExiting to main menu...")
                    play_game = False
                else:
                    print(f"/n{'-'*15} INVALID INPUT! {'-'*15}")
                    GAME.print_commands()
            else:
                GAME.player_death()
                play_game = False


if __name__ == "__main__":
    main()
