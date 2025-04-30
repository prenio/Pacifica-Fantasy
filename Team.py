import Pokemon

class Team(object):
    """Creates the team for a player"""

    def __init__(self, player, teamSection):

        self.name = player.replace("|j|☆", "")

        self.p1 = Pokemon.Pokemon(teamSection[0])
        self.p2 = Pokemon.Pokemon(teamSection[1])
        self.p3 = Pokemon.Pokemon(teamSection[2])
        self.p4 = Pokemon.Pokemon(teamSection[3])
        self.p5 = Pokemon.Pokemon(teamSection[4])
        self.p6 = Pokemon.Pokemon(teamSection[5])



        self.team = (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)

        for mon in self.team:
            if mon.name == "Greninja-*":
                mon.name = "Greninja"

        self.teamNames = (self.p1.name, self.p2.name, self.p3.name, self.p4.name, self.p5.name, self.p6.name)


    def updateTeamNickNames(self):
        self.teamNickNames = (self.p1.nickName, self.p2.nickName, self.p3.nickName, self.p4.nickName, self.p5.nickName, self.p6.nickName)





