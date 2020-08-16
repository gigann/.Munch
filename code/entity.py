"""
Issac Gann (gannmann) 2020

entity module handles entity related objects and methods
"""

import math
import numpy as np
import itertools
import random

import tcod

import assets

# creatures have names, coordinates, equipment container, drops, attributes, etc

class Entity(object):
    def __init__(self, name='', race='', x=0, y=0, exp = 1, vitality=10,
    metabolism=10, strength=10, dexterity=10, intelligence=10, hitdie=6, weapondie=8,
    ai='simple', sprite=None, shadow_sprite=None, inv=None, helm=None,
    armor=None, boots=None, mainhand=None, offhand=None, ring1=None, ring2=None):
        self.name = name
        self.race = race
        self.x = x
        self.y = y
        self.exp = exp
        self.vit = vitality
        self.met = metabolism
        self.str = strength
        self.dex = dexterity
        self.int = intelligence
        self.hd = hitdie
        self.wd = weapondie
        self.ai = ai
        self.sprite = sprite
        self.shadow_sprite = shadow_sprite

        self.inv = inv

        self.helm = helm # armor and weapon slots are single item inventories. when equipped, items are moved from inventory to this slot and vice versa.
        self.armor = armor
        self.boots = boots
        self.mainhand = mainhand
        self.offhand = offhand
        self.ring1 = ring1
        self.ring2 = ring2

        # determined attributes
        self.level = math.floor(math.log2(self.exp))+1
        self.max_hp = (self.bonus(self.vit) + self.hd) * self.level
        self.max_hunger = self.mod(self.met) + self.hd
        self.current_hp = (self.bonus(self.vit) + self.hd) * self.level
        self.current_hunger = self.max_hunger // 2

        self.attack_mod = self.mod(self.str)
        self.defense_mod = self.mod(self.dex) + 10

        #self.max_ingredients_known = (math.floor((self.int-10)//2)) * self.level

    def determined_attributes(self):
        self.level = math.floor(math.log2(self.exp))+1
        self.max_hp = (self.bonus(self.vit) + self.hd) * self.level
        self.max_hunger = self.mod(self.met) + self.hd

        self.attack_mod = self.mod(self.str)
        self.defense_mod = self.mod(self.dex) + 10

        #self.max_ingredients_known = (math.floor((self.int-10)//2)) * self.level

    def mod(self, attribute):
        return math.floor((attribute-10)//2)

    def bonus(self, attribute):
        if attribute <= 10:
            return 0
        else:
            return math.floor((attribute-10)//2)

    def render(self, dungeon, surface, x_offset, y_offset, fov):
        # conditions to show at half opacity:
        # wall south or east of creature

        '''
        surface.blit(assets.player_tile,
            ((self.x - self.y) * assets.tile_width//2,
            (self.x + self.y) * assets.tile_height//4))    
        '''
        if self.x+1 < dungeon.current_level.width and self.y+1 < dungeon.current_level.height: # fixes out of index crash
            if dungeon.current_level.cells[self.x][self.y].seen: 
                if fov[self.x][self.y]:
                    if dungeon.current_level.cells[self.x][self.y+1].solid or dungeon.current_level.cells[self.x+1][self.y].solid or dungeon.current_level.cells[self.x+1][self.y+1].solid :
                        self.sprite.set_alpha(128)
                    else:
                        self.sprite.set_alpha(255)
                    surface.blit(self.sprite,
                        (((self.x - self.y) * assets.tile_width//2)-x_offset,
                        ((self.x + self.y) * assets.tile_height//4)-y_offset))
                else:
                    if dungeon.current_level.cells[self.x][self.y+1].solid or dungeon.current_level.cells[self.x+1][self.y].solid or dungeon.current_level.cells[self.x+1][self.y+1].solid :
                        self.shadow_sprite.set_alpha(128)
                    else:
                        self.shadow_sprite.set_alpha(255)
                    surface.blit(self.shadow_sprite,
                        (((self.x - self.y) * assets.tile_width//2)-x_offset,
                        ((self.x + self.y) * assets.tile_height//4)-y_offset))
    
    def dynamic_render(self, surface):
        surface.blit(self.sprite,
            (((self.x - self.y) * assets.tile_width//2),
            ((self.x + self.y) * assets.tile_height//4)))

    def move(self, dungeon, x, y):
        if self.name == dungeon.player.name:
            if self.x +x >= dungeon.current_level.width or self.y +y >= dungeon.current_level.height:
                return 'no action'
            elif not dungeon.current_level.cells[self.x +x][self.y +y].solid:
                # potentially attack
                for creature in dungeon.current_level.creature_list:
                    if self.x + x == creature.x and self.y + y == creature.y:
                        return self.attack(creature, dungeon)
                # if this is reached player hasn't attacked
                self.x += x
                self.y += y
                return 'boring'
            elif dungeon.current_level.cells[self.x +x][self.y +y].door != 0:
                dungeon.current_level.cells[self.x +x][self.y +y].solid = False
                self.x += x
                self.y += y
                return 'opened door and moved.'
            else:
                return 'no action'
        else: # AI MOVEMENT
            if x == dungeon.player.x and y == dungeon.player.y:
                return self.attack(dungeon.player, dungeon)
            self.x = x
            self.y = y
            return 'boring'

    def attack(self, target, dungeon): # add modifiers for weapon and armor later
        attack_roll = random.randint(1, 20)
        if attack_roll == 1:
             ret_val = self.name + ' fumbled!'
        elif attack_roll == 20:
            ret_val = self.name + ' crit'
            # roll crit damage
            damage_roll = random.randint(1, self.wd)
            damage_bonus = 1
            while damage_roll % self.wd == 0: # exploding criticals
                ret_val += ' & exploded'
                damage_roll += random.randint(1, self.wd)
                damage_bonus += 1
            total_damage = 2 * (damage_roll + (self.bonus(self.str) * damage_bonus))
            target.current_hp -= total_damage
            ret_val += ' ' + target.name + ' for ' + str(total_damage)
            if target.current_hp <= 0:
                target.die(dungeon)
                ret_val += ' lethal'
            ret_val += (' damage.')
        else:
            attack = self.attack_mod + attack_roll
            if attack >= target.defense_mod:
                ret_val = self.name + ' hit'
                # roll damage
                damage_roll = random.randint(1, self.wd)
                damage_bonus = 1
                while damage_roll % self.wd == 0: # exploding criticals
                    ret_val += ' & exploded'
                    damage_roll += random.randint(1, self.wd)
                    damage_bonus += 1
                total_damage = damage_roll + (self.bonus(self.str) * damage_bonus)
                target.current_hp -= total_damage
                ret_val += ' ' + target.name + ' for ' + str(total_damage)
                if target.current_hp <= 0:
                    target.die(dungeon)
                    ret_val += ' lethal'
                ret_val += (' damage.')
            else:
                 ret_val = self.name + ' missed!'

        return ret_val
        

    def die(self, dungeon):
        import item
        if self in dungeon.current_level.creature_list:
            dungeon.current_level.creature_list.remove(self)
            corpse = item.Item(name='corpse',
            x=self.x,
            y=self.y,
            sprite=assets.corpse,
            shadow_sprite=assets.corpse_shade,
            quantity=1,
            action_set=['eat', 'throw'])
            dungeon.current_level.item_list.append(corpse)
            del self

    def run_ai(self, dungeon, fov):
        if self.ai == 'aggro':
            if fov[self.x][self.y]:

                start_x = self.x
                start_y = self.y
                target_x = dungeon.player.x
                target_y = dungeon.player.y

                cost = np.ndarray((dungeon.current_level.width, dungeon.current_level.height), dtype=np.int8)
                for i, j in itertools.product(range(dungeon.current_level.width), range(dungeon.current_level.height)):
                    if dungeon.current_level.cells[i][j].solid or dungeon.tile_has_creature(i, j):
                        cost[i][j] = 0
                    else:
                        cost[i][j] = 1

                pathfind = tcod.path.AStar(cost, diagonal=1)
                path = pathfind.get_path(start_x, start_y, target_x, target_y)

                if path:
                    path_x, path_y = path[0]
                    return self.move(dungeon, path_x, path_y)

        return 'boring'

            
    '''
    exp chart:  EXP     LEVEL
                +100    1
                +200    2
                +300    3 etc

    '''

    def is_on(self, entity): # true if overlapping, otherwise false
         #print('testing if ' + self.name + ' (' + str(self.x) + ', ' + str(self.y) + ') is on ' + entity.name + ' (' + str(entity.x) + ', ' + str(entity.y) + ')')
        return bool(self.x == entity.x and self.y == entity.y)

    def use_stairs(self): # specifically for nonplayer entities
        pass

    def pickup(self, dungeon):
        for i in dungeon.current_level.item_list:
            if self.x == i.x and self.y == i.y:
                dungeon.current_level.item_list.remove(i)
                self.inv.append(i)
                return 'picked up ' + i.name

        return 'no action'

    def drop(self, dungeon):
        if len(self.inv) > 0:
            dropped_item = self.inv.pop()
            dropped_item.x = self.x
            dropped_item.y = self.y
            dungeon.current_level.item_list.append(dropped_item)
            return 'dropped ' + dropped_item.name
        else:
            return 'no action'

    def get_info(self):
        ret_val = []
        ret_val.append((str(self.name) + ' the ' + str(self.race), (255, 255, 255)))
        ret_val.append(('Health: ' + str(self.current_hp) + '/' + str(self.max_hp), (255, 255, 255)))
        ret_val.append(('Hunger: ' + str(self.current_hunger) + '/' + str(self.max_hunger), (255, 255, 255)))

        ret_val.append(('STR: ' + str(self.str), (255, 255, 255)))
        ret_val.append(('DEX: ' + str(self.dex), (255, 255, 255)))
        ret_val.append(('VIT: ' + str(self.vit), (255, 255, 255)))     
        ret_val.append(('INT: ' + str(self.int), (255, 255, 255)))

        if self.mainhand is not None:
            ret_val.append(('mainhand: ' + self.mainhand.name, (255, 255, 255)))
        else:
            ret_val.append(('mainhand: fist', (255, 255, 255)))

        if self.offhand is not None:
            ret_val.append(('offhand: ' + self.offhand.name, (255, 255, 255)))
        else:
            ret_val.append(('offhand: fist', (255, 255, 255)))

        if self.helm is not None:
            ret_val.append(('helm: ' + self.helm.name, (255, 255, 255)))
        else:
            ret_val.append(('helm: empty', (255, 255, 255)))

        if self.armor is not None:
            ret_val.append(('armor: ' + self.armor.name, (255, 255, 255)))
        else:
            ret_val.append(('armor: empty', (255, 255, 255)))

        if self.boots is not None:
            ret_val.append(('boots: ' + self.boots.name, (255, 255, 255)))
        else:
            ret_val.append(('boots: empty', (255, 255, 255)))

        if self.ring1 is not None:
            ret_val.append(('L ring: ' + self.ring1.name, (255, 255, 255)))
        else:
            ret_val.append(('L ring: none', (255, 255, 255)))

        if self.ring2 is not None:
            ret_val.append(('R ring: ' + self.ring2.name, (255, 255, 255)))
        else:
            ret_val.append(('R ring: none', (255, 255, 255)))

        return ret_val