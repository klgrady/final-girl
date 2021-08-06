#!/usr/bin/python3
from datetime import datetime
from datetime import timedelta

"""Driving a simple game framework with
   a dictionary object | Alta3 Research"""

# Replace RPG starter project with this code when new instructions are live

def showInstructions():
    """Show the game instructions when called"""
    #print a main menu and the commands
    print('''
    Final Girl: A Horror RPG Game
    ========
    You came over to hang out with your friend as she babysat at a neighbor's house.
    Now you are the last would-be victim of a serial killer on the loose.
    Can you be the Final Girl and live to see daylight? Or will that honor go to the 
    child sleeping upstairs, somehow oblivious to all the screaming downstairs? Because
    of course, when it's something big, they don't wake up, but if it's a dog
    barking two miles away and you were busy doing stuff, nooooo, they won't
    sleep through that, will they?

    Anyway.

    ( No tiny people will be harmed during the playing of this game. )

    Commands:
      go [direction]
      get [item]
      use [item]
      open [item]
      close [item]
      say [dialogue]
    ''')

def showStatus():
    """determine the current status of the player"""
    #print the player's current status
    print('---------------------------')
    print('You are in the ' + currentRoom)
    #print the room description
    print(rooms[currentRoom]['description'])
    #print the current inventory
    print('Inventory : ' + str(inventory))
    #print an item if there is one
    if "item" in rooms[currentRoom]:
      print('You see a ' + rooms[currentRoom]['item'])
    print("---------------------------")

def update_time(current_time):
    current_time = current_time + timedelta(minutes=1) # add a minute for each loop
    return get_time(current_time)

def get_time(current_time):
    return current_time.strftime('%H:%M')

def init_time():
    #time keeper
    current_time = datetime.strptime('2:17', '%H:%M')
    return get_time(current_time)
    
#an inventory, which is initially empty
inventory = []

#items with descriptions and whether used


#a dictionary linking a room to other rooms
rooms = {

            'Bedroom' : { 
                'north' : 'Living Room',
                'east'  : 'Bathroom',
                'description' : f"""
                    An unmade bed sits against the wall, and a digital clock reads {timestr} """
            },

            'Living Room' : {
                'south' : 'Bedroom',
                'west'  : 'Kitchen',
                'east'  : 'Front Yard',
                'description' : """
                    A toppled couch barely hides the body of your friend, the television is playing static, 
                    and someone, somewhere in the house, is whimpering.
                    """
            },
            
            'Kitchen' : {
                'east' : 'Living Room',
                'west' : 'Back Yard',
                'description' : ''
            },

            'Bathroom' : {
                'west' : 'Bedroom',
                'description' : ''
            },

            'Front Yard' : {
                'west' : 'Living Room',
                'description' : ''
            },

            'Back Yard' : {
                'east' : 'Kitchen'
            },

            'Upstairs' : {
                'downstairs' : 'Living Room'
            }

         }

#start the player in the Hall
currentRoom = 'Living Room'

showInstructions()

#loop forever
while True:
    timestr = update_time(current_time)
    #print(time_string)
    showStatus()
  
    #get the player's next 'move'
    #.split() breaks it up into an list array
    #eg typing 'go east' would give the list:
    #['go','east']
    move = ''
    while move == '':  
        move = input('>')
    
    # split allows an items to have a space on them
    # get golden key is returned ["get", "golden key"]          
    move = move.lower().split(" ", 1)
  
    #if they type 'go' first
    if move[0] == 'go':
        #check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            #set the current room to the new room
            currentRoom = rooms[currentRoom][move[1]]
        #there is no door (link) to the new room
        else:
            print('You can\'t go that way!')
  
    #if they type 'get' first
    if move[0] == 'get' :
        #if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
            #add the item to their inventory
            inventory += [move[1]]
            #display a helpful message
            print(move[1] + ' got!')
            #delete the item from the room
            del rooms[currentRoom]['item']
        #otherwise, if the item isn't there to get
        else:
            #tell them they can't get it
            print('Can\'t get ' + move[1] + '!')
