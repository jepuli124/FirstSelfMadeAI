from selfAI import *
from node import * 

def run(mapSize:tuple,  savedAI:str = None, AI:selfAI = None, repeats:int = 0) -> None:
    
    if AI == None:
        if savedAI != None:
            AI = loadAI(savedAI)
        else:
            AI = makeAI()
            
    newMap = AI.produceMap(mapSize)
    
    if newMap == None:
        return None

    mapAsText = outputToObjects(newMap)

    if mapAsText != None:
        writeFile(mapAsText)
    else:
        print("map failed, retrying")
        if repeats > 10:
            if savedAI == None:
                run(mapSize, savedAI=savedAI, repeats= repeats+1) 
            return None
        if repeats > 100:
            return None
        run(mapSize, AI = AI, savedAI=savedAI, repeats= repeats+1)
    return None
    
def makeAI(AILayerSize:int = 10, AIlayerAmount:int = 5):
    AI = selfAI()
    AI.makeNewRandomNetwork(AILayerSize, AIlayerAmount)
    return AI

def loadAI(savedAI:str) -> selfAI:
    loadedAI = selfAI()
    layerData = []
    bridgesData = []
    bridgeData = []
    lastBridgeLineData = []
    lastBridgeMatrixData = []
    try:
        with open("selfAI/"+savedAI+".txt") as AIFile:
            data = AIFile.readlines()
            state = 0
            
            for line in data:
                try:
                    if line[0] != "-":
                        int(line[0])
                    splitedData = line.split(" ")
                    splitedData.pop()  # removes \n line marker
                    match state:
                        case 0:
                            layerData.append(splitedData)
                        case 1:
                            bridgeData.append(splitedData)
                        case 2:
                            lastBridgeLineData.append(splitedData)
                        case 3:
                            loadedAI.networkLayerSize = int(splitedData[-1])
                            
                except:
                    if line[0].upper() == "L": #layers
                        state = 0 
                    if line[0].upper() == "B": #Bridges
                        if len(bridgeData) >= 1:
                            bridgesData.append(bridgeData.copy())
                        bridgeData = []
                        state = 1 
                    if line[0].upper() == "M": #matrix of last bridge
                        if len(bridgeData) >= 1:
                            bridgesData.append(bridgeData.copy())
                            bridgeData = []
                        if len(lastBridgeLineData) >= 1:
                            lastBridgeMatrixData.append(lastBridgeLineData.copy())
                        lastBridgeLineData = []
                        state = 2 
                    if line[0].upper() == "N": #Network
                        if len(lastBridgeLineData) >= 1:
                            lastBridgeMatrixData.append(lastBridgeLineData.copy())
                            lastBridgeLineData = []
                        state = 3 
                        splitedData = line.split(" ")
                        loadedAI.networkLayerSize = int(splitedData[-1])
    except FileNotFoundError:
        print("No saved AI")
        return None
    loadedAI.layers = makeLayers(layerData)
    loadedAI.bridges = makeBridges(bridgesData)
    loadedAI.bridges.append(makeLastBridge(lastBridgeMatrixData))
    return loadedAI


def makeLayers(data: list) -> list:
    layers = []
    for line in data:
        layer = []
        for cellOfData in line:
            try:
                layer.append(node(float(cellOfData)))
            except:
                print("File read went wrong during layers, couldn't convert data to float")
        layers.append(layer.copy())
    return layers


def makeBridges(data: list) -> list:
    bridges = []
    for matrix in data:
        bridgeMatrix = []
        for line in matrix:
            bridge = []
            for cellOfData in line:
                try:
                    bridge.append((float(cellOfData)))
                except:
                    print("File read went wrong during bridges, couldn't convert data to float")
            bridgeMatrix.append(bridge.copy())
        bridges.append(bridgeMatrix.copy())
    return bridges

def makeLastBridge(data:list) -> list:
    bridge = []
    for matrix in data:
        bridgeMatrix = []
        for line in matrix:
            bridgeLine = []
            for cellOfData in line:
                try:
                    bridgeLine.append((float(cellOfData)))
                except:
                    print("File read went wrong during lastBridge, couldn't convert data to float")
            bridgeMatrix.append(bridgeLine.copy())
        bridge.append(bridgeMatrix.copy())
    return bridge

def saveAI(AI: selfAI, fixedName: str = None):
    fileNameCounter = 0
    file = None
    if fixedName == None:
        run = True
        while run:
            try:
                file = open("selfAI/selfAI"+ str(fileNameCounter) +".txt", "xt")
                run = False
            except:
                fileNameCounter += 1
    else:
        try:
            file = open("selfAI/"+ fixedName +".txt", "wt")
        except:
            print("Couldn't open file")
            return None

    file.write("Layers: \n")
    layerCounter = 0
    for layer in AI.layers:
        layerCounter += 1
        file.write("Layer "+ str(layerCounter)+ "\n")
        for object in layer:
            file.write(str(object.bias)+ " ") 
        file.write("\n")   
    
    file.write("Bridges: \n")
    bridgeCounter = 0
    for bridge in range(len(AI.bridges) - 1):
        bridgeCounter += 1
        file.write("Bridge between layers: "+ str(bridgeCounter)+ " and "+ str(bridgeCounter + 1)+ "\n")
        for matrix in AI.bridges[bridge]:
            for line in matrix:
                file.write(str(line)+ " ") 
            file.write("\n")

    file.write("Last Bridge: \n")
    for matrix in AI.bridges[-1]:
        file.write("Matrix: \n")
        for line in matrix:
            for object in line:
                file.write(str(object)+ " ")
            file.write("\n")

    file.write("Network layer size: "+ str(AI.networkLayerSize))

    file.close() 

