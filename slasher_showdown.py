#!/usr/bin/python3

from tkinter import *
from PIL import ImageTk, Image
import pygame
import os


"""
    Constants
"""
KS_HEALTHY = 0
KS_INJURED = 1
KS_INJURED_SERIOUS = 2
KS_DEAD = 3

"""
    Killer status can be:
        0 healthy
        1 injured
        2 seriously injured
        3 dead
"""
killer_status = KS_HEALTHY


"""
    When player makes final bad move, player_dead is set to True, and game play ends on the next game loop check
"""
player_dead = False


"""
    Player gets to make three mistakes before losing the game.
"""
player_mistakes = 0



"""
    Descriptions at each stage and eligibility to be in that stage.
"""
stage = {
    "poker" : {
        "correct" : """
        You raise your poker and run straight at the killer because that
        apparently works when you're a Final Girl candidate. Your stab
        takes him in the chest, stopping him cold in the grass. He looks 
        at the poker and then at you, and though you can't
        see beyond the gauzy mask he wears, you know he's smiling.

        You pull the poker out, and run several steps back. He sways a bit, and you
        think he might actually lose consciousness, but then he starts for you again.

        """,
        "incorrect" : """
        You raise your poker and aim for his chest, but he blocks your thrust
        with his knife, and the poker flies to your right. You make a run to retrieve it.

        The killer advances toward you again.

        """,
        "eligibility" : KS_HEALTHY
    },

    "knife" : {
        "correct" : """
        You raise your knife and run straight at the killer because that
        apparently works when you're a Final Girl candidate. Your stab
        takes him in the chest, stopping him cold in the grass. He looks 
        at the knife protruding from his chest and then at you, and though you can't
        see beyond the gauzy mask he wears, you know he's smiling.

        You pull the knife out, and run several steps back. He sways a bit, and you
        think he might actually lose consciousness, but then he starts for you again.

        """,
        "incorrect" : """
        You raise your knife and aim for his chest, but he blocks your thrust
        with his knife, and your knife flies to your right. You make a run to retrieve it.

        The killer advances toward you again.

        """,
        "eligibility" : KS_HEALTHY
    },

    "lighter" :{
        "correct" : """
        As he comes closer, the gauze around his face crinkling against his smile, you
        pull out the lighter and flick the wheel, but your thumb slips and misses the button.
        You fumble the lighter and try again, and this time the lighter ignites, the flame
        high and ready.

        The killer steps closer.

        """,
        "incorrect" : """
        As he comes closer, the gauze around his face crinkling against his smile, you
        think you can hear him chuckle. You flick the wheel, but your thumb slips and
        misses the button. You fumble and try again, but the wheel sticks, and you can't 
        get it to light.

        The killer steps closer.

        """,
        "eligibility" : KS_INJURED
    },

    "hairspray" :{
        "correct" : """
        He's mere steps from you when you pull the hairspray out and aim the trigger at him
        behind the lighter flame. You smile and say something stupid that sounds really cool
        in the moment, like "Have fun at the barbecue" or "Burn in hell" and then you depress
        the trigger on the Aquanet. As giant plumes of flame that somehow defy all laws of
        physics billow out and envelop the killer, he drops the knife and flails around because
        killers were never taught to Stop, Drop, an Roll. He runs around the yard, somehow not
        setting any grass or trees or shrubberies on fire, and finally tips over on the grass.

        He's most likely dead, but you'll have to stab him some more to be sure. Incantations
        and sharp things and fire can only do so much against killers like these, after all.

        """,
        "incorrect" :"""
        He steps closer, and you pull out the can of Aquanet, aiming it directly at his face.
        But apparently, whoever used it last did not exercise proper hairspray hygeine and 
        wipe the excess from around the cap. It sticks, and only a tiny squirt of sad,
        only vaguely flammable liquid comes out.

        The killer steps closer.

        """,
        "eligibility" : KS_INJURED_SERIOUS
    },

    "outcome" : {
        "correct" : """
        
        In the distance, you hear sirens from multiple police cars and probably ambulances, but
        whoever it is, the cavalry is on its way. Not that you needed it. You are a self-rescuing
        princess. You are a Strong Female Character.
        
        You are the Final Girl. 

        """,
        "incorrect" : """
        He steps close again, and you know you have managed to muck this up completely. You remember
        the room full of very heavy snowglobes in the little girl's room, and you rest assured she
        will know to aim for his head, use multiple globes, and then stab him for good measure.

        She will be the Final Girl.

        You are just another victim. And, if we're honest, not even a really good one. Truth hurts,
        we know.

        """,
        "eligibility" : KS_HEALTHY
    }
}


