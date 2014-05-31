import sys
import json
import npcs
from copy import copy as _c
from items import *

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

inventory = {'q_items': [], 'consum': [_c(s_potion), _c(s_elixir)], 'coord': [],
             'weapons': [], 'armor': [], 'misc': []}
equipped = {'weapon': '', 'head': _c(straw_hat), 'body': _c(cotton_shirt), 'legs': _c(sunday_trousers)}

gs_stock = [[s_potion, s_potion, m_potion, l_potion, l_potion, x_potion],
            [s_elixir, s_elixir, m_elixir, l_elixir, l_elixir, x_elixir],
            [s_rejuv, s_rejuv, m_rejuv, m_rejuv, l_rejuv, l_rejuv],
            [cpr_swd, en_cpr_swd, bnz_spr, en_bnz_spr, irn_axe, en_irn_axe],
            [oak_stf, en_oak_stf, arc_spb, en_arc_spb, rnc_stf, en_rnc_stf],
            [sht_bow, en_sht_bow, lng_bow, en_lng_bow, myth_sb, en_myth_sb],
            [bnz_hlm, en_bnz_hlm, irn_hlm, stl_hlm],
            [bnz_cst, en_bnz_cst, irn_cst, stl_cst],
            [bnz_leg, en_bnz_leg, irn_leg, stl_leg],
            [wiz_hat, en_wiz_hat, myst_hat, en_myst_hat, elem_hat],
            [wiz_rob, en_wiz_rob, myst_rob, en_myst_rob, elem_rob],
            [wiz_gar, en_wiz_gar, myst_gar, en_myst_gar, elem_gar],
            [lth_cap, en_lth_cap, std_cwl],
            [lth_bdy, en_lth_bdy, std_bdy],
            [lth_leg, en_lth_leg, std_leg]]

gs_stock = list(gs_stock)
item_setup_vars()


