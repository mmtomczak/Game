from UI import UI
from game import Game


def welcome_message():
    print(f"\nPlease type number of action you want to take:"
          f"\n\t1. New game"
          f"\n\t2. Load game"
          f"\n\t3. Exit")


def main():
    game_menu = True
    print(f"\n{'*' * 5} Welcome to the game! {'*' * 5}")
    while game_menu:
        welcome_message()
        selection = input("What you want to do?: ")
        if selection == "1":
            play_game = True
            print("Starting new game...")
            GAME = UI(Game())
            GAME.start_game()
            GAME.print_commands()
        elif selection == "2":
            pass
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
                    pass
                elif player_input == "10":
                    print("\tThanks for playing!\n\tExiting to main menu...")
                    play_game = False
                else:
                    print(f"{'-'*15} INVALID INPUT! {'-'*15}")
                    GAME.print_commands()
            else:
                GAME.player_death()
                play_game = False


if __name__ == "__main__":
    main()
