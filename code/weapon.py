'''
weapon component (for items)
base weapons
'''
import pygame
import random

import assets
import item

pygame.init()

#with open('docs/weapon table.csv', newline='') as csvfile:
#    weapon_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#    for row in weapon_reader:
#        print(', '.join(row))

class Weapon(object):
    def __init__(self, name, ddie_count, ddie_size, cdie, cmult,
    melee=True, hands=1, skill='sword', throw=False, ammo=None, reach=False,
    slash=False, stab=False, strike=False, parry=False,
    riposte=False, feint=False, trip=False, disarm=False, enhance_list = None):
        self.name = name
        self.ddie_count = ddie_count
        self.ddie_size = ddie_size
        self.cdie = cdie
        self.cmult = cmult
        self.melee = melee
        self.hands = hands
        self.skill = skill
        self.throw = throw
        self.ammo = ammo
        self.reach = reach
        self.slash = slash
        self.stab = stab
        self.strike = strike
        self.parry = parry
        self.riposte = riposte
        self.feint = feint
        self.trip = trip
        self.disarm = disarm

        if self.slash:
            self.bleed = True
            self.cleave = True
            self.amputate = True
        
        if self.stab:
            self.bleed = True
            self.pierce = True

        if self.strike:
            self.pierce = True
            self.daze = True
            self.holy = True

        self.enhance_list = enhance_list

# components
fist_com = Weapon('fist', 1, 3, 20, 3, skill='unarmed', strike=True, feint=True, trip=True, disarm=True)
fist = item.Item(name='fist', x=0, y=0, sprite=None, shadow_sprite=None, quantity=1, action_set=['wield', 'sheathe'], weapon_com=fist_com)

# corpses
small_corpse = Weapon('small corpse', 1, 2, 20, 4, skill='unarmed', throw=True)

# items
banana = Weapon('banana', 1, 2, 18, 2, skill='unarmed', throw=True, trip=True)

