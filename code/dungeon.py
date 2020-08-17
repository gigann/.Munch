"""
Issac Gann (gannmann) 2020

dungeon module handles all things related to dungeon generation and rendering
"""

import gc
import random
import itertools
import copy
import enum
import numpy as np
import pygame
import tcod

import assets
import entity
import item
import weapon

class Cell(object): #each tile of the map
    def __init__(self, seen=False, solid=True, w=0, door=0):
        self.seen = seen
        self.solid = solid
        self.w = w
        self.door = door # 0 = no door, 1 = door type 1, 2 = door type 2

class Level(object): #each dungeon level
    def __init__(self, width=41, height=21): # 24, 18
        self.width = width
        self.height = height

        self.cells = np.ndarray((self.width, self.height), dtype=np.object) # create 2D array

        self.room_list = []

        self.feature_list = []

        self.item_list = []

        self.creature_list = []

        # iterate and fill with solid cells
        for i, j in itertools.product(range(self.width), range(self.height)):
            self.cells[i][j] = Cell()

        # ROOMS create a randomly sized room and place it randomly in the level
        room_count = 0
        max_rooms = 10 #5
        min_room_width = 3 #3
        max_room_width = 8 #8
        min_room_height = 3 #3
        max_room_height = 6 #6
        while room_count < max_rooms:

            room = pygame.Rect(0, 0,
                               random.randint(min_room_width, max_room_width),
                               random.randint(min_room_height, max_room_height))

            room.topleft = (random.randint(0, self.width-1 - room.w),
                            random.randint(0, self.height-1 - room.h))
            self.room_list.append(room)
             #print('added room')
            room_count += 1

            for n in self.room_list:
                if room.colliderect(n) and room != n and room in self.room_list:
                    self.room_list.remove(room)
                     #print('deleted room')
                    room_count -= 1 


        for n in self.room_list: # dig all rooms
             #print('dug room: '+ str(n))
            for i, j in itertools.product(range(n.x, n.x + n.width), range(n.y, n.y + n.height)):
                self.cells[i][j].solid = False
            
        
        # TUNNELS
        # connect each room to each other room by A* pathfinding to the center
        
        #graph = tcod.SimpleGraph(cost=cost, dtype=np.int8, cardinal=1, diagonal = 0)
        for pair in itertools.combinations(self.room_list, r=2):

            cost = np.ndarray((self.width-1, self.height-1), dtype=np.int8)
            for i, j in itertools.product(range(self.width-1), range(self.height-1)):
                if self.cells[i][j].solid:
                    cost[i][j] = 2
                else:
                    cost[i][j] = 1

            pathfind = tcod.path.AStar(cost, diagonal=0)
            path = pathfind.get_path(pair[0].centerx, pair[0].centery, pair[1].centerx, pair[1].centery)
            for x in path:
                pass #print(str(x[0]) + ', ' + str(x[1]))

            for n in path:
                self.cells[n[0]][n[1]].solid = False
                 #print('dug out ' + str(n[0]) + ', ' +str(n[1]))

        #doors
        for i, j in itertools.product(range(self.width - 1), range(self.height - 1)):
            if not self.cells[i][j].solid:
                if (
                    self.cells[i+1][j].solid and
                    self.cells[i-1][j].solid and
                    not self.cells[i][j-1].solid and
                    not self.cells[i][j+1].solid):
                        if ((not self.cells[i-1][j-1].solid and not self.cells[i+1][j-1].solid) or
                        (not self.cells[i-1][j+1].solid and not self.cells[i+1][j+1].solid)):
                            self.cells[i][j].door = 2
                if (
                    self.cells[i][j+1].solid and
                    self.cells[i][j-1].solid and
                    not self.cells[i-1][j].solid and
                    not self.cells[i+1][j].solid):
                        if ((not self.cells[i-1][j-1].solid and not self.cells[i-1][j+1].solid) or
                        (not self.cells[i+1][j-1].solid and not self.cells[i+1][j+1].solid)):
                            self.cells[i][j].door = 1

        # set tiles
        for i, j in itertools.product(range(self.width - 1), range(self.height - 1)):
            if self.cells[i][j].solid or self.cells[i][j].door != 0:
                self.cells[i][j].w = 0
                # east north south west VERY IMPORTANT ORDER

                if self.cells[i-1][j].solid or self.cells[i-1][j].door != 0:
                    self.cells[i][j].w += 1
                if self.cells[i][j-1].solid or self.cells[i][j-1].door != 0:
                    self.cells[i][j].w += 2
                if self.cells[i][j+1].solid or self.cells[i][j+1].door != 0:
                    self.cells[i][j].w += 4
                if self.cells[i+1][j].solid or self.cells[i+1][j].door != 0:
                    self.cells[i][j].w += 8

        # border
        for i in range(self.width):
            self.cells[i][self.height-1].w=15
            self.cells[i][0].w=15
            self.cells[i][self.height-1].solid=True
            self.cells[i][0].solid=True

            self.cells[i][self.height-2].w=15
            self.cells[i][1].w=15
            self.cells[i][self.height-2].solid=True
            self.cells[i][1].solid=True


        for i in range(self.height):
            self.cells[self.width -1][i].w=15
            self.cells[0][i].w=15
            self.cells[self.width -1][i].solid=True
            self.cells[0][i].solid=True

            self.cells[self.width -2][i].w=15
            self.cells[1][i].w=15
            self.cells[self.width -2][i].solid=True
            self.cells[1][i].solid=True

        # close doors
        for i, j in itertools.product(range(self.width-1), range(self.height-1)):
            if self.cells[i][j].door != 0:
                self.cells[i][j].solid = True
        
        # staircases
        up_stairs = entity.Entity(name='up stairs',
        x=self.room_list[0].centerx, y=self.room_list[0].centery,
        ai='none', sprite=assets.up_staircase, shadow_sprite=assets.up_staircase_shade)
        down_stairs = entity.Entity(name='down stairs',
        x=self.room_list[-1].centerx, y=self.room_list[-1].centery,
        ai='none', sprite=assets.down_staircase, shadow_sprite=assets.down_staircase_shade)    
        self.feature_list.append(up_stairs)
        self.feature_list.append(down_stairs)

        # items
        for room in self.room_list:
            if self.room_list.index(room) > 0:
                rand_x = random.randint(room.x+1, room.x + room.width-1)
                rand_y = random.randint(room.y+1, room.y + room.height-1)
                while rand_x == room.centerx and rand_y == room.centery:
                    rand_x = random.randint(room.x+1, room.x + room.width-1)
                    rand_y = random.randint(room.y+1, room.y + room.height-1)
                new_item = item.Item(name='banana',
                x=random.randint(room.x+1, room.x + room.width-1),
                y=random.randint(room.y+1, room.y + room.height-1),
                sprite=assets.banana_tile,
                shadow_sprite=assets.banana_tile_shade,
                quantity=1,
                action_set=['eat', 'throw'])
                self.item_list.append(new_item)
        
        new_weapon = item.Item(name='battle axe', x=self.room_list[0].centerx,  y=self.room_list[0].centery,
        sprite=assets.battleax, shadow_sprite = assets.battleax_shade, quantity=1, action_set=['wield', 'sheathe'],
        weapon_com=weapon.battleax)
        self.item_list.append(new_weapon)
        # traps


        # monsters
        for room in self.room_list:
            if room != self.room_list[0]: # make sure monsters spawn far from player
                for num_monsters in range(random.randint(1, 4)):
                    rand_x = random.randint(room.x+1, room.x + room.width-1)
                    rand_y = random.randint(room.y+1, room.y + room.height-1)
                    while rand_x == room.centerx and rand_y == room.centery:
                        rand_x = random.randint(room.x+1, room.x + room.width-1)
                        rand_y = random.randint(room.y+1, room.y + room.height-1)
                    new_monster = entity.Entity(name='goblin',race='Goblin', x=rand_x, y=rand_y,
                    vitality=6, strength=4, dexterity=8, intelligence=4, hitdie=4,
                    ai='aggro',sprite=assets.goblin_tile, shadow_sprite=assets.goblin_tile_shade)
                    self.creature_list.append(new_monster)


