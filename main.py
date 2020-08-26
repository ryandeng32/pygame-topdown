##########################################
# Game name: Undecided                   #
# File name: main.py                     #
# Author: Ryan Deng                      #
# Last Edited: 26/08/2020                #
##########################################
import pygame as pg
import sys
import time
from os import path
from random import uniform, randint, choice
from math import sin, pi

from settings import *
from sprites import *
from tilemap import *
from scenes import *
from usedFunc import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.mini_map = pg.Surface((WIDTH_MINI, HEIGHT_MINI))

        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()


    def load_data(self):
#-------------------------basic   loading------------------------------#
        # Folders
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'map')
        self.snd_folder = path.join(self.game_folder, 'snd')
        self.music_folder = path.join(self.game_folder, 'music')
        self.zombie_folder = path.join(self.game_folder, 'zombie')
        self.player_folder = path.join(self.game_folder, 'player')
        self.boss1_folder = path.join(self.game_folder, 'Boss1')

        boss1_adjust = (200, 253)
        self.boss1_death = []
        for i in range(10):
            self.boss1_death.append(reimage(pg.image.load(path.join(self.boss1_folder, f'death/{str(i)}.png')).convert_alpha(), boss1_adjust))

        self.boss1_move = []
        for i in range(8):
            self.boss1_move.append(reimage(pg.image.load(path.join(self.boss1_folder, f'move/{str(i)}.png')).convert_alpha(), boss1_adjust))

        self.boss1_attack1 = []
        for i in range(14):
            self.boss1_attack1.append(reimage(pg.image.load(path.join(self.boss1_folder, f'attack1/{str(i)}.png')).convert_alpha(), boss1_adjust))

        self.boss1_attack2 = []
        for i in range(10):
            self.boss1_attack2.append(reimage(pg.image.load(path.join(self.boss1_folder, f'attack2/{str(i)}.png')).convert_alpha(), boss1_adjust))

        self.boss1_idle = []
        for i in range(8):
            self.boss1_idle.append(reimage(pg.image.load(path.join(self.boss1_folder, f'idle/{str(i)}.png')).convert_alpha(), boss1_adjust))





        zombie_adjust = (158, 127)
        self.zombie_death = []
        for i in range(6):
            self.zombie_death.append(reimage(pg.image.load(path.join(self.zombie_folder, f'death/{str(i)}.png')).convert_alpha(), zombie_adjust))
        self.zombie_idle = []
        for i in range(7):
            self.zombie_idle.append(reimage(pg.image.load(path.join(self.zombie_folder, f'idle/{str(i)}.png')).convert_alpha(), zombie_adjust))
        self.zombie_move = []
        for i in range(9):
            self.zombie_move.append(reimage(pg.image.load(path.join(self.zombie_folder, f'move/{str(i)}.png')).convert_alpha(), zombie_adjust))
        self.zombie_attack = []
        for i in range(9):
            self.zombie_attack.append(reimage(pg.image.load(path.join(self.zombie_folder, f'attack/{str(i)}.png')).convert_alpha(),zombie_adjust))





        player_adjust = (62, 104)

        self.player_death = []
        for i in range(6):
            self.player_death.append(reimage(pg.image.load(path.join(self.player_folder, f'death/{str(i)}.png')).convert_alpha(), player_adjust))
       # self.zombie_idle = []
       # for i in range(1):
         #   self.zombie_idle.append(reimage(pg.image.load(path.join(self.zombie_folder, f'idle/{str(i)}.png')).convert_alpha(), zombie_adjust))
        player_adjust = (62, 104)
        self.player_move = []
        for i in range(6):
            self.player_move.append(reimage(pg.image.load(path.join(self.player_folder, f'move/{str(i)}.png')).convert_alpha(), player_adjust))



        self.player_attack = []
        player_adjust = (63, 103)
        for i in range(12):
            self.player_attack.append(reimage(pg.image.load(path.join(self.player_folder, f'bat/{str(i)}.png')).convert_alpha(),player_adjust))


        # logo and menu images
        self.logo_img = pg.image.load(path.join(self.img_folder, LOGO_IMAGE)).convert()
        self.menu_img = pg.image.load(path.join(self.img_folder, MENU_IMAGE)).convert()
        self.collection_img = pg.image.load(path.join(self.img_folder, COLLECTION_IMAGE)).convert_alpha()

        # tiledmap
        self.map = TiledMap(path.join(self.map_folder, '32map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # dialog box
        self.text_box_img = pg.image.load(path.join(self.img_folder, 'text_box.png')).convert()
        self.text_box_img = pg.transform.scale(self.text_box_img, (WIDTH, 300))
        self.text_box_img.set_colorkey((255, 255, 255))
        self.text_box_img.set_alpha(180)


        # fog and light source
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.light_mask = pg.image.load(path.join(self.img_folder, LIGHT_MASK2)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        # images
        self.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG)).convert_alpha()
        self.car_img = pg.image.load(path.join(self.img_folder, CAR_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(self.img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, MOB_IMG)).convert_alpha()
        self.splat_img = pg.image.load(path.join(self.img_folder, SPLAT)).convert_alpha()
        self.venom_img = pg.image.load(path.join(self.img_folder, VENOM_IMG)).convert_alpha()

        # gun flashes and item images
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(self.img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(self.img_folder, ITEM_IMAGES[item])).convert_alpha()

        # images to display on item bar
        self.item_bar_images = {}
        for item in ITEM_IMAGES:
            self.item_bar_images[item] = pg.image.load(path.join(self.img_folder, ITEM_IMAGES[item])).convert_alpha()
        self.item_bar_images['torch'] = pg.transform.scale(self.item_bar_images['torch'], (15, 40))

        # images of notes
        self.note_images = {}
        for image in NOTE_IMAGES:
            self.note_images[image] = pg.image.load(path.join(self.img_folder, NOTE_IMAGES[image])).convert_alpha()

        # # trailer images
        # self.trailer_images = []
        # for image in TRAILER_IMAGES:
        #     self.trailer_images.append(pg.image.load(path.join(self.img_folder, image)).convert())
#-------------------------sound   loading -----------------------------#
        self.logo_music = pg.mixer.Sound(path.join(self.music_folder, LOGO_MUSIC))
        self.logo_music.set_volume(0.7)

        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(self.snd_folder, EFFECTS_SOUNDS[type]))
        self.effects_sounds['page_turn'].set_volume(0.3)

        self.weapon_sounds = {}
        self.weapon_sounds['handgun'] = (pg.mixer.Sound(path.join(self.snd_folder, 'sfx_weapon_singleshot2.wav')))
        self.weapon_sounds['destroyer'] = (pg.mixer.Sound(path.join(self.snd_folder, 'destroyer.wav')))
        self.weapon_sounds['destroyer'].set_volume(0.3)
        self.weapon_sounds['handgun'].set_volume(0.5)

        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(self.snd_folder, snd))
            s.set_volume(0.8)
            self.zombie_moan_sounds.append(s)

        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(self.snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(self.snd_folder, snd)))
