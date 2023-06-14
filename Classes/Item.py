class Item:

    def __init__(self, name, item_id, description, picture):
        self.item_id = item_id  # int
        self.description = description
        self.name = name  # string
        self.picture = picture
        self.quantity = 1

    def throw(self):
        del self