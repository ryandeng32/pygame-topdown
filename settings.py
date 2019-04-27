import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
WHITEGREY = (170, 170, 170)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
###########################################

# game settings
WIDTH = 1024
HEIGHT = 768
WIDTH_MINI = 2024
HEIGHT_MINI = 1768

FPS = 60
TITLE = "GAME NAME HERE"

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
############################################

LIGHT_MASK1 = 'light_350_hard.png'
LIGHT_MASK2 = 'light_350_med.png'
LIGHT_MASK3 = 'light_350_soft.png'
NIGHT_COLOR = (40, 40, 40)
LIGHT_RADIUS = (500, 500)
LIGHT_RADIUS2 = (1000, 1000)


CAR_IMG = 'car_black_3.png'
CAR_FUEL = 5000
CAR_SPEED = 500
CAR_ROT_SPEED = 180

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'manBlue_hold.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 30, 30)
BARREL_OFFSET = vec(30, 10)

# Gun settings
BULLET_IMG = 'bullet_dark.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = {'handgun': 150, 'destroyer': 30}
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 125, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
VENOM_IMG = 'venom.png'
DETECT_RADIUS = 400

# game images
LOGO_IMAGE = 'logo.png'
#LOGO_IMAGE = 'nintendo_logo.jpg'

MENU_IMAGE = 'menu_img.jpg'
TRAILER_IMAGES = ['bg1.jpg', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg']


# Items
ITEM_IMAGES = {'health': 'health_pack.png', 'fuel': 'gas_tank.png',
               'map': 'minimap.png', 'torch': 'torch.png',
               'handgun': 'handgun.gif', 'destroyer': 'destroyer.gif',
               'note': 'note.png'}

ITEM_LIST_ALL = ['health', 'fuel', 'map', 'torch', 'note', 'handgun', 'destroyer']
ITEM_LIST = ['health', 'torch', 'fuel']
ITEM_BAR_Y = {'health': 13, 'torch': 8, 'fuel': 15}
GUN_LIST = ['handgun', 'destroyer']


BOB_RANGE = 4
BOB_SPEED = 0.1


# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 40
SPLAT = 'splat green.png'
# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4


# Sounds
BG_MUSIC = 'espionage.wav'
MENU_MUSIC = 'menu.wav'
#BG_MUSIC = 'open.mp3'
LOGO_MUSIC = 'logo.wav'


#MENU_MUSIC_2 = 'open.mp3'

PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']

ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = {'handgun': 'sfx_weapon_singleshot2.wav', 'destroyer': 'destroyer.wav'}

EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'typing': 'typing.wav',
                  'alert': 'alert.wav',
                  'page_turn': 'page_turn.wav'}

NOTE_IMAGES = {1: 'note_display1.png', 2: 'note_display2.png', 3: 'note_display3.png'}
COLLECTION_IMAGE = 'white_bg.jpg'
