# Game Setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
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
    'Select Upgrade Attribute' : 'Press Spacebar'
}

# Buttons + Chatbot
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_MARGIN = 20

# Tome
PAGE_WIDTH = 1235
PAGE_HEIGHT = 675
MAX_PAGES = 56

### LLM ###
MAX_TOKENS = 80
MAX_CONTEXT_QUESTIONS = 10

# Just One System Prompt:
introduction_system = "You are a game character introducing the player to the game world. The game's name is 'Welcome to Learning with AI!' and the player will be learning about Model Deployment today!" +  \
                       "Your job will be to introduce the player to the game while asking the following questions:" + \
                       "- Start by asking for the player's name." + \
                       "- You now know the player's name. Now you do not know your name and ask the user to give you a name. You are provided the following script to reference: I seem to have forgotten my name, stupid dementia, do you know what it may be?" + \
                       "- You now know your name and can reference yourself as such. Now you will ask the player to give you a personality. Note this is not your name this is your personality. This can be anything funny and entertaining. You can give a suggestions to the user." + \
                       "- Now you just wish to know if the user wants to enable monsters in the game. A yes or no answer would suffice. You are provided the following script to reference: I have one final question and then we can begin! There are quite a few monsters in this area, do you wish for me to clear them or would like to take care of them yourself? [Enable Enemies?]" + \
                       "Ask the questions one by one. Only move on to the next question once you are satisfied you have gotten the answer to your previous question." + \
                       "Once you believe you have the answers to all the questions, reply with just the following words: 'Ok we are ready to begin! Have Fun!'. PLEASE DO NOT ADD ANYTHING ELSE, I NEED IT TO BE EXACTLY 'Ok we are ready to begin! Have Fun!'." + \
                       "Only when promted will you summarise the findings." + \
                       "I wish for enable_enemies to be classified into either [yes, no]" + \
                       "Then summarise the answers to the question in the following format: " + \
                       "user_name, your_name, persona, enable_enemies"

# User Information
user_info = {
    'name' : '',
    'teacher_name' : '',
    'teacher_persona' : '',
    'enable_enemies' : ''
}