import Item


class Consumables(Item):

    def __init__(self, name, description, item_id, effect, picture):
        self.name = name
        self.picture = picture
        self.description = description
        self.item_id = item_id
        self.effect = effect
        self.quantity = 1

    def use(self):
        if self.quantity > 0:
            exec(self.effect)
            self.quantity -= 1
        if self.quantity == 0:
            del Current_player.inventory[self.name]