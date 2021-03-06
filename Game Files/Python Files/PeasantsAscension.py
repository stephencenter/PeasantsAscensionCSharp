#!/usr/bin/env python
# Peasants' Ascension v1.0.0 Beta
# --------------------------------------------------------------------------- #
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
# --------------------------------------------------------------------------- #
# Music by Ben Landis: http://www.benlandis.com/
# And Eric Skiff: http://ericskiff.com/music/
# --------------------------------------------------------------------------- #
# Contact me via Twitter (@TheFrozenMawile) or email (stephenbcenter@gmail.com)
# for questions/feedback. Visit the subreddit at http://reddit.com/PeasantsAscension
# --------------------------------------------------------------------------- #
# Notes for people reading this code:
#  1. print('-'*save_load.divider_size) <-- This line appears constantly in my
#     code. It's purpose is to enhance readability and organization for people
#     playing the game.
#
#  2. I am completely open to any and all criticism! I'm still pretty new to
#     programming, so I need all the advice I can get. Bug reports are great
#     too! Contact information is near the top of this module.
#
#  3. If you encounter an error message at any point when playing this, please
#     email the error_log.out file to stephenbcenter@gmail.com. If you could
#     provide a description of what you did to cause the bug, that'd be great.
#
#  4. I made an attempt to comment most of my code, and hopefully the rest is
#     pretty self-explanatory. But if you have any questions about how something
#     works or why something is the way it is, feel free to ask me! I love
#     answering questions!
# --------------------------------------------------------------------------- #

import ctypes
import logging
import msvcrt
import random
import sys
import time
import traceback

import pygame

import tiles
import title_screen
import save_load
import towns
import sounds
import units
import battle
import items
import magic

# Log everything and send it to stderr.
logging.basicConfig(filename='../error_log.out', level=logging.DEBUG, format="\n%(message)s")

# Setup Pygame audio
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# A dictionary containing generic information about the player's party
party_info = {'music': '../Music/Through the Forest.ogg',
              'prov': "Overshire",
              'current_tile': tiles.find_tile_with_id('nearton_tile'),
              'current_town': '',
              'prev_town': tiles.find_tile_with_id('nearton_tile'),
              'gp': 20,
              'visited_towns': [],
              'steps_without_battle': 0,
              'do_spawns': True,
              'scout_list': [],
              'dif': 0,
              'map_pow': 1,
              'gamestate': "overworld",
              'musicbox_folder': '',
              'musicbox_isplaying': False,
              'musicbox_mode': 'A->Z',
              'musicbox_process': None}

# Set to 1 when auto-testing
do_debug = 0

# A list of usernames that apply to some of my friends. Adds a few easter eggs.
friend_names = ["apollo kalar", "apollokalar", "apollo_kalar",
                "flygon jones", "flygonjones", "flygon_jones",
                "cynder887",
                "starkiller106024", "starkiller", "star killer",
                "atomic vexal", "vexal", "wave vex",
                "therichpig", "therichpig64", "spaghettipig64", "spaghettipig"]


# Custom input, plays a "blip" sound after the player presses enter.
# Also can be used to automatically play the game and find crashes.
def s_input(string=''):
    if do_debug:
        print(string, end='')
        char = random.choice('0123456789abcdefghijklmnopqrstuvwxyz')
        print(char)

        return char

    x = input(string)

    if save_load.do_blip:
        sounds.item_pickup.play()

    return x


# "Pauses" the game for a specific duration, and then does some magic to make everything work correctly
def smart_sleep(duration):
    if do_debug:
        duration = 0.02

    time.sleep(duration)

    # I have no idea how this works but I found it on Stack Overflow and it makes the text sync properly
    while msvcrt.kbhit():
        msvcrt.getwch()


