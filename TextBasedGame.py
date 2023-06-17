import os #For determining Operating system, and clearing screen.


class Character:

    instances = [] #For storing a list of all existing characters.
    player_character = None #Used to determine which character instance is the player character.


    def __init__(self, name, race='Human', character_class='Fighter', ):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.inventory = []
        self.__class__.instances.append(self) #Any new character instance should be added to class instances list.

    def find_item(self, new_item):
        ''' Checks to see if an item exists in object inventory and returns the item, or FALSE. '''
        for item in self.inventory:
            if item['item_id'] == new_item['item_id']: #If item already exists, RETURN the item.
                return item
        return False

    def add_to_inventory(self, new_item):
        ''' Checks if item is in inventory and either adds the item to inventory or increments it's count value. '''
        item = self.find_item(new_item) #Checks to see if item exists in inventory.
        if item:
            item['count'] += new_item['count'] #If self.find returns item, Increment it's count.
        else:
            self.inventory.append(new_item) #ELSE add item to the players inventory.
        return None

    def print_inventory(self):
        ''' Formats and prints the player character's inventory to the screen based on the item type. '''
        if len(self.inventory) == 0:
            print('Inventory is empty')
            return None
        for item in self.inventory: #Iterate through all items in inventory.
            if item['type'] == 'weapon':
                stats = (f"Atk: {str(item['dice_count'])}d{str(item['sides'])}")
            elif item['type'] == 'armor':
                stats = (f"Def: {str(item['ac'])}")
            else: stats = ''
            print(f"{item['name'].capitalize()}: type: {item['type']} x{item['count']}, {stats}") #Prints item name, type, and count.
        return None

#-------------------------------- END Character Class --------------------------------------------


class Room:

    instances = [] #For storing all Room instances.
    current_room = False #Used to determine what room instance is the current room.

    @classmethod
    def find_room(cls, room_name):
        ''' IF room exists in room instances RETURN room object. else RETURN False '''
        for room in cls.instances: #Iterate through all rooms.
            if room.name == room_name:
                return room #IF room exists, return the room.
        return False

    @classmethod
    def travel(cls, direction):
        ''' Used to change the current room, and print updates to screen. '''
        if cls.current_room.direction_true(direction): #IF the chosen direction is valid.
            cls.current_room = cls.find_room(cls.current_room.directions[direction]) #Change current room to the previous rooms direciton.
            print(f'You traveled {direction} to {cls.current_room.name}') #Notifies the player that they changed rooms.
        else: print(f'Can\'t go "{direction}".') #IF direction is invalid, tell the player they can't move in that direction.
        return None

    @classmethod
    def describe_room(cls):
        ''' Prints info about the current room, such as enemies, items, and valid directions to screen. '''
        print(cls.current_room.name) #Prints the current room name.

        valid_directions = format_list(cls.current_room.valid_directions()) #Returns a list of valid directions formatted for printing.
        print(f'You can go {valid_directions}') #Prints the valid directions to the screen.

        if cls.current_room.item:
            item_name = cls.current_room.item['name']
            determiner = 'an ' if item_name[0] in vowels else 'a '
            print(f"You see {determiner}{cls.current_room.item['name']}") #IF item in the current room, print that item.

        if cls.current_room.enemy:
            enemy = cls.current_room.enemy
            determiner = 'an ' if enemy.name[0] in vowels else 'a '
            if enemy.race in humanoid_races: determiner = ''
            print(f"You see {determiner}{enemy.name} the {enemy.character_class}") #IF enemy in current room, print the name of the enemy.

        else:
            print('The Room is clear') #IF there are no enemies, print the room is clear.

        new_line()
        return None

    def __init__(self, name, item=False, enemy=False, north=False, east=False, south=False, west=False):
        ''' Initialize room instances with a name, item, enemy, and valid directions. '''
        self.name = name
        self.directions = {'north': north, 'east': east, 'south': south, 'west': west}
        self.item = item
        self.enemy = enemy
        self.__class__.instances.append(self) #Add self to list of class instances at initialization.


    @property
    def attribute(self):
        ''' Allows reading instance attributes '''
        return self._attribute

    @attribute.setter
    def attribute(self, value):
        ''' Allows the changing, and creating of instance attributes. '''
        self._attribute = value
        return None

    @attribute.deleter
    def attribute(self):
        ''' Allows the deleting of instance attributes. '''
        del self._attribute
        return None

    def direction_true(self, direction):
        ''' If a direction is valid for a given room instance return TRUE, ELSE FALSE. '''
        if direction not in Room.current_room.directions: #Check if input is direction input matches a key. 
            return False

        if not self.directions[direction]: #Check if direction key has valid value.
            return False

        return True #Return TRUE only if key exists, and value associated with that key.

    def valid_directions(self):
        ''' Returns a list of all valid direciton elements beloning to room's direction attribute. '''
        valid_directions = []
        for direction in self.directions: #Iterate through directions.
            if self.direction_true(direction):
                valid_directions.append(direction) #IF the direction is valid, add it to the valid directions list.
        return valid_directions

    def remove_item(self):
        ''' Checks to see if item exists in the room, and removes it if it does. '''
        if self.item:
            self.item = False
        return None

