import pandas as pd
import numpy as np
import requests
import Team, Pokemon, Field, Move


def getLogData(replay):
    url = replay + ".log"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        return data
    else:
        print("Returned a " + str(response.status_code))

def SectionLog(replay):
    data = getLogData(replay)
    dataList = data.split("\n")
    tblOfContents = {}
    tblOfContents["PlayersSection"] = dataList[:2]
    teamIndex, startIndex = dataList.index('|clearpoke'), dataList.index('|teampreview'),
    tblOfContents["TeamPreviewSection"] = dataList[teamIndex+1:startIndex]
    tblOfContents["BattleSection"] = dataList[dataList.index('|start')-1:]
    return(tblOfContents)

def ParseBattle(battleSection):
    listOfTurns = []
    turnDetails = []
    turnNo = 0
    for line in battleSection:
        if line[:3] != "|j|" and line[:3] != "|l|" and line[:4] != "|t:|" and line[:6] != "|start" and line != "|":
            if line[:5] == "|win|":
                listOfTurns.append((turnNo, turnDetails))
                break
            turnDetails.append(line)
            if line[:6] == "|turn|":
                listOfTurns.append((turnNo, turnDetails))
                turnNo += 1
                turnDetails = []
    return listOfTurns



def PlayBattle(tblOfContents):
    team1 = Team.Team(tblOfContents["PlayersSection"][0], tblOfContents["TeamPreviewSection"][0:6])
    team2 = Team.Team(tblOfContents["PlayersSection"][1], tblOfContents["TeamPreviewSection"][6:])
    field = Field.Field()
    currentMove = None
    


    listOfTurns = ParseBattle(tblOfContents["BattleSection"])








    active1 = None
    active2 = None
    attacker = None
    target = None

    i = 0
    for turn in listOfTurns:
        for turnDetail in turn[1]:
            print(turnDetail)

            if "|move|p1a" in turnDetail:
                currentMove = Move.Move(team1, active1, active2, turnDetail.replace("|move|p1a: ", "").split("|")[1], "[miss]" in turnDetail)
            if "|move|p2a" in turnDetail:
                currentMove = Move.Move(team2, active2, active1, turnDetail.replace("|move|p2a: ", "").split("|")[1], "[miss]" in turnDetail)





            if "|switch|p1a" in turnDetail:
                team1Index = team1.teamNames.index(turnDetail.replace("|switch|p1a: ", "").split("|")[1].split(",")[0])
                active1 = team1.team[team1Index]

                if not team1.team[team1Index].participated:
                    team1.team[team1Index].nickName = turnDetail.replace("|switch|p1a: ", "").split("|")[0].split(",")[0]
                    team1.team[team1Index].participated = True
                    team1.updateTeamNickNames()
            elif "|switch|p2a" in turnDetail:
                team2Index = team2.teamNames.index(turnDetail.replace("|switch|p2a:", "").split("|")[1].split(",")[0])
                active2 = team2.team[team2Index]
                
                if not team2.team[team2Index].participated:
                    team2.team[team2Index].nickName = turnDetail.replace("|switch|p2a: ", "").split("|")[0].split(",")[0]
                    team2.team[team2Index].participated = True
                    team2.updateTeamNickNames()

            elif "faint|p1a" in turnDetail:
                team1Index = team1.teamNickNames.index(turnDetail.replace("|faint|p1a: ", "").split(",")[0])
                team1.team[team1Index].alive = False
            elif "faint|p2a" in turnDetail:
                team2Index = team2.teamNickNames.index(turnDetail.replace("|faint|p2a: ", "").split(",")[0])
                team2.team[team2Index].alive = False



            elif "|-damage|p1a" in turnDetail: 
                team1Index = team1.teamNickNames.index(turnDetail.replace("|-damage|p1a: ", "").split("|")[0])
                if "0 fnt" in turnDetail:
                    team1.team[team1Index].health = 0
                else:
                    team1.team[team1Index].health = int(turnDetail.replace("|-damage|p1a: ", "").split("|")[1].split("/")[0])  #check to see if it works, otherwise will need to reconnect attacker -> team1 pokemon (replace with team1.team[team1Index)]
                if team1.team[team1Index].health > 0:
                    team1.team[team1Index].tankHits += 1


                if "[from]" in turnDetail:
                    if turnDetail.split("[from] ")[1] in field.p1side:
                        team2Index = team2.teamNickNames.index(currentMove.user.nickName)
                        team2.team[team2Index].damageHits += 1
                        if team1.team[team1Index].nickName not in team2.team[team2Index].monsDamagedList:
                            team2.team[team2Index].monsDamagedList.append(team1.team[team1Index].nickName)


            elif "|-damage|p2a" in turnDetail: 
                team2Index = team2.teamNickNames.index(turnDetail.replace("|-damage|p2a: ", "").split("|")[0])
                if "0 fnt" in turnDetail:
                    team2.team[team2Index].health = 0
                else:
                    team2.team[team2Index].health = int(turnDetail.replace("|-damage|p2a: ", "").split("|")[1].split("/")[0])  #check to see if it works, otherwise will need to reconnect attacker -> team1 pokemon (replace with team1.team[team1Index)]
                if team2.team[team2Index].health > 0:
                    team2.team[team2Index].tankHits += 1


                if "[from]" in turnDetail:
                    if turnDetail.split("[from] ")[1] in field.p1side:
                        team2Index = team2.teamNickNames.index(currentMove.user.nickName)
                        team2.team[team2Index].damageHits += 1
                        if team1.team[team1Index].nickName not in team2.team[team2Index].monsDamagedList:
                            team2.team[team2Index].monsDamagedList.append(team1.team[team1Index].nickName)





            elif "-sidestart|p1:" in turnDetail:
                if currentMove.moveName == turnDetail.split(": ")[2] and "move:" in turnDetail:
                    field.addEffect("p1", turnDetail.split(": ")[2], currentMove.user)

            elif "-sidestart|p2:" in turnDetail:
                if currentMove.moveName == turnDetail.split(": ")[2] and "move:" in turnDetail:
                    field.addEffect("p2", turnDetail.split(": ")[2], currentMove.user)



            elif "-weather" in turnDetail:
                if "[upkeep]" not in turnDetail:
                    if "p1a: " in turnDetail:
                        team1Index = team1.teamNickNames.index((turnDetail.split(": ")[-1]))
                        field.addEffect("wholeField", "p1a", team1.team[team1Index])
                    if "p2a: " in turnDetail:
                        team2Index = team2.teamNickNames.index((turnDetail.split(": ")[-1]))
                        field.addEffect("wholeField", "p2a", team2.team[team2Index])


                #Add case for "|move|"












            lastDetail = turnDetail












        i += 1
    test3=3










tblOfContents = SectionLog("https://replay.pokemonshowdown.com/gen9draft-2262951572")
PlayBattle(tblOfContents)
