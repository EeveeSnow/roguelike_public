import csv
from operator import le
import random as rd
from re import X, search
import timeit
from tokenize import Special
from turtle import ycor
import numpy as np
from math import sqrt

from PIL import Image, ImageDraw

from settings import localsotrage as ls
from settings import floors_720 as fl720
from settings import floors_1080 as fl1080
from settings import barricade_1080 as br1080
from side.blueprints import barricades
import os

file_name_csv = "level.csv"


class levelgen():
    def __init__(self):
        self.roomcount = 100
        self.rawlvl = list()
        global file_name_csv
        self.one = ["10001", "10010", "10100", "11000"]
        self.two = ["10011",  "10110", "11100", "10101", "11001", "11010"]
        self.three = ["10111", "11110", "11011", "11101"]
        self.four = ["11111"]
        self.floor = ["0", "0", "0", "0", "0", "0", "1", "1", "1", "2"]
        self.floorzero = ["011", "012", "013"]
        self.floorone = ["001"]
        self.floortwo = ["001"]
        self.room_choise_tupl = (3, 3, 3, 4)
        zero_percent = [0 for ze1 in range(100)]
        twenty_percent = [1 for tw1 in range(20)]
        twenty_percent.extend([0 for tw0 in range(80)])
        forty_percent = [1 for fo1 in range(40)]
        forty_percent.extend([0 for fo0 in range(60)])
        sixty_percent = [1 for si1 in range(60)]
        sixty_percent.extend([0 for si0 in range(40)])
        self.chance = {"0": zero_percent, "20": twenty_percent,
                       "40": forty_percent, "60": sixty_percent}
        self.names = os.listdir("local/modify/enemies")

    def levelgen(self):
        self.find_path_rooms()
        self.baricades = []
        self.enemycount = list()
        self.listen = list()
        self.encords = list()
        with open(ls[file_name_csv], 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(10):
                for c in range(10):
                    roomtype = self.rooms[i][c]
                    encordsraw = list()
                    barricade, barricadraw = self.gen_barricade()
                    enraw, listen, encords = self.gen_enemies(barricade)
                    listenraw = ", ".join(listen)
                    for _ in encords:
                        encordsraw.append(f"{_[0]}_{_[1]}")
                    encordsraw = "&".join(encordsraw)
                    roomkey, roomids, roomidstype, enemycount, enemynames, enemycords = {
                        roomtype == 3: (11111, self.roomidgen(3), 3, enraw, listenraw, encordsraw),
                        roomtype == 4: (11111, 4, 4, enraw, listenraw, encordsraw),
                        roomtype == 0: (10000, 0, 0, 0, 0, encordsraw),
                        roomtype == 1: (11111, 1, 1, 0, 0, encordsraw),
                        roomtype == 2: (11111, 2, 2, 0, 0, encordsraw)}[True]
                    writer.writerow(
                        [roomkey, i, c, roomids, roomidstype,
                         str(roomtype), barricadraw, enemycount, enemynames, enemycords])
                    self.enemycount.append(enemycount)
                    self.encords.append(encords)
                    self.listen.append(listen)
                self.baricades.append(barricade)
        return self.rooms, self.baricades, self.enemycount, self.listen, self.encords

    # Создаёт пустой масив комнат с комнатой входа и выхода
    def gen_level(self):
        in_raw = coordinate_container(rd.randint(0, 9), rd.randint(0, 9))
        out_raw = coordinate_container(rd.randint(0, 9), rd.randint(0, 9))
        secret_one_raw = coordinate_container(
            rd.randint(0, 9), rd.randint(0, 9))
        secret_two_raw = coordinate_container(
            rd.randint(0, 9), rd.randint(0, 9))
        while self.a_search(in_raw, out_raw)[0][0] < 2 and self.a_search(in_raw, out_raw)[1][0] < 2\
            and self.a_search(in_raw, out_raw)[0][0] > 5 and self.a_search(in_raw, out_raw)[1][0] > 5:
            out_raw.cords = (rd.randint(0, 9), rd.randint(0, 9))
        while self.a_search(in_raw, secret_one_raw)[0][0] < 2\
             and self.a_search(in_raw, secret_one_raw)[1][0] < 2\
                  and self.a_search(secret_two_raw, secret_one_raw)[0][0] < 2\
                       and self.a_search(secret_one_raw, secret_one_raw)[1][0] < 2\
                           and self.a_search(in_raw, secret_one_raw)[0][0] < 5\
                               and self.a_search(in_raw, secret_one_raw)[1][0] < 5\
                                   and self.a_search(secret_two_raw, secret_one_raw)[0][0] < 5\
                                       and self.a_search(secret_one_raw, secret_one_raw)[1][0] < 5:
            secret_one_raw.cords = (rd.randint(0, 9), rd.randint(0, 9))
            secret_two_raw.cords = (rd.randint(0, 9), rd.randint(0, 9))
        self.haveout = in_raw
        self.havein = out_raw
        self.secret_one = secret_one_raw
        self.secret_two = secret_two_raw
        sp1 = [out_raw, secret_one_raw, secret_two_raw]
        sp2 = [in_raw, secret_one_raw, secret_two_raw]
        sp3 = [in_raw, out_raw, secret_two_raw]
        sp4 = [in_raw, out_raw, secret_one_raw]
        self.rooms = [[0 for c in range(10)] for i in range(10)]
        if in_raw in sp1 or\
            out_raw in sp2 or\
                secret_one_raw in sp3 or\
                    secret_two_raw in sp4:
                    self.gen_level()




    # создаёт массив состоящий из комнат уровня
    def find_path_rooms(self):
        self.gen_level()
        in_room, out_room = self.havein, self.haveout
        secret_one = self.secret_one
        secret_two = self.secret_two
        self.gen_path_support(in_room, out_room)
        self.gen_path_support(in_room, secret_one)
        self.gen_path_support(in_room, secret_two)
        self.gen_path_support(secret_one, out_room)
        self.gen_path_support(secret_two, out_room)
        self.rooms[self.secret_one.x][self.secret_one.y] = 4
        self.rooms[self.secret_two.x][self.secret_two.y] = 4
        self.rooms[int(self.havein.x)][int(self.havein.y)] = 1
        self.rooms[self.haveout.x][self.haveout.y] = 2

        return self.rooms

    def gen_path_support(self, in_room, out_room):
        while True:
            x, y = self.a_search(in_room, out_room)
            distance_x_abs, distance_x = x
            distance_y_abs, distance_y = y
            try:
                x, y = {(distance_x_abs < distance_y_abs or distance_y_abs == 0)
                        and distance_x > 0: (in_room.x - 1, in_room.y),
                        (distance_x_abs < distance_y_abs or distance_y_abs == 0)
                        and distance_x < 0: (in_room.x + 1, in_room.y),
                        (distance_x_abs > distance_y_abs or distance_x_abs == 0)
                        and distance_y > 0: (in_room.x, in_room.y - 1),
                        (distance_x_abs > distance_y_abs or distance_x_abs == 0)
                        and distance_y < 0: (in_room.x, in_room.y + 1)}[True]
                in_room = coordinate_container(x, y)
                self.gen_random_rooms(x, y)
                self.rooms[x][y] = 3
            except KeyError:
                break

    def a_search(self, in_room, out_room):
        distance_x_abs = abs(in_room.x - out_room.x)
        distance_x = in_room.x - out_room.x
        distance_y_abs = abs(in_room.y - out_room.y)
        distance_y = in_room.y - out_room.y
        return ((distance_x_abs, distance_x), (distance_y_abs, distance_y))

    def gen_random_rooms(self, x, y):
        room0 = coordinate_container(x, y)
        room1 = coordinate_container(x, y + 1)
        room2 = coordinate_container(x, y - 1)
        room3 = coordinate_container(x + 1, y)
        room4 = coordinate_container(x - 1, y)
        chance = (self.rooms[room0.x][room0.y] + self.rooms[room1.x][room1.y] + self.rooms[room2.x][room2.y]
                  + self.rooms[room3.x][room3.y] + self.rooms[room4.x][room4.y])
        chance = {"0": "0", "1": "20", "2": "20", "3": "40", "4": "60", "5": "40", "6": "20", "7": "20",
                  "8": "0", "9": "0", "10": "0", "11": "0", "12": "0",
                  "13": "0", "14": "0", "15": "0", "16": "0", "17": "0"}[str(chance)]
        ex_room = rd.choice(self.chance[chance])
        type_1 = {not ex_room: 0, ex_room: 3}[True]
        ex_room = rd.choice(self.chance[chance])
        type_2 = {not ex_room: 0, ex_room: 3}[True]
        ex_room = rd.choice(self.chance[chance])
        type_3 = {not ex_room: 0, ex_room: 3}[True]
        ex_room = rd.choice(self.chance[chance])
        type_4 = {not ex_room: 0, ex_room: 3}[True]
        if self.rooms[room1.x][room1.y] == 0:
            self.rooms[room1.x][room1.y] = type_1
        if self.rooms[room2.x][room2.y] == 0:
            self.rooms[room2.x][room2.y] = type_2
        if self.rooms[room3.x][room3.y] == 0:
            self.rooms[room3.x][room3.y] = type_3
        if self.rooms[room4.x][room4.y] == 0:
            self.rooms[room4.x][room4.y] = type_4

    def roomidgen(self, roomtype):
        idstr = list()
        roomtextures = {"0": self.floorzero,
                        "1": self.floorone, "2": self.floortwo}
        for i in range(9):
            for c in range(16):
                n = "0"
                idstr.append(rd.choice(roomtextures[n]))
        idstr = "#".join(idstr)
        return idstr

    def gen_barricade(self):
        n = rd.randrange(0, len(barricades))
        raw = barricades[n]
        strraw = ""
        for i in range(len(raw)):
            strraw += "@".join(raw[i])
        return raw, strraw

    def gen_enemies(self, map):
        n = rd.randrange(2, 10)
        enemies = list()
        enemiescords = list()
        for i in range(n):
            enemies.append(rd.choice(self.names).split(".")[0])
            a = True
            while a:
                c1 = rd.randrange(0, 9)
                c2 = rd.randrange(0, 16)
                if map[c1][c2] == "0":
                    a = False
                    enemiescords.append([c2 * 110 + 80, c1 * 110 + 25])
        return n, enemies, enemiescords

# класс хранения координат


class coordinate_container():
    def __init__(self, x, y):
        self.cord_x, self.cord_y = {-1 < x < 10 and -1 < y < 10: (x, y),
                                    -1 < x < 10 and y < -1: (x, y + 10),
                                    -1 < x < 10 and 10 < y: (x, y - 10),
                                    x < -1 and -1 < y < 10: (x + 10, y),
                                    10 < x and -1 < y < 10: (x - 10, y),
                                    x < -1 and y < -1: (x + 10, y + 10),
                                    10 < x and 10 < y: (x - 10, y - 10)}[True]

    @property
    def x(self):
        return self.cord_x

    @property
    def y(self):
        return self.cord_y

    @property
    def cords(self):
        return self.cord_x, self.cord_y

    @cords.setter
    def cords(self, other):
        x, y = other
        self.cord_x, self.cord_y = {-1 < x < 10 and -1 < y < 10: (x, y),
                                    -1 < x < 10 and y < -1: (x, y + 10),
                                    -1 < x < 10 and 10 < y: (x, y - 10),
                                    x < -1 and -1 < y < 10: (x + 10, y),
                                    10 < x and -1 < y < 10: (x - 10, y),
                                    x < -1 and y < -1: (x + 10, y + 10),
                                    10 < x and 10 < y: (x - 10, y - 10)}[True]

    def pythagoras(self, other):
        out = sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return out


class roomImageFor1920x1080():
    def __init__(self):
        super().__init__()
        self.height = 1760
        self.wight = 990
        self.side = 110
        self.fl = fl1080
        self.br = br1080
        self.defenition = "1080p"

    def genfloorandbarricade(self, x, y):
        global file_name_csv
        with open(ls[file_name_csv], 'r', newline='') as csvfile:
            writer = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i in writer:
                if i[1] == x and i[2] == y:
                    types = i[4]
                    raw = i[3].split("#")
                    raw2 = i[6]
                    c = 0
                    out = list()
                    for b in range(0, len(raw2) + 31, 31):
                        out.append(raw2[c:b].split("@"))
                        c = b
                    raw2 = out[1:10]
                    break
        img = Image.new("RGB", (self.height, self.wight), (256, 256, 256))
        img2 = Image.new("RGBA", (self.height, self.wight), (0, 0, 0, 0))
        i = 0
        c = 0
        room_normal_type = ("3")
        room_special_type = ("1", "2", "4")
        if types in room_normal_type:
            for i in range(0, self.height, self.side):
                for j in range(0, self.wight, self.side):
                    pastimg = Image.open(self.fl["0"][raw[c]])
                    img.paste(pastimg, (i, j))
                    c += 1
                    if raw2[j // self.side][i // self.side] == "1":
                        pastimg = Image.open(self.br["001"])
                        img2.paste(pastimg, (i, j), pastimg)
        elif types in room_special_type:
            img = Image.open(self.fl[str(types)]["002"])
        img2.save(f"assets/barricade_endless/{int(x)}{int(y)}.png")
        return img

    def genfloorandwall(self, x, y):
        img = Image.new("RGB", (self.height + 160, self.wight + 90))
        pastfloor = self.genfloorandbarricade(x, y)
        wall = wallchoise()
        walltype = wall.imagechoise(int(x), int(y))
        pastwall = Image.open(
            f"assets/{self.defenition}/{walltype}_wall_002.png")
        img.paste(pastfloor, (80, 55))
        img.paste(pastwall, (0, 0), pastwall)
        img.save(f"assets/rooms_endless/{int(x)}{int(y)}.png")


class wallchoise():
    def imagechoise(self, x, y):
        wall = ""
        wallx1, wally1, wallx2, wally2 = ["0"] * 4
        global file_name_csv
        with open(ls[file_name_csv], 'r', newline='') as csvfile:
            writer = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i in writer:
                if i[1] == str(x + 1) and i[2] == str(y):
                    wallx1 = i[0][3]
                elif i[1] == str(x - 1) and i[2] == str(y):
                    wallx2 = i[0][1]
                elif i[1] == str(x) and i[2] == str(y + 1):
                    wally1 = i[0][2]
                elif i[1] == str(x) and i[2] == str(y - 1):
                    wally2 = i[0][4]
        wall = wallx2 + wally2 + wallx1 + wally1
        return wall


class start_end_get():
    def simplget(self):
        roomstype = ("1", "2", "4")
        with open(ls["level.csv"], 'r', newline='') as csvfile:
            writer = csv.reader(csvfile, delimiter=';', quotechar='"')
            inendraw = list(filter(lambda x: x[5] in roomstype, writer))
            endnotraw = list(filter(lambda x: x[5] == "2", inendraw))[0][1:3]
            innotraw = list(filter(lambda y: y[5] == "1", inendraw))[0][1:3]
            special1raw= list(filter(lambda y: y[5] == "4", inendraw))[0][1:3]
            special2raw= list(filter(lambda y: y[5] == "4", inendraw))[1][1:3]
        return endnotraw, innotraw, special1raw, special2raw


class lvl_loader():
    def load(self, file):
        self.rooms = [[0 for c in range(10)] for g in range(10)]
        self.baricades = [[0 for d in range(10)] for f in range(10)]
        self.enemycount = list()
        self.listen = list()
        self.encords = list()
        with open(file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i in reader:
                encords = list()
                self.rooms[int(i[1])][int(i[2])] = int(i[5])
                c = 0
                out = list()
                raw = i[6]
                for b in range(0, len(raw) + 31, 31):
                    out.append(raw[c:b].split("@"))
                    c = b
                self.baricades[int(i[1])][int(i[2])] = out[1:10]
                self.enemycount.append(int(i[7]))
                self.listen.append(i[8].split(", "))
                raw = i[9]
                raw = raw.split("&")
                for _ in raw:
                    _ = _.split("_")
                    encords.append([int(_[0]), int(_[1])])
                self.encords.append(encords)
        return self.rooms, self.baricades, self.enemycount, self.listen, self.encords

# a = levelgen()
# # print(a.levelgen())
# # c, d = a.gen_barricade()
# # print(a.gen_enemies(c))
# b = start_end_get()
# print(b.simplget())