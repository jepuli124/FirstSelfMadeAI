def calculateReward(map:list) -> float: #the legend tells that there is a deeply nested if-tree span across a hundred lines. It is mimicing the project "hot oven", locals say.
    reward = 0
    blockCounter = 0
    SpikeCounter = 0
    mapSize = (len(map)* len(map[0]))
    EmptyObjects = [" ", "e", "s"]

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

    if blockCounter > mapSize/4:
        reward += (-blockCounter + (mapSize)/4) * 0.6
    else:
        reward += (blockCounter) * 0.6
    
    if SpikeCounter > mapSize/5:
        reward += (-SpikeCounter + (mapSize)/5) * 0.6
    else:
        reward += (SpikeCounter) * 0.6

    

    return reward