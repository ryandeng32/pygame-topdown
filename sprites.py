import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from usedFunc import *
import pytweening as tween
from os import path

vec = pg.math.Vector2


class Boss1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.boss1s
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.ani_speed_init = 2
        self.ani_speed = 2

        self.default()

        self.image = self.ani[self.ani_pos].copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()

        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

        self.attack = False
        self.death = False

    def default(self):
        self.ani_pos = 0
        self.ani = self.game.boss1_idle
        self.ani_max = len(self.ani) - 1
        if self.ani_pos > self.ani_max:
            self.ani_pos = 0

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 50:
                    self.acc += dist.normalize()

    def set_attack(self):
        self.attack = True
        self.ani = self.game.boss1_attack2
        self.ani_max = len(self.ani) - 1
        self.ani_pos = 0

    def set_move(self):
        self.ani = self.game.boss1_move
        self.ani_max = len(self.ani) - 1
        if self.ani_pos > self.ani_max:
            self.ani_pos = 0

    def set_death(self):
        self.death = True
        self.ani_pos = 0
        self.ani = self.game.boss1_death
        self.ani_max = len(self.ani) - 1

    def update(self):
        if self.death or self.attack:
            self.ani_speed -= 1
            if self.ani_speed == 0:
                self.ani_speed = self.ani_speed_init
                if self.ani_pos == self.ani_max:
                    if self.death:
                        self.kill()
                    if self.attack:
                        self.attack = False
                else:
                    self.ani_pos += 1

            self.image = pg.transform.rotate(self.ani[self.ani_pos], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

        else:
            target_dist = self.target.pos - self.pos
            # avoid using sqrt because it is slow for computer
            if target_dist.length_squared() < DETECT_RADIUS ** 2:
                if random() < 0.004:
                    choice(self.game.zombie_moan_sounds).play()

                self.ani_speed -= 1
                if self.ani_speed == 0:
                    self.ani_speed = self.ani_speed_init
                    if self.ani_pos == self.ani_max:
                        self.ani_pos = 0
                        if self.attack:
                            self.attack = False
                    else:
                        self.ani_pos += 1

                self.rot = target_dist.angle_to(vec(1, 0))

                if target_dist.length_squared() < ATTACK_RADIUS ** 2 and self.attack == False:
                    self.set_attack()

                else:
                    self.ani_max = len(self.game.boss1_move) - 1
                    if self.ani_pos > self.ani_max:
                        self.ani_pos = 0

                    self.image = pg.transform.rotate(self.game.boss1_move[self.ani_pos], self.rot)

#------------------things you have to set for collisions and stuff----#
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                self.acc.scale_to_length(self.speed)
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls, 'y')
                self.rect.center = self.hit_rect.center
            else:
                self.ani_speed -= 1
                if self.ani_speed == 0:
                    self.ani_speed = self.ani_speed_init
                    if self.ani_pos == self.ani_max:
                        self.ani_pos = 0
                    else:
                        self.ani_pos += 1

                self.ani_max = len(self.game.zombie_idle) - 1
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 0
                self.image = pg.transform.rotate(self.game.boss1_idle[self.ani_pos], self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos

#------------------health reaches 0 --------------#
            if self.health <= 0:
                choice(self.game.zombie_hit_sounds).play()
                self.set_death()

                self.game.player.exp += EXP_FROM_ACTION['zombie']
                if self.game.player.exp >= exp_required(self.game.player.level):
                    self.game.player.exp -= exp_required(self.game.player.level)
                    self.game.player.level += 1

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(200, 200, 50, 7)

        if self.health < MOB_HEALTH:

            pg.draw.rect(self.image, col, self.health_bar)


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.ani_speed_init = 2
        self.ani_speed = 2

        self.default()

        self.image = self.ani[self.ani_pos].copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()

        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

        self.attack = False
        self.death = False

    def default(self):
        self.ani_pos = 0
        self.ani = self.game.zombie_idle
        self.ani_max = len(self.ani) - 1
        if self.ani_pos > self.ani_max:
            self.ani_pos = 0

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 50:
                    self.acc += dist.normalize()

    def set_attack(self):
        self.attack = True
        self.ani = self.game.zombie_attack
        self.ani_max = len(self.ani) - 1
        self.ani_pos = 0

    def set_move(self):
        self.ani = self.game.zombie_move
        self.ani_max = len(self.ani) - 1
        if self.ani_pos > self.ani_max:
            self.ani_pos = 0

    def set_death(self):
        self.death = True
        self.ani_pos = 0
        self.ani = self.game.zombie_death
        self.ani_max = len(self.ani) - 1

    def update(self):
        if self.death or self.attack:
            self.ani_speed -= 1
            if self.ani_speed == 0:
                self.ani_speed = self.ani_speed_init
                if self.ani_pos == self.ani_max:
                    if self.death:
                        self.kill()
                    if self.attack:
                        self.attack = False
                else:
                    self.ani_pos += 1

            self.image = pg.transform.rotate(self.ani[self.ani_pos], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

        else:
            target_dist = self.target.pos - self.pos
            # avoid using sqrt because it is slow for computer
            if target_dist.length_squared() < DETECT_RADIUS ** 2:
                if random() < 0.004:
                    choice(self.game.zombie_moan_sounds).play()

                self.ani_speed -= 1
                if self.ani_speed == 0:
                    self.ani_speed = self.ani_speed_init
                    if self.ani_pos == self.ani_max:
                        self.ani_pos = 0
                        if self.attack:
                            self.attack = False
                    else:
                        self.ani_pos += 1

                self.rot = target_dist.angle_to(vec(1, 0))

                if target_dist.length_squared() < ATTACK_RADIUS ** 2 and self.attack == False:
                    self.set_attack()

                else:
                    self.ani_max = len(self.game.zombie_move) - 1
                    if self.ani_pos > self.ani_max:
                        self.ani_pos = 0

                    self.image = pg.transform.rotate(self.game.zombie_move[self.ani_pos], self.rot)

#------------------things you have to set for collisions and stuff----#
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                self.acc.scale_to_length(self.speed)
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls, 'y')
                self.rect.center = self.hit_rect.center
            else:
                self.ani_speed -= 1
                if self.ani_speed == 0:
                    self.ani_speed = self.ani_speed_init
                    if self.ani_pos == self.ani_max:
                        self.ani_pos = 0
                    else:
                        self.ani_pos += 1

                self.ani_max = len(self.game.zombie_idle) - 1
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 0
                self.image = pg.transform.rotate(self.game.zombie_idle[self.ani_pos], self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos

#------------------health reaches 0 --------------#
            if self.health <= 0:
                choice(self.game.zombie_hit_sounds).play()
                self.set_death()

                self.game.player.exp += EXP_FROM_ACTION['zombie']
                if self.game.player.exp >= exp_required(self.game.player.level):
                    self.game.player.exp -= exp_required(self.game.player.level)
                    self.game.player.level += 1

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(200, 200, 50, 7)

        if self.health < MOB_HEALTH:

            pg.draw.rect(self.image, col, self.health_bar)


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
#####################################################################################################################################################


class Car(pg.sprite.Sprite):
    def __init__(self, game, x, y, rot):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.cars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.car_img
        self.rot = rot
        self.vel = vec(0, 0)
       # self.acc = vec(0, 0)
        self.pos = vec(x, y)
        self.image = pg.transform.rotate(self.game.car_img, self.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = vec(x, y)
        self.hit_rect.center = self.rect.center
        self.fuel = CAR_FUEL
        self.drive_mode = False

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = CAR_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -CAR_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(CAR_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-CAR_SPEED / 2, 0).rotate(-self.rot)
        # shooting disbled
        if keys[pg.K_g]:
            if self.drive_mode:
                self.drive_mode = False

    def update(self):
        if self.drive_mode:
            self.get_keys()
            if self.vel.length() > 0:
                self.fuel -= 1
            if self.fuel <= 0:
                self.vel = vec(0, 0)
            if self.vel.length() > 0:
                self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.car_img, self.rot)

            self.rect = self.image.get_rect()
            self.rect.center = self.pos
##
# self.acc = vec(1, 0).rotate(-self.rot)
# self.acc.scale_to_length(CAR_SPEED)
# self.acc += self.vel * -1
# self.vel += self.acc * self.game.dt
# self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
##

            self.pos += self.vel * self.game.dt

            self.pos += self.vel * self.game.dt
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center


#############################################################################################################################################################


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.ani_speed_init = 4
        self.ani_speed = self.ani_speed_init
        self.ani = game.player_move

        self.ani_pos = 0
        self.ani_max = len(self.ani) - 1
        self.image = self.ani[0]

        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.center = (x, y)
        self.hit_rect.center = self.rect.center
        self.rot = 180
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.PLAYER_SPEED = PLAYER_SPEED
        self.num_of_items = {'health': 0, 'fuel': 0, 'torch': 0}
        self.car = game.car
        self.gun_type = []
        self.gun_chosen = 0
        self.gun_received = 0
        self.bat = False

        self.item_order = []
        self.item_received = {'health': 0, 'fuel': 0, 'torch': 0}
        self.note_received = []
        self.exp = 0
        self.level = 0

    def player_death(self):
        pass

    def swing_bat(self):
        self.bat = True
        self.ani = self.game.player_attack
        self.ani_speed = 2
        self.ani_max = len(self.ani) - 1
        self.ani_pos = 0
        self.game.player_adjust = (80, 110)

    def default(self):
        self.ani = self.game.player_move
        self.ani_speed = self.ani_speed_init

        self.ani_max = len(self.ani) - 1
        self.ani_pos = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP]:
            self.vel = vec(self.PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN]:
            self.vel = vec(-self.PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE] and len(self.gun_type) > 0:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE[self.gun_type[self.gun_chosen]]:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir, self.rot)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)

                self.game.weapon_sounds[self.gun_type[self.gun_chosen]].play()
                MuzzleFlash(self.game, pos)
        if keys[pg.K_b]:
            if self.bat == False:
                self.swing_bat()
        if keys[pg.K_f]:
            hits = pg.sprite.spritecollide(self, self.game.cars, False, collide_hit_rect)
            if hits:
                self.car.drive_mode = True

    def update(self):

        if not self.car.drive_mode:
            self.get_keys()
            if self.vel.length() != 0 or self.bat:
                self.ani_speed -= 1
                if self.ani_speed == 0:
                    if self.bat:
                        self.ani_speed = 2
                    else:
                        self.ani_speed = self.ani_speed_init
                    if self.ani_pos == self.ani_max:
                        self.ani_pos = 0
                        if self.bat:
                            self.bat = False
                            self.default()
                    else:
                        self.ani_pos += 1

            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.ani[self.ani_pos], self.rot)

            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.pos += self.vel * self.game.dt
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        else:
            self.rect.center = self.car.hit_rect.center
            self.hit_rect.center = self.rect.center
            self.pos = self.rect.center
            self.rot = self.car.rot
            self.image = pg.transform.rotate(self.game.player_img, self.rot)


class Guide(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pass


class Venom(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.venoms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.venom_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.offset = 80
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS) + 200
        self.hit_rect.center = self.rect.center
        self.mask = pg.mask.from_surface(self.image)
       # self.mask.set_at(self.hit_rect.topleft)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 50:
                    self.acc += dist.normalize()

    def update(self):
        # self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        # self.image = pg.transform.rotate(self.game.venom_img, self.rot)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rot = rot
        self.game = game
        self.image = pg.transform.rotate(game.bullet_img, self.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.__layer = 1
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.hit_rect = self.rect
        self.type = type
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5) * BOB_RANGE
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()
