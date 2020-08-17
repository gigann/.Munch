"""
Issac Gann (gannmann) 2020

item module handles item creation and types such as weapons, armor, bananas, etc...
"""

import enum

import entity
import menus
import assets

class Quality(enum.Enum):
    MUNDANE, ENHANCED, CURSED = range(0, 3)


# effects is a list of functions the item is capable of e.g. throw, consume, etc
class Item(entity.Entity):
    def __init__(self, name, x, y, sprite, shadow_sprite,
                quantity, action_set, weapon_com = None, armor_com = None):
        self.name = name
        self.x = x
        self.y = y
        self.sprite = sprite
        self.shadow_sprite = shadow_sprite
        super(Item, self).__init__(
            name=self.name,
            x=self.x,
            y=self.y,
            sprite=self.sprite,
            shadow_sprite=self.shadow_sprite)
        self.quantity = quantity
        self.action_set = action_set
        
        # components. should probably change item's inheritance from entity to keep it consistent
        self.weapon_com = weapon_com
        self.armor_com = armor_com

    def add(self, num, ):
        # if item not in list, add item to list with quantity equal to the item's quantity
        # if item is already in list, increment item-in-list's quantity by the added item's quantity
        pass

    def sub(self, num):
        # if item not in list, do nothing
        # if item in list and decrementing item-in-list's quantity by num would be greater than or equal to 1, decrement item-in-list's quantity by num
        # if item in list and decrementing item-in-list's quantity by num would be less 1, remove item from list    
        pass


    def eat(self):
        name = self.name
        if 'eat' in self.action_set:
            # do eat stuff
            return 'ate ' + name
        else:
            return 'no action'

    def toss(self, target):
        name = self.name
        if 'toss' in self.action_set:
            # object gets tossed towards target
            return 'tossed ' + name
        else:
            return 'no action'


'''
class Armor(Item):
    def __init__(self, name, x, y, sprite, shadow_sprite, quantity=1, action_set=['don', 'doff'], armor_bonus=1, quality=Quality.MUNDANE):
        self.name = name
        self.x = x
        self.y = y
        self.sprite = sprite
        self.shadow_sprite = shadow_sprite
        self.quantity = quantity
        self.action_set = action_set
        super(Armor, self).__init__(
            name=self.name,
            x=self.x,
            y=self.y,
            sprite=self.sprite,
            shadow_sprite=self.shadow_sprite,
            quantity=quantity,
            action_set=action_set)
        self.armor_bonus= armor_bonus
        self.quality = quality

class Weapon(Item):
    def __init__(self, name, x, y, sprite, shadow_sprite,
    weapon_die,
    crit_range,
    crit_mult,
    kind,
    hands,
    skill,
    throwable=False,
    ammo=False,
    reach=False,
    slash=False,
    pierce=False,
    blunt=False,
    parry=False,
    riposte=False,
    feint=False,
    trip=False,
    disarm=False,
    quantity=1, action_set=['wield', 'sheathe']):
        self.name = name
        self.x = x
        self.y = y
        self.sprite = sprite
        self.shadow_sprite = shadow_sprite
        self.quantity = quantity
        self.action_set = action_set
        super(Weapon, self).__init__(
            name=self.name,
            x=self.x,
            y=self.y,
            sprite=self.sprite,
            shadow_sprite=self.shadow_sprite,
            quantity=quantity,
            action_set=action_set)
        self.weapon_die = weapon_die
        self.crit_range = crit_range
        self.crit_mult = crit_mult
        self.kind = kind
        self.hands = hands
        self.skill = skill
        self.throwable = throwable
        self.ammo = ammo
        self.reach = reach
        self.slash = slash
        self.pierce = pierce
        self.blunt = blunt
        self.parry = parry
        self.riposte = riposte
        self.feint = feint
        self.trip = trip
        self.disarm = disarm
        

battle_ax = Weapon('battle ax', 0, 0, assets.battle_ax, assets.battle_ax_shade,
weapon_die=8, crit_range=[20], crit_mult=3, kind='melee', hands=1, skill='ax',
slash=True)

tomahawk = Weapon('tomahawk', 0, 0, assets.tomahawk, assets.tomahawk_shade,
weapon_die=6, crit_range=[20], crit_mult=2, kind='melee', hands=1, skill='ax',
throwable=True, slash=True)

cleaver = Weapon('cleaver', 0, 0, assets.cleaver, assets.cleaver_shade,
weapon_die=4, crit_range=[19-20], crit_mult=2, kind='melee', hands=1, skill='ax',
throwable=True, slash=True)

halberd = Weapon('halberd', 0, 0, assets.halberd, assets.halberd_shade,
weapon_die=10, crit_range=[20], crit_mult=3, kind='melee', hands=2, skill='ax',
reach=True, slash=True, pierce=True, feint=True, trip=True)

pollaxe = Weapon('pollaxe', 0, 0, assets.pollaxe, assets.pollaxe_shade,
weapon_die=8, crit_range=[20], crit_mult=4, kind='melee', hands=2, skill='ax',
reach=True, slash=True, pierce=True, trip=True)
'''