# Takes a string and coverts it into a list, cutting off at every 79th character.
# This is so that text, such as item/tile descriptions or NPC dialogue, does not get word-wrapped.
# Also does some magic to make sure that sentences don't get cut off mid w
# ord
def chop_by_79(string, num=79):
    sentences = []
    current_sentence = ''

    for word in string.split():
        if len(current_sentence + word) > num:
            sentences.append(current_sentence)
            current_sentence = ''

        current_sentence += f'{word} '

    sentences.append(current_sentence) if current_sentence else ''

    return sentences


def text_scroll(string, spacing=0.025):
    # Causes each character in a string to appear one at a time with `spacing` time in between
    # each one, as opposed to all at once.
    string = ''.join([string, "\n"])

    for num, char in enumerate(string):
        # end='' prevents print() from printing a newline after each character
        print(char, end='')

        if char != ' ' and num + 1 != len(string):
            smart_sleep(spacing)

        sys.stdout.flush()  # Prevent "print" from waiting until the loop is completed to print() "char"


def input_ts(string, spacing=0.025):
        # Input mode prints all but the last character. The last character
        # is instead passed as the argument for the "main.s_input()" function,
        # the result of which is returned.

        if not string.endswith(' '):
            # If there isn't a space, then user main.s_input will be
            # mashed together with the printed characters.

            string = ''.join([string, ' '])

        text_scroll(string[:-1], spacing)  # Select all but the last character
        return s_input(string[-1])


def game_loop():
    party_info['music'] = tiles.find_cell_with_tile_id(party_info['current_tile'].tile_id).music
    sounds.play_music(party_info['music'])

    while True:
        if not towns.search_towns():
            print('-'*save_load.divider_size)

        available_dirs = game_ui()

        while True:
            party_info['gamestate'] = 'overworld'
            command = s_input('Input Command (type "help" to view command list): ').lower()

            if command == "debug-menu":
                debug_command()

            elif any(map(command.startswith, [x[0] for x in available_dirs])):
                move_command(available_dirs, command[0])

                break

            elif command.startswith('p'):
                stats_command()

            elif command.startswith('m'):
                magic_command()

            elif command.startswith('i'):
                inv_command()

            elif command.startswith('t'):
                tools_command()

            elif command.startswith('l'):
                look_command()

            elif command.startswith('r'):
                recheck_command()

            elif command.startswith('c'):
                title_screen.edit_settings()

            elif command.startswith('h'):
                help_command()

            else:
                continue

            available_dirs = game_ui()


def game_ui():
    available_dirs = []
    mpi = party_info
    tile = mpi['current_tile']

    print(f"-CURRENT LOCATION-")
    print(mpi['current_tile'].generate_ascii())

    print(f"Region [{tile.name}] | Province: [{tiles.find_prov_with_tile_id(tile.tile_id).name}]")

    # Tells the player which directions are available to go in
    for drc in [x for x in [tile.to_n, tile.to_s, tile.to_e, tile.to_w, tile.to_dn, tile.to_up] if x is not None]:
        if drc == tile.to_e:
            print("    To the [E]ast", end='')
            available_dirs.append(['e', drc])

        if drc == tile.to_w:
            print("    To the [W]est", end='')
            available_dirs.append(['w', drc])

        if drc == tile.to_n:
            print("    To the [N]orth", end='')
            available_dirs.append(['n', drc])

        if drc == tile.to_s:
            print("    To the [S]outh", end='')
            available_dirs.append(['s', drc])

        if drc == tile.to_up:
            print("    [U]pwards, above your party,", end='')
            available_dirs.append(['u', drc])

        if drc == tile.to_dn:
            print("    [D]ownwards, below your party,", end='')
            available_dirs.append(['d', drc])

        adj_tile = tiles.find_tile_with_id(drc)
        print(f" lies the {adj_tile.name}")

    return available_dirs


