#!/usr/bin/python3
from datetime import datetime
from datetime import time
from datetime import timedelta
from tkinter import *
from PIL import ImageTk, Image
import time
import pygame
import os

"""Driving a simple game framework with
   a dictionary object | Alta3 Research"""

# Replace RPG starter project with this code when new instructions are live
current_time = datetime(year=1993, month=6, day= 18, hour=2, minute=17, second=0)
time_str = current_time.strftime('%H:%M')

def splashScreen():
    try:
        display = Tk()
        img = ImageTk.PhotoImage(Image.open('image/finalfinalgirl.png'))
        mlabel = Label(display)
        mlabel.pack()
        panel = Label(display, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        
        display.after(5000, lambda:display.destroy())
        display.mainloop()
    except Exception as ex:
        file = open("errors.log", "w")
        file.write("Error on Tkinter video window close:", str(ex))
        file.close()


def showInstructions():
    """Show the game instructions when called"""
    #print a main menu and the commands
    print('''
    Final Girl: A Horror RPG Game
    ========
    It's 1993. You were visiting a friend as she babysat at a neighbor's house.
    But now, you are the last would-be victim of a preternatural killer on the loose.

    Can you be the Final Girl and live to see daylight? Or will that honor go to the 
    child sleeping upstairs, somehow oblivious to all the screaming downstairs? Because
    of course, when it's something big, they don't wake up, but if it's a dog
    barking two miles away and you were busy doing stuff, nooooo, they won't
    sleep through that, will they?

    Anyway.

    Find a way to kill the psycho before the psycho kills you.

    ( No tiny people will be harmed during the playing of this game. )

    Commands:
      go [direction]
      get [item]
      open [item]
      say [dialogue]
      inventory (to see what you're carrying)
    ''')

def showStatus():
    """determine the current status of the player"""
    #print the player's current status
    print('---------------------------')
    print('You are in the ' + currentRoom)
    #print the room description
    print(rooms[currentRoom]['description'])
    #print the current inventory
    #print('Inventory : ' + str(inventory))
    #print an item if there is one
    if "item" in rooms[currentRoom]:
        print('You see: ', end="")
        for thing in rooms[currentRoom]['item']:
            print(thing + " ", end="")
    print("\n---------------------------")

def update_time():
    global current_time, time_str
    current_time += timedelta(seconds=20) # add a minute for each loop
    time_str = current_time.strftime('%H:%M')

def check_win():
    global inventory, currentRoom
    # must have completed the incantation, gone outside, and collected hairspray and lighter
    # and something cutty
    retval = True
    if currentRoom != "Front Yard" and currentRoom != "Back Yard": retval = False
    if "hairspray" not in inventory: retval = False
    if "lighter" not in inventory: retval = False
    if "knife" not in inventory and "poker" not in inventory: retval = False
    if "incantation" not in inventory: retval = False
    return retval




#an inventory, which is initially empty
inventory = []

#a dictionary linking a room to other rooms
rooms = {

            'Bedroom' : { 
                'north' : 'Living Room',
                'east'  : 'Bathroom',
                'description' : f"""
                    An unmade bed sits against the wall, and a bedside table holds a stack of books and a phone. 
                    The curtains for the south-facing window are torn and partially obscure the streetlights. The
                    doors are to the north and east. A digital alarm clock shows the current time.
                    """,
                'item' : ['book', 'phone']
            },

            'Living Room' : {
                'south' : 'Bedroom',
                'west'  : 'Kitchen',
                'east'  : 'Front Yard',
                'upstairs' : "Upstairs",
                'description' : """
                    A toppled couch barely hides the body of your friend, the television is playing static, 
                    and someone, somewhere in the house, is whimpering. A bloody poker sits by the fireplace.
                    There are doors to the south, west, and east, and a dark staircase is behind the television.
                    """,
                'item' : ['poker']
            },
            
            'Kitchen' : {
                'east' : 'Living Room',
                'west' : 'Back Yard',
                'description' : """
                    Window curtains billow from the window over the sink. The water is running, and a large knife
                    sits by the sink. The kitchen table has a pack of cigarettes, an ashtray, and a lighter. The
                    doors are to the east and west.
                    """,
                'item' : ['knife', 'cigarettes', 'ashtray', 'lighter']
            },

            'Bathroom' : {
                'west' : 'Bedroom',
                'description' : """
                    A body lies in the bathtub, rolled up in the shower curtain. A can of hairspray, a brush,
                    and a bloody tube of toothpaste are scattered around the sink. The only door is the way you
                    came in. There is no other way out.
                    """,
                'item' : ['hairspray', 'brush', 'toothpaste']
            },

            'Front Yard' : {
                'west' : 'Living Room',
                'description' : """
                    The streetlamps are giving off an eerie light, and the night is quiet -- no frogs croak,
                    no cicadas chirp, no dogs bark. There is nothing but the sound of static on the TV from
                    inside. A crushed walkman is at your feet.
                    """,
                'item' : ['walkman']
            },

            'Back Yard' : {
                'east' : 'Kitchen',
                'description' : """
                    Dense woods line the back of the yard, and the night is quiet. Too quiet. A rake is propped
                    against the house, and a kids' pink beach ball lies abandoned in the grass.
                    """,
                'item' : ['rake', 'ball']
            },

            'Upstairs' : {
                'downstairs' : 'Living Room',
                'description' : """
                    What are you, a noob? Never run up the stairs when a killer's on the loose. You've earned
                    what you get now.
                    """
            }

         }

def main():
    global currentRoom, inventory
    currentRoom = 'Living Room'
    pygame.init()
    pygame.mixer.init()
    sd = 'sound'

    opening = pygame.mixer.Sound(os.path.join(sd, 'opening.ogg'))
    killer  = pygame.mixer.Sound(os.path.join(sd, 'killer.ogg'))
    #os.system('start image/finalgirl.jpg')

    # start with some sound
    opening.play()
    
    # show splash screen
    splashScreen()
    
    showInstructions()

    #loop forever
    while True:
        update_time()
        showStatus()
    
        # Prompt for next user move
        move = ''
        while move == '':  
            move = input('>')
        
        # split input into action and detail
        move = move.lower().split(" ", 1)
    
        #if they type 'inventory'
        if move[0] == 'inventory':
            print('You\'re carrying: ' + 'empty' if not inventory else 'You\'re carrying: ' + ' '.join(inventory))

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
            if move[1] == 'time' and currentRoom == 'Bedroom':
                print('The time is ' + time_str)
            elif move[1] == 'phone':
                print("""
                You pick up the phone and see the cord has been cut. There is no dial tone. You shake your fist at the gods
                and wish technology didn't suck in the early 90s.
                """)
            elif "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item'] and len(inventory) < 6:
                #add the item to their inventory
                inventory += [move[1]]
                #display a helpful message
                print('You pick up the ' + move[1] + '. Maybe this will help...')
                #delete the item from the room
                rooms[currentRoom]['item'].remove(move[1])
            #otherwise, if the item isn't there to get
            else:
                #tell them they can't get it
                print('Can\'t get ' + move[1] + '!')
                if len(inventory) < 6: 
                     print("""
                 Your pockets are full, my friend, and you\'re too panicked to drop anything.
                 """)

        if move[0] == 'open':
            if move[1] != 'book':
                print("""
                Why, tho? I mean, don't you have better things to do? Like, outwit a killer?
                """)
            else:
                print("""
                When you crack open the cover of the very old, leather-bound book, it flops open
                to a bookmarked page. There is blood spatter on the paper, but the page has only
                some words that look like Latin, and someone has scrawled in pencil beside it: 
                say incantation!
                """)

        if move[0] == 'say':
            if move[1] == 'incantation':
                inventory += ['incantation']
                print("""
                You try out the words in a whisper a few times, and when you think you might
                have the words somewhat right, you say them aloud:
                
                Morrigan mé a chosaint agus neart a thabhairt dom!

                You realize that's probably not Latin after all, but whatever. Now you've made noise.
                It's time to move before the killer finds you.
                """)
            else:
                print("""
                So, like, when did you decide you have a deathwish? Do you not understand what's
                going on here?? Hush it and survive.
                """)
            
        # if they're dumb enough to run upstairs when there's a killer in the house
        if currentRoom == "Upstairs":
            print("""
                What are you, a noob?? Never run up the stairs when a killer is looking for you.
                The killer comes up behind you, and you lunge for the landing. You never make it.
                As you lose consciousness, you see the terrified little girl run from the bedroom with
                a snowglobe in her hand. She throws it at the killer, and the wet crack of its impact 
                against his head and his body crashing down the stairs are the last things you hear. 
                
                She is the Final Girl.
            """)
            killer.play()
            while (pygame.mixer.get_busy()):
                time.sleep(0.1)
            break

        # if they've run out of time
        if time_str == "02:34":
            print("""
                From behind you in the {currentRoom}, you hear the shuffle of feet and the scrape of metal against wall.

                Time has run out. The killer has found you. 
                
                You are not the Final Girl.
            """)
            killer.play()
            while (pygame.mixer.get_busy()):
                time.sleep(0.1)
            break

        # if they've managed to win
        if check_win():
            print('Great battle ensues! You win!')
            break

if __name__ == "__main__":
    main()