def pick_category():
    global inventory
    while True:
        print("""Categories:
      [1] Armor
      [2] Consumables
      [3] Weapons
      [4] Quest Items
      [5] Coordinates
      [6] Miscellaneous
      [7] Quests""")
        while True:
            cat = input('Input [#] (or type "exit"): ')
            try:
                cat = cat.lower()
            except AttributeError:
                pass
            if cat in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                return
            elif cat == '1':
                cat = 'armor'
                vis_cat = 'Armor'
            elif cat == '2':
                cat = 'consum'
                vis_cat = 'Consumables'
            elif cat == '3':
                cat = 'weapons'
                vis_cat = 'Weapons'
            elif cat == '4':
                cat = 'q_items'
                vis_cat = 'Quest Items'
            elif cat == '5':
                cat = 'coord'
                vis_cat = 'Coordinates'
            elif cat == '6':
                cat = 'misc'
                vis_cat = 'Miscellaneous'
            elif cat == '7':
                cat = 'quests'
                vis_cat = 'Quests'
            else:
                continue
            if cat in inventory:
                if inventory[cat]:
                    if cat not in ['coord', 'weapons', 'armor']:
                        pick_item(cat, vis_cat)
                        print('-'*25)
                    elif cat == 'coord':
                        print('-'*25)
                        print(inventory[cat])
                        input("Press enter/return when you are finished viewing these coordinates.")
                        print('-'*25)
                    else:
                        if [x for x in inventory[cat] if not x.equip]:
                            pick_item(cat, vis_cat)
                            print('-'*25)
                        else:
                            print('-'*25)
                            print('The "{0}" category is empty...'.format(vis_cat))
                            print('-'*25)
                    break
                else:
                    print('-'*25)
                    print('The "{0}" category is empty...'.format(vis_cat))
                    print('-'*25)
                    break
            elif cat == 'quests' and [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break
            else:
                print("You have no active or completed quests.")


def pick_item(cat, vis_cat, gs=False):
    while cat == 'quests' or inventory[cat]:
        if cat == 'quests':
            print('-'*25)
            while True:
                fizz = True
                choice = input('View [f]inished or [u]nfinished quests? | Input letter (or type "back"): ')
                try:
                    choice = choice.lower()
                except AttributeError:
                    continue

                if choice.startswith('f'):
                    print('-'*25)
                    dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest)
                                and x.finished]
                    if dialogue:
                        while fizz:
                            print('Finished Quests: ')
                            print('     ', '\n     '.join(['[' + str(num + 1) + '] ' + x.name
                                for num, x in enumerate([y for y in npcs.all_dialogue
                                if isinstance(y, npcs.Quest) and y.finished])]))

                            while True:
                                number = input('Input [#] (or type "back"): ')
                                try:
                                    number = int(number) - 1
                                except (TypeError, ValueError):
                                    try:
                                        if number.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                            fizz = False
                                            break
                                        else:
                                            continue
                                    except AttributeError:
                                        continue
                                if (number < 0) or (number > len(dialogue) - 1):
                                    continue
                                quest = dialogue[number]
                                print('-'*25)
                                print("""{0}:\n    "{1}"\nGiven by: {2}""".format(
                                    quest.name, '\n     '.join([x for x in quest.desc]), quest.q_giver))
                                print('-'*25)
                                break
                    else:
                        print('You have no finished quests!')
                    print('-'*25)

                elif choice.startswith('u'):
                    print('-'*25)
                    dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest)
                                and not x.finished and x.started]
                    if dialogue:
                        while fizz:
                            print('Active Quests: ')
                            print('     ', '\n     '.join(['[' + str(num + 1) + '] ' + x.name
                            for num, x in enumerate([y for y in npcs.all_dialogue
                            if isinstance(y, npcs.Quest) and not y.finished and y.started])]))
                            while True:
                                number = input('Input [#] (or type "back"): ')
                                try:
                                    number = int(number) - 1
                                except (TypeError, ValueError):
                                    try:
                                        if number.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                            fizz = False
                                            break
                                        else:
                                            continue
                                    except AttributeError:
                                        continue
                                if (number < 0) or (number > len(dialogue) - 1):
                                    continue
                                quest = dialogue[number]
                                print('-'*25)
                                print("""{0}:\n    "{1}"\nGiven by: {2}""".format(
                                    quest.name, '\n     '.join([x for x in quest.desc]), quest.q_giver))
                                print('-'*25)
                                break
                    else:
                        print('You have no active quests!')
                    print('-'*25)
                elif choice in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return
        else:
            if cat in ['armor', 'weapons']:
                if [x for x in inventory[cat] if not x.equip]:
                    print('-'*25)
                    print(vis_cat + ': \n      ' + '\n      '.join(
                        ['[' + str(x + 1) + '] ' + str(y) for x, y in enumerate(
                            inventory[cat]) if not y.equip]))
                else:
                    return
            else:
                print('-'*25)
                print(''.join([vis_cat, ': \n      ', '\n      '.join(
                    ['[' + str(x + 1) + '] ' + str(y)
                     for x, y in enumerate(inventory[cat])])]))
            while True:
                item = input('Input [#] (or type "back"): ')
                try:
                    item = int(item) - 1
                    if item < 0:
                        continue
                except (TypeError, ValueError):
                    try:
                        item = item.lower()
                    except AttributeError:
                        continue
                    if item in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return
                    else:
                        continue
                try:
                    if cat in ['weapons', 'armor']:
                        item = [x for x in inventory[cat] if not x.equip][item]
                    else:
                        item = inventory[cat][item]
                except IndexError:
                    continue
                if gs:
                    sell_item(cat, item)
                else:
                    pick_action(cat, item)
                break


