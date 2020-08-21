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
                quantity, action_set, weapon_com = None, armor_com = None, selected = False,
                mainhand_sprite=None, mainhand_shadow_sprite=None,
                offhand_sprite=None, offhand_shadow_sprite=None):
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
        self.selected = selected

        self.mainhand_sprite = mainhand_sprite
        self.mainhand_shadow_sprite = mainhand_shadow_sprite
        self.offhand_sprite = offhand_sprite
        self.offhand_shadow_sprite = offhand_shadow_sprite

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
    

def banana():
    import weapon
    i = Item(name='banana',
            x=0, y=0,
            sprite=assets.banana_tile,
            shadow_sprite=assets.banana_tile_shade,
            quantity=1,
            action_set=['eat', 'throw'], weapon_com=weapon.banana)
    return i