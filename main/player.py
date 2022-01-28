import math
from settings import playerconst, playerPos, playerFov
from side.UI_elements import Text
import pygame as pg
from settings import languagestorage as lg

class Player(pg.sprite.Sprite):
    def __init__(self, room_x, room_y, walls, end, sp1, sp2, type, barricade_group, *group):
        super().__init__(*group)
        self.idle_img = [pg.image.load('sprites/Idle1.png'), pg.image.load('sprites/Idle2.png'),
                         pg.image.load('sprites/Idle3.png'), pg.image.load('sprites/Idle4.png')]
        self.run_img = [pg.image.load('sprites/run1.png'), pg.image.load('sprites/run2.png'),
                        pg.image.load('sprites/run3.png'), pg.image.load('sprites/run4.png'), 
                        pg.image.load('sprites/run5.png'), pg.image.load('sprites/run6.png'),
                        pg.image.load('sprites/run7.png'), pg.image.load('sprites/run8.png'), 
                        pg.image.load('sprites/run9.png'), pg.image.load('sprites/run10.png')]
        self.death_img = [pg.image.load('sprites/death1.png'), pg.image.load('sprites/death2.png'),
                          pg.image.load('sprites/death3.png'), pg.image.load('sprites/death4.png'), 
                          pg.image.load('sprites/death5.png'), pg.image.load('sprites/death6.png'),
                          pg.image.load('sprites/death7.png'), pg.image.load('sprites/death8.png'), 
                          pg.image.load('sprites/death9.png'), pg.image.load('sprites/death10.png'),
                          pg.image.load('sprites/death11.png'), pg.image.load('sprites/death12.png')]
        self.w_img = pg.image.load('sprites/bow.png')
        self.is_dead = False
        self.walls = walls
        self.barricade_group = barricade_group
        self.x, self.y = playerPos
        self.angel = playerFov
        self.is_boss_room = False
        self.floor = (135, 0, 1840, 990)
        self.floor_boss = (170, 280, 1830, 910)
        self.room_x, self.room_y = room_x, room_y
        self.idle_anim_count = 32
        self.run_anim_count = 40
        self.death_anim_count = 0
        self.end_room = end
        self.sp1_room = sp1
        self.sp1_room_use = True
        self.sp2_room = sp2
        self.sp_gift = False
        self.sp2_room_use = True
        self.sp_room = (self.sp1_room, self.sp2_room)
        self.rooms = (self.end_room, self.sp1_room, self.sp2_room)
        self.moving_right = False
        self.moving_left = False
        self.moving_hor = False
        self.check = 0
        self.room_change = False
        self.lvl_change = False
        self.lvl_boss = False
        self.text = Text((30, 1054), butHeigth=14,
                            butWidth=100, text="")
        self.full_dead = False

    def weapon(self):
        mouse_x, mouse_y = pg.mouse.get_pos()

        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        weapon_copy = pg.transform.rotate(self.w_img, angle)
        return weapon_copy
    
    def image_choise(self):
        if self.moving_right:
            self.image = pg.transform.scale(self.run_img[self.run_anim_count//4],
                                                (125, 115))
            self.check = 0
            self.moving_right = False
        elif self.moving_left:
            self.image = pg.transform.scale(pg.transform.flip(self.run_img[self.run_anim_count//4],
                                  True, False), (125, 115))
            self.check = 1
            self.moving_left = False
        elif self.moving_hor:
            if not self.check:
                self.image = pg.transform.scale(self.run_img[self.run_anim_count//4],
                                                    (125, 115))
                self.moving_hor = False
            else:
                self.image = pg.transform.scale(pg.transform.flip(self.run_img[self.run_anim_count//4],
                                      True, False), (125, 115))
                self.moving_hor = False
        else:
            if self.check:
                self.image = pg.transform.scale(pg.transform.flip(self.idle_img[self.idle_anim_count//8],
                                      True, False), (125, 115))
            else:
                self.image = pg.transform.scale(self.idle_img[self.idle_anim_count//8],
                                                    (125, 115))
        self.rect = (self.x-100, self.y-50)
    
    def blit(self, screen):
        screen.blit(self.image, self.rect)
    
    def death(self):
        self.image = pg.transform.scale(self.death_img[self.death_anim_count//4],
                                                (125, 115))
        if self.death_anim_count + 1 < 48:
            self.death_anim_count += 1
        print(self.death_anim_count)
        if self.death_anim_count == 47:
            self.full_dead = True

    @property
    def end_screen(self):
        return self.full_dead
    @property
    def now_barricade(self):
        return self.barricade_group

    @now_barricade.setter
    def now_barricade(self, other):
        self.barricade_group = other         

    @property
    def pos(self):
        return(self.x, self.y)

    @property
    def type(self):
        return self.is_boss_room

    @type.setter
    def type(self, value):
        self.is_boss_room = value

    @property
    def room(self):
        return(str(self.room_x), str(self.room_y))

    @room.setter
    def room(self, value):
        self.room_x, self.room_y = value
        self.room_x, self.room_y = int(self.room_x), int(self.room_y)

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

    @property
    def change_room(self):
        return self.room_change
    
    @property
    def sp_get(self):
        return self.sp_gift

    @property
    def lvl_to_boss(self):
        return self.lvl_boss
    
    @lvl_to_boss.setter
    def lvl_to_boss(self, other):
        self.lvl_boss = other

    @property
    def change_lvl(self):
        return self.lvl_change
    
    @change_lvl.setter
    def change_lvl(self, other):
        self.lvl_change = other

    @property
    def text_use(self):
        return self.text

    def movement(self):
        self.sp_gift = False
        # now outs
        wall = self.walls[int(str(self.room_x) + str(self.room_y))]
        # now player pos
        pos = (self.x, self.y)
        # dict of outs positions
        outs = {"x1": (-4, 150), "y1": (470, 590),
                "x2": (980, 1110), "y2": (-4, 20),
                "x3": (1800, 1920), "y3": (470, 590),
                "x4": (980, 1110), "y4": (960, 1080)}
        # dict of after out positions
        outs2 = {"x1": 1810, "y1": self.y,
                 "x2": self.x, "y2": 970,
                 "x3": 160, "y3": self.y,
                 "x4": self.x, "y4": 30}
        # movement
        self.vel_x = 0
        self.vel_y = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel_y += -playerconst["speed"]
            self.moving_hor = True
        if keys[pg.K_s]:
            self.vel_y += playerconst["speed"]
            self.moving_hor = True
        if keys[pg.K_a]:
            self.vel_x += -playerconst["speed"]
            self.moving_left = True
        if keys[pg.K_d]:
            self.vel_x += playerconst["speed"]
            self.moving_right = True
        if self.idle_anim_count + 1 >= 32:
            self.idle_anim_count = 0
        self.idle_anim_count += 1
        if self.run_anim_count + 1 >= 40:
            self.run_anim_count = 0
        self.run_anim_count += 1
        self.x += self.vel_x
        self.y += self.vel_y
        # cheack does player now on floor
        if self.is_boss_room is False:
            try:
                # if true player pos change to prev position 'cause he not in room floor rect
                self.x, self.y = {not(self.x > self.floor[0] and self.x < self.floor[2]
                                  and self.y > self.floor[1] and self.y < self.floor[3]): pos}[True]
            except KeyError:
                pass
            # cheack does player go to out
            try:
                self.room_change = False
                self.x, self.y, self.room_x, self.room_y, self.room_change \
                = {self.x > outs["x1"][0] and self.x < outs["x1"][1]
                   and self.y > outs["y1"][0] and self.y < outs["y1"][1] and wall[0] == "1":
                   (outs2["x1"], outs2["y1"],
                    self.room_x - 1, self.room_y, True),
                   self.x > outs["x2"][0] and self.x < outs["x2"][1]
                   and self.y > outs["y2"][0] and self.y < outs["y2"][1] and wall[1] == "1":
                   (outs2["x2"], outs2["y2"],
                    self.room_x, self.room_y - 1, True),
                   self.x > outs["x3"][0] and self.x < outs["x3"][1]
                   and self.y > outs["y3"][0] and self.y < outs["y3"][1] and wall[2] == "1":
                   (outs2["x3"], outs2["y3"],
                    self.room_x + 1, self.room_y, True),
                   self.x > outs["x4"][0] and self.x < outs["x4"][1]
                   and self.y > outs["y4"][0] and self.y < outs["y4"][1] and wall[3] == "1":
                   (outs2["x4"], outs2["y4"], self.room_x, self.room_y + 1, True)}[True]
            except KeyError:
                pass
            text = ""
            if [str(self.room_x), str(self.room_y)] in self.rooms:
                r = 100
                hypotenuse = math.sqrt((self.x - 980) ** 2 + (self.y - 540) ** 2)
                if hypotenuse <= r:
                    self.text = Text((950, 580), butHeigth=14,
                            butWidth=100, text=lg["use"], color=(210, 105, 30), background=(120, 120, 120))
                    if [str(self.room_x), str(self.room_y)] == self.end_room and keys[pg.K_e]:
                        self.lvl_boss = True
                    elif [str(self.room_x), str(self.room_y)] == self.sp1_room and keys[pg.K_e]:
                        if self.sp1_room_use:
                            text = "U got ..."
                            self.sp1_room_use = False
                            self.text = Text((950, 580), butHeigth=14,
                            butWidth=100, text=text, color=(210, 105, 30), background=(120, 120, 120))
                            self.sp_gift = True
                        else:
                            text = lg["can't"]
                            self.text = Text((950, 580), butHeigth=14,
                            butWidth=100, text=text, color=(210, 105, 30), background=(120, 120, 120))
                    elif [str(self.room_x), str(self.room_y)] == self.sp2_room and keys[pg.K_e]:
                        if self.sp2_room_use:
                            text = "U got ..."
                            self.sp2_room_use = False
                            self.text = Text((950, 580), butHeigth=14,
                            butWidth=100, text=text, color=(210, 105, 30), background=(120, 120, 120))
                            self.sp_gift = True
                        else:
                            text = lg["can't"]
                            self.text = Text((950, 580), butHeigth=14,
                            butWidth=100, text=text, color=(210, 105, 30), background=(120, 120, 120))
                else:
                    self.text = Text((1000, 580), butHeigth=14,
                            butWidth=100, text=text)
            else:
                self.text = Text((540, 900), butHeigth=14,
                            butWidth=100, text=text)
        else:
            self.text = Text((950, 580), butHeigth=14,
                            butWidth=100, text=lg["use"], color=(210, 105, 30), background=(120, 120, 120))
            if keys[pg.K_e]:
                self.lvl_change = True
            try:
                # if true player pos change to prev position 'cause he not in room floor rect
                self.x, self.y = {not(self.x > self.floor_boss[0] and self.x < self.floor_boss[2]
                                  and self.y > self.floor_boss[1] and self.y < self.floor_boss[3]): pos}[True]
            except KeyError:
                pass
        self.image_choise()
        if pg.sprite.collide_mask(self, self.barricade_group):
            self.x, self.y = pos
            self.image_choise()

        


class PlayerArrow(pg.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, *group):
        super().__init__(*group)
        self.arrow_img = pg.image.load("sprites/arrow.png")
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 35
        self.len = 0
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.rendering = 100
        self.angle = (180 / math.pi) * -self.angle
        self.image = pg.transform.rotate(self.arrow_img, self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.len += 1
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.len > 20:
            self.kill()


    # def arrow(self, mouse_x, mouse_y):
    #     rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
    #     self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    #     if self.angle != 0:
    #         arrow_copy = pg.transform.rotate(self.arrow_img, self.angle)
    #         return arrow_copy
    #     else:
    #         return pg.image.load('sprites/return.png')

class Stats:
    def __init__(self):
        self.hp = 100
        self.ammo = 50
        self.hp_img = pg.image.load('sprites/bar/health.png')
        self.ammo_img = pg.image.load('sprites/bar/ammo.png')
        self.font = pg.font.Font('sprites/ARCADECLASSIC.TTF', 75)
    
    @property
    def change_hp(self):
        return self.hp
    
    @change_hp.setter
    def change_hp(self, other):
        self.hp += other

    @property
    def change_arrows(self):
        return self.ammo
    
    @change_hp.setter
    def change_arrows(self, other):
        self.ammo += other

    def blit(self, screen):
        s = pg.Surface((400, 300), pg.SRCALPHA)
        s.fill((0, 0, 0, 100))
        screen.blit(s, (0, 0))

        stats = self.font.render('STATS', True, (255, 255, 255))
        screen.blit(stats, (100, 6))

        hp = self.font.render(str(self.hp), True, (255, 255, 255))
        screen.blit(self.hp_img, (25, 75))
        screen.blit(hp, (125, 70))

        ammo = self.font.render(str(self.ammo), True, (255, 255, 255))
        screen.blit(self.ammo_img, (25, 190))
        screen.blit(ammo, (125, 190))