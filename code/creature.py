'''
creature templates
'''

import assets
import entity
import item
import weapon


# corpses


# creatures

def small_corpse():
    corpse = item.Item(name='small corpse', x=0, y=0,
                         sprite=assets.corpse, shadow_sprite=assets.corpse_shade,
                         quantity=1, action_set=['eat', 'throw'],
                         weapon_com=weapon.small_corpse)
    return corpse

def goblin():
    creature = entity.Entity(name='goblin', race='Goblin', x=0, y=0,
                       vitality=3, strength=2, dexterity=4, intelligence=4, hitdie=4, ai='aggro',
                       sprite=assets.goblin_tile, shadow_sprite=assets.goblin_tile_shade,
                       corpse=small_corpse())
    return creature