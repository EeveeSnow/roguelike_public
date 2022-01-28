import pygame
import json

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name: str, cords: list, *group, type: str = None):
        super().__init__(*group)
        self.group_now = group
        self.idle_img = list()
        self.run_img = list()
        self.attack_img = list()
        self.death_img = list()
        self.len_idle = 0
        self.len_run = 0
        self.len_attack = 0
        self.len_death = 0
        self.floor = (135, 0, 1840, 990)
        self.tp2 = type
        with open(f'local/modify/enemies/{name}.json') as enemy_file:
            data = json.load(enemy_file)
            self.name = data['name']
            self.hp = data['hp']
            self.tp = data["type"]
            self.speed = data["speed"]
            self.dmg = data["dmg"]
            self.range = data["dmg_range"]
            self.score = data["score"]
            for img1 in data["idle"]:
                self.idle_img.append(pygame.image.load(img1))
                self.len_idle += 1
            for img2 in data["run"]:
                self.run_img.append(pygame.image.load(img2))
                self.len_run += 1
            for img3 in data["attack"]:
                self.attack_img.append(pygame.image.load(img3))
                self.len_attack += 1
            for img4 in data["death"]:
                self.death_img.append(pygame.image.load(img4))
                self.len_death += 1
        self.x = cords[0]
        self.y = cords[1]
        self.idle_anim_count = 0
        self.run_anim_count = 0
        self.attack_anim_count = 0
        self.death_anim_count = 0
        self.image = pygame.transform.scale(self.idle_img[self.idle_anim_count//8], (125, 115))
        self.rect = self.image.get_rect()
        self.rect.x = self.x-100
        self.rect.y = self.y-50
        self.is_dead = False

    def update(self, player_x, player_y, arrows):
        self.dmg_now = 0
        pos = (self.x, self.y)
        if pygame.sprite.spritecollideany(self, arrows) and self.tp2 is None:
            self.is_dead = True
        if not self.is_dead:
            if self.tp2 is None:
                if self.tp == "melee":
                    self.move_melee(player_x, player_y)
                try:
                    self.x, self.y = {not(self.x > self.floor[0] and self.x < self.floor[2]
                                  and self.y > self.floor[1] and self.y < self.floor[3]): pos}[True]
                except KeyError:
                    pass
            else:
                self.idle()
        else:
            self.death()
        return self.dmg_now
    
    def move_melee(self, player_x, player_y):
        distance_x_abs, distance_x, distance_y_abs, distance_y =\
            self.a_search(player_x, player_y, self.x, self.y)
        if self.run_anim_count + 1 >= self.len_run ** 2:
            self.run_anim_count = 0
        self.run_anim_count += 1
        if (distance_x_abs < distance_y_abs and distance_x_abs > self.range) or\
             (distance_y_abs <= self.range and distance_x_abs > self.range):
            if distance_x < 0:
                self.x -= self.speed
                self.image = pygame.transform.scale(pygame.transform.flip(
                    self.run_img[self.run_anim_count//self.len_run],
                                  True, False), (125, 115))
                self.rect.x = self.x-100
                self.rect.y = self.y-50
            elif distance_x > 0:
                self.x += self.speed
                self.image = pygame.transform.scale(self.run_img[self.run_anim_count//self.len_run], (125, 115))
                self.rect.x = self.x-100
                self.rect.y = self.y-50
        elif (distance_x_abs > distance_y_abs and distance_y_abs > self.range) or\
             (distance_x_abs <= self.range and distance_y_abs > self.range):
            if distance_y < 0:
                self.y -= self.speed
                self.image = pygame.transform.scale(pygame.transform.flip(
                    self.run_img[self.run_anim_count//self.len_run],
                 True, False), (125, 115))
                self.rect.x = self.x-100
                self.rect.y = self.y-50
            elif distance_y > 0:
                self.y += self.speed
                self.image = pygame.transform.scale(self.run_img[self.run_anim_count//self.len_run], (125, 115))
                self.rect.x = self.x-100
                self.rect.y = self.y-50
        else:
            self.punch(player_x, player_y)

    def idle(self):
        if self.idle_anim_count + 1 >= self.len_idle ** 2:
            self.idle_anim_count = 0
        self.idle_anim_count += 1
        self.image = pygame.transform.scale(self.idle_img[self.idle_anim_count//self.len_idle], (457, 457))
        self.rect.x = self.x-100
        self.rect.y = self.y-50
    
    def punch(self, player_x, player_y):
        distance_x_abs, distance_x, distance_y_abs, distance_y =\
            self.a_search(player_x, player_y, self.x, self.y)
        self.dmg_now = 0
        if distance_x_abs <= self.range and distance_y_abs <= self.range:
            if self.attack_anim_count + 1 >= self.len_attack ** 2:
                self.attack_anim_count = 0
                self.dmg_now = self.dmg
            self.attack_anim_count += 1
            if distance_x > 0:
                self.image = pygame.transform.scale(self.attack_img[self.attack_anim_count//self.len_attack],
                 (125, 115))
            else:
                self.image = pygame.transform.scale(pygame.transform.flip(
                    self.attack_img[self.attack_anim_count//self.len_attack],True, False), (125, 115))
            self.rect.x = self.x-100
            self.rect.y = self.y-50
        return True, self.dmg_now

    def death(self):
        print(self.death_anim_count)
        if self.death_anim_count + 1 >= self.len_death * 2:
            self.death_anim_count = 0
            score_raw = open("local/score.txt")
            score = score_raw.readline()
            score_raw.close()
            print(score)
            score = str(int(score) + self.score)
            f = open("local/score.txt", 'w')
            f.write(f"{str(score)}")
            f.close()
            self.kill()
        self.death_anim_count += 1
        self.image = pygame.transform.scale(self.death_img[self.death_anim_count//self.len_death],
                 (125, 115))
        

    def a_search(self, player_x, player_y, x, y):
        distance_x_abs = abs(player_x - x)
        distance_x = player_x - x
        distance_y_abs = abs(player_y - y)
        distance_y = player_y - y
        return distance_x_abs, distance_x, distance_y_abs, distance_y
