class Lifeform:

    def __init__(self, name, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp

    def dies(self):
        del self