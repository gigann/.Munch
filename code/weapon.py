'''
weapon component (for items)
base weapons
'''

import csv

import item

#with open('docs/weapon table.csv', newline='') as csvfile:
#    weapon_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#    for row in weapon_reader:
#        print(', '.join(row))

class Weapon(object):
    def __init__(self, ddie_count, ddie_size, cdie, cmult,
    melee=True, hands=1, skill='sword', throw=False, ammo=None, reach=False,
    slash=False, stab=False, strike=False, parry=False,
    riposte=False, feint=False, trip=False, disarm=False, enhance_list = None):
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
fist_com = Weapon(1, 3, 20, 3, skill='unarmed', strike=True, feint=True, trip=True, disarm=True)
fist = item.Item(name='fist', x=0, y=0, sprite=None, shadow_sprite=None, quantity=1, action_set=['wield', 'sheathe'], weapon_com=fist_com)

# corpses
small_corpse = Weapon(1, 2, 20, 4, skill='unarmed', throw=True)

# items
banana = Weapon(1, 2, 18, 2, skill='unarmed', throw=True, trip=True)

battleax = Weapon(1, 8, 20, 3, skill='axe', slash=True)
tomahawk = Weapon(1, 6, 20, 2, skill='axe', throw=True, slash=True)
cleaver = Weapon(1, 4, 19, 2, skill='axe', throw=True, slash=True)
halberd = Weapon(1, 10, 20, 3, hands=2, skill='axe', reach=True, slash=True, stab=True, feint=True, trip=True)
pollaxe = Weapon(1, 8, 20, 4, hands=2, skill='axe', reach=True, slash=True, stab=True, trip=True)
daneaxe = Weapon(1, 12, 20, 3, hands=2, skill='axe', slash=True)
warpick = Weapon(1, 6, 20, 4, skill='axe', stab=True)
claymore = Weapon(1, 12, 19, 2, hands=2, slash=True, stab=True, feint=True)
zweihander = Weapon(2, 6, 19, 2, hands=2, slash=True, stab=True, strike=True)
svardstav = Weapon(1, 10, 19, 2, hands=2, reach=True, slash=True, feint=True, trip=True)
sabre = Weapon(1, 8, 19, 2, stab=True, riposte=True, feint=True)
gladius = Weapon(1, 8, 20, 3, slash=True, stab=True, riposte=True, feint=True)
dirk = Weapon(1, 4, 19, 2, throw=True, slash=True, stab=True, riposte=True, feint=True)
rapier = Weapon(1, 6, 18, 2, stab=True, riposte=True, feint=True)
hooksword = Weapon(1, 6, 19, 2, slash=True, disarm=True)
katana = Weapon(2, 4, 18, 2, hands=2, slash=True, feint=True)
cutlass = Weapon(1, 8, 18, 2, slash=True)
javelin = Weapon(1, 8, 19, 2, skill='spear', throw=True, reach=True, stab=True)
trident = Weapon(1, 8, 20, 2, skill='spear', throw=True, reach=True, stab=True, disarm=True)
guisarme = Weapon(2, 4, 20, 3, hands=2, skill='spear', reach=True, stab=True, feint=True, trip=True, disarm=True)
glaive = Weapon(1, 10, 20, 3, hands=2, skill='spear', reach=True, slash=True, feint=True)
naginata = Weapon(2, 6, 20, 2, hands=2, reach=True, slash=True)
scythe = Weapon(2, 4, 20, 4, hands=2, skill='spear', slash=True, trip=True)
spear = Weapon(1, 10, 20, 2, skill='spear', throw=True, reach=True, stab=True)
pike = Weapon(1, 12, 20, 2, hands=2, skill='spear', reach=True, stab=True, feint=True)
partizan = Weapon(2, 4, 20, 3, hands=2, skill='spear', reach=True, slash=True, stab=True, feint=True)
shillelagh = Weapon(1, 8, 20, 3, skill='club', strike=True)
morningstar = Weapon(1, 10, 20, 3, skill='club', stab=True, strike=True)
nunchaku = Weapon(1, 4, 18, 20, skill='club', strike=True, feint=True, disarm=True)
mace = Weapon(1, 6, 20, 3, skill='club', strike=True)
kanabo = Weapon(2, 6, 19, 2, hands=2, skill='club', strike=True)
cudgel = Weapon(1, 12, 20, 3, hands=2, skill='club', strike=True)
flail = Weapon(2, 4, 20, 4, skill='club', reach=True, strike=True, trip=True, disarm=True)
warhammer = Weapon(1, 12, 20, 2, skill='club', throw=True, strike=True)
maul = Weapon(1, 10, 18, 20, 3, hands=2, skill='club', strike=True)
lucerne = Weapon(2, 4, 20, 3, hands=2, skill='club', reach=True, stab=True, strike=True, feint=True)
harpoon = Weapon(1, 6, 20, 2, melee=False, hands=2, skill='bow', ammo='none', stab=True)
recurve_bow = Weapon(1, 12, 19, 2, melee=False, hands=2, skill='bow', ammo='arrow', stab=True)
longbow = Weapon(1, 12, 20, 3, melee=False, hands=2, skill='bow', ammo='arrow', stab=True)
arbalest = Weapon(2, 6, 20, 3, melee=False, hands=2, skill='bow', ammo='bolt', stab=True)
crossbow = Weapon(2, 6, 19, 2, melee=False, hands=2, skill='bow', ammo='bolt', stab=True)
bola = Weapon(1, 4, 20, 2, melee=False, skill='throw', ammo='self', strike=True)
dart = Weapon(1, 4, 19, 3, melee=False, skill='throw', ammo='self', stab=True)
shuriken = Weapon(1, 4, 18, 2, melee=False, skill='throw', ammo='self', slash=True)
boomerang = Weapon(1, 4, 20, 2, melee=False, skill='throw', ammo='none', strike=True)
roundshield = Weapon(1, 12, 20, 2, melee=False, skill='shield', throw=True, parry=True)
kiteshield = Weapon(1, 12, 20, 3, melee=False, skill='shield', parry=True)
heatershield = Weapon(1, 8, 19, 2, melee=False, skill='shield', parry=True)
scutum = Weapon(2, 6, 20, 2, melee=False, skill='shield', parry=True)
buckler = Weapon(1, 6, 18, 3, melee=False, skill='shield', parry=True)

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