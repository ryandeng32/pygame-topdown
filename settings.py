import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024 # 1024  16 * 64 or 32 * 32 or 64 * 16    1024
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12      768

FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = (40, 40, 40)

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'
LIGHT_MASK1 = 'light_350_hard.png'
LIGHT_MASK2 = 'light_350_med.png'
LIGHT_MASK3 = 'light_350_soft.png'

NIGHT_COLOR = (40, 40, 40)
LIGHT_RADIUS = (500, 500)

CAR_IMG = 'car_black_3.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_FUEL = 5000
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'manBlue_hold.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 30, 30)
BARREL_OFFSET = vec(30, 10)

# Gun settings
BULLET_IMG = 'bullet_dark.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
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

# Items
ITEM_IMAGES = {'health': 'health_pack.png', 'gas': 'gas_tank.png', 'map' : 'minimap.png'}
