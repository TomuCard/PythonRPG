from Classes.Lifeform import Lifeform
import json

class Player(Lifeform):

    def __init__(self, name, max_hp, max_mana, attacks, magics, equipped_items, inventory, statistics):
        self.name = name  # string
        self.max_hp = max_hp  # int
        self.current_hp = max_hp  # int
        self.max_mana = max_mana  # int
        self.current_mana = max_mana  # int
        self.attacks = attacks  # list [attack_name, attack_name, ...]
        self.magics = magics  # list [magic_name, magic_name, ...]
        self.equipped_items = equipped_items  # dict {head : item, body_armour : item, ...}
        self.inventory = inventory  # dict -> {item_id : xxx, item_name : xxx, quantity : x}
        self.statistics = statistics  # dict -> {str : str_amount, dex : dex_amount, int : int_amount}
        self.level = 1
        self.max_xp = 100
        self.current_xp = 0

    def choose_stat(self):
        return

    def level_up(self):
        self.level += 1
        self.max_xp = self.max_xp * 1.2
        self.current_xp -= self.max_xp
        self.max_xp += 10
        self.current_hp = self.max_hp
        self.max_mana += 10
        self.current_mana = self.max_mana

    def add_item_in_inventory(self, item):
        for temp in self.inventory.items():
            if item.name == temp.name:
                item.quantity += 1
            else:
                self.inventory[f'{item.name}'] = item

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)