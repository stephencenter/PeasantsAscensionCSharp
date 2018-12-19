﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Methods
{
    public class Battle
    {
        string vowels = "AEIOU";
        //vowels = 'AEIOU'
        //m_list = []
        //enabled_pcus = []
        //turn_counter = 0

        //def battle_system(is_boss= False) :
        //    global m_list
        //    global enabled_pcus
        //    global turn_counter

        //    enabled_pcus = [x for x in [units.player,
        //                                units.solou,
        //                                units.chili,
        //                                units.chyme,
        //                                units.storm,
        //                                units.adorine,
        //                                units.parsto] if x.enabled]
        //    turn_counter = 0

        //    # Bosses use a different battle music than when battling normal enemies
        //    if is_boss:
        //        m_list = ([units.monster] + units.monster.lackies) if units.monster.lackies else [units.monster]

        //print(units.monster.ascii_art % '')

        //        if len(m_list) > 2:
        //            print(f'The legendary {units.monster.name} and its lackys have awoken!')

        //        elif len(m_list) == 2:
        //            print(f'The legendary {units.monster.name} and its lacky have awoken!')

        //        else:
        //            print(f'The legendary {units.monster.name} has awoken!')

        //        sounds.play_music('../Music/Terrible Tarantuloid.ogg')

        //        main.smart_sleep(0.35)

        //    else:
        //        # Add monsters to the battle.
        //        m_list = [units.monster]
        //        if random.randint(0, 1):
        //            m_list.append(units.monster_2)

        //            if random.randint(0, 1):
        //                m_list.append(units.monster_3)

        //        print(units.monster.ascii_art % '')

        //        if len(m_list) == 3:
        //            print(f'A {units.monster.name} and 2 other monsters suddenly appeared out of nowhere!')

        //        elif len(m_list) == 2:
        //            print(f'A {units.monster.name} and 1 other monster suddenly appeared out of nowhere!')

        //        else:
        //            print(f'A {units.monster.name} suddenly appeared out of nowhere!')

        //        sounds.play_music('../Music/Ruari 8-bit Battle.ogg')

        //        main.smart_sleep(1)

        //    # Record the player's non-hp/mp stats (e.g. defense)
        //    # So they can go back to normal after the battle
        //    set_temp_stats()
        //    main.party_info['gamestate'] = 'battle'

        //    # While all active party members are alive, continue the battle
        //    while any([mstr.hp > 0 for mstr in m_list]) and any([char.hp > 0 for char in enabled_pcus]):
        //        turn_counter += 1

        //        # A list of the battle participants sorted by speed. Updates once per turn.
        //        speed_list = sorted(m_list + enabled_pcus,
        //                            key= lambda x: 0.5*x.spd if "paralyzed" in x.status_ail else x.spd,
        //                            reverse= True)

        //        # Display HP, MP, Levels, and Statuses for all battle participants
        //bat_stats()

        //        for num, character in enumerate(enabled_pcus) :
        //            # If any of your party members are at less than 20% health, play a small jingle
        //            if 0 < character.hp <= 0.20 * character.max_hp:
        //                print(f"Warning: {character.name}'s HP is low, heal as soon as possible!\n")
        //                sounds.health_low.play()
        //                main.smart_sleep(1)

        //            # Let each awake and alive character choose their move
        //            if 'dead' not in character.status_ail:
        //                character.player_choice()

        //                if num + 1 < len([x for x in enabled_pcus if 'dead' not in x.status_ail]) :
        //                    print('-'*save_load.divider_size)

        //        # Make sure each participant in the battle goes according to who's fastest
        //        for char in speed_list:
        //            if 'dead' not in char.status_ail:
        //                if all(x.hp <= 0 for x in m_list) :
        //                    break

        //                print('-'*save_load.divider_size)

        //                if ((isinstance(char, units.PlayableCharacter) and char.battle_turn() == 'Ran') or
        //                        (isinstance(char, units.Monster) and char.base_turn() == 'Ran')):
        //                    return

        //                if any(x.hp > 0 for x in enabled_pcus) :
        //                    if any(x.hp > 0 for x in m_list) and 'dead' not in char.status_ail:
        //                        main.s_input('\nPress enter/return ')

        //                    elif all(x.hp <= 0 for x in m_list):
        //                        break

        //                else:
        //                    break

        //            # Check if any characters died on the participants turn
        //            for char_2 in speed_list:
        //                if isinstance(char_2, units.PlayableCharacter) and char_2.hp <= 0 and 'dead' not in char_2.status_ail:
        //                    char_2.hp = 0
        //                    char_2.status_ail = ['dead']
        //                    sounds.ally_death.play()

        //                    print('-'*save_load.divider_size)
        //                    print(f"{char_2.name} has fallen to the monsters!")
        //                    main.s_input("\nPress enter/return ")

        //                if isinstance(char_2, units.Monster) and char_2.hp <= 0 and 'dead' not in char_2.status_ail:
        //                    char_2.hp = 0
        //                    char_2.status_ail = ['dead']
        //                    sounds.enemy_death.play()

        //                    print('-'*save_load.divider_size)
        //                    print(f"The {char_2.name} was defeated by your party!")
        //                    main.s_input("\nPress enter/return ")

        //    after_battle(is_boss)


        //def run_away(runner):
        //    print(ascii_art.player_art[runner.class_.title()] % f"{runner.name} is making a move!\n")
        //    print(f'Your party starts to run away from the {units.monster.name}...')
        //    sounds.foot_steps.play()

        //    main.smart_sleep(0.75)

        //    if 'paralyzed' in runner.status_ail:
        //        # 20% chance of success
        //        chance = 20

        //    elif bool (runner.spd > sorted(m_list, key= lambda x: x.spd, reverse= True)[0].spd) != \
        //            bool (runner.evad > sorted(m_list, key= lambda x: x.evad, reverse= True)[0].spd):
        //        # 60% chance of success
        //        chance = 60

        //    elif runner.spd > sorted(m_list, key= lambda x: x.spd, reverse= True)[0].spd and \
        //            runner.evad > sorted(m_list, key= lambda x: x.evad, reverse= True)[0].spd:
        //        # 80% chance of success
        //        chance = 80

        //    else:
        //        # 40% chance of success
        //        chance = 40

        //    if random.randint(0, 100) <= chance:
        //        sounds.buff_spell.play()
        //        print(f'Your party manages to escape from the {units.monster.name}!')
        //        main.s_input("\nPress enter/return ")
        //        return True

        //    else:
        //        sounds.debuff.play()
        //        print("Your party's attempt to escape failed!")
        //        return False


        //def after_battle(is_boss) :
        //    # Assess the results of the battle
        //    print('-'*save_load.divider_size)

        //    for unit in enabled_pcus + m_list:
        //        if unit.hp <= 0 and 'dead' not in unit.status_ail:
        //            unit.hp = 0
        //            unit.status_ail = ['dead']

        //    while True:
        //        # If the monster wins...
        //        if any(['dead' not in m.status_ail for m in m_list]) and all(['dead' in x.status_ail for x in enabled_pcus]):
        //            sounds.play_music('../Music/Power-Up.ogg')

        //            print(f'Despite your best efforts, the {units.monster.name} has killed your party.')
        //            print('-'*save_load.divider_size)

        //            auto_yes = False
        //            while True:
        //                if auto_yes:
        //                    y_n = 'y'

        //                else:
        //                    y_n = main.s_input('Do you wish to continue playing? | Y/N: ').lower()

        //                if y_n.startswith('y'):
        //                    # If you die, you return to the last town visited or 0'N, 0'W if you haven't been to a town yet.

        //                    main.party_info['current_tile'] = main.party_info['prev_town']
        //                    units.heal_pcus(1)

        //                    sounds.play_music(main.party_info['music'])

        //                    return

        //                elif y_n.startswith('n'):
        //                    while True:
        //                        y_n = main.s_input('Are you sure you want to quit and lose unsaved progress? |  Y/N: ').lower()

        //                        if y_n.startswith('n') or main.do_debug:
        //                            auto_yes = True

        //                            break

        //                        elif y_n.startswith('y'):
        //                            pygame.quit()
        //                            sys.exit()

        //        # If the player wins...
        //elif all(['dead' in m.status_ail for m in m_list]) and any(['dead' not in x.status_ail for x in enabled_pcus]):
        //            sounds.play_music('../Music/Python_RM.ogg')

        //            if is_boss:
        //                print(f'The almighty {units.monster.name} has been slain!')
        //                units.defeated_bosses.append(units.monster.boss_id)
        //                units.monster.upon_defeating()

        //            else:
        //                print(f'The {units.monster.name} falls to the ground, dead as a stone.')

        //            # Formulas for item, gold, and experience drops
        //gold_drops = math.ceil(sum([max(1, x.gold, 2.5 * x.lvl) for x in m_list]))
        //            expr_drops = math.ceil(sum([max(1, y.experience, 1.5 * *y.lvl) / 2 for y in m_list]))
        //            item_drops = []

        //            for monster in m_list:
        //                for item in monster.items:
        //                    item_drops.append((monster.name, item))

        //            main.party_info['gp'] += gold_drops
        //            main.s_input(f'Your party has gained {gold_drops} GP! ')

        //            # Each party member gets their own XP
        //            for character in enabled_pcus:
        //                character.exp += expr_drops
        //                main.s_input(f'{character.name} gained {expr_drops} XP! ')

        //            # Each monster can drop their own item
        //            for drop in item_drops:
        //                main.s_input(f"The {drop[0]} dropped a {items.find_item_with_id(drop[1]).name}! ")
        //                items.add_item(drop[1])

        //            for character in enabled_pcus:
        //                character.level_up()

        //            sounds.play_music(main.party_info['music'])

        //            return

        //        else:
        //            units.player.hp = 1
        //            units.player.status_ail = ['alive']

        //            continue


        //def battle_inventory(user):
        //    # The player can use items from the Consumables category of their inventory during battles.
        //    while True:
        //        print('Battle Inventory: ')

        //        for x, y in enumerate(items.inventory['consumables']) :
        //            print(f'      [{x + 1}] {y.name}')

        //        while True:
        //            item = main.s_input('Input [#] (or type "exit"): ').lower()

        //            try:
        //                item = items.inventory['consumables'][int(item) - 1]

        //            except(IndexError, ValueError):
        //                if item in ['e', 'x', 'exit', 'b', 'back']:
        //                    print('-'*save_load.divider_size)
        //                    return False

        //                continue

        //            if isinstance(item, items.StatusPotion) :
        //                if item.status != user.status_ail:
        //                    print('-'*save_load.divider_size)
        //                    print(f'{user.name} is not {item.status}, they have no reason to drink that.')
        //                    main.s_input("\nPress enter/return ")
        //                    print('-'*save_load.divider_size)
        //                    break

        //            print('-' * save_load.divider_size)
        //            item.use_item(user)
        //            return True


        //def bat_stats() :
        //    units.fix_stats()
        //    print('-'*save_load.divider_size)

        //    # Player Stats
        //player_pad1 = max([len(x.name) for x in enabled_pcus])
        //    player_pad2 = len(max([f'{unit.hp}/{unit.max_hp} HP' for unit in enabled_pcus], key= len))
        //    player_pad3 = len(max([f'{unit.mp}/{unit.max_mp} MP' for unit in enabled_pcus], key= len))

        //    print("Your party: ")
        //    for pcu in enabled_pcus:
        //        print("  {0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
        //              pcu.name, pcu.hp,
        //              pcu.max_hp, pcu.mp,
        //              pcu.max_mp, pcu.lvl,
        //              ', '.join([x.title() for x in pcu.status_ail]),
        //              pad1= ' ' * (player_pad1 - len(pcu.name)),
        //              pad2= ' ' * (player_pad2 - len(f'{pcu.hp}/{pcu.max_hp} HP')),
        //              pad3= ' ' * (player_pad3 - len(f'{pcu.mp}/{pcu.max_mp} MP'))))

        //    # Monster Stats
        //    monster_pad1 = max([len(x.name) for x in m_list])
        //    monster_pad2 = len(max([f'{unit.hp}/{unit.max_hp} HP' for unit in m_list], key= len))
        //    monster_pad3 = len(max([f'{unit.mp}/{unit.max_mp} MP' for unit in m_list], key= len))

        //    print("\nEnemy Team: ")
        //    for each_monster in m_list:
        //        print("  {0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
        //              each_monster.name, each_monster.hp,
        //              each_monster.max_hp, each_monster.mp,
        //              each_monster.max_mp, each_monster.lvl,
        //              ', '.join([x.title() for x in each_monster.status_ail]),
        //              pad1= ' ' * (monster_pad1 - len(each_monster.name)),
        //              pad2= ' ' * (monster_pad2 - len(f'{each_monster.hp}/{each_monster.max_hp} HP')),
        //              pad3= ' ' * (monster_pad3 - len(f'{each_monster.mp}/{each_monster.max_mp} MP'))))

        //    print('-'*save_load.divider_size)

    }
}