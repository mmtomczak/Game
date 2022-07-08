from game_map import Map


def main():
    gmap = Map("map.txt")
    print(gmap.game_map[0].name)
    print(gmap.game_map[0].is_hidden)
    


if __name__ == "__main__":
    main()
