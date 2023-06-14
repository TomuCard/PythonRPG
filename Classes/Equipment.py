import Item


class Equipment(Item):

    def __init__(self, name, item_id, attack_type, base_dmg, requirements, Current_Player, emplacement, equip_effects, unequip_effects, picture):
        self.name = name    # string
        self.item_id = item_id    # int
        self.picture = picture
        self.attack_type = attack_type  # Phys or magical
        self.requirements = requirements    # dict contenant 3 clés "str","dex","int"
        self.owner = Current_Player  # player
        self.emplacement = emplacement
        self.quantity = 1
        self.base_dmg = base_dmg
        self.equip_effects = equip_effects
        self.unequip_effects = unequip_effects
        if emplacement == "weapon 1" or emplacement == "weapon 2":
            self.type = "weapon"
        else:
            self.type = "armour"

    def equip(self):
        equipable = True
        for i in self.requirements.items():
            if self.owner.statistics[i] < self.requirements[i]:
                equipable = False
                print("cannot equip this because the player does not meet its requirements")
        if equipable is True:
            if self.owner.equipped_items[self.emplacement] is not None:
                self.owner.inventory.append(self.owner.equipped_items[self.emplacement])
                exec(self.owner.equipped_items[self.emplacement].unequip_effects)
            exec(self.equip_effects)
            self.owner.equipped_items[self.emplacement] = self
            self.quantity -= 1
        if self.quantity == 0:
            del self
