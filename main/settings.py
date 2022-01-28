import csv

import pygame

############################# STORAGE #############################

localsotrage = {"settings.csv": "local/settings.csv", "save.db": "local/save.db", "level.csv": "local/level.csv",
 "level.json": "local/level.json"}

with open(localsotrage["settings.csv"]) as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for i in reader:
        if i[0] == "screen":
            screenpxl_type = i[1]
        elif i[0] == "lang":
            lang_type = i[1]

############################# SCREEN #############################

# screenpxl_types = {"0": (1920, 1080), "1": (1280, 720)}

# screenpxl = {"Wight": screenpxl_types[screenpxl_type][0], "Height": screenpxl_types[screenpxl_type][1]}

screenpxl = {"Wight": 1920, "Height": 1080}
fpslim = 60

############################# Language #############################
lang_types = {"0": "local/en.csv", "1": "local/ru.csv"}

with open(lang_types[lang_type], encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    out = list()
    for i in reader:
        out.append(i[1])

languagestorage = {"version": "release 1.0", "mode1": out[0], "mode2": out[1], "settings": out[2], "exit": out[3],
 "load": out[4], "new": out[5], "save": out[6], "close": out[7], "menu": out[8], "info1": out[9], "use": out[10],
  "can't": out[11], "score": out[12]}

############################# PLAYER #############################

playerconst = {"speed": 10}

playerPos = [screenpxl["Wight"] // 2, screenpxl["Height"] // 2]

playerFov = 0

############################# TEXTURES #############################

############################# 720p #############################

floor720 = {"001": "assets/720p/floor001.png", "002": "assets/720p/floor002.png", "003": "assets/720p/floor003.png"}
hole_floor_720 = {"001": "assets/720p/hole-floor001.png"}
jump_floor_720 = {"001": "assets/720p/jump-floor001.png"}

floors_720 = {"0": floor720, "1": jump_floor_720, "2": hole_floor_720}

############################# 1080p #############################

floor_1080 = {"001": "assets/1080p/floor001.png", "002": "assets/1080p/floor002.png",
 "003": "assets/1080p/floor003.png",
    "011": "assets/1080p/floor_011.png", "012": "assets/1080p/floor_012.png", "013": "assets/1080p/floor_013.png"}
barricade_1080 = {"001": "assets/1080p/barricade_001.png"}
end_room_1080 = {"001": "assets/1080p/end_room_001.png", "002": "assets/1080p/end_room_002.png"}
special_room_1080 = {"002": "assets/1080p/special_room_002.png"}
boss_room_1080 = {"002": "assets/1080p/boss_room_002.png"}
start_room_1080 = {"001": "assets/1080p/start_room_001.png", "002": "assets/1080p/start_room_002.png"}
hole_floor_1080 = {"001": "assets/1080p/hole-floor001.png"}
jump_floor_1080 = {"001": "assets/1080p/jump-floor001.png"}
collides = {"floor": "assets/1080p/collides/floor_collide.png",
 "out_vertical": "assets/1080p/collides/out_collide_vertical.png",
 "out_horisontal": "assets/1080p/collides/out_collide_horisontal.png"}
floors_1080 = {"0": floor_1080, "1": start_room_1080, "2": end_room_1080, "4": special_room_1080}