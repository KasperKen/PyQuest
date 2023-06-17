import os #For determining Operating system, and clearing screen.


def format_list(input_list):
    if len(input_list) > 1:
        part1 = slice(-1)
        output_list = ', '.join(input_list[part1]) + ' and ' + input_list[-1]
    else:
        output_list = (input_list[0])
    return output_list


def clear(): # 
    ''' Determine OS type and clear screen. '''
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def new_line():
    ''' Boiler plate to avoid typing "print()" constantly. '''
    print('\n')



class Character:

    instances = [] #For storing a list of all existing characters.
    player_character = False #Used to determine which character instance is the player character.


    def __init__(self, name, race='Human', character_class='Fighter', ):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.inventory = [
            {'item_id': '001', 'name': 'apple', 'type': 'food', 'count': 2},
            {'item_id': '002', 'name': 'health potion', 'type': 'potion', 'count': 1}]
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

    def print_inventory(self):
        ''' Formats and prints the player character's inventory to the screen based on the item type. '''
        for item in self.inventory: #Iterate through all items in inventory.
            if item['type'] == 'weapon':
                stats = (f"Atk: {str(item['dice_count'])}d{str(item['sides'])}")
            elif item['type'] == 'armor':
                stats = (f"Def: {str(item['ac'])}")
            else: stats = ''
            print(f"{item['name'].capitalize()}: type: {item['type']} x{item['count']}, {stats}") #Prints item name, type, and count.



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

    @classmethod
    def describe_room(cls):
        ''' Prints info about the current room, such as enemies, items, and valid directions to screen. '''
        print(cls.current_room.name) #Prints the current room name.

        valid_directions = format_list(cls.current_room.valid_directions()) #Returns a list of valid directions formatted for printing.
        print(f'You can go {valid_directions}') #Prints the valid directions to the screen.

        if cls.current_room.item:
            print(f"You see a {cls.current_room.item['name']}") #IF there is an item in the current room, print that item.
        if cls.current_room.enemy:
            print(f"You see a {cls.current_room.enemy['name']}") #IF there is an enemy in the current room, print the name of the enemy.
        else:
            print('The Room is clear') #IF there are no enemies, print the room is clear.

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

    @attribute.deleter
    def attribute(self):
        ''' Allows the deleting of instance attributes. '''
        del self._attribute

    def direction_true(self, direction):
        ''' If a direction is valid for a given room instance return TRUE, ELSE FALSE. '''
        if direction in self.directions:
          if self.directions[direction]:
              return True
          else:
              return False
        else:
            return False

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


#Environment
#Create variables representing dicts with item information. 
apple = {'item_id': '001', 'name': 'apple', 'type': 'food', 'count': 1}
health_potion = {'item_id': '002', 'name': 'health potion', 'type': 'potion', 'count': 1}
Crown = {'item_id': '003', 'name': 'crown', 'type': 'armor', 'ac': '2', 'count': 1}
cloak = {'item_id': '004', 'name': 'cloak', 'type': 'armor', 'ac': '1', 'count': 1}
steel_sword = {'item_id': '005', 'name': 'Steel Sword', 'type': 'weapon', 'dice count': 2, 'sides': '6', 'count': 1}
wooden_shield = {'item_id': '006', 'name': 'Wooden Shield', 'type': 'armor', 'ac': 5, 'count': 1}

#Create variables representing room instances which will be created and added to the Room class instances list.
room1 = Room(name='Dragons Keep', north='Endless Pit', west='Solitary Room', east='Main Hall', item=apple)
room2 = Room(name='Endless Pit', south ='Dragons Keep', item=health_potion)
room3 = Room(name='Solitary Room', east='Dragons Keep')
room4 = Room(name='Main Hall', west='Dragons Keep')
Room.current_room = room1 #Sets the current room to the starting room.

player_character = Character(name='Johan the Mighty', race='Human', character_class='Paladin') #Creates a default player charecter.
Character.player_character = player_character #Sets the player charecter to be the character instance created in previous step.


def print_command_list():
    ''' Prints a list of all useable commands. '''
    print('Command List')
    new_line()
    print('go, travel, walk, etc.: Travels to new area. example: "go south".')
    print('help: Get list of valid commands.')
    print('get, take, grab, etc.: Takes item from the room')
    print('quit: Quits the current game.')


def quit_game():
    ''' Ask the player to confirm, and then quit the game. '''
    while True:
        user_input = str(input('Are you sure you want to quit game? (Yes:No): ')).lower()
        if user_input in ['yes', 'y', 'sure', 'yeah', 'yup']:
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
        print(f"You took the {item['type']}")
    else: print('No item to take')


clear()

def main():
    ''' Main gameplay loop. Ask for commands and fulfill player request before notifying them of results or error. '''
    while True: #Loop until quit.
        user_input = str(input('Enter a command: ')).lower().split(' ') #Take a user command and split it into command, and argument.
        command = user_input[0]
        argument = user_input[-1]

        if command in ['go', 'travel', 'move', 'walk', 'north', 'south', 'east', 'west']:
            ''' IF travel command then check to see if direction is valid, and change rooms. '''
            clear()
            Room.travel(argument) #Argument would be the intended direction e.g "go 'north'"
            new_line()
            Room.describe_room()
            new_line()

        elif command in ['where', 'look', 'describe', 'location', 'room', 'area', 'place']:
            ''' IF describe command, describe the current room and it's properties '''
            clear()
            Room.describe_room()
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

main()
