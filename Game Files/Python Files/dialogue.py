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

import json
import sys
import copy

import items
import units
import save_load

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Conversation:
    def __init__(self, dialogue, conv_id, active):
        self.dialogue = dialogue
        self.active = active
        self.conv_id = conv_id

    def after_talking(self):
        pass


class Quest(Conversation):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        Conversation.__init__(self, dialogue, conv_id, active)
        self.name = name  # The name of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.started = False  # is True if the quest has been started, false otherwise
        self.finished = False  # is True if the quest is complete, false otherwise

    def give_quest(self):
        print('-'*save_load.divider_size)
        print(f'{self.q_giver} is offering you the quest "{self.name}".')

        while True:
            accept = main.s_input('Do you accept this quest? | Y/N: ').lower()

            if accept.startswith('y'):
                print('-'*save_load.divider_size)
                print(f'{self.q_giver}: "Terrific! Thank you for your help!"')
                main.s_input("\nPress enter/return ")
                self.started = True
                self.upon_starting()

                return

            elif accept.startswith('n'):
                print('-'*save_load.divider_size)
                print(f'{self.q_giver}: "Oh... That\'s fine. Come back later if you change your mind."')

                return

    def completion(self):
        self.upon_completing()

        print("Quest Complete!")
        print(f"You've received {self.reward[0]} XP and {self.reward[1]} GP for completing this quest.")
        main.s_input('\nPress enter/return')

        main.party_info['gp'] += self.reward[1]
        units.player.exp += self.reward[0]
        units.player.level_up()

        self.active = False

    def upon_starting(self):
        pass

    def upon_completing(self):
        pass


# -- Name: Solou -- Town: Nearton
class SolouConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        units.solou.enabled = True
        self.active = False

        print('-'*save_load.divider_size)
        print("Solou the Mage has been added to your party!")
        main.s_input('\nPress enter/return ')


solou_convo_a = SolouConvoA("""\
""", "solou_c1", True
)


class SolouQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global joseph_quest_a

        joseph_convo_b.active = True
        joseph_quest_a.active = True


solou_quest_a = SolouQuestA("A Courier's Resignation [MAIN QUEST]", """\
""", "Solou", [25, 25], "solou_q1", True)


# -- Name: Joseph -- Town: Overshire City
class JosephConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


joseph_convo_a = JosephConvoA("""\
Greetings, young adventurer. Welcome to Overshire.""", "joseph_c1", True)


class JosephConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global joseph_convo_b

        joseph_convo_b.active = False
        solou_quest_a.completion()


joseph_convo_b = JosephConvoB("""\
Ah, Solou! Long time no see! I see you've taken up adventuring.
It must be nice to finally put that spellbook of yours to use!
Oh, what's this? A letter for me? Well, I'll be sure to read this
later. Thank you for delivering this to me!""", "joseph_c2", False)


class JosephConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


joseph_convo_c = JosephConvoC("""\
Go visit my friend Azura in Parceon. She knows more about this than
I do. Parceon is located at 24\u00b0N, 28\u00b0E in case you forgot.""", "joseph_c3", False)


class JosephQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global joseph_convo_c
        global joseph_convo_a

        joseph_convo_a.active = False
        joseph_convo_c.active = True


joseph_quest_a = JosephQuestA("To Parceon! [MAIN QUEST]", """\
Ah, Solou! Long time no see! I see you've taken up adventuring.
It must be nice to finally put that spellbook of yours to use!
*Solou and Joseph chat for a while. As mayor of Overshire, Joseph
is already well aware of Celeste being kidnapped.* Ah, so you adventurers
are questing to save his daughter? Well, I happen to know of a person
whose information would prove invaluable to you. Her name is Azura, and
she is the head of the Sorcerer's guild. She has been studying tomes and
has supposedly come up with a possible solution. She lives in a town
called Parceon, located at 24\u00b0N, 28\u00b0E.""", "Joseph", [75, 75], "joseph_q1", False)


# -- Name: Orius -- Town: Valice

# -- Name: Azura -- Town: Parceon
class AzuraConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


azura_convo_a = AzuraConvoA("""\
Hello, I'm Azura, leader of this town and head of the Sorcerer's Guild.
I'm quite busy right now, so please come back later if you wish to speak
to me.""", "azura_c1", True)


class AzuraConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global azura_convo_c

        print('You write down the coordinates of Ambercreek.')
        main.s_input("\nPress enter/return ")
        self.active = False
        azura_convo_c.active = True


