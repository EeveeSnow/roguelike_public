# roguelike_public

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e78ddf2b5d57441bbf5a66a207b0c9a5)](https://app.codacy.com/gh/EeveeSnow/roguelike_public?utm_source=github.com&utm_medium=referral&utm_content=EeveeSnow/roguelike_public&utm_campaign=Badge_Grade_Settings)

## Not for sale 

This game is a open source project by 2 student programmers.

## Using assets

This game using some assets from other game: 
- [Undermine](https://undermine.game/)

And some hand made assets

## Moding

This game suport modification and ading new enemies. For example in game given one enemy [Nemesis](https://github.com/EeveeSnow/roguelike_public/blob/main/local/modify/enemies/Nemesis.json) you can edit his JSON file or make your own enemy using this gide below 

### Enemy modifying

* create or open JSON file in local/modify/enemies
* create this keys:
  ~~~~
  "name":
  "hp":
  "type":
  "speed":
  "dmg":
  "dmg_range":
  "score": 
  "idle":
  "run":
  "attack":
  "death"
  ~~~~
* add to keys data but remember:
  - for keys 1 and 3 you need use string 
  - for 2 and 4 - 7 number
  - for 8 - 11 Array with path from game launcher to assets (example in [Nemesis](https://github.com/EeveeSnow/roguelike_public/blob/main/local/modify/enemies/Nemesis.json))
* save and cheack enemy in game!