#-------------------------dialog  loading -----------------------------#
        # dialog loading
        self.code = 0



    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.venoms = pg.sprite.Group()
        self.cars = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.guns = pg.sprite.Group()
        self.boss1s = pg.sprite.Group()
#------------------------spawn all sprites-----------------------------#
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)

            if tile_object.name == 'car':
                self.car = Car(self, obj_center.x, obj_center.y, -90)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)

            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'boss1':
                Boss1(self, obj_center.x, obj_center.y)
                print("Boss1 is spawned")
            if tile_object.name == 'venom':
                Venom(self, obj_center.x, obj_center.y)
            if tile_object.name in ITEM_LIST_ALL:
                Item(self, obj_center, tile_object.name)
#-------------------cameras and game setting booleans---------------#
        self.camera_main = Camera(self.map.width, self.map.height, WIDTH, HEIGHT)
        self.camera_mini = Camera(self.map.width, self.map.height, WIDTH_MINI, HEIGHT_MINI)

        self.draw_debug = False           # display hit_rect of sprites
        self.night = True                 # toggle night mode
        self.paused = False               # pause the game when set to True

        self.show_item_bar = False
        self.has_item_bar = False

        self.show_mini_map = False
        self.has_mini_map = False

        self.show_weapon = False
        self.has_weapon = False

        self.show_message = True
        self.show_note = False

        self.show_collection = False  # in testing

        self.show_exp = True

        # reset the opening dialog
        self.scene = 'start'
        self.dialog = SCENES
        self.dialog['start'][0] = 'Welcome back, subject #' + str(self.code)
        self.counter = 0
        self.x = 0
        self.note_chosen = -1
        self.col = WHITE

        # intense level start sound, too loud, needs to be decreased later
        # self.effects_sounds['level_start'].play()


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        # load game bgm
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC))
        pg.mixer.music.play(loops=-1)

        # game loop
        while self.playing:

            # this is for the game to run frame-rate independent
            # a tutorial can be found on https://www.youtube.com/watch?v=TIiYJaY8ZR0&feature=youtu.be
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x

            self.events()
            if not self.paused:
                self.update()
            self.draw('')


    def update(self):
