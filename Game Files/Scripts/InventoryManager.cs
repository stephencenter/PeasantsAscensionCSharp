﻿using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class InventoryManager
    {
        private static Dictionary<CEnums.InvCategory, List<Item>> inventory = new Dictionary<CEnums.InvCategory, List<Item>>()
        {
            { CEnums.InvCategory.quest, new List<Item>() { } },
            { CEnums.InvCategory.consumables, new List<Item>() { } },
            { CEnums.InvCategory.weapons, new List<Item>() { } },
            { CEnums.InvCategory.armor, new List<Item>() { } },
            { CEnums.InvCategory.tools, new List<Item>() { } },
            { CEnums.InvCategory.accessories, new List<Item>() { } },
            { CEnums.InvCategory.misc, new List<Item>() { } }
        };

        private static Dictionary<string, Dictionary<CEnums.EquipmentType, string>> equipment = new Dictionary<string, Dictionary<CEnums.EquipmentType, string>>()
        {
             {
                "_player", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_solou", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_chili", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_chyme", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_storm", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_parsto", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_adorine", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_kaltoh", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },
        };

        public static Dictionary<CEnums.InvCategory, List<Item >> GetInventory()
        {
            return inventory;
        }

        public static Dictionary<CEnums.EquipmentType, Item> GetEquipment(string pcu_id)
        {
            // The equipment dictionary only stores ItemIDs, not actual items. So we have to convert
            // them into real items before we return the dictionary
            Dictionary<CEnums.EquipmentType, Item> real_equipped = new Dictionary<CEnums.EquipmentType, Item>()
            {
                { CEnums.EquipmentType.weapon, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.weapon]) },
                { CEnums.EquipmentType.armor, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.armor]) },
                { CEnums.EquipmentType.accessory, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.accessory]) }
            };

            return real_equipped;
        }

        public static void AddItemToInventory(string item_id)
        {
            Item new_item = ItemManager.FindItemWithID(item_id);
            GetInventory()[new_item.Category].Add(new_item);
        }

        public static void RemoveItemFromInventory(string item_id)
        {
            Item deleted_item = GetInventory()[ItemManager.FindItemWithID(item_id).Category].First(x => x.ItemID == item_id);
            GetInventory()[ItemManager.FindItemWithID(item_id).Category].Remove(deleted_item);
        }
    }
}
