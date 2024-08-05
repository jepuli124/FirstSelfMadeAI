import math

def inspectStructure(map:list) -> list: #the legend tells that there is a deeply nested if-tree span across a hundred lines. It is mimicing the project "hot oven", locals say.
    reward = 0
    blockCounter = 0
    SpikeCounter = 0
    mapSize = (len(map)* len(map[0]))
    EmptyObjects = [" ", "e", "s"]
    endLocation = [-1, -1]
    startLocation = [-1, -1]

    for ylocation, y in enumerate(map):
        for xlocation, x in enumerate(y):
            if x == "b":
                blockCounter += 1
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] not in EmptyObjects: 
                        reward -= 0.2 
                if ylocation <= 1:
                    if map[ylocation - 2][xlocation] not in EmptyObjects: 
                        reward -= 0.1 
                if ylocation <= 2:
                    if map[ylocation - 3][xlocation] == " ": 
                        reward -= 0.1 
                    if map[ylocation - 3][xlocation] == "b": 
                        reward += 0.1 
                if xlocation != len(map[0])-1:
                    if map[ylocation][xlocation+1] == "b": 
                        reward += 0.1 
                if xlocation != 0:
                    if map[ylocation][xlocation-1] == "b": 
                        reward += 0.1 

            if x == "t":
                SpikeCounter += 1
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] not in EmptyObjects: 
                        reward -= 0.6 
                    if ylocation != 1:
                        if map[ylocation - 2][xlocation] not in EmptyObjects: 
                            reward -= 0.2
                if ylocation != len(map)-1:
                    if map[ylocation + 1][xlocation] not in EmptyObjects: 
                        reward -= 0.6 
                
                if xlocation != len(map[0])-1:
                    if map[ylocation][xlocation+1] == "t": 
                        reward += 0.1 
                if xlocation != 0:
                    if map[ylocation][xlocation-1] == "t": 
                        reward += 0.1 

            if x == "e":
                endLocation = [ylocation, xlocation]
                if ylocation != len(map)-1:
                    if map[ylocation + 1][xlocation] == "b": 
                        reward += 1.2 
                    if xlocation != len(map[0])-1:
                        if map[ylocation + 1][xlocation+1] == "b": 
                            reward += 0.8 
                    if xlocation != 0:
                        if map[ylocation + 1][xlocation-1] == "b": 
                            reward += 0.8 
                else:
                    reward -= 2
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] == " ": 
                        reward += 0.4
                    if xlocation != len(map[0])-1:
                        if map[ylocation - 1][xlocation + 1] == " ": 
                            reward += 0.4
                    if xlocation != 0:
                        if map[ylocation - 1][xlocation - 1] == " ": 
                            reward += 0.4

                reward += -2 + (xlocation*0.3)

            if x == "s":
                startLocation = [ylocation, xlocation]
                if ylocation != len(map)-1:
                    if map[ylocation + 1][xlocation] == "b": 
                        reward += 1.2 
                    if xlocation != len(map[0])-1:
                        if map[ylocation + 1][xlocation+1] == "b": 
                            reward += 0.8 
                    if xlocation != 0:
                        if map[ylocation + 1][xlocation-1] == "b": 
                            reward += 0.8
                else:
                    reward -= 2 
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] == " ": 
                        reward += 0.4
                    if xlocation != 0:
                        if map[ylocation - 1][xlocation - 1] == " ": 
                            reward += 0.4
                    if xlocation != len(map[0])-1:
                        if map[ylocation - 1][xlocation + 1] == " ": 
                            reward += 0.4

                if ylocation == 0 or ylocation == len(map)-1:
                    reward -= 1.2
                elif xlocation == 0: 
                    reward += 0.3
                
                reward += 2 - (xlocation*0.3)
    return [reward, blockCounter, SpikeCounter, mapSize, endLocation, startLocation]


def calculateReward1(structureAnalysis: list) -> float: 
    reward = structureAnalysis[0]
    blockCounter = structureAnalysis[1]
    spikeCounter = structureAnalysis[2]
    mapSize = structureAnalysis[3]
    endLocation = structureAnalysis[4]
    startLocation = structureAnalysis[5]

    blockRatio = 1/4 # ratio to map size
    spikeRatio = 1/5 
    rewardMultiplier = 0.4

    if blockCounter > mapSize * blockRatio:
        reward += (-blockCounter + (mapSize * blockRatio)) * rewardMultiplier
    else:
        reward += (blockCounter) * rewardMultiplier
    
    if spikeCounter > mapSize * spikeRatio:
        reward += (-spikeCounter + (mapSize * spikeRatio)) * rewardMultiplier
    else:
        reward += (spikeCounter) * rewardMultiplier
    
    # Negative reward for distance between start and end
    reward += math.dist(startLocation, endLocation) * (-0.1)

    return reward

def calculateReward2(structureAnalysis: list) -> float: 
    reward = structureAnalysis[0]
    blockCounter = structureAnalysis[1]
    spikeCounter = structureAnalysis[2]
    mapSize = structureAnalysis[3]
    endLocation = structureAnalysis[4]
    startLocation = structureAnalysis[5]

    blockRatio = 1/6 # ratio to map size
    spikeRatio = 2/9  
    rewardMultiplier = 0.4

    if blockCounter > mapSize * blockRatio:
        reward += (-blockCounter + (mapSize * blockRatio)) * rewardMultiplier
    else:
        reward += (blockCounter) * rewardMultiplier
    
    if spikeCounter > mapSize * spikeRatio:
        reward += (-spikeCounter + (mapSize * spikeRatio)) * rewardMultiplier
    else:
        reward += (spikeCounter) * rewardMultiplier

    # positive reward for distance between start and end
    reward += math.dist(startLocation, endLocation) * (0.1)

    return reward

def calculateReward3(structureAnalysis: list) -> float: 
    reward = structureAnalysis[0]
    blockCounter = structureAnalysis[1]
    spikeCounter = structureAnalysis[2]
    mapSize = structureAnalysis[3]
    endLocation = structureAnalysis[4]
    startLocation = structureAnalysis[5]

    blockRatio = 1/8 # ratio to map size
    spikeRatio = 1/4  
    rewardMultiplier = 0.4

    if blockCounter > mapSize * blockRatio:
        reward += (-blockCounter + (mapSize * blockRatio)) * rewardMultiplier
    else:
        reward += (blockCounter) * rewardMultiplier
    
    if spikeCounter > mapSize * spikeRatio:
        reward += (-spikeCounter + (mapSize * spikeRatio)) * rewardMultiplier
    else:
        reward += (spikeCounter) * rewardMultiplier
    
    # positive reward for distance between start and end
    reward += math.dist(startLocation, endLocation) * (0.2)

    return reward

def chooseRewardStructure(map: list, difficult: int) -> float:
    structureAnalysis = inspectStructure(map)
    match difficult:
        case 1:
            return calculateReward1(structureAnalysis)
        case 2:
            return calculateReward2(structureAnalysis)
        case 3:
            return calculateReward3(structureAnalysis)