class Dungeon(object):
    def __init__(self):
        self.level_list = []
        self.entity_set = set()
        self.level_count = 10
        for x in range(self.level_count):
            self.level_list.append(Level())

        self.current_depth = 0
        self.current_level = self.level_list[self.current_depth]
        
        player_inv = []
        self.player = entity.Entity(name='Player',race='Human',
        x=self.current_level.room_list[0].centerx,
        y=self.current_level.room_list[0].centery, sprite=assets.player_tile,
        shadow_sprite=assets.player_tile_shade, inv=player_inv)
        self.entity_set.add(self.player)

    def find_fov(self):
        trans = np.ndarray((self.current_level.width, self.current_level.height), dtype=np.int8)
        for i, j in itertools.product(range(self.current_level.width), range(self.current_level.height)):
            if self.current_level.cells[i][j].solid:
                trans[i][j] = 0
            else:
                trans[i][j] = 1
        fov = tcod.map.compute_fov(transparency=trans, pov=(self.player.x, self.player.y),
        radius=4, light_walls=True, algorithm=tcod.FOV_PERMISSIVE_8)

        for i, j in itertools.product(range(self.current_level.width), range(self.current_level.height)):
            if fov[i][j]:
                self.current_level.cells[i][j].seen = True
        return fov

    def render_minimap(self, surface, blip_player):
        surface.fill((0, 0, 0))

        gc.collect()

        fov = self.find_fov()
        x=4
        y=4

        for i, j in itertools.product(range(self.current_level.width), range(self.current_level.height)):

            if self.current_level.cells[i][j].seen:
                if fov[i][j]:
                    pygame.draw.rect(surface, assets.floor_color, (i*x, j*y, x, y))
                    if self.current_level.cells[i][j].door == 0:
                        if self.current_level.cells[i][j].solid:   
                            pygame.draw.rect(surface, assets.wall_color, (i*x, j*y, x, y))
                    elif self.current_level.cells[i][j].door >= 1:
                        if self.current_level.cells[i][j].solid:
                            pygame.draw.rect(surface, assets.closed_door_color, (i*x, j*y, x, y))
                        else:
                            pygame.draw.rect(surface, assets.open_door_color, (i*x, j*y, x, y))
                else:
                    pygame.draw.rect(surface, assets.floor_color_dark, (i*x, j*y, x, y))
                    
                    if self.current_level.cells[i][j].door == 0:
                        if self.current_level.cells[i][j].solid:   
                            pygame.draw.rect(surface, assets.wall_color_dark, (i*x, j*y, x, y))
                    elif self.current_level.cells[i][j].door >= 1:
                        if self.current_level.cells[i][j].solid:
                            pygame.draw.rect(surface, assets.closed_door_color_dark, (i*x, j*y, x, y))
                        else:
                            pygame.draw.rect(surface, assets.open_door_color_dark, (i*x, j*y, x, y))

        
        for i in self.current_level.item_list: # draw items
            if self.current_level.cells[i.x][i.y].seen:
                if fov[i.x][i.y]:
                    pygame.draw.rect(surface, assets.item_color, (i.x*x, i.y*y, x, y))
                else:
                    pygame.draw.rect(surface, assets.item_color_dark, (i.x*x, i.y*y, x, y))

        for i in self.current_level.feature_list: # draw objects
            if self.current_level.cells[i.x][i.y].seen:
                if fov[i.x][i.y]:
                    pygame.draw.rect(surface, assets.feature_color, (i.x*x, i.y*y, x, y))
                else:
                    pygame.draw.rect(surface, assets.feature_color_dark, (i.x*x, i.y*y, x, y))


        for i in self.entity_set: # draw creatures
            if self.current_level.cells[i.x][i.y].seen:
                if fov[i.x][i.y]:
                    pygame.draw.rect(surface, assets.entity_color, (i.x*x, i.y*y, x, y))
                else:
                    pygame.draw.rect(surface, assets.entity_color_dark, (i.x*x, i.y*y, x, y))

        blip_player = not blip_player

        if blip_player:
            pygame.draw.rect(surface, (255, 255, 255),
            (self.player.x*x, self.player.y*y, x, y))
        else:
            pygame.draw.rect(surface, (0, 0, 0),
            (self.player.x*x, self.player.y*y, x, y))


        return blip_player

    def render_proper(self, surface):
        # 1. if in FOV 2-7 and seen
        # 2. render floor
        # 3. render features
        # 4. render items
        # 5. render monsters
        # 6. render player
        # 7. render walls with bitwise and make wall translucent if overlap entity
        # 8. else if REPEAT 2-7 for seen but shaded variants
        # 
        # 
        fov = self.find_fov()

        x_offset = ((self.player.x - self.player.y) * assets.tile_width//2) - surface.get_width()//2 + assets.tile_width//2
        y_offset = ((self.player.x + self.player.y) * assets.tile_height//4) - surface.get_height()//2 + assets.tile_height//4

        for i, j in itertools.product(range(self.current_level.width), range(self.current_level.height)): # iterate through all cells
            if fov[i][j] and self.current_level.cells[i][j].seen: # 1. if seen and in FOV
                if not self.current_level.cells[i][j].solid: # 2. floor / open door
                    if self.current_level.cells[i][j].door == 0:
                        surface.blit(assets.floor_stone, # 2a floor
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    else:
                        surface.blit(assets.floor_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                        if ((i > 0) and (j > 0) and (i+1 < self.current_level.width) and (j+1 < self.current_level.height)): # only check if indexes are in bounds
                            if (self.tile_has_entity(i-1, j-1) or self.tile_has_entity(i, j)): # hide the door
                                if self.current_level.cells[i][j].door == 1:
                                    surface.blit(assets.open_door_1_stone_hide, # 2b door 1
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))
                                elif self.current_level.cells[i][j].door == 2:
                                    surface.blit(assets.open_door_2_stone_hide, # 2c door 2
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))
                            else:
                                if self.current_level.cells[i][j].door == 1:
                                    surface.blit(assets.open_door_1_stone, # 2b door 1
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))
                                elif self.current_level.cells[i][j].door == 2:
                                    surface.blit(assets.open_door_2_stone, # 2c door 2
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))

                    feature_at_tile = self.entity_at_tile(self.current_level.feature_list, i, j)
                    item_at_tile = self.entity_at_tile(self.current_level.item_list, i, j)
                    creature_at_tile = self.entity_at_tile(self.current_level.creature_list, i, j)

                    if feature_at_tile is not None: # 3. tile has feature
                        surface.blit(feature_at_tile.sprite,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))

                    if item_at_tile is not None: # 4. tile has item
                        surface.blit(item_at_tile.sprite,
                        (((i - j) * assets.tile_width//2)-(x_offset-16),
                        ((i + j) * assets.tile_height//4)-(y_offset-28)))

                    if creature_at_tile is not None: # 5. tile has creature
                        surface.blit(creature_at_tile.sprite,
                        (((i - j) * assets.tile_width//2)-(x_offset-16),
                        ((i + j) * assets.tile_height//4)-(y_offset-28)))

                else: # 6. wall / closed door
                    if ((i > 0) and (j > 0) and (i+1 < self.current_level.width) and (j+1 < self.current_level.height)): # only check if indexes are in bounds
                        if ((self.tile_has_entity(i-1, j-1) and self.current_level.cells[i-1][j-1].seen) or
                        (self.tile_has_entity(i, j-1) and self.current_level.cells[i][j-1].seen) or
                        (self.tile_has_entity(i-2, j-1) and self.current_level.cells[i-2][j-1].seen) or
                        (self.tile_has_entity(i-1, j) and self.current_level.cells[i-1][j].seen)):
                            # only make tiles invisible if player has seen them before
                            self.render_wall(surface, i, j, x_offset, y_offset, shadow=False, hide=True)
                        else: # doesn't visually block an entity
                            self.render_wall(surface, i, j, x_offset, y_offset, shadow=False, hide=False)
            elif self.current_level.cells[i][j].seen: 
                if not self.current_level.cells[i][j].solid: # 2. floor / open door
                    if self.current_level.cells[i][j].door == 0: 
                        surface.blit(assets.floor_stone_shade, # 2a floor
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    else:
                        surface.blit(assets.floor_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                        if ((i > 0) and (j > 0) and (i+1 < self.current_level.width) and (j+1 < self.current_level.height)): # only check if indexes are in bounds
                            if (self.tile_has_entity(i-1, j-1) or self.tile_has_entity(i, j)): # hide the door
                                if self.current_level.cells[i][j].door == 1:
                                    surface.blit(assets.open_door_1_stone_shade_hide, # 2b door 1
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))
                                elif self.current_level.cells[i][j].door == 2:
                                    surface.blit(assets.open_door_2_stone_shade_hide, # 2c door 2
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))
                            else:
                                if self.current_level.cells[i][j].door == 1:
                                    surface.blit(assets.open_door_1_stone_shade, # 2b door 1
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))
                                elif self.current_level.cells[i][j].door == 2:
                                    surface.blit(assets.open_door_2_stone_shade, # 2c door 2
                                    (((i - j) * assets.tile_width//2)-x_offset,
                                    ((i + j) * assets.tile_height//4)-y_offset))

                    feature_at_tile = self.entity_at_tile(self.current_level.feature_list, i, j)
                    item_at_tile = self.entity_at_tile(self.current_level.item_list, i, j)
                    creature_at_tile = self.entity_at_tile(self.current_level.creature_list, i, j)

                    if feature_at_tile is not None: # 3. tile has feature
                        surface.blit(feature_at_tile.shadow_sprite,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))

                    if item_at_tile is not None: # 4. tile has item
                        surface.blit(item_at_tile.shadow_sprite,
                        (((i - j) * assets.tile_width//2)-(x_offset-16),
                        ((i + j) * assets.tile_height//4)-(y_offset-28)))

                    if creature_at_tile is not None: # 5. tile has creature
                        surface.blit(creature_at_tile.shadow_sprite,
                        (((i - j) * assets.tile_width//2)-(x_offset-16),
                        ((i + j) * assets.tile_height//4)-(y_offset-28)))

                else: # 6. wall / closed door
                    if ((i > 0) and (j > 0) and (i+1 < self.current_level.width) and (j+1 < self.current_level.height)): # only check if indexes are in bounds
                        if ((self.tile_has_entity(i-1, j-1) and self.current_level.cells[i-1][j-1].seen) or
                        (self.tile_has_entity(i, j-1) and self.current_level.cells[i][j-1].seen) or
                        (self.tile_has_entity(i-2, j-1) and self.current_level.cells[i-2][j-1].seen) or
                        (self.tile_has_entity(i-1, j) and self.current_level.cells[i-1][j].seen)):
                            # only make tiles invisible if player has seen them before
                            self.render_wall(surface, i, j, x_offset, y_offset, shadow=True, hide=True)
                        else: # doesn't visually block an entity
                            self.render_wall(surface, i, j, x_offset, y_offset, shadow=True, hide=False)
            
        surface.blit(self.player.sprite,
        (((self.player.x - self.player.y) * assets.tile_width//2)-(x_offset-16),
        ((self.player.x + self.player.y) * assets.tile_height//4)-(y_offset-28)))

    def render(self, surface):

        gc.collect()

        fov = self.find_fov()

        x_offset = ((self.player.x - self.player.y) * assets.tile_width//2) - surface.get_width()//2 + assets.tile_width//2
        y_offset = ((self.player.x + self.player.y) * assets.tile_height//4) - surface.get_height()//2 + assets.tile_height//4

        # shoutout clint bellanger for the isometric math http://clintbellanger.net/articles/isometric_math/
        for i, j in itertools.product(range(self.current_level.width), range(self.current_level.height)): # draw floor underneath everything
            
            if self.current_level.cells[i][j].seen:
                if fov[i][j]:
                    surface.blit(assets.floor_stone,
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
                    
                    if self.current_level.cells[i][j].door == 0:
                        if self.current_level.cells[i][j].solid:   
                            # bitmasking
                            if self.current_level.cells[i][j].w == 0:
                                surface.blit(assets.w0_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 1:
                                surface.blit(assets.w1_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 2:
                                surface.blit(assets.w2_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 3:
                                surface.blit(assets.w3_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 4:
                                surface.blit(assets.w4_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 5:
                                surface.blit(assets.w5_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 6:
                                surface.blit(assets.w6_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 7:
                                surface.blit(assets.w7_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 8:
                                surface.blit(assets.w8_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 9:
                                surface.blit(assets.w9_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 10:
                                surface.blit(assets.wA_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 11:
                                surface.blit(assets.wB_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 12:
                                surface.blit(assets.wC_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 13:
                                surface.blit(assets.wD_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 14:
                                surface.blit(assets.wE_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 15:
                                surface.blit(assets.wF_stone,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 16: # border
                                #surface.blit(assets.border_tile,
                                #((i - j) * assets.tile_width//2,
                                #(i + j) * assets.tile_height//4))
                                pass
                    elif self.current_level.cells[i][j].door == 1:
                        if self.current_level.cells[i][j].solid:
                            surface.blit(assets.closed_door_1_stone,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                        else:
                            surface.blit(assets.open_door_1_stone,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            
                    elif self.current_level.cells[i][j].door == 2:
                        if self.current_level.cells[i][j].solid:
                            surface.blit(assets.closed_door_2_stone,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                        else:
                            surface.blit(assets.open_door_2_stone,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                else:
                    surface.blit(assets.floor_stone_shade,
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + + j) * assets.tile_height//4)-y_offset))
                    
                    if self.current_level.cells[i][j].door == 0:
                        if self.current_level.cells[i][j].solid:   
                            # bitmasking
                            if self.current_level.cells[i][j].w == 0:
                                surface.blit(assets.w0_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 1:
                                surface.blit(assets.w1_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 2:
                                surface.blit(assets.w2_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 3:
                                surface.blit(assets.w3_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 4:
                                surface.blit(assets.w4_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 5:
                                surface.blit(assets.w5_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 6:
                                surface.blit(assets.w6_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 7:
                                surface.blit(assets.w7_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 8:
                                surface.blit(assets.w8_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 9:
                                surface.blit(assets.w9_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 10:
                                surface.blit(assets.wA_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 11:
                                surface.blit(assets.wB_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 12:
                                surface.blit(assets.wC_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 13:
                                surface.blit(assets.wD_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 14:
                                surface.blit(assets.wE_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 15:
                                surface.blit(assets.wF_stone_shade,
                                (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            if self.current_level.cells[i][j].w == 16: # border
                                #surface.blit(assets.border_tile,
                                #((i - j) * assets.tile_width//2,
                                #(i + j) * assets.tile_height//4))
                                pass
                    elif self.current_level.cells[i][j].door == 1:
                        if self.current_level.cells[i][j].solid:
                            surface.blit(assets.closed_door_1_stone_shade,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                        else:
                            surface.blit(assets.open_door_1_stone_shade,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                            
                    elif self.current_level.cells[i][j].door == 2:
                        if self.current_level.cells[i][j].solid:
                            surface.blit(assets.closed_door_2_stone_shade,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                        else:
                            surface.blit(assets.open_door_2_stone_shade,
                            (((i - j) * assets.tile_width//2)-x_offset,
                                ((i + j) * assets.tile_height//4)-y_offset))
                
                #if not fov[i][j]:
                #    surface.blit(assets.fog_tile, # draw shadows
                #    (((i - j) * assets.tile_width//2)-x_offset,
                #    ((i + j) * assets.tile_height//4)-y_offset))

        for i in self.current_level.item_list: # draw items
            i.render(self, surface, x_offset=x_offset-16, y_offset=y_offset-28, fov=fov)

        for f in self.current_level.feature_list: # draw objects
            f.render(self, surface, x_offset=x_offset, y_offset=y_offset, fov=fov)

        for c in self.current_level.creature_list: # draw objects
            c.render(self, surface, x_offset=x_offset-16, y_offset=y_offset-28, fov=fov)

        self.player.render(self, surface, x_offset=x_offset-16, y_offset=y_offset-28, fov=fov)

        #for c in self.entity_set: # draw creatures
        #    c.render(self, surface, x_offset=x_offset, y_offset=y_offset, fov=fov)
        
        # blah

    def static_render(self, surface): # render tiles once
        gc.collect()


        # only iterate/draw what would be on screen
        # only should ever draw 13 x 10 tiles NOT A PROBLEM BECAUSE IT AUTO CLIPS
        # ONLY CALL THIS FUNCTION ONCE FOR BACKGROUND TILES :)

        # shoutout clint bellanger for the isometric math http://clintbellanger.net/articles/isometric_math/
        for i in range(self.current_level.width):
            for j in range(self.current_level.height): # draw floor underneath everything

                        surface.blit(assets.floor_stone,
                        (((i - j) * assets.tile_width//2),
                        ((i + j) * assets.tile_height//4)))
                        
                        if self.current_level.cells[i][j].door == 0:
                            if self.current_level.cells[i][j].solid:   
                                # bitmasking
                                if self.current_level.cells[i][j].w == 0:
                                    surface.blit(assets.w0_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 1:
                                    surface.blit(assets.w1_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 2:
                                    surface.blit(assets.w2_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 3:
                                    surface.blit(assets.w3_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 4:
                                    surface.blit(assets.w4_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 5:
                                    surface.blit(assets.w5_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 6:
                                    surface.blit(assets.w6_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 7:
                                    surface.blit(assets.w7_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 8:
                                    surface.blit(assets.w8_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 9:
                                    surface.blit(assets.w9_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 10:
                                    surface.blit(assets.wA_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 11:
                                    surface.blit(assets.wB_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 12:
                                    surface.blit(assets.wC_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 13:
                                    surface.blit(assets.wD_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 14:
                                    surface.blit(assets.wE_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))
                                if self.current_level.cells[i][j].w == 15:
                                    surface.blit(assets.wF_stone,
                                    (((i - j) * assets.tile_width//2),
                                    ((i + j) * assets.tile_height//4)))

    def toggle_door(self): # must be adjacent to door to toggle it
        toggled_doors = 0

        if self.current_level.cells[self.player.x + 1][self.player.y].door != 0:
            self.current_level.cells[self.player.x + 1][self.player.y].solid = not self.current_level.cells[self.player.x + 1][self.player.y].solid
            toggled_doors += 1
                
        if self.current_level.cells[self.player.x - 1][self.player.y].door != 0:
            self.current_level.cells[self.player.x - 1][self.player.y].solid = not self.current_level.cells[self.player.x - 1][self.player.y].solid
            toggled_doors += 1

        if self.current_level.cells[self.player.x + 1][self.player.y + 1].door != 0:
            self.current_level.cells[self.player.x + 1][self.player.y + 1].solid = not self.current_level.cells[self.player.x + 1][self.player.y + 1].solid
            toggled_doors += 1

        if self.current_level.cells[self.player.x + 1][self.player.y - 1].door != 0:
            self.current_level.cells[self.player.x + 1][self.player.y - 1].solid = not self.current_level.cells[self.player.x + 1][self.player.y - 1].solid
            toggled_doors += 1

        if self.current_level.cells[self.player.x - 1][self.player.y + 1].door != 0:
            self.current_level.cells[self.player.x - 1][self.player.y + 1].solid = not self.current_level.cells[self.player.x - 1][self.player.y + 1].solid
            toggled_doors += 1

        if self.current_level.cells[self.player.x - 1][self.player.y - 1].door != 0:
            self.current_level.cells[self.player.x - 1][self.player.y - 1].solid = not self.current_level.cells[self.player.x - 1][self.player.y - 1].solid
            toggled_doors += 1

        if self.current_level.cells[self.player.x][self.player.y + 1].door != 0:
            self.current_level.cells[self.player.x][self.player.y + 1].solid = not self.current_level.cells[self.player.x][self.player.y + 1].solid
            toggled_doors += 1

        if self.current_level.cells[self.player.x][self.player.y - 1].door != 0:
            self.current_level.cells[self.player.x][self.player.y - 1].solid = not self.current_level.cells[self.player.x][self.player.y - 1].solid
            toggled_doors += 1

        if toggled_doors > 0:
            return 'toggled door(s)'
        else:
            return 'no action'

    def use_stairs(self, direction):
        if direction == 'up':
            for e in self.current_level.feature_list:
                if e.name == 'up stairs' and self.player.is_on(e):
                    self.current_depth -= 1
                    self.current_level = self.level_list[self.current_depth]
                    self.player.x = self.current_level.room_list[-1].centerx
                    self.player.y = self.current_level.room_list[-1].centery
                    return 'ascended the stairs.'
        elif direction == 'down':
            for e in self.current_level.feature_list:
                if e.name == 'down stairs' and self.player.is_on(e):
                    self.current_depth += 1
                    self.current_level = self.level_list[self.current_depth]
                    self.player.x = self.current_level.room_list[0].centerx
                    self.player.y = self.current_level.room_list[0].centery
                    return 'descended the stairs.'
        else:
            return 'no action'
        return 'no action'

    def tile_has_creature(self, x, y):
        for creature in self.current_level.creature_list:
            if creature.x == x and creature.y == y:
                return True
        return False

    def entity_at_tile(self, entity_list, x, y):
        for i in entity_list:
            if i.x == x and i.y == y:
                return i
        return None

    def tile_has_entity(self, x, y):
        # check player first to save time
        if self.player.x == x and self.player.y == y:
            return True
        for (feature, iitem, creature) in itertools.zip_longest(
            self.current_level.feature_list,
            self.current_level.item_list,
            self.current_level.creature_list):
            if feature is not None:
                if feature.x == x and feature.y == y:
                    return True
            if iitem is not None:
                if iitem.x == x and iitem.y == y:
                    return True
            if creature is not None:
                if creature.x == x and creature.y == y:
                    return True
        return False

    def render_wall(self, surface, i, j, x_offset, y_offset, shadow, hide):
        if not shadow:
            surface.blit(assets.floor_stone,
            (((i - j) * assets.tile_width//2)-x_offset,
            ((i + j) * assets.tile_height//4)-y_offset))
            if not hide:
                if self.current_level.cells[i][j].door == 0: # wall confirmed
                    if self.current_level.cells[i][j].w == 0:
                        surface.blit(assets.w0_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 1:
                        surface.blit(assets.w1_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 2:
                        surface.blit(assets.w2_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 3:
                        surface.blit(assets.w3_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 4:
                        surface.blit(assets.w4_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 5:
                        surface.blit(assets.w5_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 6:
                        surface.blit(assets.w6_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 7:
                        surface.blit(assets.w7_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 8:
                        surface.blit(assets.w8_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 9:
                        surface.blit(assets.w9_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 10:
                        surface.blit(assets.wA_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 11:
                        surface.blit(assets.wB_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 12:
                        surface.blit(assets.wC_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 13:
                        surface.blit(assets.wD_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 14:
                        surface.blit(assets.wE_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 15:
                        surface.blit(assets.wF_stone,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset)) 
                elif self.current_level.cells[i][j].door == 1:
                    surface.blit(assets.closed_door_1_stone, # door 1
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
                elif self.current_level.cells[i][j].door == 2:
                    surface.blit(assets.closed_door_2_stone, # door 2
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
            else:
                if self.current_level.cells[i][j].door == 0: # wall confirmed
                    if self.current_level.cells[i][j].w == 0:
                        surface.blit(assets.w0_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 1:
                        surface.blit(assets.w1_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 2:
                        surface.blit(assets.w2_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 3:
                        surface.blit(assets.w3_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 4:
                        surface.blit(assets.w4_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 5:
                        surface.blit(assets.w5_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 6:
                        surface.blit(assets.w6_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 7:
                        surface.blit(assets.w7_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 8:
                        surface.blit(assets.w8_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 9:
                        surface.blit(assets.w9_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 10:
                        surface.blit(assets.wA_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 11:
                        surface.blit(assets.wB_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 12:
                        surface.blit(assets.wC_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 13:
                        surface.blit(assets.wD_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 14:
                        surface.blit(assets.wE_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 15:
                        surface.blit(assets.wF_stone_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset)) 
                elif self.current_level.cells[i][j].door == 1:
                    surface.blit(assets.closed_door_1_stone_hide, # door 1
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
                elif self.current_level.cells[i][j].door == 2:
                    surface.blit(assets.closed_door_2_stone_hide, # door 2
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
        else:
            surface.blit(assets.floor_stone_shade,
            (((i - j) * assets.tile_width//2)-x_offset,
            ((i + j) * assets.tile_height//4)-y_offset))
            if not hide:
                if self.current_level.cells[i][j].door == 0: # wall confirmed
                    if self.current_level.cells[i][j].w == 0:
                        surface.blit(assets.w0_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 1:
                        surface.blit(assets.w1_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 2:
                        surface.blit(assets.w2_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 3:
                        surface.blit(assets.w3_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 4:
                        surface.blit(assets.w4_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 5:
                        surface.blit(assets.w5_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 6:
                        surface.blit(assets.w6_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 7:
                        surface.blit(assets.w7_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 8:
                        surface.blit(assets.w8_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 9:
                        surface.blit(assets.w9_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 10:
                        surface.blit(assets.wA_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 11:
                        surface.blit(assets.wB_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 12:
                        surface.blit(assets.wC_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 13:
                        surface.blit(assets.wD_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 14:
                        surface.blit(assets.wE_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 15:
                        surface.blit(assets.wF_stone_shade,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset)) 
                elif self.current_level.cells[i][j].door == 1:
                    surface.blit(assets.closed_door_1_stone_shade, # door 1
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
                elif self.current_level.cells[i][j].door == 2:
                    surface.blit(assets.closed_door_2_stone_shade, # door 2
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
            else:
                if self.current_level.cells[i][j].door == 0: # wall confirmed
                    if self.current_level.cells[i][j].w == 0:
                        surface.blit(assets.w0_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 1:
                        surface.blit(assets.w1_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 2:
                        surface.blit(assets.w2_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 3:
                        surface.blit(assets.w3_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 4:
                        surface.blit(assets.w4_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 5:
                        surface.blit(assets.w5_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 6:
                        surface.blit(assets.w6_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 7:
                        surface.blit(assets.w7_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 8:
                        surface.blit(assets.w8_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 9:
                        surface.blit(assets.w9_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 10:
                        surface.blit(assets.wA_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 11:
                        surface.blit(assets.wB_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 12:
                        surface.blit(assets.wC_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 13:
                        surface.blit(assets.wD_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 14:
                        surface.blit(assets.wE_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset))
                    if self.current_level.cells[i][j].w == 15:
                        surface.blit(assets.wF_stone_shade_hide,
                        (((i - j) * assets.tile_width//2)-x_offset,
                        ((i + j) * assets.tile_height//4)-y_offset)) 
                elif self.current_level.cells[i][j].door == 1:
                    surface.blit(assets.closed_door_1_stone_shade_hide, # door 1
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))
                elif self.current_level.cells[i][j].door == 2:
                    surface.blit(assets.closed_door_2_stone_shade_hide, # door 2
                    (((i - j) * assets.tile_width//2)-x_offset,
                    ((i + j) * assets.tile_height//4)-y_offset))

