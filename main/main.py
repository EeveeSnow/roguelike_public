import csv
from operator import imod
import os
import queue
import random
import sqlite3
import sys
from threading import Thread
from time import sleep

import pygame
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QApplication

from consoleForm import console
from levelgenerator import (levelgen, lvl_loader,
                            roomImageFor1920x1080, start_end_get, wallchoise)
from player import Player, PlayerArrow, Stats
from settings import collides, fpslim, screenpxl
from settings import languagestorage as lg
from settings import localsotrage as ls
from settings import boss_room_1080 as br
from side.UI_elements import Button, OptionBox, Rect, Slider, Text
from enemy import Enemy

loading_percent = 0



class Menu():
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (screenpxl["Wight"], screenpxl["Height"]))
        self.names = os.listdir("local/modify/enemies")
        self.endless_mode = Endless()

    def main_menu_screen(self):
        fps = pygame.time.Clock()
        pygame.init()
        name = random.choice(self.names)
        enemies = pygame.sprite.Group()
        Enemy(name.split(".")[0], [294, 372], enemies, type="idle")
        story_mode_button = Button((810, 312), text=lg["mode1"])
        endless_mode_button = Button((810, 441), text=lg["mode2"])
        settings_button = Button((810, 570), text=lg["settings"])
        exit_button = Button((810, 699), text=lg["exit"])
        info = Rect((1169, 312), butHeigth=457, butWidth=457, text=lg["info1"])
        build_number = Text((30, 1054), butHeigth=14,
                            butWidth=100, text=lg["version"])
        while True:
            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or\
                        (event.type == pygame.MOUSEBUTTONDOWN and exit_button.mouse_in(mousePos) is True):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and story_mode_button.mouse_in(mousePos) is True:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN and endless_mode_button.mouse_in(mousePos) is True:
                    self.save_load("endless")
                if event.type == pygame.MOUSEBUTTONDOWN and settings_button.mouse_in(mousePos) is True:
                    self.settings()
                self.screen.fill((227, 227, 227))
                enemies.update(0, 0, enemies)
                enemies.draw(self.screen)
                # story_mode_button.render(self.screen)
                endless_mode_button.render(self.screen)
                settings_button.render(self.screen)
                exit_button.render(self.screen)
                build_number.render(self.screen)
                # info.render(self.screen)
                fps.tick(fpslim)
            pygame.display.flip()

    def save_load(self, type):
        fps = pygame.time.Clock()
        pygame.init()
        load_game_button = Button((810, 376), text=lg["load"])
        new_game_button = Button((810, 505), text=lg["new"])
        exit_button = Button((810, 634), text=lg["close"])
        build_number = Text((30, 1054), butHeigth=14,
                            butWidth=100, text=lg["version"])
        while True:
            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and load_game_button.mouse_in(mousePos) is True:
                    if type == "endless":
                        self.endless_mode.loading_scren("load")
                if event.type == pygame.MOUSEBUTTONDOWN and new_game_button.mouse_in(mousePos) is True:
                    if type == "endless":
                        self.endless_mode.loading_scren("new")
                if event.type == pygame.MOUSEBUTTONDOWN and exit_button.mouse_in(mousePos) is True:
                    self.main_menu_screen()
                self.screen.fill((227, 227, 227))
                if os.access(ls["level.csv"], os.R_OK):
                    load_game_button.render(self.screen)
                new_game_button.render(self.screen)
                exit_button.render(self.screen)
                build_number.render(self.screen)
                fps.tick(fpslim)
            pygame.display.flip()

    def settings(self):
        dropbox_language = OptionBox(810, 272, 300, 70, (240, 240, 240), (40, 40, 40),
                                     pygame.font.SysFont("Segoe UI", 30), ["English", "Russian"])
        selected_option_gb = 0
        save_button = Button((510, 739), text=lg["save"])
        exit_button = Button((1111, 739), text=lg["close"])
        build_number = Text((30, 1054), butHeigth=14,
                            butWidth=100, text=lg["version"])
        fps = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            for event in events:
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and save_button.mouse_in(mousePos) is True:
                    with open(ls["settings.csv"], 'w', newline='') as csvfile:
                        writer = csv.writer(
                            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(["lang", selected_option_gb])
                if event.type == pygame.MOUSEBUTTONDOWN and exit_button.mouse_in(mousePos) is True:
                    self.main_menu_screen()
                selected_option = dropbox_language.update(events)
                if selected_option >= 0:
                    print(selected_option)
                    selected_option_gb = selected_option
                self.screen.fill((227, 227, 227))
                save_button.render(self.screen)
                build_number.render(self.screen)
                exit_button.render(self.screen)
                dropbox_language.draw(self.screen)
                fps.tick(fpslim)
            pygame.display.flip()


class Endless():
    def __init__(self):
        self.image = roomImageFor1920x1080()
        self.gen = levelgen()
        self.load = lvl_loader()
        self.db = sqlite3.connect(ls["save.db"])
        self.cur = self.db.cursor()
        global outs
        self.all_sprites = pygame.sprite.Group()
        self.outs = outs
        self.screen = pygame.display.set_mode(
            (screenpxl["Wight"], screenpxl["Height"]))

    def loading_scren(self, type: str):
        fps = pygame.time.Clock()
        pygame.init()
        wall = wallchoise()
        self.walls = list()
        treads = 0
        self.id_of_run = self.cur.execute(f"SELECT id FROM endless").fetchall()[-1][0]
        if type == "new":  
            self.id_of_run += 1
            self.id_lvl, self.id_boss, self.id_score = 1, 0, 0
            info = f'INSERT INTO endless VALUES({self.id_of_run}, 0, 0, 0)'
            self.cur.execute(info)
            self.db.commit()
            self.level, self.baricades, self.enemiescount, self.ennames, self.encords = self.gen.levelgen()
        elif type == "load":
            self.id_lvl, self.id_boss, self.id_score =\
                 self.cur.execute(f"SELECT lvls, bosses, score FROM endless WHERE id = {self.id_of_run}").fetchall()[0]
            self.level, self.baricades, self.enemiescount, self.ennames, self.encords = self.load.load(ls["level.csv"])
        elif type == "new2":
            self.level, self.baricades, self.enemiescount, self.ennames, self.encords = self.gen.levelgen()
        slider_percents = Slider(
            (0, 1050), upperValue=1920, sliderWidth=960, text='loading', outlineSize=(1920, 30))
        build_number = Text((30, 1054), butHeigth=14,
                            butWidth=100, text=lg["version"])
        f = open("local/score.txt", 'w')
        f.write(f"{str(self.id_score)}")
        f.close()
        for self.x in range(10):
            for self.y in range(10):
                treads += 1
                thread1 = Thread(target=self.imagegens)
                thread1.start()
                self.walls.append(wall.imagechoise(self.x, self.y))
                sleep(0.05)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                slider_percents.sliderValue = treads
                self.screen.fill((112, 112, 112))
                slider_percents.render(self.screen)
                build_number.render(self.screen)
                fps.tick(fpslim)
                pygame.display.flip()
        sleep(1)
        self.update()

    def map(self, x, y):
        x, y = int(x), int(y)
        ni = Image.new("RGBA", (3 * 20, 3 * 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ni)
        i2 = 0
        j2 = 0
        w = (255, 255, 255)
        g = (0, 255, 0)
        r = (255, 0, 0)
        b = (0, 0, 255)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                try:
                    if self.level[i][j] == 3:
                        draw.rectangle([i2, j2, i2 + 20, j2 + 20], w)
                    elif self.level[i][j] == 1:
                        draw.rectangle([i2, j2, i2 + 20, j2 + 20], g)
                    elif self.level[i][j] == 2:
                        draw.rectangle([i2, j2, i2 + 20, j2 + 20], r)
                    elif self.level[i][j] == 4:
                        draw.rectangle([i2, j2, i2 + 20, j2 + 20], b)
                except IndexError:
                    pass
                j2 += 20
            j2 = 0
            i2 += 20
        ni.save('assets/map.png', 'PNG')

    def new_room(self):
        self.map(self.x, self.y)
        enemylist = []
        map1 = pygame.image.load('assets/map.png', 'assets/map.png')
        map1.convert_alpha()
        rect_map1 = (screenpxl["Wight"] - 60, screenpxl["Height"] - 60, 60, 60)
        wall_floor_image = pygame.image.load(
            f"assets/rooms_endless/{int(self.x)}{int(self.y)}.png")
        wall_floor_rect = wall_floor_image.get_rect()
        barricade_image = f"assets/barricade_endless/{int(self.x)}{int(self.y)}.png"
        for i in range(self.enemiescount[int(self.x + self.y)]):
            e = Enemy(self.ennames[int(self.x + self.y)][i], self.encords[int(self.x + self.y)][i], self.enemies)
            enemylist.append(e)
        return map1, rect_map1, wall_floor_image, wall_floor_rect, barricade_image, enemylist

    def full_map(self):
        ni = Image.new("RGBA", (10 * 20, 10 * 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ni)
        w = (255, 255, 255)
        g = (0, 255, 0)
        r = (255, 0, 0)
        b = (0, 0, 255)
        for i in range(0, 200, 20):
            for j in range(0, 200, 20):
                if self.level[i//20][j//20] == 3:
                    draw.rectangle([i, j, i+20, j+20], w)
                elif self.level[i//20][j//20] == 1:
                    draw.rectangle([i, j, i+20, j+20], g)
                elif self.level[i//20][j//20] == 2:
                    draw.rectangle([i, j, i+20, j+20], r)
                elif self.level[i//20][j//20] == 4:
                    draw.rectangle([i, j, i+20, j+20], b)
        ni.save('assets/full_map.png', 'PNG')

    def imagegens(self):
        self.image.genfloorandwall(str(self.x), str(self.y))

    def update(self):
        startget = start_end_get()
        self.end, self.start, self.sp1, self.sp2  = startget.simplget()
        self.x, self.y = self.start
        self.console = console(self.x, self.y)
        self.is_boss_room = False
        self.full_map()
        map1, rect_map1, wall_floor_image, wall_floor_rect, barricade_image, self.enemylist = self.new_room()
        self.baricade = Barricade(barricade_image)
        self.player = Player(int(self.x), int(self.y), self.walls, self.end, self.sp1, self.sp2, self.is_boss_room,
         self.baricade)
        self.player_arrows = pygame.sprite.Group()
        self.bar = Stats()
        fps = pygame.time.Clock()
        map_image, rect_map = map1, rect_map1
        map2 = pygame.image.load('assets/full_map.png', 'assets/full_map.png')
        map2.convert_alpha()
        rect_map2 = (screenpxl["Wight"] - 200,
                     screenpxl["Height"] - 200, 200, 200)
        # MENU
        menu = False
        menu_button = Button((810, 386), text=lg["menu"])
        menu_button2 = Button((810, 654), text=lg["menu"])
        exit_button = Button((810, 505), text=lg["exit"])
        exit_button2 = Button((810, 540), text=lg["exit"])
        close_button = Button((810, 624), text=lg["close"])
        background = Rect((710, 240), butHeigth=600, butWidth=500)
        background2 = Rect((537, 380), butHeigth=401, butWidth=842)
        build_number = Text((30, 1054), butHeigth=14,
                            butWidth=100, text=lg["version"])
        room_inf = Text((30, 30), butHeigth=14, butWidth=100,
                        text=f"x: {self.x}, y: {self.y}")
        wall = self.walls[int(str(self.x) + str(self.y))]
        room_inf2 = Text((70, 30), butHeigth=14, butWidth=100,
                         text=f"wall: {str(wall)}")
        room_inf5 = Text((1730, 30), butHeigth=14, butWidth=100,
                         text=f"start: {str(self.start[0])} {str(self.start[1])}")
        room_inf6 = Text((1730, 70), butHeigth=14, butWidth=100,
                         text=f"end: {str(self.end[0])} {str(self.end[1])}")
        room_inf7 = Text((1730, 110), butHeigth=14, butWidth=100,
                         text=f"special: {str(self.sp1), str(self.sp2)}")
        self.enemies = pygame.sprite.Group()
        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_HOME:
                    self.console.show()
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    menu = True
                if event.type == pygame.MOUSEBUTTONDOWN and ((exit_button.mouse_in(mousePos) and menu) or\
                     (exit_button2.mouse_in(mousePos) and self.player.end_screen)):
                    info = f'UPDATE endless SET score = {self.id_score}, lvls = {self.id_lvl}, bosses = {self.id_boss} WHERE id = {self.id_of_run}'
                    self.cur.execute(info)
                    self.db.commit()
                    if self.player.end_screen:
                        os.remove("local/level.csv")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and ((menu_button.mouse_in(mousePos) and menu) or\
                    (menu_button2.mouse_in(mousePos) and self.player.end_screen)):
                    info = f'UPDATE endless SET score = {self.id_score}, lvls = {self.id_lvl}, bosses = {self.id_boss} WHERE id = {self.id_of_run}'
                    self.cur.execute(info)
                    self.db.commit()
                    if self.player.end_screen:
                        os.remove("local/level.csv")
                    m = Menu()
                    m.main_menu_screen()
                if event.type == pygame.MOUSEBUTTONDOWN and close_button.mouse_in(mousePos) and menu:
                    menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.bar.ammo > 0:
                            PlayerArrow(self.player.x, self.player.y, mouse_x, mouse_y, self.player_arrows)
                            self.bar.ammo -= 1
                if self.console.map_type:
                    map_image, rect_map = map2, rect_map2
                else:
                    map_image, rect_map = map1, rect_map1
            if menu is False and self.player.is_dead is False:
                self.player.movement()
                x = self.player.x
                y = self.player.y
                self.player_arrows.update()
                self.enemies.update(x, y, self.player_arrows)
            if self.player.sp_get:
                self.bar.change_arrows = 10
            if self.player.change_room:
                self.enemies = pygame.sprite.Group()
                self.x, self.y = self.player.room
                map1, rect_map1, wall_floor_image, wall_floor_rect, barricade_image, self.enemylist = self.new_room()
                room_inf = Text((30, 30), butHeigth=14,
                                butWidth=100, text=f"x: {self.x}, y: {self.y}")
                wall = self.walls[int(str(self.x) + str(self.y))]
                room_inf2 = Text((30, 70), butHeigth=14,
                                 butWidth=100, text=f"wall: {str(wall)}")
                self.baricade = Barricade(barricade_image)
                self.console.room = self.x, self.y
                self.player.now_barricade = self.baricade
            if self.player.lvl_to_boss:
                self.player.lvl_to_boss = False
                self.is_boss_room = True
                self.player.type = True
                wall_floor_image = pygame.image.load(br["002"])
            if self.player.change_lvl:
                self.player.change_lvl = False
                self.id_lvl += 1
                self.id_boss += 1
                score_raw = open("local/score.txt", encoding="utf8")
                score = score_raw.read()
                score_raw.close()
                self.id_score = score
                self.loading_scren("new2")
            self.screen.blit(wall_floor_image, wall_floor_rect)
            if self.is_boss_room is False:
                self.baricade.blit(self.screen)
                self.screen.blit(map_image, rect_map)
            self.player.blit(self.screen)
            self.screen.blit(self.player.weapon(), (self.player.x-10-int(self.player.weapon().get_width()/2), 
                            self.player.y+25-int(self.player.weapon().get_height()/2)))
            self.player_arrows.draw(self.screen)
            self.enemies.draw(self.screen)
            self.bar.blit(self.screen)
            for enemy in self.enemylist:
                e, dmg = enemy.punch(self.player.x, self.player.y)
                if e:
                    if self.bar.hp != 0:
                        self.bar.hp -= dmg
            if self.bar.hp <= 0:
                self.player.is_dead = True
            self.player.text_use.render(self.screen)
            if self.player.is_dead:
                self.player.death()
                if self.player.end_screen:
                    score_raw = open("local/score.txt", encoding="utf8")
                    score = score_raw.read()
                    score_raw.close()
                    text = lg["score"] + " " + score
                    self.text = Text((810, 426), butHeigth=14,
                            butWidth=100, text=text, color=(210, 105, 30))
                    info = f'UPDATE endless SET score = {score} WHERE id = {self.id_of_run}'
                    self.cur.execute(info)
                    self.db.commit()
                    self.enemylist = []
                    background2.render(self.screen)
                    exit_button2.render(self.screen)
                    self.text.render(self.screen)
                    menu_button2.render(self.screen)
            if menu:
                # in game menu
                background.render(self.screen)
                menu_button.render(self.screen)
                exit_button.render(self.screen)
                close_button.render(self.screen)
            if self.console.debug:
                room_inf3 = Text((100, 110), butHeigth=14,
                                 butWidth=100, text=f"player x: {x}, y: {y}")
                room_inf4 = Text((150, 150), butHeigth=14,
                                 butWidth=100, text=f"normal player x: {x - 960}, y: {y - 540}")
                build_number.render(self.screen)
                room_inf.render(self.screen)
                room_inf2.render(self.screen)
                room_inf3.render(self.screen)
                room_inf4.render(self.screen)
                room_inf5.render(self.screen)
                room_inf6.render(self.screen)
                room_inf7.render(self.screen)
                if self.console.change_room:
                    self.x, self.y = self.console.room
                    map1, rect_map1, wall_floor_image, wall_floor_rect, barricade_image = self.new_room()
                    room_inf = Text(
                        (30, 30), butHeigth=14, butWidth=100, text=f"x: {self.x}, y: {self.y}")
                    wall = self.walls[int(str(self.x) + str(self.y))]
                    room_inf2 = Text((30, 70), butHeigth=14,
                                     butWidth=100, text=f"wall: {str(wall)}")
                    self.player.room = self.x, self.y
                    self.console.change_room = False
            fps.tick(fpslim)
            pygame.display.flip()

class Barricade(pygame.sprite.Sprite):
    def __init__(self, barricade_image):
        super().__init__()
        self.image = pygame.image.load(barricade_image)
        self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = (80, -25, 1760, 990)

    def blit(self, screen):
        screen.blit(self.image, self.rect)



if __name__ == "__main__":
    outs = pygame.sprite.Group()
    app = QApplication(sys.argv)
    game = Menu()
    game.main_menu_screen()
    sys.exit(app.exec_())
