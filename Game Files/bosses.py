#   This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Peasants' Ascension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import sys
import copy
import json
import random

import npcs
import monsters
import battle
import items as i_items
import inv_system
import sounds

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#     spam = random.choice('0123456789ynxpsewrt')
#     print(string, spam)
#     return spam
#
# input = test_input

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Boss(monsters.Monster):
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad,
                 lvl, pos_x, pos_y, items, gold, experience,
                 active=True, element='none', multiphase=0, currphase=1):
        monsters.Monster.__init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk,
                                  m_dfns, spd, evad, lvl, element)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.items = items
        self.gold = gold
        self.experience = experience
        self.active = active
        self.max_stats()
        self.monster_name = copy.copy(self.name)
        self.hp = hp
        self.mp = mp
        self.multiphase = multiphase
        self.currphase = currphase
        self.max_hp = copy.copy(self.hp)
        self.max_mp = copy.copy(self.mp)
        self.is_poisoned = False
        self.dodge = 0

    def max_stats(self):
        self.hp = copy.copy(self.max_hp)
        self.mp = copy.copy(self.max_mp)

    def new_location(self, add=True):  # Translate the location of the boss
        if self.pos_y >= 0:  # into a string, then add to inventory.
            foo = "\u00b0N"
        else:
            foo = "\u00b0S"

        if self.pos_x >= 0:
            bar = "\u00b0E"
        else:
            bar = "\u00b0W"

        spam = ''.join([self.name, "'s lair: ", str(self.pos_y), foo, ', ', str(self.pos_x), bar])
        if add:
            if spam not in inv_system.inventory['coord']:
                inv_system.inventory['coord'].append(spam)
                print('-'*25)
                print("You quickly mark down the location of {0}'s lair.".format(self.name))

        else:
            return spam


def check_bosses(x, y):
    for boss in boss_list:
        if [boss.pos_x, boss.pos_y] == [x, y] and boss.name not in defeated_bosses and boss.active:
            print('-'*25)

            sounds.item_pickup.play()

            if boss.new_location(add=False) not in inv_system.inventory['coord']:
                print('You feel the presence of an unknown entity...')

            else:
                print('You come across the lair of the {0}.'.format(boss.name))

            while True:

                if boss.new_location(add=False) not in inv_system.inventory['coord']:
                    y_n = input('Do you wish to investigate? | Yes or No: ')

                else:
                    y_n = input('Do you wish to confront the {0}? | Yes or No: '.format(boss.name))

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    monsters.monster = boss
                    monsters.setup_vars()
                    battle.setup_vars()
                    boss.max_stats()
                    boss.new_location()

                    print('-'*25)

                    battle.battle_system(is_boss=True)

                    return True

                elif y_n.startswith('n'):
                    return True

                else:
                    continue
    else:
        return False


def serialize_bosses(path):
    json_bosslist = {}

    for boss in boss_list:
        json_bosslist[boss.name] = boss.active

    with open(path, encoding='utf-8', mode='w') as i:
        json.dump(json_bosslist, i)


def deserialize_bosses(path):
    global boss_list

    with open(path, encoding='utf-8') as i:
        json_bosslist = json.load(i)

    for key in json_bosslist:
        for boss in boss_list:
            if key == boss.name:
                boss.active = json_bosslist[key]


def unimportant_boss_ud():
    pass


# Boss: Master Slime -- Position: 0'N, 1'E
master_slime = Boss('Master Slime',
                    35, 5,   # 35 HP and 5 MP
                    12, 5,   # 12 Attack, 5 Defense
                    6, 5,    # 6 Pierce Attack, 5 Pierce Defense
                    8, 0,    # 8 Magic Attack, 0 Magic Defense
                    6, 6,    # 6 Speed, 6 Evasion
                    3,       # Level 3
                    1, 0,    # Located at 0'N, 1'W
                    None,    # Drops no items
                    25, 25,  # Drops 25 XP and 25 GP
                    active=False)
master_slime.battle_turn = monsters.melee_ai


def mastslim_ud():
    # Stands for "Master Slime -- Upon Defeating"
    npcs.alfred_quest_1.finished = True
    npcs.alfred_phrase_2.active = False


master_slime.upon_defeating = mastslim_ud

# Boss: Whispering Goblin -- Position: 4'N, -2'W  (This is for you, Jacob!)
whisp_goblin = Boss('Whispering Goblin',
                    50, 10,  # 50 HP and 10 MP
                    20, 20,  # 20 Attack, 20 Defense
                    12, 15,  # 12 Pierce Attack, 15 Pierce Defense
                    8, 12,   # 8 Magic Attack, 12 Magic Defense
                    15, 7,   # 15 Speed, 7 Evasion
                    5,       # Level 5
                    -2, 4,   # Located at 4'N, -2'W
                    None,    # Drops no items
                    45, 45)  # Drops 45 XP and 45 GP
whisp_goblin.battle_turn = monsters.melee_ai

whisp_goblin.upon_defeating = unimportant_boss_ud

# Boss: Menacing Phantom -- Position: 8'N, -12'W
menac_phantom = Boss('Menacing Phantom',
                     75, 50,  # 75 HP and 50 MP
                     10, 20,  # 10 Attack, 20 Defense
                     5, 20,   # 5 Pierce Attack, 20 Pierce Defense
                     35, 25,  # 35 Magic Attack, 25 Magic Defense
                     20, 15,  # 20 Speed, 15 Evasion
                     8,       # Level 8
                     -12, 8,  # Located at 8'N, -12'W
                     None,    # Drops no items
                     75, 75,  # Drops 75 XP and 75 GP
                     active=False, element='death')