#-----------------------sprite update and camera update------------#
        # call update function on each sprite
        self.all_sprites.update()
        # update cameras
        self.camera_main.update(self.player)
        self.camera_mini.update(self.player)
#----------------------player collide health, fuel, torch----------------------#
        hits = pg.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
        for hit in hits:
            if hit.type in ITEM_LIST:
                hit.kill()
                self.player.num_of_items[hit.type] += 1
                self.player.item_received[hit.type] += 1
                if hit.type not in self.player.item_order:
                    self.player.item_order.append(hit.type)
                if self.player.item_received[hit.type] == 1:
                    self.effects_sounds['alert'].play()

                    # display this message if this is the first item received
                    num = 0
                    for i in ITEM_LIST:
                        if i != hit.type:
                            num += self.player.item_received[i]
                    if num == 0:
                        self.dialog[hit.type].insert(0, "Use [i] to toggle item view")
                        self.show_item_bar = True
                        self.has_item_bar = True

                    self.show_message = True
                    self.scene = hit.type
#----------------------player collide guns--------------------------------#
            if hit.type in GUN_LIST:
                hit.kill()
                self.player.gun_type.append(hit.type)
                self.player.gun_received += 1
                if self.player.gun_received == 1:
                    self.show_weapon = True
                    self.has_weapon = True
                    self.effects_sounds['alert'].play()
                    self.show_message = True
                    self.scene = 'first_weapon'
#--------------------map and note collision--------------------#
            if hit.type == 'map':
                hit.kill()
                self.has_mini_map = True
                self.show_mini_map = True

                self.effects_sounds['alert'].play()
                self.show_message = True
                self.scene = 'map'

            if hit.type == 'note':
                hit.kill()
                self.effects_sounds['page_turn'].play()

                self.show_note = True
                self.dialog['note'][0] = f'Note Found ({len(self.player.note_received)+1} / {len(self.note_images)})'

                self.scene = 'note'

#---------------------mob hit player---------------------------------------#
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect2)
        for hit in hits:
            # chance of playing player hit sounds when getting hit
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            # decrease player health
            self.player.health -= MOB_DAMAGE
            # reset mobs' velocity
            hit.vel = vec(0, 0)
#---------------------end game------------------------
            # exit when player's health reaches 0
            if self.player.health <= 0:   #death quote in testing
                self.code += 1
                self.show_message = True
                self.scene = 'death'
                self.dialog[self.scene].append(choice(DEATH_QUOTE))
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
#-------------------------bullet hit mobs-----------------------------#
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True, collide_hit_rect2)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

        hits = pg.sprite.groupcollide(self.boss1s, self.bullets, False, True, collide_hit_rect2)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)


    def draw(self, string):


        pg.display.flip()
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))  # for testing [display framerate on title]
        # blit map onto surfaces
        self.screen.blit(self.map_img, self.camera_main.apply_rect(self.map_rect))
        self.mini_map.blit(self.map_img, self.camera_mini.apply_rect(self.map_rect))