def move_command(available_dirs, command):
    global party_info

    sounds.item_pickup.stop()
    sounds.foot_steps.play()

    party_info['current_tile'] = tiles.find_tile_with_id([a[1] for a in available_dirs if a[0] == command][0])

    # If none of these fucntions return True, then a battle can occur.
    if not any([units.check_bosses(), towns.search_towns(enter=False)]):

        # There is a 1 in 4 chance for a battle to occur (25%)
        # However, a battle cannot occur if the number of steps since the last battle is less than three,
        # and is guaranteed to occur if the number of steps is above 10.
        is_battle = random.randint(0, 3) == 0

        if party_info['steps_without_battle'] > 10:
            is_battle = True

        elif party_info['steps_without_battle'] < 3:
            is_battle = False

        # Certain tiles can have battling disabled on them
        if is_battle and tiles.find_cell_with_tile_id(party_info['current_tile'].tile_id) != -1 \
                and party_info['do_spawns']:

            print('-' * save_load.divider_size)
            units.spawn_monster()
            party_info['steps_without_battle'] = 0

            highest_perception = max([pcu.attributes['per'] for pcu in [units.player,
                                                                        units.solou,
                                                                        units.chili,
                                                                        units.chyme,
                                                                        units.adorine,
                                                                        units.parsto]])

            if highest_perception > random.randint(0, 100):
                print(f"You see a {units.monster.name} - it has not detected you yet.")

                while True:
                    y_n = s_input("Fight it?").lower()

                    if y_n.startswith("y"):
                        print('-' * save_load.divider_size)
                        battle.battle_system()

                    elif y_n.startswith("n"):
                        break

            else:
                battle.battle_system()

        else:
            party_info['steps_without_battle'] += 1


def recheck_command():
    towns.search_towns()
    units.check_bosses()


def help_command():                       
    print('-'*save_load.divider_size)
    print("""Command List:
 [NSEW] - Moves your party if the selected direction is unobstructed
 [L]ook - Displays a description of your current location
 [P]arty Stats - Displays the stats of a specific party member
 [T]ool Menu - Allows you to quickly use tools without opening your inventory
 [M]agic - Allows you to use healing spells outside of battle
 [I]nventory - Displays your inventory and lets you equip/use items
 [R]e-check - Searches the current tile for a town or boss
 [C]onfig - Opens the settings list and allows you to change them in-game
 [H]elp - Reopens this list of commands
Type the letter in brackets while on the overworld to use the command""")

    s_input("\nPress enter/return ")
    print('-'*save_load.divider_size)


def stats_command():
    print('-'*save_load.divider_size)
    print('You stop to rest for a moment.')

    target_options = [x for x in [units.player,
                                  units.solou,
                                  units.chili,
                                  units.adorine,
                                  units.storm,
                                  units.parsto,
                                  units.chyme] if x.enabled]

    if len(target_options) == 1:
        target = units.player

    else:
        print("Select Character:")

        for num, character in enumerate(target_options):
            print(f"      [{int(num) + 1}] {character.name}")

        while True:
            target = s_input('Input [#] (or type "exit"): ').lower()

            try:
                target = target_options[int(target) - 1]

            except (IndexError, ValueError):
                if target in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)

                    break

                continue

            break

    if isinstance(target, units.PlayableCharacter):
        print('-'*save_load.divider_size)
        target.player_info()
        print('-'*save_load.divider_size)


def inv_command():
    print('-'*save_load.divider_size)
    items.pick_category()
    print('-'*save_load.divider_size)


def magic_command():
    units.player.choose_target("Choose Spellbook:", ally=True, enemy=False)

    if magic.spellbook[units.player.target.name if units.player.target != units.player else 'player']['Healing']:
        magic.pick_spell('Healing', units.player.target, False)

    else:
        print('-'*save_load.divider_size)
        print(f'{units.player.target.name} has no overworld spells in their spellbook.')
        s_input("\nPress enter/return ")


def look_command():
    print('-'*save_load.divider_size)
    print(party_info['current_tile'].desc)
    s_input("\nPress enter/return ")
    print('-'*save_load.divider_size)