menac_phantom.battle_turn = monsters.magic_ai


def menacphan_ud():
    # Stands for "Menacing Phantom -- Upon Defeating"
    npcs.stewson_quest_1.finished = True
    npcs.stewson_phrase_2.active = False


menac_phantom.upon_defeating = menacphan_ud

# Boss: Terrible Tarantuloid -- Position: -23'S, -11'W  (Adventure in Pixels)
terr_tarant = Boss('Terrible Tarantuloid',
                   100, 25,   # 100 Health, 25 Mana
                   45, 30,    # 45 Attack, 30 Defense
                   25, 15,    # 25 Pierce Attack, 15 Pierce Defense
                   15, 25,     # 15 Magic Attack, 25 Magic Defense
                   35, 25,    # 35 Speed, 25 Evasion
                   12,        # Level 12
                   -11, -23,  # Located at -23'S, -11'W
                   None,      # Drops no items
                   150, 150)  # Drops 150 XP and 150 GP
terr_tarant.battle_turn = monsters.melee_ai


def terrtar_ud():
    npcs.krystal_phrase_2.active = False
    npcs.krystal_phrase_3.active = True
    npcs.kyle_phrase_2.active = False
    npcs.kyle_phrase_3.active = True
    npcs.alden_phrase_1.active = False
    npcs.alden_phrase_2.active = True


terr_tarant.upon_defeating = terrtar_ud

# Boss: Cursed Spectre -- Position 22'N, 3'E
cursed_spect = Boss('Cursed Spectre',
                    125, 75,             # 125 Health, 75 Mana
                    15, 30,              # 15 Attack, 30 Defense
                    20, 25,              # 20 Pierce Attack, 25 Pierce Defense
                    50, 35,              # 50 Magic Attack, 35 Magic Defense
                    25, 20,              # 25 Speed, 20 Evasion
                    15,                  # Level 15
                    3, 22,               # Located at 22'N, 3'E
                    i_items.spect_wand,  # Drops a spectre wand
                    250, 250,            # Drops 250 XP and 250 GP
                    element='death', active=False)
cursed_spect.battle_turn = monsters.magic_ai


def cursspect_ud():
    npcs.rivesh_phrase_3.active = False
    npcs.rivesh_quest_1.finished = True


cursed_spect.upon_defeating = cursspect_ud

# Boss: Ent -- Position: 27'N, 15'E
giant_ent = Boss('Giant Ent',
                 125, 35,         # 125 Health, 75 Mana
                 35, 50,          # 35 Attack, 50 Defense
                 15, 50,          # 15 Pierce Attack, 50 Pierce Defense
                 20, 15,          # 20 Magic Attack, 15 Magic Defense
                 15, 5,           # 15 Speed, 5 Evasion
                 15,              # Level 15
                 15, 27,          # Located at 27'N, 15'E
                 i_items.enc_yw,  # Drops an enchanted yew wand
                 250, 250,        # Drops 250 XP and 250 GP
                 element='grass', active=True)
giant_ent.battle_turn = monsters.melee_ai

giant_ent.upon_defeating = unimportant_boss_ud

# Boss: Anti-blood Squad -- Position: -68'S, -93'W
anti_blood_squad = Boss('Hunter Lackey #1',
                        75, 20,
                        30, 35,
                        55, 50,
                        25, 25,
                        40, 45,
                        15,
                        -93, -68,
                        None,
                        200, 200,
                        active=False,
                        multiphase=3)


def antibloodsquad_et(is_boss):
    if monsters.monster.name == "Hunter Lackey #1" and monsters.monster.hp <= 0:
        monsters.monster.currphase += 1
        print('The first lackey falls dead, and the second one takes her place!')

        monsters.monster.name = "Hunter Lackey #2"
        monsters.monster.monster_name = "Hunter Lackey #2"
        monsters.monster.hp = 75
        monsters.monster.mp = 20
        self.is_poisoned = False

        return

    elif monsters.monster.name == "Hunter Lackey #2" and monsters.monster.hp <= 0:
        monsters.monster.currphase += 1
        print('Seeing that his guards have fallen, Typhen is forced to defend himself!')

        monsters.monster.name = "Typhen the Vampire Hunter"
        monsters.monster.monster_name = "Typhen the Vampire Hunter"

        monsters.monster.hp = 200
        monsters.monster.max_hp = 200

        monsters.monster.mp = 50
        monsters.monster.max_mp = 50

        monsters.monster.attk += 15
        monsters.monster.dfns += 15
        monsters.monster.p_attk += 20
        monsters.monster.p_dfns += 15
        monsters.monster.m_attk -= 5
        monsters.monster.m_dfns -= 10
        monsters.monster.spd += 10
        monsters.monster.evad += 5

        monsters.monster.level = 25
        monsters.monster.experience = 1000
        monsters.monster.gold = 1000

        monsters.monster.items = i_items.wind_bow
        self.is_poisoned = False

        return

    elif monsters.monster.hp <= 0:
        return

    monsters.ranged_ai(is_boss)

anti_blood_squad.battle_turn = antibloodsquad_et


def absquad_ud():
    npcs.pime_phrase_3.active = False
    npcs.pime_quest_1.finished = True

anti_blood_squad.upon_defeating = absquad_ud


# theonimbus = Boss('Theonimbus',

boss_list = [whisp_goblin, master_slime, menac_phantom, terr_tarant, cursed_spect, giant_ent,
             anti_blood_squad]

defeated_bosses = []  # Make sure you can only defeat the boss one time
