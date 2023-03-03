# Python terminal-based adventure game
This game was used as my final project for Introduction to Python programming class.

### Game information
Player starts at level 1 and with 2 HP points. Leveling up is possible by killing enemies. 
Player can find listed below items that, if present in inventory, can provide combat bonuses:
  - Armor - decreases incoming damage by factor of 5
  - Shield - decreases incoming damage by factor of 2
  - Sword - increases damage power by 10 points
  
  If Armor and Shield are both present in player's inventory only Armor effect will be applied
  
Some locations are hidden. To uncover them you need to use correct action.
If location is hidden loot present there is also hidden.

Success of attack is random, damage applied is random value in range [power; power*2]. Player power is equal to player level.


Player progress and map can be saved. **To print all avaliable commands player must type '0' in command line during the game.**

### Game map
Map for the game can be created by anyone in .csv format. To create map you need to add desired location to map.csv file. To do that you need to provide below information in shown order:
1. Location number
2. Location category (location/enemy/item)
3. Level (if category is enemy, else 0)
4. Location name
5. Location description
6. Location visibility status (0 - visible; 1 - hidden)
7. Numerical location on x-axis
8. Numerical location on y-axis
9. Loot present at location (0 if no loot is present)

**Each value is separated using _comma_.**


