import pygame
pygame.init()

# CONFIG
window_width = 800
window_height = 600
#fullscreen = False
framerate = 60

# INTIALIZE
master_window = pygame.display.set_mode((window_width, window_height), flags=pygame.HWSURFACE | pygame.ASYNCBLIT)

# ASSET STUFF

tile_width = 64
tile_height = 64

item_width = 32
item_height = 32

#sheet = pygame.image.load('tiles/nethack_tiles_32x32px_by_nevanda.png')
sheet = pygame.image.load('tiles/rltiles-pack/64x64.png')
sheet = sheet.convert_alpha()

shade = (0, 0, 50)

floor_tile = sheet.subsurface((10*tile_width, 4*tile_height, tile_width, tile_height))
wall_tile = sheet.subsurface((2*tile_width, 3*tile_height, tile_width, tile_height))

# really nice bitmasking tutorial helped a bunch!!! https://www.youtube.com/watch?v=1Sgvkfl6qGc

w0_tile = sheet.subsurface((3*tile_width, 2*tile_height, tile_width, tile_height))
w1_tile = sheet.subsurface((4*tile_width, 2*tile_height, tile_width, tile_height))
w2_tile = sheet.subsurface((5*tile_width, 2*tile_height, tile_width, tile_height))
w3_tile = sheet.subsurface((6*tile_width, 2*tile_height, tile_width, tile_height))
w4_tile = sheet.subsurface((7*tile_width, 2*tile_height, tile_width, tile_height))
w5_tile = sheet.subsurface((8*tile_width, 2*tile_height, tile_width, tile_height))
w6_tile = sheet.subsurface((9*tile_width, 2*tile_height, tile_width, tile_height))
w7_tile = sheet.subsurface((10*tile_width, 2*tile_height, tile_width, tile_height))
w8_tile = sheet.subsurface((11*tile_width, 2*tile_height, tile_width, tile_height))
w9_tile = sheet.subsurface((12*tile_width, 2*tile_height, tile_width, tile_height))
wA_tile = sheet.subsurface((13*tile_width, 2*tile_height, tile_width, tile_height))
wB_tile = sheet.subsurface((14*tile_width, 2*tile_height, tile_width, tile_height))
wC_tile = sheet.subsurface((15*tile_width, 2*tile_height, tile_width, tile_height))
wD_tile = sheet.subsurface((0*tile_width, 3*tile_height, tile_width, tile_height))
wE_tile = sheet.subsurface((1*tile_width, 3*tile_height, tile_width, tile_height))
wF_tile = sheet.subsurface((2*tile_width, 3*tile_height, tile_width, tile_height))
border_tile = sheet.subsurface((0*tile_width, 0*tile_height, tile_width, tile_height))

closed_door_1 = sheet.subsurface((1*tile_width, 2*tile_height, tile_width, tile_height))
closed_door_2 = sheet.subsurface((2*tile_width, 2*tile_height, tile_width, tile_height))
open_door_1 = sheet.subsurface((11*tile_width, 4*tile_height, tile_width, tile_height))
open_door_2 = sheet.subsurface((12*tile_width, 4*tile_height, tile_width, tile_height))

# CREATURES or features lol

up_staircase = sheet.subsurface((5*tile_width, 5*tile_height, tile_width, tile_height))
up_staircase_shade = up_staircase.copy()
up_staircase_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

down_staircase = sheet.subsurface((4*tile_width, 5*tile_height, tile_width, tile_height))
down_staircase_shade = down_staircase.copy()
down_staircase_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)


#floor_tile = sheet.subsurface((32*tile_width, 20*tile_height, tile_width, tile_height))
#wall_tile = sheet.subsurface((13*tile_width, 25*tile_height, tile_width, tile_height))


player_tile = sheet.subsurface((4*tile_width, 7*tile_height, tile_width, tile_height))
player_tile_shade = player_tile.copy()
player_tile_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

#player_tile = sheet.subsurface((0*tile_width, 9*tile_height, tile_width, tile_height))

#fog_tile = sheet.subsurface((6*tile_width, 11*tile_height, tile_width, tile_height))
#fog_tile = pygame.image.load('tiles/shadow.png')

game_background = (16, 16, 16)

