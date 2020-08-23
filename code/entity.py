"""
Issac Gann (gannmann) 2020

entity module handles entity related objects and methods
"""
import pygame
pygame.init()

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
    ai='simple', sprite=None, shadow_sprite=None, inv=None, corpse=None, helm=None,
    armor=None, boots=None, mainhand=None, offhand=None, ring1=None, ring2=None,
    sword_skill=0, axe_skill=0, spear_skill=0, club_skill=0, unarmed_skill = 0,
    bow_skill=0, throw_skill=0, defense_skill = 0, total_armor = 0):
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
        self.corpse = corpse
        self.inv = inv

        self.bananas = 0

        self.helm = helm # armor and weapon slots are single item inventories. when equipped, items are moved from inventory to this slot and vice versa.
        self.armor = armor
        self.boots = boots
        self.mainhand = mainhand
        self.offhand = offhand
        self.ring1 = ring1
        self.ring2 = ring2

        self.sword_skill = sword_skill
        self.axe_skill = axe_skill
        self.spear_skill = spear_skill
        self.club_skill = club_skill
        self.unarmed_skill = unarmed_skill
        self.bow_skill = bow_skill
        self.throw_skill = throw_skill
        self.defense_skill = defense_skill

        # determined attributes
        self.level = (math.floor(math.log2(self.exp))+1)

        #self.max_hp = (self.bonus(self.vit) + self.hd) * self.level
        self.max_hp = (self.vit + self.hd) * self.level
        self.current_hp = (self.vit + self.hd) * self.level

        self.max_hunger = self.mod(self.met) + self.hd
        #self.current_hp = (self.bonus(self.vit) + self.hd) * self.level
        self.current_hunger = self.max_hunger // 2

        self.attack_mod = self.mod(self.str)
        self.defense_mod = self.mod(self.dex) + 10

        #self.max_ingredients_known = (math.floor((self.int-10)//2)) * self.level
        self.total_armor = total_armor

    def determined_attributes(self):
        self.level = math.floor(math.log2(self.exp))+1
        self.max_hp = (self.vit + self.hd) * self.level
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
    
    #def dynamic_render(self, surface):
    #    surface.blit(self.sprite,
    #        (((self.x - self.y) * assets.tile_width//2),
    #        ((self.x + self.y) * assets.tile_height//4)))

    def move(self, dungeon, x, y, console):
        if self.name == dungeon.player.name:
            if self.x +x >= dungeon.current_level.width or self.y +y >= dungeon.current_level.height:
                return False
            elif not dungeon.current_level.cells[self.x +x][self.y +y].solid:
                # potentially attack
                for creature in dungeon.current_level.creature_list:
                    if self.x + x == creature.x and self.y + y == creature.y:
                        #return self.attack(creature, dungeon)
                        self.weapon_attack(creature, dungeon, console)
                        return True
                # if this is reached player hasn't attacked
                self.x += x
                self.y += y
                return True
            elif dungeon.current_level.cells[self.x +x][self.y +y].door != 0:
                dungeon.current_level.cells[self.x +x][self.y +y].solid = False
                self.x += x
                self.y += y
                #console.out('opened door and moved.')
                return True
            else:
                return False
        else: # AI MOVEMENT
            if x == dungeon.player.x and y == dungeon.player.y:
                #return self.attack(dungeon.player, dungeon)
                self.weapon_attack(dungeon.player, dungeon, console)
                return True
            self.x = x
            self.y = y
            return True

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
        
    def weapon_attack(self, target, dungeon, console, bonus=1): # will replace default attack eventually
        damage_roll = 0

        console_msg = self.name

        #from weapon import fist
        #if self.mainhand == None:
        #    self.mainhand = fist
        #if self.offhand == None:
        #    self.offhand = fist
        #if target.mainhand == None:
        #    target.mainhand = fist
        #if target.offhand == None:
        #    target.offhand = fist

        attack_roll = self.get_attack_roll()

        if attack_roll >= random.randint(1, target.dex + target.defense_skill):
            for dice in range(self.mainhand.weapon_com.ddie_count):
                damage_roll += random.randint(1, self.mainhand.weapon_com.ddie_size)

            # critical  
            if random.randint(1, self.mainhand.weapon_com.cdie) == self.mainhand.weapon_com.cdie:
                damage_roll *= self.mainhand.weapon_com.cmult
                console_msg += (' crit ' + target.name)
            else: # normal hit
                console_msg += (' hit ' + target.name)
            # add STR
            damage_roll += self.str

            # add bonus (from throwing etc)
            damage_roll *= bonus

            # weapon abilities here
            damage_roll -= target.total_armor

            # target has shield
            if target.offhand.weapon_com.parry:
                if target.attack_roll(hand='offhand') >= attack_roll:
                    for dice in target.offhand.weapon_com.ddie_count:
                        shield_roll += random.randint(1, target.offhand.weapon_com.ddie_size)
                    shield_roll += target.str
                    if damage_roll - shield_roll < 0:
                        damage_roll = 0
                        console_msg += (' (' + target.name + ' blocked)')
                    else:
                        damage_roll -= shield_roll
                        console_msg += (' (' + target.name + ' parried ' + shield_roll + ')')
        else: # miss
            damage_roll = 0
            console_msg += (' missed ' + target.name)
            if target.mainhand.weapon_com.riposte:
                console.out(console_msg)
                console.out(target.name + ' ripostes ' + self.name + '!')
                target.weapon_attack(self, dungeon, console, bonus=0.5)

        # subtract from health
        if damage_roll > 0:
            target.current_hp -= damage_roll
            console_msg += (' for ' + str(damage_roll) + ' damage.')
            console.out(console_msg)

        if target.current_hp <= 0:
            target.die(dungeon)
            console.out(target.name + ' is slain!')


    def get_attack_roll(self, hand='mainhand'):
        if hand=='mainhand':
            if self.mainhand != None:
                if self.mainhand.weapon_com.skill == 'sword':
                    attack_roll = random.randint(1, self.dex + self.sword_skill)
                elif self.mainhand.weapon_com.skill == 'axe':
                    attack_roll = random.randint(1, self.dex + self.axe_skill)
                elif self.mainhand.weapon_com.skill == 'spear':
                    attack_roll = random.randint(1, self.dex + self.spear_skill)
                elif self.mainhand.weapon_com.skill == 'club':
                    attack_roll = random.randint(1, self.dex + self.club_skill)
                elif self.mainhand.weapon_com.skill == 'bow':
                    attack_roll = random.randint(1, self.dex + self.bow_skill)
                elif self.mainhand.weapon_com.skill == 'throw':
                    attack_roll = random.randint(1, self.dex + self.throw_skill)
                elif self.mainhand.weapon_com.skill == 'unarmed':
                    attack_roll = random.randint(1, self.dex + self.unarmed_skill)                           
        else:
            if self.offhand != None:
                if self.offhand.weapon_com.skill == 'sword':
                    attack_roll = random.randint(1, self.dex + self.sword_skill)
                elif self.offhand.weapon_com.skill == 'axe':
                    attack_roll = random.randint(1, self.dex + self.axe_skill)
                elif self.offhand.weapon_com.skill == 'spear':
                    attack_roll = random.randint(1, self.dex + self.spear_skill)
                elif self.offhand.weapon_com.skill == 'club':
                    attack_roll = random.randint(1, self.dex + self.club_skill)
                elif self.offhand.weapon_com.skill == 'bow':
                    attack_roll = random.randint(1, self.dex + self.bow_skill)
                elif self.offhand.weapon_com.skill == 'throw':
                    attack_roll = random.randint(1, self.dex + self.throw_skill)                                
                elif self.offhand.weapon_com.skill == 'unarmed':
                    attack_roll = random.randint(1, self.dex + self.unarmed_skill)  

        return attack_roll

    def die(self, dungeon):
        import item
        import weapon

        if self in dungeon.current_level.creature_list:
            dungeon.current_level.creature_list.remove(self)
            dungeon.current_level.item_list.append(self.corpse)
            self.corpse.x = self.x
            self.corpse.y = self.y

            if self.mainhand != weapon.fist:
                dungeon.current_level.item_list.append(self.mainhand)
                self.mainhand.x = self.x
                self.mainhand.y = self.y

        del self

    def run_ai(self, dungeon, fov, console):
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
                    self.move(dungeon, path_x, path_y, console)

            
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

    def pickup(self, dungeon, console):
        for i in dungeon.current_level.item_list:
            if self.x == i.x and self.y == i.y:
                dungeon.current_level.item_list.remove(i)
                self.inv.append(i)

                # automatically select it
                #for x in self.inv:
                #    x.selected = False
                #i.selected = True

                if len(self.inv) == 1: # first item
                    self.inv[0].selected = True

                console.out('picked up ' + i.name)
                return True

        return False

    def drop(self, dungeon, console):
        for i in self.inv:
            if i.selected:
                i.selected = False
                i.x = self.x
                i.y = self.y
                dungeon.current_level.item_list.append(i)
                self.inv.remove(i)

                if len(self.inv) > 0:
                    self.inv[0].selected = True
                
                console.out('dropped ' + i.name)
                return True

        return False

    def fling(self, dungeon, target, console):
        start_x = self.x
        start_y = self.y
        target_x = target[0]
        target_y = target[1]

        cost = np.ndarray((dungeon.current_level.width, dungeon.current_level.height), dtype=np.int8)
        for i, j in itertools.product(range(dungeon.current_level.width), range(dungeon.current_level.height)):
            if dungeon.current_level.cells[i][j].solid:
                cost[i][j] = 0
            else:
                cost[i][j] = 1

        pathfind = tcod.path.AStar(cost, diagonal=1)
        path = pathfind.get_path(start_x, start_y, target_x, target_y)

        if path: 
            for i in self.inv:
                if i.selected:
                    i.selected = False
                    i.x = target_x
                    i.y = target_y
                    dungeon.current_level.item_list.append(i)
                    self.inv.remove(i)

                    if len(self.inv) > 0:
                        self.inv[0].selected = True

                    target_creature = dungeon.entity_at_tile(dungeon.current_level.creature_list, target_x, target_y)
                    if target_creature != None and i.weapon_com != None:
                        if i.weapon_com.throw:
                            self.weapon_attack(target_creature, dungeon, console, bonus=1)
                            return True
                        else:
                            self.weapon_attack(target_creature, dungeon, console, bonus=0.25)
                            return True
                    else:
                        console.out('flung ' + i.name)
                        return True

        else:
            return False





        return 'no action'

        '''
        if len(self.inv) > 0:
            dropped_item = self.inv.pop()
            dropped_item.x = self.x
            dropped_item.y = self.y
            dungeon.current_level.item_list.append(dropped_item)
            return 'dropped ' + dropped_item.name
        else:
            return 'no action'
        '''
    def get_info(self):
        ret_val = []
        #ret_val.append((str(self.name) + ' the ' + str(self.race), (255, 255, 255)))
        ret_val.append(('LVL: ' + str(self.level), (255, 255, 255)))
        ret_val.append(('HP: ' + str(self.current_hp) + '/' + str(self.max_hp), (255, 0, 0)))
        ret_val.append(('Hunger: ' + str(self.current_hunger) + '/' + str(self.max_hunger), (255, 128, 0)))
        ret_val.append(('Bananas: ' + str(self.bananas), (255, 255, 0)))

        ret_val.append(('STR: ' + str(self.str), (255, 255, 255)))
        ret_val.append(('DEX: ' + str(self.dex), (255, 255, 255)))
        ret_val.append(('VIT: ' + str(self.vit), (255, 255, 255)))     
        ret_val.append(('INT: ' + str(self.int), (255, 255, 255)))

        
        if self.mainhand is not None:
            ret_val.append(('mainhand: ' + self.mainhand.name, (255, 255, 255)))
        else:
            ret_val.append(('mainhand: none', (255, 255, 255))) # this should never show because fists should be equipped


        if self.offhand is not None:
            ret_val.append(('offhand: ' + self.offhand.name, (255, 255, 255)))
        else:
            ret_val.append(('offhand: none', (255, 255, 255))) # this should never show because fists should be equipped

        '''
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
        '''
        return ret_val
        
    def don(self, dungeon): # for donning armor
        pass

    def doff(self, dungeon): # for donning armor
        pass

    def wield(self, dungeon, console):
        # If weapon is one handed
        #     If mainhand slot is empty, equip the weapon there  
        #     Elif offhand slot is empty, equip the weapon there
        #     Else slot full
        # Else weapon is two handed
        # If mainhand and offhand slots are empty, euqip the weapon there
        # Else slot full
        from weapon import fist

        for i in self.inv:
            if i.selected and i.weapon_com: # selected and a weapon
                if i.weapon_com.hands == 1: # one handed
                    if self.mainhand == fist: # main hand is empty
                        i.selected = False
                        self.mainhand = i
                        self.inv.remove(i)
                        if len(self.inv) > 0:
                            self.inv[0].selected = True
                        console.out('wielded ' + i.name + ' in main hand.')
                        return True
                    elif self.offhand == fist:
                        i.selected = False
                        self.offhand = i
                        self.inv.remove(i)
                        if len(self.inv) > 0:
                            self.inv[0].selected = True
                        console.out('wielded ' + i.name + ' in off hand.')
                        return True
                    else:
                        return False
        '''
        if self.mainhand == fist:
            for i in self.inv:
                if i.selected:
                    i.selected = False
                    self.mainhand = i
                    self.inv.remove(i)

                    if len(self.inv) > 0:
                        self.inv[0].selected = True

                    return 'wielded ' + i.name
        return 'no action'
        '''
    def sheathe(self, dungeon, console):
        # if weapon in offhand, sheathe it
        # if weapon in mainhand, sheathe it
        from weapon import fist
        
        if self.offhand != fist:
            self.inv.append(self.offhand)
            self.offhand = fist

        elif self.mainhand != fist:
            self.inv.append(self.mainhand)
            self.mainhand = fist

        else:
            return 'no action'
        
        if len(self.inv) == 1: # select if only item left
            self.inv[0].selected = True

            return 'sheathed weapons'

        '''
        sheathed_name = self.mainhand.name
        from weapon import fist

        if self.mainhand != fist:
            self.inv.append(self.mainhand)
            self.mainhand = fist
            return 'sheathed ' + sheathed_name
        
        return 'no action'
        '''
        

    def select(self, direction, text, text_surface, surface, window_width, window_height):
        selected_index = 0 # default to the first item
        
        if len(self.inv) > 0:
            # get index of currently selected item
            for i in self.inv:
                if i.selected:
                    selected_index = self.inv.index(i)

                    # deselect it
                    i.selected = False

            # select either the one above or the one below, if possible
            
            if direction == 'up':# and selected_index > 0:
                self.inv[selected_index - 1].selected = True
                #print('selected up')
            elif selected_index == len(self.inv) - 1:
                self.inv[0].selected = True
            elif direction == 'down':
                self.inv[selected_index + 1].selected = True
                #print('selected down')

        
            text.out()
            surface.blit(text_surface, (window_width - window_width//5, window_height//2))
            pygame.display.update()