#---------------draw sprites------------------------
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob) or isinstance(sprite, Boss1):
                sprite.draw_health()


            self.screen.blit(sprite.image, self.camera_main.apply(sprite))
            self.mini_map.blit(sprite.image, self.camera_mini.apply(sprite))

            if self.draw_debug:
                if isinstance(sprite, Mob) or isinstance(sprite, Player) or isinstance(sprite, Boss1):
                    pg.draw.rect(self.screen, CYAN, self.camera_main.apply_rect(sprite.rect), 1)

                pg.draw.rect(self.screen, CYAN, self.camera_main.apply_rect(sprite.hit_rect), 1)
                # if isinstance(sprite, Venom):
                #     olist = sprite.mask.outline()
                #     pg.draw.rect(self.screen, CYAN, sprite.hit_rect, 1)
                #   # pg.draw.rect(self.screen, CYAN, self.camera.apply_mask(olist), 1)
                #     pg.draw.lines(self.screen,(WHITE),True,olist)
                #    # self.camera.get_xy()
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera_main.apply_rect(wall.rect), 1)
#------------------HUD functions--------------------------#
        # HUD functions
        if self.night:
            self.render_fog()

        self.draw_bar(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        if self.car.drive_mode:
            self.draw_bar(self.screen, 10, 40, self.car.fuel / CAR_FUEL, ORANGE)

        if self.show_item_bar:
            self.draw_item_bar(135, 10)

        if self.show_mini_map:
            self.draw_mini_map(WIDTH-310, 10)

        if self.show_weapon:
            self.draw_weapon_bar(10, 90)
# -----------------other stuff------------------------
        if self.show_collection:                   # in testing
            if self.x == 1:
                self.paused = False
                self.show_collection = False
                self.x = 0
            else:
                self.paused = True
                self.draw_collection()

        if self.show_exp:
            self.draw_exp(135, 80)

        if self.show_message and string != "message":
            if self.counter == len(self.dialog[self.scene]):
                self.counter = 0
                self.show_message = False
                self.paused = False
                self.note_chosen = -1
            else:
                self.paused = True
                self.draw_dialog(130, 550)

        #    self.paused = False

        if self.show_note:
           # if self.counter == len(self.dialog[self.scene]):
                #self.show_note = False
               # self.paused = False
               # self.counter = 0
            #else:
            self.paused = True
            self.draw_note(200, 60)



    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    quit()
# d- debug, n- night, 1- health, 2- fuel, 3- torch, i- item. m- map, c- collection, q,e - weapon toggle, w- weapon, p-pause#
                if event.key == pg.K_d:
                    self.draw_debug = not self.draw_debug

                if event.key == pg.K_n:
                    self.night = not self.night

                if event.key == pg.K_p:
                    self.paused = not self.paused

                if event.key == pg.K_1:
                    if self.player.num_of_items['health'] > 0 and self.player.health < PLAYER_HEALTH:
                        self.player.num_of_items['health'] -= 1
                        self.player.health += 30
                        self.player.health = min(self.player.health, PLAYER_HEALTH)
                        self.effects_sounds['health_up'].play()

                if event.key == pg.K_2:
                    if self.player.num_of_items['fuel'] > 0 and self.car.fuel < CAR_FUEL and self.car.drive_mode:
                        self.player.num_of_items['fuel'] -= 1
                        self.car.fuel += self.car.fuel / 2
                        self.car.fuel = min(self.car.fuel, CAR_FUEL)

                if event.key == pg.K_3:
                    if self.player.num_of_items['torch'] > 0:
                        self.player.num_of_items['torch'] -= 1

                        self.light_mask = pg.image.load(path.join(self.img_folder, LIGHT_MASK1)).convert_alpha()
                        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS2)
                        self.light_rect = self.light_mask.get_rect()

                if event.key == pg.K_i and self.has_item_bar:
                    self.show_item_bar = not self.show_item_bar

                if event.key == pg.K_m and self.has_mini_map:
                    self.show_mini_map = not self.show_mini_map

                if event.key == pg.K_c:
                    self.show_collection = not self.show_collection

                if event.key == pg.K_e:
                    self.player.gun_chosen += 1
                    if self.player.gun_chosen == len(self.player.gun_type):
                        self.player.gun_chosen = 0
                if event.key == pg.K_q:
                    self.player.gun_chosen -= 1
                    if self.player.gun_chosen < 0:
                        self.player.gun_chosen = len(self.player.gun_type) - 1


                if event.key == pg.K_w and self.has_weapon:
                    self.show_weapon = not self.show_weapon


    def show_logo(self):
        self.logo_music.play()
        cross_fade(self.screen, self.logo_img, self.clock)


    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.music_folder, MENU_MUSIC))
        pg.mixer.music.play(loops=-1)

       # self.draw_progress()

        # display on screen messages
        self.screen.blit(self.menu_img, (0, 0))

        self.message_display("Game Project", WIDTH / 2, HEIGHT / 4, 80, col=RED)
        self.message_display("", WIDTH / 2, HEIGHT / 2, 22, col=RED)
        self.message_display("Press space to begin your mission...", WIDTH / 2, HEIGHT * 3 / 4, 16, col=WHITE)

        pg.display.flip()
        wait()
        pg.mixer.music.stop()


    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.music_folder, MENU_MUSIC))
        pg.mixer.music.play(loops=-1)

       # self.draw_progress()

        # display on screen messages
        self.screen.blit(self.menu_img, (0, 0))

        self.message_display("Game OVER", WIDTH / 2, HEIGHT / 4, 80, col=RED)
        self.message_display("", WIDTH / 2, HEIGHT / 2, 22, col=RED)
        self.message_display("Press space to restart your mission...", WIDTH / 2, HEIGHT * 3 / 4, 16, col=WHITE)

        pg.display.flip()
        wait()
        pg.mixer.music.stop()


    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)

        self.light_rect.center = self.camera_main.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)


    def draw_mini_map(self, x, y):
        another = pg.transform.scale(self.mini_map, (300, 300))
        self.outline_rect = pg.Rect(x-1, y-1, 300, 300)
        pg.draw.rect(self.screen, WHITEGREY, self.outline_rect, 10)
        self.screen.blit(another, (x,y))


    def draw_weapon_bar(self, x, y):
        BAR_LENGTH = 100
        BAR_HEIGHT = 100
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        pg.draw.rect(self.screen, LIGHTGREY, outline_rect, 10)
        pg.draw.rect(self.screen, WHITEGREY, fill_rect)
        if len(self.player.gun_type) > 0:
            new_image = pg.transform.scale(self.item_images[self.player.gun_type[self.player.gun_chosen]], (110, 60))
            self.screen.blit(new_image, (5, 110))


    def draw_bar(self, surf, x, y, pct, set_col = None):
        if pct < 0:
            pct = 0

        BAR_LENGTH = 100
        BAR_HEIGHT = 20

        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        if set_col:
            col = set_col

        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, BLACK, outline_rect, 2)


    def draw_progress(self):
        done = False
        current = 0

        while not done:
            self.screen.fill(WHITE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        quit()

            self.clock.tick(FPS)
            pct = current + (1-sin(current * pi * 2 + pi / 2)) / -8         # needs to be frame independent
            if current >= 0 and current <= 0.15:
                self.screen.blit(self.trailer_images[1], (0, 0))
            if current >= 0.25 and current <= 0.4:
                self.screen.blit(self.trailer_images[0], (0, 0))
            if current >= 0.5 and current <= 0.65:
                self.screen.blit(self.trailer_images[2], (0, 0))
            if current >= 0.75 and current <= 0.9:
                self.screen.blit(self.trailer_images[3], (0, 0))

            self.draw_progress_bar(self.screen, 150, 700, pct)
            current += 0.0065
            if pct >= 1:
                done = True
            pg.display.flip()


    def draw_progress_bar(self, surf, x, y, pct):
        BAR_LENGTH = WIDTH - 300
        BAR_HEIGHT = 30

        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

        col = ORANGE

        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, BLACK, outline_rect, 2)

    def draw_exp(self, x, y):
        BAR_LENGTH = 550
        BAR_HEIGHT = 10

        # vertical lines
        num_of_columns = 20
        cell_width = BAR_LENGTH / num_of_columns

        fill = (self.player.exp / exp_required(self.player.level)) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)


        pg.draw.rect(self.screen, CYAN, fill_rect)
        pg.draw.rect(self.screen, LIGHTGREY, outline_rect, 5)

        for i in range(num_of_columns-1):
            pg.draw.line(self.screen, WHITEGREY, (x + (i + 1) * cell_width, y+3),
                         (x + (i + 1) * cell_width, y + BAR_HEIGHT-3), 2)

        self.message_display(str(self.player.level),x + BAR_LENGTH/2, y -5, 14, WHITE)



    def draw_item_bar(self, x, y):
        BAR_LENGTH = 550
        BAR_HEIGHT = 50

        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y + 36, BAR_LENGTH, 13)

        pg.draw.rect(self.screen, WHITEGREY, fill_rect)
        pg.draw.rect(self.screen, LIGHTGREY, outline_rect, 2)


        # vertical lines
        num_of_columns = 8
        cell_width = BAR_LENGTH / num_of_columns

        for i in range(num_of_columns-1):
            pg.draw.line(self.screen, LIGHTGREY, (x + (i + 1) * cell_width, y),
                         (x + (i + 1) * cell_width, y + BAR_HEIGHT), 1)

        # horizontal line
        pct = 0.68
        pg.draw.line(self.screen, DARKGREY, (x, y + pct * BAR_HEIGHT), (x + BAR_LENGTH, y + pct * BAR_HEIGHT), 2)

        for i in range(len(self.player.item_order)):
            c = self.player.item_order[i]
            self.screen.blit(self.item_bar_images[c],
                             (x + cell_width/2 - self.item_bar_images[c].get_size()[0]/2 + i * cell_width,
                            ITEM_BAR_Y[c]))
        for i in range(len(self.player.item_order)):
            self.message_display(str(self.player.num_of_items[self.player.item_order[i]]), (x + cell_width/2 + i * cell_width), 53, 12)


    def draw_dialog(self, x, y):
        done = False
        while not done:
            if self.counter == len(self.dialog[self.scene]):
                done = True
            else:
                if self.note_chosen > 0:
                    self.draw_chosen_note(200, 60, self.note_chosen)
                else:
                    self.draw('message')
                self.screen.blit(self.text_box_img, (0, HEIGHT - 300))
                self.message_display_animation(self.dialog[self.scene][self.counter], x, y, self.col)
                wait()
                self.counter += 1
        if self.note_chosen > 0:
            self.note_chosen = -1
        if self.col != WHITE:
            self.col = WHITE


    def draw_note(self, x, y):
        done = False
        while not done:
            if self.counter == len(self.dialog[self.scene]):
                done = True
            else:
                self.screen.fill(NIGHT_COLOR)

                # randomize note obtained
                li = []
                for i in self.note_images:
                    li.append(i)
                for i in self.player.note_received:
                    li.remove(i)

                chosen = choice(li)
                self.player.note_received.append(chosen)
                if chosen == 2:
                      # load game bgm
                    pg.mixer.music.stop()
                    pg.mixer.music.load(path.join(self.music_folder, GLITCH_MUSIC))
                    pg.mixer.music.play(loops=-1)

                self.screen.blit(self.note_images[chosen], (WIDTH/2 - self.note_images[chosen].get_size()[0]/2, 0))

                self.message_display_animation(self.dialog[self.scene][self.counter], x, y)
                self.counter += 1
                wait()

        if chosen == 2:
            pg.mixer.music.stop()
            pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC))
            pg.mixer.music.play(loops=-1)

        self.show_note = False
        self.counter = 0
        self.show_message = True
        self.scene = chosen
        self.note_chosen = chosen
        self.col = GREEN


    def message_display(self, text, x, y, size, col=BLACK):
        largeText = pg.font.Font('freesansbold.ttf', size)
        TextSurf = largeText.render(text, True, col)
        TextRect = TextSurf.get_rect()

        TextRect.center = (x, y)
        self.screen.blit(TextSurf, TextRect)


    def message_display_animation(self, string, x, y, col = WHITE):
        self.effects_sounds['typing'].play()
        basicfont = pg.font.Font('freesansbold.ttf', 30)

        text = ''
        letter = 0
        for i in range(len(string)):
            pg.event.clear()

            # randomize speed typing
            rand_t = uniform(0.01, 0)
            time.sleep(rand_t)
            text += string[letter]
            text_surface = basicfont.render(text, True, col)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)
            self.screen.blit(text_surface, text_rect)
            pg.display.update()
            letter += 1

        self.effects_sounds['typing'].stop()


    def draw_collection(self): # in testing
        self.screen.blit(self.collection_img, (100, 100))
        self.message_display(str(self.player.note_received), 150, 120, 20)
        pg.display.flip()
        done = False
        note_chosen = -1
        while not done:
            self.paused = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_c:
                        done = True
                    if event.key ==  pg.K_1:
                        note_chosen = 1
                    if event.key == pg.K_2:
                        note_chosen = 2
                    if event.key == pg.K_3:
                        note_chosen = 3
                    if event.key == pg.K_4:
                        note_chosen = 4
                    if note_chosen in self.player.note_received:
                        self.scene = 'note'
                        self.draw_chosen_note(200, 60, note_chosen)
                        wait()

                        done = True
        self.x = 1


    def draw_chosen_note(self, x, y, note_chosen): # in testing
        self.screen.fill(NIGHT_COLOR)
        self.screen.blit(self.note_images[note_chosen],
                         (WIDTH/2 - self.note_images[note_chosen].get_size()[0]/2, 0))
        pg.display.update()


# create the game object
g = Game()
g.show_logo()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
