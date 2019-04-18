import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import time


# HUD functions
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()
    

class Game:
    # lore: soldiers #death count, your mission is to clear out the dangerous zone
    # fix bullet rotation
    # add weapon 
    # currently working on getting a item slot presented on screen
    # reminder: disable knockback on car by bullets
    # add invisible boss2, spawn after boss1 is killed
    # score = survival time + item found + puzzle solved(treasure found) + total kill
    # add boss1 : venom
    def draw_bar(self, surf, x, y, pct, obj):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        if obj == self.player: 
            if pct > 0.6:
                col = GREEN
            elif pct > 0.3:
                col = YELLOW
            else:
                col = RED
        else:
            col = YELLOW
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)


    def draw_item_bar(self, surf, x, y, obj):
        BAR_LENGTH = 50
        BAR_HEIGHT = 400
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        pg.draw.rect(surf, BLACK, outline_rect, 2)
        self.message_display(str(self.player.num_of_items['health']), 35, 220)
        self.message_display(str(self.player.num_of_items['gas']),35, 240)



    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.mini_map = pg.Surface((WIDTH + 1000, HEIGHT + 1000))
        
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        
    def message_display(self, text, x, y):
        largeText = pg.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = x, y
        self.screen.blit(TextSurf, TextRect)
        self.mini_map.blit(TextSurf, TextRect)

    
    
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, '32map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.car_img = pg.image.load(path.join(img_folder, CAR_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        

        self.venom_img_old = pg.image.load(path.join(img_folder, VENOM_IMG)).convert_alpha()
        w, h = self.venom_img_old.get_size()
        self.venom_img = pg.Surface((w * 2, h * 2), pg.SRCALPHA)
        self.venom_img.blit(self.venom_img_old, (w-80, h/2-10))


        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        
       # self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        #self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK3)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
                                        
                                    
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.venoms = pg.sprite.Group()
        self.cars = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
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
            if tile_object.name == 'venom':
                Venom(self, obj_center.x, obj_center.y)
            if tile_object.name == 'car':
                self.car = Car(self, obj_center.x, obj_center.y, -90)
            if tile_object.name in ['health', 'gas', 'map']:
                Item(self, obj_center, tile_object.name)
          
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.night = False
        self.show_item_bar = True
        self.show_mini_map = False
        self.has_mini_map = False
       # self.pause_button = Button(GREEN, 10, 10, 20, 20, 'Pause')
        
      
    

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'gas':
                hit.kill()
                self.player.num_of_items['gas'] += 1
            if hit.type == 'health':
                hit.kill()
                self.player.num_of_items['health'] += 1
            if hit.type == 'map':
                hit.kill()
                self.has_mini_map = True
                

        
            
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
         # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.venoms, False, collide_hit_rect2)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

            
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            
      
            


    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)
        self.mini_map.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)
        
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.mini_map.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            self.mini_map.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
                pg.draw.rect(self.mini_map, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
                pg.draw.rect(self.mini_map, CYAN, self.camera.apply_rect(wall.rect), 1)


        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)

        if self.night:
            self.render_fog()
        # HUD functions
       # self.pause_button.draw(self.screen, BLACK)
        self.draw_bar(self.screen, 40, 10, self.player.health / PLAYER_HEALTH, self.player)
        self.draw_bar(self.mini_map, 40, 10, self.player.health / PLAYER_HEALTH, self.player)

        if self.player.in_car: 
            self.draw_bar(self.screen, 40, 40, self.player.fuel / PLAYER_FUEL, self.cars)
            self.draw_bar(self.mini_map, 40, 40, self.player.fuel / PLAYER_FUEL, self.cars)

        if self.show_item_bar: 
            self.draw_item_bar(self.screen, 10, 100, self.player)
            self.draw_item_bar(self.mini_map, 10, 100, self.player)

        if self.show_mini_map:         
            self.another = pg.transform.scale(self.mini_map, (300, 300))
            self.outline_rect = pg.Rect(49, 49, 80, 110)
            pg.draw.rect(self.screen, WHITE, self.outline_rect, 2)
            self.screen.blit(self.another,(50, 50))
      
    
        #self.screen.fill(BLACK)
        pg.display.flip()
        

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_i:
                    self.show_item_bar = not self.show_item_bar
                if event.key == pg.K_1:
                    if self.player.num_of_items['health'] > 0 and self.player.health < PLAYER_HEALTH:
                        self.player.num_of_items['health'] -= 1
                        self.player.health += 30
                        self.player.health = min(self.player.health, PLAYER_HEALTH)
                if event.key == pg.K_2:
                    if self.player.num_of_items['gas'] > 0 and self.player.fuel < PLAYER_FUEL:
                        self.player.num_of_items['gas'] -= 1
                        self.player.fuel += self.player.fuel / 2 
                        self.player.fuel = min(self.player.fuel, PLAYER_FUEL)
                if event.key == pg.K_m and self.has_mini_map:
                    self.show_mini_map = not self.show_mini_map
                
                    
                
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
