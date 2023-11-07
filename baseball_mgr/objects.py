from dataclasses import dataclass

@dataclass
class Player:
    fname: str = ""
    lname: str = ""
    pos: str = ""
    ab: int = 0
    hits: int = 0
    avg: float = 0.0

    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    def getBattingAvg(self, hits, ab):
        return round(hits / ab, 3)
    

class Lineup:
    def __init__(self):
        self.__list = []

    def __iter__(self):
        for player in self.__list:
            yield player

    # function adds player
    def addPlayer(self, player):
        self.__list.append(player)
      
    # function removes player
    def removePlayer(self, player):
        self.__list.remove(player)

    # function moves player index on the list
    def movePlayer(self, current, new):
        self.__list.insert(new - 1, self.__list.pop(current - 1))   

    # function gets the index of the player
    def getPlayer(self, number):
        index = number - 1
        return self.__list[index]   

    # function sets new stats to the Player_object attr's
    def editPlayerStats(self, player, ab, hits, avg):
        player.ab = ab
        player.hits = hits
        player.avg = avg
        
    # function sets new pos to the Player_object attr
    def editPlayerPos(self, player, pos):
        player.pos = pos        

    @property
    def count(self):
        return len(self.__list)
