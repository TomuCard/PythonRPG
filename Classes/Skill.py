class Skill:

    def __init__(self, name, description, mana_cost, ratio, base_dmg, requirements):
        self.name = name
        self.description = description
        self.mana_cost = mana_cost
        self.ratio = ratio
        self.base_dmg = base_dmg
        self.requirements = requirements

    def use(self, caster, target):
        dmg = self.base_dmg + self.ratio["int"] * caster.statistics["int"] + self.ratio["str"] * caster.statistics["str"] + self.ratio["dex"] * caster.statistics["dex"]
        target.current_hp -= dmg