#-------------------------------- END Room Class --------------------------------------------


vowels = ['a', 'e', 'i', 'o', 'u'] #For determining if grammar determiner should be 'a' or 'an'.
humanoid_races = ['Human', 'Elf', 'Dwarf', 'Orc', 'Halfling']

def print_command_list():
    ''' Prints a list of all useable commands. '''
    print('Command List')
    new_line()
    print('help: Get list of valid commands.')
    print('describe, look, room, etc: Describe the current room, and valid directions to travel.')
    print('go, travel, walk, etc.: Travels to new area. example: "go south".')
    print('get, take, grab, etc.: Takes item from the room')
    print('bag, inventory, gear, etc: Get a list of all the items in your inventory')
    print('quit: Quits the current game.')


def quit_game():
    ''' Ask the player to confirm, and then quit the game. '''
    while True:
        user_input = str(input('Are you sure you want to quit game? (Yes:No): ')).lower()
        if user_input in ['yes', 'y', 'sure', 'yeah', 'yup']:
            clear()
            quit()
        elif user_input in ['no', 'nah', 'nope', 'n']:
            clear()
            break
        else:
            clear()
            print(f'"{user_input}" is not a valid input')


def take_item():
    ''' If item exists add item to inventory and delete from room, or notify player there is no item. '''
    if Room.current_room.item: #IF item exists in room.
        item = Room.current_room.item #Set item variable to = the item in the room.
        Character.player_character.add_to_inventory(item) #Add item to players inventory.
        Room.current_room.remove_item() #Delete item from room.
        print(f"You took the {item['name']}.")
    else: print('No item to take')


def format_list(input_list):
    ''' Used to format the printing of list values according to propper gramatical rules. '''
    if len(input_list) > 1: #IF list has more than one element.
        part1 = slice(-1) #All list values except the last element.
        output_list = ', '.join(input_list[part1]) + ' and ' + input_list[-1] #JOIN list with last element adding 'and' to string.
    else:
        output_list = (input_list[0]) #ELSE return only the first element.
    return output_list #Return the formatted list as a gramatically correct string.


def clear(): # 
    ''' Determine OS type and clear screen. '''
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def new_line():
    ''' Boiler plate to avoid typing "print()" constantly. '''
    print('\n')


def win_loss_condition():
    ''' Check if player has collected all items and print victory or loss output depending on victory condition '''
    if len(Character.player_character.inventory) < 8: #IF player hasn't collected all items.
        print('Game Over')
        print('---------\n')
        print('You failed to gather all the items needed to defeat the Wizard.')
        print('The wizard turned you into a toad. Enjoy your new life on display in a jar.\n')
    else:
        print('You saved the realm!')
        print('--------------------\n')
        print('You used all of the items at your disposal to vanquish the evil wizard.')
        print('Stories of your heroic deed will be told for generations.')
    input('\n\nPress Enter to continue...')
    clear()
    quit()


