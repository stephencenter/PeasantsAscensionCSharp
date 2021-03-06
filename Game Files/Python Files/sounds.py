# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peasants' Ascension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import sys
import copy

from pygame import mixer
from pygame.mixer import Sound

import save_load


if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

# noinspection PyArgumentList
mixer.pre_init(frequency=44100, buffer=1024)
mixer.init()

# Sword Slash -- Played when you attempt to physically attack an enemy
sword_slash = Sound('../Sound FX/sword_slash.wav')

# Magical Attack -- Played when you attempt to use a magical attack
magic_attack = Sound('../Sound FX/magic_attack.wav')

# Magic Healing -- Played when you attempt to use a magical healing spell
magic_healing = Sound('../Sound FX/magic_healing.wav')

# Enemy-hit -- Played when the enemy is hit by a player attack
enemy_hit = Sound('../Sound FX/enemy_hit.wav')

# Foot-steps -- Played when you move on the overworld
foot_steps = Sound('../Sound FX/foot_steps.wav')

# Aim Weapon -- Played when attempting to attack with a ranged weapon
aim_weapon = Sound('../Sound FX/aim_weapon.wav')

# Attack Miss -- Played when attempting to attack and then failing
attack_miss = Sound('../Sound FX/attack_miss.wav')

# Got Item -- Played when you receive an item, GP, or XP
item_pickup = Sound('../Sound FX/item_pickup.wav')

# Low Health -- Played when you have low (less than 20%) health remaining
health_low = Sound('../Sound FX/health_low.wav')

# Poison Damage -- Played when the player or enemy take poison damage
poison_damage = Sound('../Sound FX/poison_damage.wav')

# Use Buff Spell -- Played when the player or enemy use a buff spell
buff_spell = Sound('../Sound FX/buff_spell.wav')

# Ally Death -- Played when a member of your party dies
ally_death = Sound('../Sound FX/ally_death.wav')

# Enemy Death -- Played when a member of the enemy team dies
enemy_death = Sound('../Sound FX/enemy_death.wav')

# Critical Hit -- Played when someone lands a critical hit
critical_hit = Sound('../Sound FX/critical_hit.wav')

# Lockpick Break -- Played when failing to pick a lock (Stolen from Oblivion)
lockpick_break = Sound('../Sound FX/lockpick_break.wav')

# Lockpicking -- Played when attempting to pick a lock
lockpicking = Sound('../Sound FX/lockpicking.wav')

# Unlock Chest -- Played when succeeding to pick a lock
unlock_chest = Sound('../Sound FX/unlock_chest.wav')

# Debuff -- Played when the player suffers from a debuff
debuff = Sound('../Sound FX/debuff.wav')

# Ability cast -- Used when non-magical abilities are casted
ability_cast = Sound('../Sound FX/ability_cast.wav')

# Potion Brew -- Used when brewing potions
potion_brew = Sound('../Sound FX/potion_brew.wav')

# Eerie Sound -- No current use
eerie_sound = Sound('../Sound FX/eerie_sound.wav')

# Random encounter -- No current use
random_enc = Sound('../Sound FX/random_encounter.wav')

bard_sounds = {"snare_drum": [
    Sound('../Sound FX/Bard Sounds/snare_1.wav'),
    # Sound('../Sound FX/Bard Sounds/snare_2.wav'),
    # Sound('../Sound FX/Bard Sounds/snare_3.wav'),
    # Sound('../Sound FX/Bard Sounds/snare_4.wav'),
    # Sound('../Sound FX/Bard Sounds/snare_5.wav')
               ], "violin": [
    Sound('../Sound FX/Bard Sounds/violin_1.wav'),
    # Sound('../Sound FX/Bard Sounds/violin_2.wav'),
    # Sound('../Sound FX/Bard Sounds/violin_3.wav'),
    # Sound('../Sound FX/Bard Sounds/violin_4.wav'),
    # Sound('../Sound FX/Bard Sounds/violin_5.wav')
               ], "flute": [
    Sound('../Sound FX/Bard Sounds/flute_1.wav'),
    # Sound('../Sound FX/Bard Sounds/flute_2.wav'),
    # Sound('../Sound FX/Bard Sounds/flute_3.wav'),
    # Sound('../Sound FX/Bard Sounds/flute_4.wav'),
    # Sound('../Sound FX/Bard Sounds/flute_5.wav')
               ], "trumpet": [
    Sound('../Sound FX/Bard Sounds/trumpet_1.wav'),
    # Sound('../Sound FX/Bard Sounds/trumpet_2.wav'),
    # Sound('../Sound FX/Bard Sounds/trumpet_3.wav'),
    # Sound('../Sound FX/Bard Sounds/trumpet_4.wav'),
    # Sound('../Sound FX/Bard Sounds/trumpet_5.wav')
               ], "kazoo": [
    Sound('../Sound FX/Bard Sounds/kazoo_1.wav'),
    # Sound('../Sound FX/Bard Sounds/kazoo_2.wav'),
    # Sound('../Sound FX/Bard Sounds/kazoo_3.wav'),
    # Sound('../Sound FX/Bard Sounds/kazoo_4.wav'),
    # Sound('../Sound FX/Bard Sounds/kazoo_5.wav')
               ], "bagpipes": [
    Sound('../Sound FX/Bard Sounds/bagpipes_1.wav'),
    # Sound('../Sound FX/Bard Sounds/bagpipes_2.wav'),
    # Sound('../Sound FX/Bard Sounds/bagpipes_3.wav'),
    # Sound('../Sound FX/Bard Sounds/bagpipes_4.wav'),
    # Sound('../Sound FX/Bard Sounds/bagpipes_5.wav')
               ]
}

all_sounds = [sword_slash, magic_attack,
              magic_healing, enemy_hit,
              foot_steps, aim_weapon,
              attack_miss, item_pickup,
              health_low, poison_damage,
              buff_spell, ally_death,
              critical_hit, lockpicking,
              lockpick_break, unlock_chest,
              debuff, eerie_sound,
              random_enc, enemy_death,
              ability_cast, potion_brew]


def play_music(song, num_plays=-1):
    if not main.party_info['musicbox_isplaying']:
        mixer.music.load(song)
        mixer.music.play(num_plays)
        mixer.music.set_volume(save_load.music_vol)


def change_volume():
    for sound1 in all_sounds:
        sound1.set_volume(save_load.sound_vol)

    for key in bard_sounds:
        for sound2 in bard_sounds[key]:
            sound2.set_volume(save_load.sound_vol)


for item in copy.copy(globals()):
    if isinstance(globals()[item], Sound) and globals()[item] not in all_sounds:
        print(f'{item} not in all_sounds!')