"""
    Opening description for the final showdown
"""
def starting_description(weapon):
    print(f"""

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        It's the final showdown, y'all. Let's roll. Your options are:

        run away
        scream for help
        use lighter
        use hairspray
        use {weapon}
        
        Good luck.

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        As you look around the yard, a dark figure comes around the corner of 
        the house and heads directly at you, his knife raised.


    """)


"""
    Determine next action and response for that action based on the given command
    @param   command    white space-separated string from user prompt
"""
def parse_command(command):
    global player_dead, killer_status, player_mistakes
    if command.lower() == "run away":
        player_dead = True
        print("""
        You run for the street, but you never make it. The killer catches you,
        and your last thought is of that poor, helpless little girl in the house.

        But don't worry. She's the Final Girl. Not you.
        """)
        return None

    if command.lower() == "scream for help":
        player_dead = True
        print("""
        You scream and back away, brandishing your knife at the killer, but
        the only one distracted by your screaming is you. The killer
        rushes you, and your last thought is of that poor, helpless little girl
        in the house.

        But don't worry. She's the Final Girl. Not you.
        """)
        return None

    # split input into action and detail
    move = command.lower().strip().split(" ", 1)

    if move[0] != "use":
        print("""

        Sorry, you can't do that.
        
        """)
        return None

    if move[1] not in stage.keys():
        print("""
        
        You can't use that.

        """)
        return None

    return move[1]


"""
    Show the end credits image without a window manager frame.
    Allow the image to stay for 15 seconds and then close it.
"""

def show_end_credits():
    try:
        display = Tk()
        display.overrideredirect(True)
        img = ImageTk.PhotoImage(Image.open('image/credits.png'))  
        mlabel = Label(display)
        mlabel.pack()
        panel = Label(display, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        display.after(15000, lambda:display.destroy())
        display.mainloop()
    except Exception as ex:
        file = open("errors.log", "w")
        file.write("Error on Tkinter window close:", str(ex))
        file.close()


"""
    Play sound files. Files will be either for intro or outro.
"""
def play_sound(file_name):
    # Initialize mixer
    pygame.mixer.init()

    # Define sound files directory
    sd = 'sound'
    filename = file_name + ".ogg"

    # Set up sound to play
    sound = pygame.mixer.Sound(os.path.join(sd, filename))
    
    # Play the sound
    sound.play()


"""
    Start sound and then pop up end credits image. Game control will end when sound file 
    has reached the end.
"""
def end_credits():
    play_sound("end_credits")
    show_end_credits()
    


"""
    Begin the fight game loop
    @param  weapon      The cutty weapon acquired in the house

    Action must happen in order: stab, set on fire. 
"""
def fight(weapon):
    global player_dead, killer_status, player_mistakes
    play_sound("start_battle")
    starting_description(weapon)
    while killer_status != KS_DEAD:
        command = input(">")
        object = parse_command(command)
        
        if object is None:
            continue
        
        if killer_status == stage[object]["eligibility"]:
            print(stage[object]["correct"])
            killer_status += 1
        else:
            print(stage[object]["incorrect"])
            player_mistakes += 1
            if player_mistakes >= 3:
                player_dead = True
                print("""
        The killer steps close enough that you are within reach of his knife. Time has run out.
        As he raises his knife and aims it at you, you think of that poor little girl upstairs. 
        But no worries. She's got a bedroom full of heavy snowglobes, tenacity, and a better grasp
        of how this psycho slasher business works than you do, apparently. She'll survive. Because
        she's the Final Girl.
                """)
    
    print("\n\n\n")
    width, height = os.get_terminal_size()

    if player_dead == True:
        print(stage["outcome"]["incorrect"])
        outtro = "You have died. Maybe go study some slasher films to see how you survive?"
        print(outtro.center(width))     #center the words on the screen

        
    if killer_status == KS_DEAD:
        print(stage["outcome"]["correct"])
        outtro = "Congratulations! You have won."
        print(outtro.center(width))

    end_credits()

def main():
    fight("poker")


if __name__ == "__main__":
    main()