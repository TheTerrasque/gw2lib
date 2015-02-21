# gw2lib
A small collection of python code to work with Guild Wars 2 api's

This have libraries for working with both Mumble link to get 
position info and current player data from Guild Wars 2, and a generic web api for working
with Guild Wars 2's json web api.


## Usage

### Web API Client
```
>>> from gw2lib.webapi import SimpleClient
>>> api = SimpleClient("v2")
>>> api.items(12341).name
u'Grape'
>>> api.items(12341).type
u'CraftingMaterial'
>>> api.recipes.search(input=12341)
[2916, 3366, 3374, 9638, 9643]
>>> api.recipes(2916).output_item_id
12262
>>> api.items(12262).name
u'Bowl of Grape Pie Filling'
```

Documentation for all API calls can be found at http://wiki.guildwars2.com/wiki/API:Main

Mapping the API urls to the client is pretty straight forward. URL parts are either part of the dot path, or as argument to a call. URL parameters are entered as keywords.

Example: http://wiki.guildwars2.com/wiki/API:2/recipes/search
```
>>> from gw2lib.webapi import SimpleClient
>>> c = SimpleClient("v2")
>>> c.recipes.search(input=46731)
[7314, 7839, 7840, 7841, 7846, 7847, 7848, 7849, 7850]
>>> c.recipes("search", input=46731)
[7314, 7839, 7840, 7841, 7846, 7847, 7848, 7849, 7850]
>>> c("recipes", "search", input=46731)
[7314, 7839, 7840, 7841, 7846, 7847, 7848, 7849, 7850]
>>> c.recipes.search(output=50065)
[8455, 8459, 8460]
```
And for various parameter access:
```
>>> print c.items(46731, lang="es").name
Montón de polvo de hematites
>>> print c.items(46731).name
Pile of Bloodstone Dust
>>> c.items(ids=[46731, 50065])
[[Structure]
  restrictions : []
  name : u'Pile of Bloodstone Dust'
  level : 0
  rarity : u'Ascended'
  vendor_value : 80
  game_types : [u'Activity', u'Dungeon', u'Pve', u'Wvw']
  flags : [u'AccountBound', u'NoSalvage', u'NoSell', u'AccountBindOnUse']
  icon : u'https://render.guildwars2.com/file/1468C6A946BFF0A42CBD08A70E45F8F05851FED0/631480.png'
  type : u'CraftingMaterial'
  id : 46731
  description : u'Refine into bloodstone bricks.',
  [Structure]
  restrictions : []
  name : u'Gift of Blades'
  level : 0
  rarity : u'Ascended'
  vendor_value : 320
  game_types : [u'Activity', u'Dungeon', u'Pve', u'Wvw']
  flags : [u'AccountBound', u'NoSalvage', u'AccountBindOnUse']
  icon : u'https://render.guildwars2.com/file/02F941EE376D490DDD5428294F2EF05EDB07E405/740277.png'
  type : u'Trophy'
  id : 50065
  description : u'A gift of blades used to create Tempered Spinal Blades.']
>>>
```


### Mumble client
```
>>> from gw2lib.mumble import GW2MumbleData
>>> mumble = GW2MumbleData()
>>> mumble.identity
[Struct]
  map_id : 18
  name : u'Player name'
  world_id : 268435470
  team_color_id : 0
  profession : 3
  commander : False
>>> mumble.extra
[Struct]
  player_direction : [0.954851329327,0.0,-0.297084093094]
  server_ip : '206.127.146.90'
  client_build : 45456L
  camera_direction : [97.7617340088,139.420944214,-17.2377490997]
  player_position : [111.966590881,135.065628052,-21.5646572113]
  camera_position : [97.7617340088,139.420944214,-17.2377490997]
>>> mumble.update()
>>> mumble.extra
[Struct]
  player_direction : [0.183639481664,0.0,0.982993662357]
  server_ip : '206.127.146.90'
  client_build : 45456L
  camera_direction : [166.087097168,148.355056763,-21.6510562897]
  player_position : [166.908126831,139.840316772,-8.46068000793]
  camera_position : [166.087097168,148.355056763,-21.6510562897]
>>> mumble.extra.player_position.in_inches()
[6571.18608901,5505.52427676,-333.097637768]
```
More examples can be found in test.py
