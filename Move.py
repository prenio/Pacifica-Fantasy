class Move(object):
    """Object for Pokemon Move"""

    def __init__(self, team, user, target, moveName, miss):
    
        self.team = team
        self.user = user
        self.target = target
        self.moveName = moveName
        self.miss = miss



