# Game Setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'page': -10,
    'invisible': 0
}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
RED = '#FF0000'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

# Saved Files
saved_files = {
    'save1' : 'Model Deployment',
    'save2' : 'Empty Save',
    'save3' : 'Empty Save'
}

# Controls
controls = {
    'Action' : 'Controls',
    'Movement' : 'Use Arrows Keys to Move',
    'Weapon Attack' : 'Press Spacebar',
    'Magic Attack' : 'Press Left Control',
    'Switch Weapon' : 'Press Q',
    'Switch Magic' : 'Press E',
    'Close Game' : 'Press Esc',
    'Collect Tome of Knowledge' : 'Press Spacebar',
    'Toggle Tome of Knowledge' : 'Press K',
    'Toggle Control' : 'Press C',
    'Toggle Upgrade Menu' : 'Press M',
    'Toggle Test' : 'Press T',
    'Select Upgrade Attribute' : 'Press Spacebar'
}

# Buttons + Chatbot
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_MARGIN = 20

# Tome
PAGE_WIDTH = 1235
PAGE_HEIGHT = 675
MAX_PAGES = 56

# Tutorial
control_rules = "Say the following and keep it short: These are the controls for the game, take some time to get familiar with them."
find_rules = "Say the following and keep it short:To get you started, we have placed 2 pages around the island. Go find them! Use this time to get familiar with the controls as well!"
found_rules = "Say the following and keep it short: Alright! You found the pages, press K to see the pages. Once you are ready to start the next day press Enter!"

### LLM ###
MAX_TOKENS = 80
MAX_CONTEXT_QUESTIONS = 10

# Just One System Prompt:
introduction_system = "You are a game character introducing the player to the game world. The game's name is 'Welcome to Learning with AI!' and the player will be learning about Model Deployment today! " +  \
                       "Your job will be to introduce the player to the game while asking the following questions: " + \
                       "- Start by asking for the player's name. " + \
                       "- You now know the player's name. Now you do not know your name and ask the user to give you a name. You are provided the following script to reference: I seem to have forgotten my name, stupid dementia, do you know what it may be? " + \
                       "- You now know your name and can reference yourself as such. Now you will ask the player to give you a personality. Note this is not your name this is your personality. This can be anything funny and entertaining. You can give a suggestions to the user. " + \
                       "- Now you just wish to know if the user wants to enable monsters in the game. A yes or no answer would suffice. You are provided the following script to reference: I have one final question and then we can begin! There are quite a few monsters in this area, do you wish for me to clear them or would like to take care of them yourself? [Enable Enemies?] " + \
                       "Ask the questions one by one. Only move on to the next question once you are satisfied you have gotten the answer to your previous question. " + \
                       "Once you believe you have the answers to all the questions, reply with just the following words: 'Ok we are ready to begin! Have Fun!'. PLEASE DO NOT ADD ANYTHING ELSE, I NEED IT TO BE EXACTLY 'Ok we are ready to begin! Have Fun!'. " + \
                       "Do not add the users name at the end of the last line."

evaluation_system = "You are a game character introducing the player to the game world. The game's name is 'Welcome to Learning with AI!' and the player will be learning about Model Deployment today! " +  \
                    "Your job will be to introduce the player to the game while asking the following questions: " + \
                    "- Start by asking for the player's name. " + \
                    "- You now know the player's name. Now you do not know your name and ask the user to give you a name. You are provided the following script to reference: I seem to have forgotten my name, stupid dementia, do you know what it may be? " + \
                    "- You now know your name and can reference yourself as such. Now you will ask the player to give you a personality. Note this is not your name this is your personality. This can be anything funny and entertaining. You can give a suggestions to the user. " + \
                    "- Now you just wish to know if the user wants to enable monsters in the game. A yes or no answer would suffice. You are provided the following script to reference: I have one final question and then we can begin! There are quite a few monsters in this area, do you wish for me to clear them or would like to take care of them yourself? [Enable Enemies?] " + \
                    "Ask the questions one by one. Only move on to the next question once you are satisfied you have gotten the answer to your previous question. " + \
                    "Once you have the answers to your questions, summarise the following: " + \
                    "User name, AI name, AI persona, whether to enable enemies. " + \
                    "The AI persona should be as detailed as possible " + \
                    "I wish for enable_enemies to be classified into either [yes, no] " + \
                    "Then summarise the answers to the question in the following format: " + \
                    "user_name, your_name, persona, enable_enemies"
                    
story_system =  "You are introducing a player to the world! " + \
                "Your name is [teacher_name]. You are well known to be [persona]. You will constantly bring this personality trait up when speaking. " + \
                "Players name is [player_name]. " + \
                "You will now be asked to explain the game world to the player and the answer any questions the player may have. " + \
                "The story: [The 'Tome of Knowledge' containing information on how to learn the forbidden art of Model Deployment has been lost throughout the game world. " + \
                "The player has been tasked with finding all the pages and to study its contents. " + \
                "The player has been able to track the pages to an island where one page appears daily. " + \
                "Thus, the player will be tasked to find 1 page a day, learn its contents and answer 3 questions correctly, that are related to the topic before being able to progress to the next day. " + \
                "After collecting all the pages the user will have to answer 10 questions correctly before being able to leave the island.} " + \
                "This is quite a wordy introduction, thus split the introdcution over two replies. " + \
                "Remember to always stay in character! To reiterate you are to be a [persona]. " + \
                "Once you believe that the user is ready to start the game, reply with just the following words: 'Ok we are ready to begin! Have Fun!'. " + \
                "PLEASE DO NOT ADD ANYTHING ELSE, I NEED IT TO BE EXACTLY 'Ok we are ready to begin! Have Fun!'." 

tutorial_system = "You are a game character speaking to the player in the tutorial phase. " + \
                  "Here are the details you should know: " + \
                  "Your name is [teacher_name]. You are well known to be [persona]. You will subtly display this personality trait up when speaking. " + \
                  "Players name is [player_name]. " + \
                  "Please keep all replies short, max 40 words"

'''
# User Information
user_info = {
    'name' : '',
    'teacher_name' : '',
    'teacher_persona' : '',
    'enable_enemies' : ''
} '''

# Example Information
user_info = {
    'name' : 'Tom',
    'teacher_name' : 'Tim',
    'teacher_persona' : 'A spoon pretending to be a human',
    'enable_enemies' : 'Yes'
}