# stone brick tiles
sheet_stone = pygame.image.load('tiles/rltiles-pack/catacomb.png')
sheet_stone = sheet_stone.convert_alpha()
w0_stone = sheet_stone.subsurface((0*tile_width, 0*tile_height, tile_width, tile_height))
w0_stone_shade = w0_stone.copy()
w0_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w1_stone = sheet_stone.subsurface((1*tile_width, 0*tile_height, tile_width, tile_height))
w1_stone_shade = w1_stone.copy()
w1_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w2_stone = sheet_stone.subsurface((2*tile_width, 0*tile_height, tile_width, tile_height))
w2_stone_shade = w2_stone.copy()
w2_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w3_stone = sheet_stone.subsurface((3*tile_width, 0*tile_height, tile_width, tile_height))
w3_stone_shade = w3_stone.copy()
w3_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w4_stone = sheet_stone.subsurface((4*tile_width, 0*tile_height, tile_width, tile_height))
w4_stone_shade = w4_stone.copy()
w4_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w5_stone = sheet_stone.subsurface((5*tile_width, 0*tile_height, tile_width, tile_height))
w5_stone_shade = w5_stone.copy()
w5_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w6_stone = sheet_stone.subsurface((6*tile_width, 0*tile_height, tile_width, tile_height))
w6_stone_shade = w6_stone.copy()
w6_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w7_stone = sheet_stone.subsurface((7*tile_width, 0*tile_height, tile_width, tile_height))
w7_stone_shade = w7_stone.copy()
w7_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w8_stone = sheet_stone.subsurface((0*tile_width, 1*tile_height, tile_width, tile_height))
w8_stone_shade = w8_stone.copy()
w8_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

w9_stone = sheet_stone.subsurface((1*tile_width, 1*tile_height, tile_width, tile_height))
w9_stone_shade = w9_stone.copy()
w9_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

wA_stone = sheet_stone.subsurface((2*tile_width, 1*tile_height, tile_width, tile_height))
wA_stone_shade = wA_stone.copy()
wA_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

wB_stone = sheet_stone.subsurface((3*tile_width, 1*tile_height, tile_width, tile_height))
wB_stone_shade = wB_stone.copy()
wB_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

wC_stone = sheet_stone.subsurface((4*tile_width, 1*tile_height, tile_width, tile_height))
wC_stone_shade = wC_stone.copy()
wC_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

wD_stone = sheet_stone.subsurface((5*tile_width, 1*tile_height, tile_width, tile_height))
wD_stone_shade = wD_stone.copy()
wD_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

wE_stone = sheet_stone.subsurface((6*tile_width, 1*tile_height, tile_width, tile_height))
wE_stone_shade = wE_stone.copy()
wE_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

wF_stone = sheet_stone.subsurface((7*tile_width, 1*tile_height, tile_width, tile_height))
wF_stone_shade = wF_stone.copy()
wF_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

closed_door_1_stone = sheet_stone.subsurface((0*tile_width, 2*tile_height, tile_width, tile_height))
closed_door_1_stone_shade = closed_door_1_stone.copy()
closed_door_1_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

closed_door_2_stone = sheet_stone.subsurface((1*tile_width, 2*tile_height, tile_width, tile_height))
closed_door_2_stone_shade = closed_door_2_stone.copy()
closed_door_2_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

open_door_1_stone = sheet_stone.subsurface((2*tile_width, 2*tile_height, tile_width, tile_height))
open_door_1_stone_shade = open_door_1_stone.copy()
open_door_1_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

open_door_2_stone = sheet_stone.subsurface((3*tile_width, 2*tile_height, tile_width, tile_height))
open_door_2_stone_shade = open_door_2_stone.copy()
open_door_2_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

floor_stone = sheet_stone.subsurface((4*tile_width, 2*tile_height, tile_width, tile_height))
floor_stone_shade = floor_stone.copy()
floor_stone_shade.fill(shade, special_flags=pygame.BLEND_RGBA_MIN)

# item sprites
banana_tile = pygame.image.load('tiles/Dungeon Crawl Stone Soup Full/item/food/banana_new.png')
banana_tile = banana_tile.convert_alpha()
banana_tile_shade = banana_tile.copy()
banana_tile_shade.fill(shade, special_flags = pygame.BLEND_RGBA_MIN)

# monster sprites
goblin_tile = sheet.subsurface((2*tile_width, 10*tile_height, tile_width, tile_height))
goblin_tile = goblin_tile.convert_alpha()
goblin_tile_shade = goblin_tile.copy()
goblin_tile_shade.fill(shade, special_flags = pygame.BLEND_RGBA_MIN)

# corpse sprites
corpse = pygame.image.load('tiles/Dungeon Crawl Stone Soup Full/misc/blood/blood_puddle_red.png')
corpse = corpse.convert_alpha()
corpse_shade = corpse.copy()
corpse_shade.fill(shade, special_flags = pygame.BLEND_RGBA_MIN)

'''
FONTS
'''
body_font = pygame.font.Font('fonts/Gorilla.ttf', 12)


# colors

floor_color = (96, 96, 96)
floor_color_dark = (64, 64, 64)

wall_color = (160, 160, 160)
wall_color_dark = (128, 128, 128)

open_door_color = (0, 204, 0)
open_door_color_dark = (0, 153, 0)

closed_door_color = (0, 0, 204)
closed_door_color_dark = (0, 0, 153)

feature_color = (255, 0, 255)
feature_color_dark = (204, 0, 204)

item_color = (255, 255, 0)
item_color_dark = (204, 204, 0)

entity_color = (255, 0, 0)
entity_color_dark = (204, 0, 0)


