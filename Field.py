class Field(object):
    #An object for the entire field. Divided into 3 parts, your side, opponents side, entire field.
    #Your side and opponent side can have leech seed, tailwind, stealth rocks, etc. Only hits one side
    #Entire field includes weather, terrain, trick room, etc. Affects entire field.

    def __init__(self):

        self.p1side = []
        self.p2side = []
        self.wholeField = []

    def addEffect(self, side, effectName, creator):
        if side == "wholeField":
            self.wholeField.append(fieldEffect(effectName, creator))
        if side == "p1":
            self.p1side.append(fieldEffect(effectName, creator))
        if side == "p2":
            self.p2side.append(fieldEffect(effectName, creator))






class fieldEffect(object):
    #An object for the entire field. Divided into 3 parts, your side, opponents side, entire field.
    #Your side and opponent side can have leech seed, tailwind, stealth rocks, etc. Only hits one side
    #Entire field includes weather, terrain, trick room, etc. Affects entire field.

    def __init__(self, effectName, creator):

        self.effectName = effectName
        self.creator = creator

