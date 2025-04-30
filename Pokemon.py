class Pokemon(object):
    """Creates Pokemon Object for each Team"""

    def __init__(self, monSection):
    
        self.name = monSection.split("|")[3].split(",")[0]
        self.nickName = ""

        self.alive = True
        self.health = 100

        self.move1 = ""
        self.move2 = ""
        self.move3 = ""
        self.move4 = ""
        self.ability = ""


        self.KOs = 0
        self.passiveKOs = 0
        self.assists = 0
        self.tankHits = 0
        self.participated = False

        self.monsDamagedList = []
        self.damageHits = 0 #Number of times this Pokemon dealt damage in some capasity (direct damage, status DOT, field hazards, etc)
