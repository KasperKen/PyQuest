# PyQuest
This is a simple text based game wmich can act as a basic framework for a larger text base dungeon crawler. Currently the game supports traveling between rooms, gathering items, checking inventory, etc. Weapons and armor currently have stats, but the character cannot equip items to their paperdoll, and there is no combat system at this time. There is a temporary win condition used as a placeholder. In order to win the game, the player must traverse all of the rooms and gather all 8 items before encountering the wizard. If the player encounters the wizard prematurely, they will lose the game.

## Downloading
Git:
>git clone https://github.com/kasperken/pyquest

## How to Play
Type a command to move between rooms, take items, or check inventory.

### Command List
| Command | Argument | Description | Alternative Commands/Aliases |
| ----------- | ----------- | ------------------------------------|-------------------------|
| go | north | Moves between rooms. | walk, run, travel, move |
| take | n/a | Moves item from room to inventory. | grab, get |
| look | n/a | Describes the current room. | describe, where, location, room, area, place |
| gear | n/a | Print character inventory to console. | inventory, bag, equipment, items |
| quit | n/a | Quits the game. | n/a |

### Win/Loss Condition
In order to beat the game, the player must collect all 8 items before encountering the wizard. If the wizard is encountered before collecting all 8 items, the game will end in a loss. *hint: Use the gear command to check your current progress.

## To Do
- [x] Navigatable Rooms
- [x] Character Generator
- [x] Items and inventory
- [ ] Convert Items from dictionarys to object instances
- [ ] Move classes to their own respective modules
- [ ] eqippable gear affects character stats
- [ ] combat system
- [ ] Fully implement character Races
- [ ] Fully implement character classes
- [ ] Experience and leveling system