azura_convo_b = AzuraConvoB("""\
Hello, I'm Azura, leader of this town and head of the Sorcerer's Guild.
I'm quite busy right now, so please come back later if you wish to speak
to me... Oh, what's that? Joseph of Overshire City sent you? Well in that
case, I suppose that I can take some time off from my duties to speak
to you. What is it that you need? ...I see. I know of a way to rescue
King Harconius II's daughter, as Joseph probably told you. It's quite
dangerous, however - none of the King's men have survived the journey.
Looking at you, however, I see much potential. There is one problem,
however: Our Kingdom has been infiltrated by the Thexus. I have no way
of verifying whether or not you are one of them. Actually, now that I
think about it, perhaps there IS a way... How about this: My father,
Raidon, has been having some problems lately. If you go help him out,
then you will have earned my trust. He lives in the town of Ambercreek, a
village right outside the exit of Barrier Cave. Good luck.""", "azura_c2", False)


class AzuraConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


azura_convo_c = AzuraConvoC("""\
My father, Raidon, lives in the town of Ambercreek at -7\u00b0S, -51\u00b0W. Good luck!""", "azura_c3", False)


# -- Name: Raidon -- Town: Ambercreek
class RaidonConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


raidon_convo_a = RaidonConvoA("""\
""", "raidon_c1", True
)


# ---------------------------------------------------------------------------- #
# SIDE-STORY ARCS

# -- Graveyard Story-arc:
# --- Name: Stewson -- Town: Overshire
class StewsonConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_a = Conversation("""\
Our amazing Kingdom has 6 different regions: Tundra in the northwest, Swamp
in the southeast, Mountains in the northeast, and Desert in the southwest.
The Forest lies in the center, while the Shore surrounds them. There's a
small region somewhere around here that is the cause of much worry and panic
in this town: The Graveyard. Inside lies a dangerous apparition, feared by
all who have seen it. As the captain of the guard, my men and I have tried
and failed countless times to defeat that wretched ghost!""", "stewson_c1", True)


class StewsonQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global stewson_convo_a
        global stewson_convo_b
        units.menacing_phantom.active = True
        stewson_convo_a.active = False
        stewson_convo_b.active = True

    def upon_completing(self):
        global stewson_convo_c
        global rivesh_convo_b
        global rivesh_quest_a

        stewson_convo_c.active = True
        rivesh_convo_b.active = False
        rivesh_quest_a.active = True
        print('-' * save_load.divider_size)
        print('You now have experience defeating ghosts!')
        main.s_input("\nPress enter/return ")


stewson_quest_a = StewsonQuestA('The Shadowy Spirit', """\
I wish someone would do something about this terrible ghost... Hey! You're a
strong adventurer, perhaps you could defeat this phantom? It's at position.
8\u00b0N, -12\u00b0W.""", 'Stewson', [50, 75], "stewson_q1", True)


class StewsonConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_b = StewsonConvoB("""\
Please save us from this monstrous wraith!""", "stewson_c2", False)


class StewsonConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_c = StewsonConvoC("""\
You... you actually defeated it?! Thank you ever so much! Finally my men and
I can rest, and the town is safe! Take this, it is the least our town can
do for your bravery.""", "stewson_c3", False)


class StewsonConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_d = Conversation("""\
Thank you again for your help, adventurer!""", "stewson_c4", False)


# --- Name: Seriph -- Town: Fort Sigil
class SeriphConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


seriph_convo_a = SeriphConvoA("""\
...You actually came to this town? And of your own free will, too?! You are
truly a fool, although I suppose your bravery is admirable.""", "seriph_c1", True
)


class SeriphConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


seriph_convo_b = SeriphConvoB("""\
What?! You're going to try to kill the evil spirit? You're truly stupider
than I thought. I wish you good luck nonetheless.""", "seriph_c2", False)


class SeriphConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


seriph_convo_c = SeriphConvoC("""\
Wuh... you killed it? Thats impossible, that wretched spectre has been haunting
us for decades... But I suppose it must be true, I can't feel its presence anymore.
Thank you hero, we are forever in your debt.""", "seriph_c3", False)


# --- Name: Rivesh -- Town: Fort Sigil
class RiveshConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_a = RiveshConvoA("""\
Welcome, brave adventurer. I'm sure that you've been informed of the
problems around here, so I'd recommend... Oh, what's that? You haven't?
Well in that case, let me tell you. A long time ago, a number of foolish
adventurers, searching for fame and glory, stumbled upon this fort.
Inside, they found a terrifying ghost, which they oh-so-cunningly
defeated -- or so they thought! No, instead the ghost had grown tired
of the pointless battle, and decided to hide in the shadows of the unsuspecting
"heroes". When they least expected it, the ghost possessed them! As
punishment for their foolishness, the evil spirit now forcefully takes a
victim from this town every 10 days and forbids its inhabitants from leaving!""", "rivesh_c1", True)


class RiveshConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_b = RiveshConvoB("""\
Hey... I don't suppose that you have any experience with fighting ghosts,
do you? No? Ok then. If you find someone who has defeated a very menacing
phantom before, please request that they come help us!""", "rivesh_c2", True)


class RiveshConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_c = RiveshConvoC("""\
Help us, young adventurer! You are the only one who can save us from this
terrible spirit!""", "rivesh_c3", False)


class RiveshConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_d = RiveshConvoD("""\
Y-you defeated the evil spirit? Praise Guido's beard! We are free of this
curse! You are forever in our gratitude, young hero!""", "rivesh_q1", False)


class RiveshConvoE(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_e = RiveshConvoE("""\
Thanks again, hero! We are forever indebted to you!""", "rivesh_c4", False)


class RiveshQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global rivesh_convo_a
        global rivesh_convo_b
        global rivesh_convo_c
        global seriph_convo_a
        global seriph_convo_b

        rivesh_convo_a.active = False
        rivesh_convo_b.active = False
        rivesh_convo_c.active = True
        seriph_convo_a.active = False
        seriph_convo_b.active = True
        units.cursed_spectre.active = True

    def upon_completing(self):
        global rivesh_convo_d
        global seriph_convo_b
        global seriph_convo_c

        rivesh_convo_d.active = True
        seriph_convo_b.active = False
        seriph_convo_c.active = True


rivesh_quest_a = RiveshQuestA("The Curse of Fort Sigil", """\
Hey... I don't suppose that you have any experience with fighting ghosts,
do you? Wait, what's that? You defeated the Phantom that was haunting the
Overshire Graveyard!? Well in that case, we may just have a chance!
Please help us, oh please!""", "Rivesh", [200, 200], "rivesh_q1", False)


# ---------------------------------------------------------------------------- #
# SIDEQUESTS

# --ALFRED OF NEARTON--
class AlfredConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_a = AlfredConvoA("""\
It is rumored that a mighty jelly-creature lives south of this very town. 
Supposedly he's been devourering wild animals in the forest at a terrifying
rate, which is causing a lot of trouble for local hunters! And we're worried
that if he gets bored of his food in the forest that he'll come for us!
Unfortunately, the local militia is busy dealing with something else, so we
can't count on them to stop it. I'd be careful around there if I were you.""", "alfred_c1", True)


class AlfredQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global alfred_convo_a
        global alfred_convo_b

        units.master_slime.active = True
        alfred_convo_a.active = False
        alfred_convo_b.active = True

    def upon_completing(self):
        global alfred_convo_c
        global alfred_convo_d

        alfred_convo_c.active = False
        alfred_convo_d.active = True


alfred_quest_a = AlfredQuestA('A Slimy Specimen', """\
...Actually, now that I think about it, do you think you could possibly
dispose of this vile creature? It's located just south of here.""", 'Alfred', [30, 50], "alfred_q1", True)


class AlfredConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_b = AlfredConvoB("""\
Come back here when you defeat the evil Master Slime. Good luck!""", "alfred_c2", False)


class AlfredConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_c = AlfredConvoC("""\
You defeated the evil Master Slime?! Amazing! Now we can sleep easy at night
knowing our animals are safe. Take this, adventurer, you've earned it.""", "aldred_c3", False)


class AlfredConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_d = AlfredConvoD("""\
Greetings, Hero! Good luck on your adventures!""", "alfred_c4", False)


# -- Name: Kyle -- Town: Tripton
class KyleConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


kyle_convo_a = KyleConvoA("""\
Greeting, traveller. I am Kyle, Tripton's Village Elder. You aren't from
Fallville, right? Good. Those stupid Fallvillians need to get away from our
land! It's they're fault they made a town that was so easy to miss! I don't
care if we have to go to war with those dingbats, I'm not leaving this spot!""", "kyle_c1", True
)


class KyleConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


kyle_convo_b = KyleConvoB("""\
Adventurer, we have heard reports that a mighty beast is in our land!
None of our men are willing to risk their lives to stop it. We are doomed.""", "kyle_c2", False)


class KyleConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        # Stands for "Kyle Phrase 3: After Talking"
        global kyle_convo_c
        global kyle_convo_d
        global alden_quest_a
        global alden_convo_b

        kyle_convo_c.active = False
        kyle_convo_d.active = True

        if krystin_convo_d.active:
            alden_quest_a.finished = True
            alden_convo_b.active = False


kyle_convo_c = KyleConvoC("""\
The mighty monster has fallen? Thank god! What's this you say? The Fallvillians
defeated it? I supposed we owe them our lives. Perhaps we should think about
negotiating peace...""", "kyle_c3", False)


class KyleConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


kyle_convo_d = KyleConvoD("Welcome, adventurer, to the town of Tripton!", "kyle_c4", False)


# -- Name: Krystin -- Town: Fallville
class KrystinConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


krystin_convo_a = KrystinConvoA("""\
Hello, I am the Village Elder of Fallville. We don't take kindly to Triptonians
around here, so tell us if you see any. What I don't understand is that the
silly Triptonians blame us for their poor eyesight. It's all their fault, and
they know it!""", "krystin_c1", True)


class KrystinConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


krystin_convo_b = KrystinConvoB("""\
AHHH! Help! There's a m-m-monster out there! Someone go kill it! AHHH!""", "krystin_c2", False)


class KrystinConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        # Stands for "Krystin Phrase 3: After Talking"
        global krystin_convo_d
        global alden_quest_a
        global alden_convo_b

        self.active = False
        krystin_convo_d.active = True

        if kyle_convo_d.active:
            alden_quest_a.finished = True
            alden_convo_b.active = False


krystin_convo_c = KrystinConvoC("""\
What, the monster is dead? Thank goodness! Oh, so the Triptonians killed it?",
Well then... I guess that we owe them our gratitude. Perhaps we should think",
about negotiating peace...""", "krystin_c3", False)


class KrystinConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


krystin_convo_d = KrystinConvoD("""\
Greetings, hero! Welcome to Fallville.""", "krystin_c4", False)


# -- Name: Frederick -- Town: Fallville
class FrederickConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


frederick_convo_a = FrederickConvoA("""\
I hear that there is a wise sage that has taken up residence in a small
cottage southwest of this town. I would go and talk to him, but monsters
have been roaming around the outskirts of town lately and it just isn't safe
to travel anymore.""", "frederick_c1", True
)


class FrederickConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


frederick_convo_b = FrederickConvoB("""\
There's a monster outside of town, and a big one at that! It looks like some
sort of spider... I hope to god our militia can handle it!""", "frederick_c2", False)


class FrederickConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


frederick_convo_c = FrederickConvoC("""\
Thank heavens, the mighty beast has fallen.""", "frederick_c3", False)


# -- Name: Alden -- Town: Small Cottage
class AldenQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global alden_convo_a
        global krystin_convo_a
        global kyle_convo_a
        global krystin_convo_b
        global kyle_convo_b
        global frederick_convo_a
        global frederick_convo_b

        alden_convo_a.active = True
        kyle_convo_a.active = False
        kyle_convo_b.active = True
        krystin_convo_a.active = False
        krystin_convo_b.active = True
        frederick_convo_a.active = False
        frederick_convo_b.active = True
        units.terr_tarant.active = True

    def upon_completing(self):
        global alden_convo_c
        alden_convo_c.active = True


alden_quest_a = AldenQuestA("Stop the Strife", """\
Greetings, adventurer. I'm sure that you have heard of the conflict going on
between the villages of Fallville and Tripton. I have an idea on how to settle
this foul feud, but alas, I cannot perform it due to my old and fragile
state. You, however, appear to be a very young and capable adventurer. Do you
perhaps think that you could help me? I need you to go defend the towns of
Fallville and Tripton from a terrible monster. This is a monster I will be
summoning, of course. Afterwards, spread word in the two towns that an
anonymous warrior from the opposite town defeated it! This should bring an end
to their constant bickering. I will summon the monster at coordinates
-23\u00b0S, -11\u00b0W.""",  'Alden', [175, 200], "alden_q1", True)


class AldenConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alden_convo_a = AldenConvoA("""\
I've summoned the mighty beast. Now hurry up and dispose of it before it causes any damage.""", "alden_c1", False)


class AldenConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alden_convo_b = AldenConvoB("""\
You've defeated him? Good, now go talk to the village elders! Good luck!""", "alden_c2", False)


class AldenConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alden_convo_c = AldenConvoC("""\
Thanks again, hero. You've saved those towns a lot of trouble.""", "alden_c3", False)


# -- Name: Polmor -- Town: Whistumn
class PolmorConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


polmor_convo_a = PolmorConvoA("""\
Our poor daughter! Serena and I have been working on a cure, but
we cannot find anyone stup-I mean brave enough to gather the
resources we need. All is lost if we cannot get the ingredients.""", "polmor_c1", True)


class PolmorConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        # Check the player's inventory for the objects necessary to finish the quest.
        any_fangs = False
        any_scales = False
        any_dust = False

        for item in items.inventory['misc']:
            if item.name == 'Monster Fang':
                any_fangs = True

            elif item.name == 'Serpent Scale':
                any_scales = True

            elif item.name == 'Fairy Dust':
                any_dust = True

        if any_fangs and any_scales and any_dust:
            # Iterate over a copy to prevent problems
            for item in items.inventory['misc'][:]:
                if item.name == 'Monster Fang' and any_fangs:
                    items.inventory['misc'].remove(item)
                    any_fangs = False

                elif item.name == 'Serpent Scale' and any_scales:
                    items.inventory['misc'].remove(item)
                    any_scales = False

                elif item.name == 'Fairy Dust' and any_dust:
                    items.inventory['misc'].remove(item)
                    any_dust = False

            polmor_quest_a.finished = True
            print('-'*save_load.divider_size)

            # TODO!!
            # npcs.polmor.speak()


polmor_convo_b = PolmorConvoB("""\
Please, return once you have obtained one Monster Fang, one Serpent Scale
and one Fairy Dust. You must save our daughter!""", "polmor_c2", False)


class PolmorConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


polmor_convo_c = PolmorConvoC("""\
...Wait, what?! You obtained the items we needed? You are our savior! We owe
our lives to you, you are truly a hero! *He walks over to his wife, and the
two begin mixing the ingredients to make the cure for Hatchnuk's Blight*
At last, we have the cure! Let us not waste time. *The two administer the
medicine to their daughter, and she immediately begins feeling better.* Oh joy
of joys! Our daughter is healed! How can we ever repay you, oh noble adventurer
and vanquisher of the Blight? Here, take this. It is the absolute least that we
can do.""", "polmor_c3", False)


class PolmorQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global serena_convo_b
        global serena_convo_a
        global polmor_convo_b
        global polmor_convo_a

        serena_convo_a.active = False
        serena_convo_b.active = True
        polmor_convo_a.active = False
        polmor_convo_b.active = True

    def upon_completing(self):
        global serena_convo_b
        global serena_convo_c
        global polmor_convo_b

        serena_convo_c.active = True
        serena_convo_b.active = False
        polmor_convo_b.active = False

        print('-'*save_load.divider_size)
        print('Serena and Polmor will now heal you for free if you visit them!')


polmor_quest_a = Quest("Fight Against the Blight", """\
Wait a minute... I am so stupid! According to my calculations, you are the
legendary adventurer of Nearton! Yes, it must be you , adventurer, help our
daughter! The only way to get the ingredients is to defeat several monsters
and collect their remains. Specifically, I need one Fairy Dust, one Serpent
Scale, and one Monster Fang. You're the only one who can save her!""", "Polmor", [450, 450], "polmor_q1", True)


# -- Name: Serena -- Town: Whistumn
class SerenaConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


serena_convo_a = SerenaConvoA("""\
Oh, woe is me! My daughter has fallen ill from a terrible disease! They call
it "Hatchnuk's Blight", and it is very deadly. Oh, what am I to do?
*sobs uncontrollably*""", "serena_c1", True)


class SerenaConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


serena_convo_b = SerenaConvoB("""\
You are a good man, trying to help our daughter! Good luck on your quest!""", "serena_c2", False)


class SerenaConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        units.heal_pcus(1)
        print('-'*save_load.divider_size)
        print('Polmor and Serena get to work on healing your party...')
        main.smart_sleep(2)
        print('Your party has been fully healed.')
        main.s_input("\nPress enter/return ")


serena_convo_c = SerenaConvoC("""\
You are our heroes! Here, allow us to treat your wounds.""", "serena_c3", False)


# -- Name: Matthew -- Town: Lantonum
class MatthewConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global matthew_convo_a
        matthew_convo_a.active = False


matthew_convo_a = MatthewConvoA("""\
*You try to talk to the man in the bar, but he is too busy listening to
music on his 'iSound' to notice you. Suddenly, a peasant walks up behind
him, screams 'Witch!', grabs the iSound, and smashes it to bits on the floor.
He then proceeds to set it on fire and bury the ashes in the dirt behind the
bar.*""", "matt_c1", True)


class MatthewQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global matthew_convo_a
        global matthew_convo_b

        matthew_convo_a.active = False
        matthew_convo_b.active = True

    def upon_completing(self):
        global matthew_convo_e
        matthew_convo_e.active = True


matthew_quest_a = MatthewQuestA('iSounds Good', """\
Dangit, that happens all the time! Those idiots keep calling my iSound MP3
player a witch - this is the fifth one I've gone through this week! The
company that makes them only sells them in Elysium, as nobody in Harconia
could tell an MP3 player from a brick if their life depended on it. Hey, I'll
tell you want: If you go to Cesura, the train town near the border of Harconia
and Elysium, and buy me a new iSound, I will reward you greatly. Remember:
iSounds have watermelons on the back. If you get one with a grapefruit, then
you're just paying a lot of money for a cheap knockoff brand. And definitely
stay away from papaya phones. Can you do that for me?""", "Matthew", [1250, 1250], "matt_q1", True)


class MatthewConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        self.active = False
        items.remove_item("musicbox")


matthew_convo_b = MatthewConvoB("""\
Hello, friend! Have you gotten me a new iSound yet?""", "matt_c2", False)


class MatthewConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        self.active = False


matthew_convo_c = MatthewConvoC("""\
No? That's okay. Just pick one up for me when you get the chance. You can
purchase them at the town of Cesura, located at 123\u00b0N, 58\u00b0E.""", "matt_c3", False)


class MatthewConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global matthew_quest_a
        global matthew_convo_d

        matthew_quest_a.finished = True
        matthew_convo_d.active = False


matthew_convo_d = MatthewConvoD("""\
You have? Wonderful! *He takes the iSound from your hand and pulls out 1250 GP*""", "matt_c4", False)


class MatthewConvoE(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


matthew_convo_e = MatthewConvoE("""\
*He looks quite depressed.*""", "matt_c5", False)


# -- Name: Pime -- Town: Sanguion
class PimeConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def pime_c1_at(self):
        global pime_quest_a

        self.active = False
        pime_quest_a.active = True


pime_convo_a = PimeConvoA("""\
Hello, traveller! You do not look familiar - quick, come inside, it's not been
safe to stay out here for the past few weeks. *Pime ushers you into a tavern
filled with people whom he seems to be quite friendly with. They likewise are
quite kind to you.* My name is Pime. I am the chief of this town, and the head
of Sanguion's militia. As I'm sure you know, me, and all the other people in
this inn, are vampires. Do not be alarmed! We only feast on wild animals and
the dead. As of late, a new group of vampire hunters named the 'Anti-blood Squad'. 
Not only do these terrorists have an extraordinarily uncreative name, but they've 
also been capturing our friends and family and are torturing, ransoming, and even 
killing them! We vampires are not harmful to society, and do not deserve this 
kind of treatment! Our loved ones are dying to those monsters, and we don't have 
anywhere near enough manpower to put a stop to it! What are we to do?!""", "pime_c1", True)


class PimeQuestA(Quest):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, active):
        super().__init__(name, dialogue, q_giver, reward, conv_id, active)

    def upon_starting(self):
        global pime_convo_a
        global pime_convo_b

        pime_convo_a.active = False
        pime_convo_b.active = True
        # units.anti_blood_squad.active = True

    def upon_completing(self):
        global pime_convo_c
        pime_convo_c.active = True


pime_quest_a = PimeQuestA("The Hated Hunter", """\
Hey - you look like quite the seasoned adventurer. Maybe you could help
us! I hope this isn't too much to ask, but could you possibly defeat
these hunters? They're causing us so much pain, we need someone to get rid of 
him.""", "Pime", [1000, 1000], "pime_q1", True)


class PimeConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


pime_convo_b = PimeConvoB("""\
Please deal with those blasted vampire hunters! Their hideout
is located at -68\u00b0S, -93\u00b0W.""", "pime_c3", False)


class PimeConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


pime_convo_c = PimeConvoC("""\
Thank you every so much for ridding us of those vile terrorists! You are
forever in our gratitude!""", "pime_c4", False)


# ----------------------------------------------------------------------------#
# UNIMPORTANT CHARACTERS

# -- Name: Philliard -- Town: Nearton
class PhilliardConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


philliard_convo_a = PhilliardConvoA("""\
Hello, adventurer! Welcome to the Kingdom of Harconia!""", "philliard_c1", True)


# -- Name: Sondalar -- Town: Nearton
class SondalarConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


sondalar_convo_a = SondalarConvoA("""\
Greetings! Say, I haven't seen you in quite a while! I've been travelling
across the Kingdom for the past few years, and haven't had time to say hello.
Let me share some of the knowledge I gained while on my route: every town
has a general store and an inn. Make good use of them! The general store
sells all sorts of helpful equipment, and the further you travel from Nearton,
the better their stock will get! Don't ask why - all I've heard is that it's
supposedly better for business or something. Inns are helpful too. They will,
usually for a fee, heal all your wounds and give you some precious time and
space to write in that travel log you've got there. That's all I've got to say,
catch up with you soon hopefully!""", "sondalar_c1", True)


# -- Name: Saar -- Town: Nearton
class SaarConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


saar_convo_a = SaarConvoA("""\
I haven't really explored too far away from this town. In fact, the only other
towns I've been to are Southford, located at -2\u00b0S, -2\u00b0W, and
Overshire, located at 5\u00b0N, -3\u00b0W. Overshire is a pretty big city,
though - in fact, it's the capital of our Kingdom!""", "saar_c1", True)


# -- Name: Wesley -- Town: Southford
class WesleyConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


wesley_convo_a = WesleyConvoA("""\
Adventurers around this area say that monsters tend to be stronger the farther
from 0\u00b0N, 0\u00b0E that you travel. However, monsters there also give better
loot. Be careful.""", "wesley_c1", True)


# -- Name: Lazaro -- Town: Southford
class LazaroConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


lazaro_convo_a = LazaroConvoA("""\
Greetings, adventurer from Nearton! How do I know who you are, you ask? Well,
I am the oracle of Southford! The Great Divinity told me that you would be 
coming. He gave me a message: "Your position is saved whenever you visit a 
town. If you die, you will return there!" That's what He said. I do not 
understand His words, but I hope they serve, you well.""", "lazaro_c1", True)


# -- Name: Typhen -- Town: Overshire
class TyphenConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


typhen_convo_a = TyphenConvoA("""\
I've heard that when you use healing spells, you restore additional HP based
on your wisdom. And paladins supposedly get an even larger restoration bonus
when they heal!""", "typhen_c1", True)


# -- Name: Jeffery -- Town: Overshire
class JefferyConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


jeffery_convo_a = JefferyConvoA("""\
Have you heard about what happened to Princess Celeste? The news of her
kidnapping is spreading across the kingdom like wildfire! Those blasted
Thexians will pay for this!""", "jeffery_c1", True)


# -- Name: Harthos -- Town: Overshire
class HarthosConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


harthos_convo_a = HarthosConvoA("""\
Welcome to Overshire, stranger! Our Kingdom's capital is pretty big, so try
not to get lost, haha!""", "harthos_c1", True)


# -- Name: Ethos -- Town: Valice
class EthosConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


ethos_convo_a = EthosConvoA("""\
Any smart adventurer would keep track of town coordinates and powerful monsters
in their inventory. If you get lost, check there.""", "ethos_c1", True)


# -- Name: Fly -- Town: New Ekanmar
class FlyConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


fly_convo_a = FlyConvoA("""\
Hello, adventurer! My name is Fly, Duke of Celemia. I'm quite busy right now,
please come back later if you wish to speak to me.""", "fly_c1", True)


# -- Name: Stravi -- Town: New Ekanmar
class StraviConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stravi_convo_a = StraviConvoA("""\
Greetings, young traveller. I am Stravi, Duchess of Celemia. My husband
and I are on important business relating to the recent kidnapping of King
Harconius II's daughter, Celeste. Please return in a few weeks if you wish
to speak to Fly and me. Oh, and whatever you do, do not under ANY
circumstances mention the word 'chandelier' to my husband. It makes him very
upset for some reason.""", "stravi_c1", True)


# -- Name: Caesar -- Town: New Ekanmar
class CaesarConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


caesar_convo_a = CaesarConvoA("""\
*Caesar, Fly's pet strawberry dragon, runs away and hides behind
his owner before you get a chance to converse with him.*""", "caesar_c1", True)


# -- Name: Sakura -- Town: Principalia
class SakuraConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


sakura_convo_a = SakuraConvoA("""\
HALT! State your business! Ah, you want to see the King, do you?
Well, the King is currently in Overshire. Sakura cannot imagine
that he is accepting visitors right now, though. Unless you have
something really important to tell him, such as how to save his
daughter, Sakura doesn't see you talking to him in your future.
Now get out of here, Sakura is busy!""", "sakura_c1", True)


# -- Name: Strathius -- Town: Ravenstone
class StrathiusConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


strathius_convo_a = StrathiusConvoA("""\
Greetings, man! I'm like, Strathius, and I'm a druid. I'm one with like,
nature. I'm gonna give you some helpful advice, man. Monsters can give you
these like, things, that are called \"Status Ailments\" which like, totally
harsh your style brah. Getting muted totally makes your stuff get like totally
lost, so you can't use those radical items you have in your backpack.
Paralyzation makes you totally slow for a while, so you have your
turn later and it's harder to away dog. Weakness makes you like
a total softy, and you won't deal much physical damage, man. Poison
is mega-harsh dude. It makes you take a little bit of damage each,
like, turn. Definitely not cool. Blindness is also totally whack
man - it makes you aim like a total nut and do less pierce damage.
Silence is bad news for mages 'cuz it means you can't use magic for a bit.
Always keep a stash of items to cure these sicknesses man.""", "strathius_c1", True)


# -- Name: Sugulat -- Town: Ambercreek
class SugulatConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


sugulat_convo_a = SugulatConvoA("""\
Greetings! My name is Sugulat, Duke of Chin'tor and legendary digger of
holes. Y'know, you look like a nice guy. I'm going to tell you a little
secret: If you buy a shovel from the general store, you can dig up valuable
gems in certain places! They're all over the place, there's usually at least
one in every area you visit.""", "sugalat_c1", True)


# -- Name: Morrison -- Town: Cesura
class MorrisonConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


morrison_convo_a = MorrisonConvoA("""\
Hello, sir! I'm Morrison, the head engineer of Cesura! I'm a native Elysian,
and have only been here for around a year, so I'm pretty new to this place!
Most of my time is spent making sure that these trains run properly. By the
way, do you know what \"witch\" means? Hythic isn't my first language, and the
townsfolk keep calling me that when I turn on the trains. Witch is a good
thing, right?""", "morrison_c1", True)


# -- Name: Ariver -- Town: Sanguion
class AriverConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


ariver_convo_a = AriverConvoA("""\
*Ariver mistakes you for a vampire hunter and runs quickly into his house,
locking the doors, shutting the windows, and closing the blinds. As you begin
walking away, scratching your head in confusion, you see him look out the
window and walk back outside, having determined you are not a threat at the
moment.*""", "ariver_c1", True)


# -- Name: Fitzgerald -- Town: Valenfall
class FitzgeraldConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


fitz_convo_a = FitzgeraldConvoA("""\
*hic* Pay no attention to the behind behind the curtain! *The man appears to
be quite drunk. You also notice a distinct lack of any curtain nearby.*
*hic* Drop that, you thief! Give me back my penny-loafers! *You slowly walk
away from the raving drunk.*""", "fitz_c1", True)


all_dialogue = [
    solou_convo_a, solou_quest_a,

    rivesh_convo_a, rivesh_convo_b, rivesh_convo_c, rivesh_convo_d, rivesh_convo_e, rivesh_quest_a,

    alfred_convo_a, alfred_convo_b, alfred_convo_c, alfred_convo_d, alfred_quest_a,

    stewson_convo_a, stewson_convo_b, stewson_convo_c, stewson_convo_d, stewson_quest_a,

    kyle_convo_a, kyle_convo_b, kyle_convo_c, kyle_convo_d,

    krystin_convo_a, krystin_convo_b, krystin_convo_c, krystin_convo_d,

    frederick_convo_a, frederick_convo_b, frederick_convo_c,

    joseph_convo_a, joseph_convo_b, joseph_convo_c, joseph_quest_a,

    alden_quest_a, alden_convo_a, alden_convo_b, alden_convo_c,

    azura_convo_a, azura_convo_b, azura_convo_c,

    polmor_convo_a, polmor_convo_b, polmor_convo_c, polmor_quest_a,
    serena_convo_a, serena_convo_b, serena_convo_c,

    matthew_convo_a, matthew_quest_a, matthew_convo_b,
    matthew_convo_c, matthew_convo_d, matthew_convo_e,

    pime_convo_a, pime_quest_a, pime_convo_b, pime_convo_c,

    lazaro_convo_a,
    philliard_convo_a,
    fly_convo_a,
    stravi_convo_a,
    sakura_convo_a,
    sugulat_convo_a,
    raidon_convo_a,
    caesar_convo_a,
    wesley_convo_a,
    seriph_convo_a,
    strathius_convo_a,
    ariver_convo_a,
    fitz_convo_a,
    harthos_convo_a,
    typhen_convo_a,
    sondalar_convo_a,
    morrison_convo_a,
    ethos_convo_a,
    jeffery_convo_a,
    saar_convo_a,
    seriph_convo_b,
    seriph_convo_c
]


def set_active(convo_id, new_state):
    for d in all_dialogue:
        if d.convo_id == convo_id:
            d.active = new_state

            return

    raise Exception(f"{convo_id} is not a valid Conversation ID!")


def serialize_dialogue(path):
    json_dialogue = {}

    for c in all_dialogue:
        if isinstance(c, Quest):
            json_dialogue[c.conv_id] = [c.active, c.started, c.finished]

        else:
            json_dialogue[c.conv_id] = [c.active]

    with open(path, encoding='utf-8', mode='w') as f:
        json.dump(json_dialogue, f, indent=4, separators=(', ', ': '))


def deserialize_dialogue(path):
    global all_dialogue

    with open(path, encoding='utf-8') as f:
        j_log = json.load(f)

    for key in j_log:
        for c in all_dialogue[:]:
            if key == c.conv_id:
                if isinstance(c, Quest):
                    c.active, c.started, c.finished = j_log[key][0], j_log[key][1], j_log[key][2]
                else:
                    c.active = j_log[key][0]


for item1 in copy.copy(globals()):
    if isinstance(globals()[item1], Conversation) and globals()[item1] not in all_dialogue:
        print(f"{item1} not in all_dialogue!")
