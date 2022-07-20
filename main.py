from UI import UI
from game import Game


def main():
    gme = Game("map.txt", 10, 5, 0, 2, 1, [])
    game_ui = UI(gme)
    game_ui.uncover_location()
    game_ui.get_current_coordinates()
    game_ui.print_inventory()
    game_ui.describe_location()
    game_ui.pickup_item()
    game_ui.print_inventory()
    game_ui.print_commands()

    


if __name__ == "__main__":
    main()