battleax = Weapon('battleax', 1, 8, 20, 3, skill='axe', slash=True)
tomahawk = Weapon('tomahawk', 1, 6, 20, 2, skill='axe', throw=True, slash=True)
cleaver = Weapon('cleaver', 1, 4, 19, 2, skill='axe', throw=True, slash=True)
halberd = Weapon('halberd', 1, 10, 20, 3, hands=2, skill='axe', reach=True, slash=True, stab=True, feint=True, trip=True)
pollaxe = Weapon('pollaxe', 1, 8, 20, 4, hands=2, skill='axe', reach=True, slash=True, stab=True, trip=True)
daneaxe = Weapon('daneaxe', 1, 12, 20, 3, hands=2, skill='axe', slash=True)
warpick = Weapon('warpick', 1, 6, 20, 4, skill='axe', stab=True)
claymore = Weapon('claymore', 1, 12, 19, 2, hands=2, slash=True, stab=True, feint=True)
zweihander = Weapon('zweihander', 2, 6, 19, 2, hands=2, slash=True, stab=True, strike=True)
svardstav = Weapon('svardstav', 1, 10, 19, 2, hands=2, reach=True, slash=True, feint=True, trip=True)
sabre = Weapon('sabre', 1, 8, 19, 2, stab=True, riposte=True, feint=True)
gladius = Weapon('gladius', 1, 8, 20, 3, slash=True, stab=True, riposte=True, feint=True)
dirk = Weapon('dirk', 1, 4, 19, 2, throw=True, slash=True, stab=True, riposte=True, feint=True)
rapier = Weapon('rapier', 1, 6, 18, 2, stab=True, riposte=True, feint=True)
hooksword = Weapon('hooksword', 1, 6, 19, 2, slash=True, disarm=True)
katana = Weapon('katana', 2, 4, 18, 2, hands=2, slash=True, feint=True)
cutlass = Weapon('cutlass', 1, 8, 18, 2, slash=True)
javelin = Weapon('javelin', 1, 8, 19, 2, skill='spear', throw=True, reach=True, stab=True)
trident = Weapon('trident', 1, 8, 20, 2, skill='spear', throw=True, reach=True, stab=True, disarm=True)
guisarme = Weapon('guisarme', 2, 4, 20, 3, hands=2, skill='spear', reach=True, stab=True, feint=True, trip=True, disarm=True)
glaive = Weapon('glaive', 1, 10, 20, 3, hands=2, skill='spear', reach=True, slash=True, feint=True)
naginata = Weapon('naginata', 2, 6, 20, 2, hands=2, reach=True, slash=True)
scythe = Weapon('scythe', 2, 4, 20, 4, hands=2, skill='spear', slash=True, trip=True)
spear = Weapon('spear', 1, 10, 20, 2, skill='spear', throw=True, reach=True, stab=True)
pike = Weapon('pike', 1, 12, 20, 2, hands=2, skill='spear', reach=True, stab=True, feint=True)
partizan = Weapon('partizan', 2, 4, 20, 3, hands=2, skill='spear', reach=True, slash=True, stab=True, feint=True)
shillelagh = Weapon('shillelagh', 1, 8, 20, 3, skill='club', strike=True)
morningstar = Weapon('morningstar', 1, 10, 20, 3, skill='club', stab=True, strike=True)
nunchaku = Weapon('nunchaku', 1, 4, 18, 20, skill='club', strike=True, feint=True, disarm=True)
mace = Weapon('mace', 1, 6, 20, 3, skill='club', strike=True)
kanabo = Weapon('kanabo', 2, 6, 19, 2, hands=2, skill='club', strike=True)
cudgel = Weapon('cudgel', 1, 12, 20, 3, hands=2, skill='club', strike=True)
flail = Weapon('flail', 2, 4, 20, 4, skill='club', reach=True, strike=True, trip=True, disarm=True)
warhammer = Weapon('warhammer', 1, 12, 20, 2, skill='club', throw=True, strike=True)
maul = Weapon('maul', 1, 10, 18, 20, 3, hands=2, skill='club', strike=True)
lucerne = Weapon('lucerne', 2, 4, 20, 3, hands=2, skill='club', reach=True, stab=True, strike=True, feint=True)
harpoon = Weapon('harpoon', 1, 6, 20, 2, melee=False, hands=2, skill='bow', ammo='none', stab=True)
recurve_bow = Weapon('recurve_bow', 1, 12, 19, 2, melee=False, hands=2, skill='bow', ammo='arrow', stab=True)
longbow = Weapon('longbow', 1, 12, 20, 3, melee=False, hands=2, skill='bow', ammo='arrow', stab=True)
arbalest = Weapon('arbalest', 2, 6, 20, 3, melee=False, hands=2, skill='bow', ammo='bolt', stab=True)
crossbow = Weapon('crossbow', 2, 6, 19, 2, melee=False, hands=2, skill='bow', ammo='bolt', stab=True)
bola = Weapon('bola', 1, 4, 20, 2, melee=False, skill='throw', ammo='self', strike=True)
dart = Weapon('dart', 1, 4, 19, 3, melee=False, skill='throw', ammo='self', stab=True)
shuriken = Weapon('shuriken', 1, 4, 18, 2, melee=False, skill='throw', ammo='self', slash=True)
boomerang = Weapon('boomerang', 1, 4, 20, 2, melee=False, skill='throw', ammo='none', strike=True)
roundshield = Weapon('roundshield', 1, 12, 20, 2, melee=False, skill='shield', throw=True, parry=True)
kiteshield = Weapon('kiteshield', 1, 12, 20, 3, melee=False, skill='shield', parry=True)
heatershield = Weapon('heatershield', 1, 8, 19, 2, melee=False, skill='shield', parry=True)
scutum = Weapon('scutum', 2, 6, 20, 2, melee=False, skill='shield', parry=True)
buckler = Weapon('buckler', 1, 6, 18, 3, melee=False, skill='shield', parry=True)

# enhancements
'''
flaming - sets target on fire
freezing - cools target
slimy - covers target in acid
moist - douses target in water
oily - douses target in oil
spiky - deals 1d4 thrust to attackers
volcanic - douses target in lava

chaotic - max rolls on damage are rerolled and added to total damage
lucky - crit range becomes 10-20
vorpal - crit multiplier becomes 6
refined - skill influences double
large - ddie count becomes 4
heavy - ddie size becomes 20

'''

# weapon creators

def gen(com, x, y):
    sprite, shadow_sprite = assets.from_file('tiles/weapons/' + com.name + '.png')
    mainhand_sprite, mainhand_shadow_sprite = assets.from_file('tiles/weapons/' + com.name + '_mainhand.png')
    offhand_sprite = pygame.transform.flip(mainhand_sprite, True, False)
    offhand_shadow_sprite = pygame.transform.flip(mainhand_shadow_sprite, True, False)
    new_weapon = item.Item(name=com.name.replace('_', ' '), x=x, y=y,
    sprite=sprite, shadow_sprite=shadow_sprite, quantity=1, action_set=['wield', 'sheathe'],
    weapon_com=com, mainhand_sprite=mainhand_sprite, mainhand_shadow_sprite=mainhand_shadow_sprite,
    offhand_sprite=offhand_sprite, offhand_shadow_sprite=offhand_shadow_sprite)
    return new_weapon

def small_weapon(x, y):
    return gen(random.choice([tomahawk, javelin, dirk, gladius, mace]), x, y)

def good_weapon(x, y):
    return gen(random.choice([halberd, pollaxe, spear, pike, partizan, cudgel, flail, morningstar, lucerne]), x, y)