#Environment
#Create variables representing dicts with item information. 
apple = {'item_id': '001', 'name': 'apple', 'type': 'food', 'count': 1}
crown = {'item_id': '003', 'name': 'crown', 'type': 'armor', 'ac': 2, 'count': 1}
cloak = {'item_id': '004', 'name': 'cloak', 'type': 'armor', 'ac': 1, 'count': 1}
steel_sword = {'item_id': '005', 'name': 'Steel Sword', 'type': 'weapon', 'dice_count': 2, 'sides': 6, 'count': 1}
plate_armor = {'item_id': '006', 'name': 'Plate Armor', 'type': 'armor', 'ac': 5, 'count': 1}
wine = {'item_id': '007', 'name': 'Wine', 'type': 'food', 'count': 1}
royal_sceptor = {'item_id': '008', 'name': 'Royal Sceptor', 'type': 'weapon', 'dice_count': 1, 'sides': 4, 'count': 1}
torch = {'item_id': '009', 'name': 'torch', 'type': 'weapon', 'dice_count': 1, 'sides': 2, 'count': 1}

#Create Variables representing character instances.
wizard = Character(name="Detarr Ur'Mayan", race='Human', character_class='Noctimancer')
player_character = Character(name='Johan the Mighty', race='Human', character_class='Paladin') #Creates a default player charecter.
Character.player_character = player_character #Sets the player charecter to be the character instance created in previous step.

#Create variables representing room instances which will be created and added to the Room class instances list.
room1 = Room(name='Courtyard', north='Main Hall')
room2 = Room(name='Main Hall', south='Courtyard', north='Throne Room', west='Black Smith', east='Dining Hall', item=torch)
room3 = Room(name='Black Smith', east='Main Hall', west="Guard's Quarters", item=steel_sword)
room4 = Room(name="Guard's Quarters", east='Black Smith', item=plate_armor)
room5 = Room(name='Throne Room', south='Main Hall', west="Wizard's Den", east="King's Quarters", item=royal_sceptor)
room6 = Room(name="King's Quarters", west='Throne Room', item=crown)
room7 = Room(name="Dining Hall", west='Main Hall', east='Hallway', item=wine)
room8 = Room(name="Hallway", west='Dining Hall', north='Kitchen', south='Servant Quarters')
room9 = Room(name="Kitchen", south='Hallway', item=apple)
room10 = Room(name="Servant Quarters", north='Hallway', item=cloak)
room11 = Room(name="Wizard's Den", east='Throne Room', enemy=wizard)
Room.current_room = room1 #Sets the current room to the starting room "Courtyard".


def main():
    print("You have been sent by the Heroes Guild to face the Mighty Noctimancer Detarr Ur'Mayan")
    print("You must navigate the castle searching for items to defeat the evil wizard.\n")
    new_line()
    print('Type "Help" for a list of commands\n')
    new_line()

    ''' Main gameplay loop. Ask for commands and fulfill player request before notifying them of results or error. '''
    while True: #Loop until quit.

        if Room.current_room.enemy:
            win_loss_condition()

        Room.describe_room()

        print('---------------------------------\n')
        user_input = str(input('Enter a command: ')).lower().split(' ') #Take a user command and split it into command, and argument.
        command = user_input[0]
        argument = user_input[-1]

        if command in ['go', 'travel', 'move', 'walk', 'north', 'south', 'east', 'west']:
            ''' IF travel command then check to see if direction is valid, and change rooms. '''
            clear()
            Room.travel(argument) #Argument would be the intended direction e.g "go 'north'"
            new_line()

        elif command in ['where', 'look', 'describe', 'location', 'room', 'area', 'place']:
            ''' IF describe command, describe the current room and it's properties '''
            #FIXME -- Not needed for now.
            clear()
            new_line()

        elif command in ['inventory', 'items', 'bag', 'equipment', 'gear']:
            ''' IF inventory command, print current inventory to screen. '''
            clear()
            Character.player_character.print_inventory()
            new_line()

        elif command in ['grab', 'get', 'take', 'add']:
            ''' IF item command, take the item, and delete it from the room. '''
            clear()
            take_item()
            new_line()

        elif command == 'help':
            ''' IF help command, print all available commands to screen. '''
            clear()
            print_command_list()
            new_line()

        elif command == 'quit':
            ''' IF quit command, ask for confirmation before quitting the game. '''
            clear()
            quit_game()

        else:
            ''' IF command does not fall into another category, notify player the command is invalid. '''
            clear()
            print(f'"{command}" is not a valid command.')
            new_line()

#-------------------------------- END Main Gameplay Loop --------------------------------------------


clear()
main()

