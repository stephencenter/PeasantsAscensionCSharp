#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
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

import inv_system
import sounds
import ascii_art
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Item:
    # The basic item class. Items are stored in the "inventory" dictionary. All
    # item-subclasses inherit from this class.
    def __init__(self, name, desc, buy, sell, cat='', imp=False, ascart='Misc'):
        self.name = name
        self.desc = desc
        self.buy = buy
        self.sell = sell  # How much money you will get from selling it
        self.cat = cat  # Ensures that items go into the correct inventory slot
        self.imp = imp
        self.ascart = ascart

    def __str__(self):
        return self.name


class Consumable(Item):
    # Items that restore your HP, MP, or both
    def __init__(self, name, desc, buy, sell, cat='consumables', imp=False, heal=0, mana=0, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.heal = heal
        self.mana = mana

    def use_item(self, user, is_battle=False):
        print('-'*25)

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

        user.hp += self.heal
        user.mp += self.mana
        units.fix_stats()
        sounds.magic_healing.play()

        print(f'{user.name} consumes the {self.name}.')

        if not is_battle:
            input("\nPress enter/return ")

        for x, y in enumerate(inv_system.inventory[self.cat]):
            if y.name == self.name:
                inv_system.inventory[self.cat].remove(y)
                break


class StatusPotion(Item):
    def __init__(self, name, desc, buy, sell, status, cat='consumables', imp=False, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.status = status

    def use_item(self, user, is_battle=False):
        print('-'*25)

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

        if user.status_ail == self.status:
            for x, y in enumerate(inv_system.inventory[self.cat]):
                if y.name == self.name:
                    inv_system.inventory[self.cat].remove(y)
                    break

            sounds.buff_spell.play()
            user.status_ail = 'none'

            print(f'{user.name} drinks the {self.name} and feels much better.')

            if not is_battle:
                input("\nPress enter/return ")

        else:
            print(f"Drinking this {self.name} probably wouldn't do anything.")
            input("\nPress enter/return ")


class Weapon(Item):
    # Items that increase your damage by a percentage.
    def __init__(self, name, desc, buy, sell, power, type_, class_, ascart, element='none', cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.element = element

        if isinstance(self.class_, str):
            self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'''])

        else:
            self.desc = ' '.join([desc, "[", ', '.join([x.title() for x in self.class_]), ']'])

    def use_item(self, user):
        if user.class_ in self.class_ or self.class_ == 'none':
            # Creating a copy of the weapon ensures that
            # only one weapon can be equipped at a time.
            spam = copy.copy(self)

            if isinstance(inv_system.equipped[user.name if user != units.player else 'player']['weapon'], Weapon):

                old = copy.copy(inv_system.equipped[user.name if user != units.player else 'player']['weapon'])
                inv_system.inventory['weapons'].remove(self)

                if old.name != 'Fists':
                    inv_system.inventory['weapons'].append(old)

                inv_system.equipped[user.name if user != units.player else 'player']['weapon'] = spam

            print('-'*25)
            print(f'{user.name} equips the {self}.')
            input("\nPress enter/return ")

        else:
            print('-'*25)

            if isinstance(self.class_, list):
                print(f"{user.name} must be a {self.class_[0].title()} or a {self.class_[1].title()} to equip.")

                input("\nPress enter/return ")

            else:
                print(f"{user.name} must be a {self.class_.title()} to equip this.")
                input("\nPress enter/return ")


class Armor(Item):
    # Items that give the player a percent increase in defense when hit.
    def __init__(self, name, desc, buy, sell, defense, part, class_, ascart, cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.defense = defense
        self.part = part
        self.class_ = class_

        if self.class_ != 'none':
            if isinstance(self.class_, str):
                self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'])

            else:
                self.desc = ' '.join([desc, '|', ' and '.join([x.title() for x in self.class_]), 'ONLY'])

        else:
            self.desc = ' '.join([desc, '|', "ANY CLASS"])

    def use_item(self, user):
        if user.class_ in self.class_ or self.class_ == 'none':
            # A copy of the armor is created for the same
            # reason as for weapons.
            fizz = copy.copy(self)

            if isinstance(inv_system.equipped[user.name if user != units.player else 'player'][self.part], Armor):

                old = copy.copy(inv_system.equipped[user.name if user != units.player else 'player'][self.part])

                inv_system.inventory['armor'].append(old)
                inv_system.inventory['armor'].remove(self)

            else:
                inv_system.equipped[user.name if user != units.player else 'player'][self.part] = fizz
                inv_system.inventory['armor'].remove(self)

            print('-'*25)
            print(f'{user.name} equips the {self}.')
            input("\nPress enter/return ")

        else:
            print('-'*25)

            if isinstance(self.class_, list):
                print(f"{user.name} must be a {self.class_[0].title()} or a {self.class_[1].title()} to equip.")

                input("\nPress enter/return ")

            else:
                print(f"{user.name} must be a {self.class_.title()} to equip this.")
                input("\nPress enter/return ")


# -- ACCESSORIES -- #
class Accessory(Item):
    def __init__(self, name, desc, buy, sell, ascart, cat='access', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)


class ElementAccessory(Accessory):
    # Gives the player an element used when taking damage
    def __init__(self, name, desc, buy, sell, element, ascart='Amulet', acc_type='elemental',
                 cat='access', imp=False):
        Accessory.__init__(self, name, desc, buy, sell, ascart, cat, imp)
        self.element = element
        self.acc_type = acc_type

    def __str__(self):
        return self.name

    def use_item(self, user):
        spam = copy.copy(self)
        if isinstance(inv_system.equipped[user.name if user != units.player else 'player']['access'], Accessory):

            old = copy.copy(inv_system.equipped[user.name if user != units.player else 'player']['access'])
            inv_system.inventory['access'].append(old)

        inv_system.inventory['access'].remove(self)
        inv_system.equipped[user.name if user != units.player else 'player']['access'] = spam
        user.element = self.element

        print('-'*25)
        print('{0} equips the {1}. Their element is now set to {2}.'.format(user.name, self.name, self.element))
        input("\nPress enter/return ")


# -- TOOLS -- #
class MagicCompass(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=True, ascart='Compass'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    def use_item(self):
        pass


class DiviningRod(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=True, ascart='Div Rod'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    def use_item(self):
        pass


class Shovel(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=True, ascart='Shovel'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    def use_item(self):
        pass


class TownTeleporter(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=False, ascart='Map'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    def use_item(self):
        pass


class LockpickKit(Item):
    def __init__(self, name, desc, buy, sell, power, cat='tools', imp=False, ascart='Lockpick'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.power = power

    @staticmethod
    def use_item():
        print('-'*25)
        print("Your party could certainly make a quick buck lockpicking chests with this thing.")
        print("But that's illegal - you wouldn't break the law, would you?")
        input("\nPress enter/return ")


# -- OTHERS -- #
class Valuable(Item):
    def __init__(self, name, desc, buy, sell, ascart='Gem', acquired=False, cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.acquired = acquired

    # noinspection PyMethodMayBeStatic
    def use_item(self):
        print('-'*25)
        print(f'Your party admires the {self.name}. It looks very valuable.')
        input("\nPress enter/return ")


class Misc(Item):
    def __init__(self, name, desc, buy, sell, ascart='Misc', cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    def use_item(self):
        print('-'*25)
        if 'Message' in self.name:
            input("""The envelop is designed in a way that makes tampering easily noticeable.
It's probably best not to try to open it and read the letter. | [ENTER] """)

        else:
            input("Your party cannot think of anything useful to do with this. | [ENTER] ")
