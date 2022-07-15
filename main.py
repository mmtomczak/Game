from game_map import MapArea, MapSquare
from game import Game


def main():
    gme = Game("map.txt", 10, 5, 0, 2, 1, [])
    print(gme.map.map_size)
    print(gme.current_location().name)
    print(gme.look_around())
    print(gme.pickup())
    print(gme.current_location())
    print(gme.player.inventory)

    


if __name__ == "__main__":
    main()