def tools_command():
    valid_tools = ['monster_book', 'shovel', 'musicbox', 'pocket_lab', 'fast_map']
    available_tools = []

    for item in items.inventory['tools']:
        if item.item_id in valid_tools:
            available_tools.append(item)

    print('-'*save_load.divider_size)

    if not available_tools:
        print('Your party has no available tools to use.')
        s_input('\nPress enter/return ')
        print('-'*save_load.divider_size)

        return

    while True:
        print('Tools: ')

        for x, y in enumerate(available_tools):
            print(f"      [{x + 1}] {y.name}")

        while True:
            tool = s_input('Input [#] (or type "exit"): ').lower()

            try:
                tool = available_tools[int(tool) - 1]

            except (IndexError, ValueError):
                if tool in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)

                    return

                continue

            print('-'*save_load.divider_size)

            tool.use_item(units.player)
            if tool.item_id == 'fast_map':
                return

            print('-'*save_load.divider_size)

            break


def debug_command():
    # Opens the debug menu. Allows the player to enter in Python Code in order to manipulate in-game variables.
    # Extremely powerful, but can potentially ruin the game state if the player doesn't know what they're doing.
    # Use with caution.
    print('-'*save_load.divider_size)
    print('-DEBUG MENU-')
    while True:
        command = s_input('Input command (or type "exit"): ')

        if command in ['e', 'x', 'exit', 'b', 'back']:
            print('-'*save_load.divider_size)

            break

        try:
            print(f">{command}")
            exec(command)

        except Exception:
            print('-'*save_load.divider_size)
            print(f"Invalid Command, error encountered: ")
            print(traceback.format_exc(), end='')
            print('-'*save_load.divider_size)


def set_prompt_properties():
    # Find the size of the screen
    screen = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    class Coord(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class ConsoleFontInfo(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("nFont", ctypes.c_ulong), ("dwFontSize", Coord),
                    ("FontFamily", ctypes.c_uint), ("FontWeight", ctypes.c_uint), ("FaceName", ctypes.c_wchar*32)]

    # Set font information
    font = ConsoleFontInfo()
    font.cbSize = ctypes.sizeof(ConsoleFontInfo)
    font.nFont = 12
    font.FontFamily = 54
    font.FontWeight = 400

    # Adjust for screen sizes
    font.dwFontSize.X = 8 if screen[0] < 1024 else 10 if screen[0] < 1280 else 12 if screen[0] < 1920 else 15
    font.dwFontSize.Y = 14 if screen[0] < 1024 else 18 if screen[0] < 1280 else 22 if screen[0] < 1920 else 28

    # Lucidia Console is a popular monospaced font, meaning that every single character is the exact same width
    font.FaceName = "Lucida Console"
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))

    # Set the console title
    ctypes.windll.kernel32.SetConsoleTitleA(f"Peasants' Ascension {title_screen.game_version}".encode())


def main():
    # main() handles all the setup for the game, and includes the main game loop.
    # Everything happens in this function in one way or another.
    set_prompt_properties()  # Set the CMD size and whatnot...
    save_load.apply_settings()  # ...set the volume and save file settings...
    title_screen.show_title()  # ...display the titlescreen...
    save_load.load_game()  # ...check for save files...
    game_loop()  # ...and then start the game!


if __name__ == "__main__":  # If this file is being run and not imported, run main()
    try:
        # Run the game.
        main()

    except Exception as e:
        # If an exception is raised and not caught, log the error message.
        logging.exception(f'Got exception of main handler on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')

        # raise # Uncomment this if you're using the auto-s_input debugger

        print(traceback.format_exc())
        print("""\
Peasants' Ascension encountered an error and crashed! Send the error message
shown above to TheFrozenMawile (https://reddit.com/u/TheFrozenMawile) to make 
sure the bug gets fixed. The error message, along with any errors messages 
encountered, can also be found in the error_log.out file.""")
        s_input("\nPress enter/return")

        pygame.quit()
        sys.exit()
