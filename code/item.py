import enum

import entity
import menus
import assets

class Quality(enum.Enum):
    MUNDANE, ENHANCED, CURSED = range(0, 3)


# effects is a list of functions the item is capable of e.g. throw, consume, etc
class Item(entity.Entity):
    def __init__(self, name, x, y, sprite, shadow_sprite,
                quantity, action_set):
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
    abilities,
    quantity=1, action_set=['wield', 'sheathe'],
    weapon_die=6, quality=Quality.MUNDANE):
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
        self.abilities = abilities

        self.weapon_die = weapon_die
        self.quality = quality

#hafted_axe = Weapon('hafted axe', 0, 0, assets.hafted_axe, assets.hafted_axe_shade,
#['melee', 'slashing'])