def outputToObjects(map: list, forceProduce:bool = False) -> list:
    outputMap = [] 
    twoRandomValues = [0, (0, 0), (0, 0)] 
    for lineNumber, line in enumerate(map):
        outputMap.append([])
        for xNumber, x in enumerate(line):
            if x < 0.2:
                outputMap[lineNumber].append(" ")
            elif x < 0.4:
                outputMap[lineNumber].append("b")
            elif x < 0.6:
                outputMap[lineNumber].append("b")
            elif x < 0.8:
                outputMap[lineNumber].append("t")
            else:
                outputMap[lineNumber].append("t")
            if x > twoRandomValues[0]:
                twoRandomValues[2] = twoRandomValues[1]
                twoRandomValues[1] = (xNumber, lineNumber)
                twoRandomValues[0] = x
    if twoRandomValues[0] < 0.21 and not forceProduce:
        return None
    outputMap[twoRandomValues[1][1]][twoRandomValues[1][0]] = "s"
    outputMap[twoRandomValues[2][1]][twoRandomValues[2][0]] = "e"
    return outputMap
        
def writeFile(map: list):
    fileNameCounter = 0
    run = True
    while run:
        try:
            file = open("map/selfAIMap"+ str(fileNameCounter) +".txt", "xt")
            run = False
        except:
            fileNameCounter += 1
    for line in map:
        for object in line:
            file.write(object) 
        file.write("\n")   
    file.close()

def trainAI(laps: int, savedAI: str):
    
    try: currentAI = loadAI(savedAI)
    except: 
        print("No valid AI given")
        return

    for times in range(laps):
        AIList = []
        mapList = []
        rewardList = []
        bestAI = 0
        baseMap = currentAI.mapStartingPosition((currentAI.networkLayerSize, currentAI.networkLayerSize ))    

        for loopAmount in range(100):
            AIList.append(currentAI.copy())
            AIList[-1].mutate()
            
            mapList.append(outputToObjects(AIList[-1].produceMap((AIList[-1].networkLayerSize -1, AIList[-1].networkLayerSize -1), baseMap), True))
            rewardList.append(calculateReward(mapList[-1]))
            if rewardList[-1] > bestAI:
                bestAI = loopAmount
            currentAI = AIList[bestAI].copy()

        if times+1 % 50 == 0: writeFile(mapList[bestAI])
        progressBar(times, laps)

    saveAI(AIList[bestAI], savedAI)

def progressBar(laps:int, totalLaps:int):
    if laps != totalLaps-1:
        print("Made", laps+1, "out of", totalLaps, end="\r")
    else:
        print("Made", laps+1, "out of", totalLaps)
        print("done")


def calculateReward(map:list) -> float: #the legend tells that there is a deeply nested if-tree span across a hundred lines. It is mimicing a hot oven, locals say.
    reward = 0
    blockCounter = 0
    SpikeCounter = 0
    mapSize = (len(map)* len(map[0]))


    for ylocation, y in enumerate(map):
        for xlocation, x in enumerate(y):
            if x == "b":
                blockCounter += 1
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] != " ": 
                        reward -= 0.2 
                    if ylocation != 1:
                        if map[ylocation - 2][xlocation] != " ": 
                            reward -= 0.1 
                if xlocation != len(map[0])-1:
                    if map[ylocation][xlocation+1] == "b": 
                        reward += 0.1 
                if xlocation != 0:
                    if map[ylocation][xlocation-1] == "b": 
                        reward += 0.1 

            if x == "t":
                SpikeCounter += 1
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] != " ": 
                        reward -= 0.6 
                    if ylocation != 1:
                        if map[ylocation - 2][xlocation] != " ": 
                            reward -= 0.2
                if ylocation != len(map)-1:
                    if map[ylocation + 1][xlocation] != " ": 
                        reward -= 0.6 
                
                if xlocation != len(map[0])-1:
                    if map[ylocation][xlocation+1] == "t": 
                        reward += 0.1 
                if xlocation != 0:
                    if map[ylocation][xlocation-1] == "t": 
                        reward += 0.1 

            if x == " ":
                if ylocation != 0:
                    if map[ylocation - 1][xlocation] == " ": 
                        reward += 0.2 

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

                reward += -2 + (xlocation*0.2)

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

                if ylocation == 0 or xlocation == 0:
                    reward -= 0.2
                else:
                    reward += 2 - (xlocation*0.1)

    if blockCounter > mapSize/3:
        reward += (-blockCounter + (mapSize)/3) * 0.1
    else:
        reward += (blockCounter - (mapSize)/3) * 0.1
    
    if SpikeCounter > mapSize/5:
        reward += (-SpikeCounter + (mapSize)/5) * 0.1
    else:
        reward += (SpikeCounter - (mapSize)/5) * 0.1

    

    return reward