def pick_action(cat, item):
    global inventory
    print('-'*25)
    while item in inventory[cat]:
        if isinstance(item, Weapon) or isinstance(item, Armor):
            use_equip = 'Equip'
            if item.equip:
                break
        else:
            use_equip = 'Use'
        action = input('{0} | 1: {1}, 2: Read Desc, 3: Drop, 4: Cancel | Input #(1-4): '.format(
            str(item), use_equip))
        try:
            action = int(action)
        except (TypeError, ValueError):
            continue
        if action == 1:
            if isinstance(item, Weapon):
                item.equip_weapon()
            elif isinstance(item, Armor):
                item.equip_armor()
            elif isinstance(item, Consumable):
                item.consume_item()
        elif action == 2:
            print('-'*25)
            print(str(item) + ': ' + item.desc)
            print('-'*25)
        elif action == 3:
            if item.imp:
                print('You cannot dispose of quest-related items.')
            else:
                while True:
                    y_n = input('Are you sure you want to get rid of this {0}? | Yes or No: '.format(str(item)))
                    try:
                        y_n = y_n.lower()
                    except AttributeError:
                        continue
                    if y_n in ['yes', 'y']:
                        print('You toss the {0} aside and continue on your journey.'.format(str(item)))
                        for x, y in enumerate(inventory[cat]):
                            if y.name == item.name:
                                inventory[cat].remove(y)
                                break
                        return
                    elif y_n in ['no', 'n']:
                        print('You decide to keep the {0} with you.'.format(str(item)))
                        break
        elif action == 4:
            return


def sell_item(cat, item):
    print('-'*25)
    print(item.desc)
    print('-'*25)
    while True:
        y_n = input('Do you wish to sell this {0} for {1} GP? | Yes or No: '.format(item.name, item.sell))
        try:
            y_n = y_n.lower()
        except AttributeError:
            continue
        if y_n.startswith('y'):
            for num, i in enumerate(inventory[cat]):
                if i.name == item.name:
                    inventory[cat].remove(inventory[cat][num])
                    main.static['gp'] += item.sell
                    print('You hand the shopkeep your {0} and recieve {1} GP.'.format(item.name, item.sell))
                    return
        elif y_n.startswith('n'):
            return


def serialize_inv(path):
    j_inventory = {}
    for category in inventory:
        j_inventory[category] = []
        for item in inventory[category]:
            if category != 'coord':
                j_inventory[category].append(item.__dict__)
            else:
                j_inventory[category].append(item)
    with open(path, mode='w', encoding='utf-8') as c:
        json.dump(j_inventory, c, indent=4, separators=(', ', ': '))


def deserialize_inv(path):
    global inventory
    norm_inv = {}
    with open(path, encoding='utf-8') as c:
        j_inventory = json.load(c)
    for category in j_inventory:
        norm_inv[category] = []
        for item in j_inventory[category]:
            if category == 'consum':
                x = Consumable('', '', '', '')
            elif category == 'weapon':
                x = Weapon('', '', '', '', '', '', '')
            elif category == 'armor':
                x = Armor('', '', '', '', '', '', '', '')
            elif category == 'coord':
                norm_inv[category].append(item)
                continue
            else:
                continue
            x.__dict__ = item
            norm_inv[category].append(x)
    inventory = norm_inv


def serialize_equip(path):
    j_equipped = {}
    for category in equipped:
        if equipped[category] != '(None)':
            j_equipped[category] = equipped[category].__dict__
        else:
            j_equipped[category] = '(None)'
    with open(path, mode='w', encoding='utf-8') as d:
        json.dump(j_equipped, d, indent=4, separators=(', ', ': '))


def deserialize_equip(path):
    global equipped
    norm_equip = {}
    with open(path, encoding='utf-8') as d:
        j_equipped = json.load(d)
    for category in j_equipped:
        if j_equipped[category] == '(None)':
            norm_equip[category] = '(None)'
            continue
        elif category == 'weapon':
            x = Weapon('', '', '', '', '', '', '')
        else:
            x = Armor('', '', '', '', '', '', '', '')
        x.__dict__ = j_equipped[category]
        norm_equip[category] = x
    equipped = norm_equip
