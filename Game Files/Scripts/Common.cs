﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public class CommonMethods
    {
        public string Input(string prompt)
        {
            Console.Write(prompt);
            return Console.ReadLine();
        }

        public void PrintDivider()
        {
            // Initialize the settings manager
            SavefileManager settings_manager = new SavefileManager();

            Console.WriteLine(new string('-', settings_manager.GetDividerSize()));
        }

        public void PressEnterReturn()
        {
            Input("\nPress enter/return ");
        }

        public List<string> SplitBy79(string the_string, int num = 79)
        {
            List<string> sentences = new List<string>();
            string current_sentence = "";

            foreach (string word in the_string.Split())
            {
                if ((current_sentence + word).Count() > num)
                {
                    sentences.Add(current_sentence);
                    current_sentence = "";
                }

                current_sentence += $"{word} ";

                current_sentence = string.Join("", new List<string>() { current_sentence, word, " " });
            }

            if (current_sentence != "")
            {
                sentences.Add(current_sentence);
            }

            return sentences;
        }

        public bool IsExitString(string the_string)
        {
            List<string> ValidExitStrings = new List<string>() { "e", "x", "exit", "b", "back", "cancel" };

            if (ValidExitStrings.Contains(the_string.ToLower()))
            {
                return true;
            }

            return false;
        }

        public int Clamp(int value, int max, int min)
        {
            return Math.Max(min, Math.Min(max, value));
        }

        public void TextScrollWrite(string the_string, int spacing = 25)
        {
            the_string = string.Join("", new List<string>() { the_string, "\n" });

            int counter = 0;
            foreach (char character in the_string)
            {
                Console.Write(character);

                if (character != ' ' && counter + 1 != the_string.Count())
                {
                    Thread.Sleep(spacing);
                }
            }
        }

        public string TextScrollInput(string the_string, int spacing = 25)
        {
            TextScrollWrite(the_string, spacing);
            return Input(the_string[the_string.Length - 1].ToString());
        }
    }

    public class CEnums
    {
        public enum UnitType { player, monster, boss }
        public enum Status { silence, poison, weakness, blindness, paralyzation, muted, alive, dead }
        public enum Element { fire, water, electric, earth, wind, grass, ice, light, dark, none }
        public enum CharacterClass { warrior, ranger, mage, assassin, paladin, monk, bard }
        public enum MonsterClass { melee, ranged, magic }
        public enum EquipmentType { head, body, legs, weapon, accessory }
        public enum WeaponType { melee, ranged, instrument }

        public string EnumToString(Enum the_enum)
        {
            Dictionary<Enum, string> StatusNameMap = new Dictionary<Enum, string>()
            {
                {Status.silence, "Silence"},
                {Status.poison, "Poison"},
                {Status.weakness, "Weakness"},
                {Status.blindness, "Blindness"},
                {Status.paralyzation, "Paralyzation" },
                {Status.muted, "Muted"},
                {Status.alive, "Alive"},
                {Status.dead, "Dead"},

                {UnitType.player, "Player" },
                {UnitType.monster, "Monster" },
                {UnitType.boss, "Boss" },

                {Element.fire, "Fire"},
                {Element.water, "Water"},
                {Element.electric, "Electric"},
                {Element.earth, "Earth"},
                {Element.wind, "Wind"},
                {Element.grass, "Grass"},
                {Element.ice, "Ice"},
                {Element.light, "Light"},
                {Element.dark, "Dark"},
                {Element.none, "None"},

                {CharacterClass.warrior, "Warrior" },
                {CharacterClass.ranger, "Ranger"},
                {CharacterClass.mage, "Mage"},
                {CharacterClass.assassin, "Assassin"},
                {CharacterClass.paladin, "Paladin"},
                {CharacterClass.monk, "Monk"},
                {CharacterClass.bard, "Bard"},

                {MonsterClass.melee, "Melee" },
                {MonsterClass.ranged, "Ranged" },
                {MonsterClass.magic, "Magic" }
            };

            return StatusNameMap[the_enum];
        }
    }
}
