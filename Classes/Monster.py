class Monster():

    def __init__(self, name,hp, max_hp, attacks, statistics, velocity, defence, level):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = max_hp
        self.attacks = attacks
        self.statistics = statistics
        self.velocity = velocity
        self.defence = defence

    def damage (self, amount) :
        self.hp -= amount