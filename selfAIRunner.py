from selfAI import *
from node import * 
from multiprocessing import Pool
import rewardV1, rewardV2, os, random

def run(mapSize:tuple,  savedAI:str = None, AI:selfAI = None, repeats:int = 0, mode: int = 1) -> None:
    
    if AI == None:
        if savedAI != None:
            AI = loadAI(savedAI)
        else:
            AI = makeAI()
    AI.input = [mode]
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
                run(mapSize, savedAI=savedAI, repeats= repeats+1, mode = mode) 
            return None
        if repeats > 100:
            return None
        run(mapSize, AI = AI, savedAI=savedAI, repeats= repeats+1, mode = mode)
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
    lastBridgeMatrixData = []
    lastBridgeCubeData = []
    lastBridges = []
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
                            lastBridgeMatrixData.append(splitedData)
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
                    if line[0].upper() == "C":
                        if len(lastBridgeMatrixData) >= 1:
                            lastBridgeCubeData.append(lastBridgeMatrixData.copy())
                        lastBridgeMatrixData = []
                        if len(lastBridgeCubeData) >= 1:
                            lastBridges.append(lastBridgeCubeData.copy())
                        lastBridgeCubeData = []
                    if line[0].upper() == "M": #matrix of last bridge
                        if len(bridgeData) >= 1:
                            bridgesData.append(bridgeData.copy())
                            bridgeData = []
                        if len(lastBridgeMatrixData) >= 1:
                            lastBridgeCubeData.append(lastBridgeMatrixData.copy())
                        lastBridgeMatrixData = []
                        state = 2 
                    if line[0].upper() == "N": #Network
                        if len(lastBridgeMatrixData) >= 1:
                            lastBridgeCubeData.append(lastBridgeMatrixData.copy())
                            lastBridgeMatrixData = []
                        if len(lastBridgeCubeData) >= 1:
                            lastBridges.append(lastBridgeCubeData.copy())
                        lastBridgeCubeData = []
                        state = 3 
                        splitedData = line.split(" ")
                        loadedAI.networkLayerSize = int(splitedData[-1])
    except FileNotFoundError:
        print("No saved AI")
        return None
    loadedAI.layers = makeLayers(layerData)
    
    loadedAI.bridges = makeBridges(bridgesData)
    
    loadedAI.bridges.extend(makeLastBridge(lastBridges))
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
    bridges = []
    for cube in data:
        bridgeCube = []
        for matrix in cube:
            bridgeMatrix = []
            for line in matrix:
                bridgeLine = []
                for cellOfData in line:
                    try:
                        bridgeLine.append((float(cellOfData)))
                    except:
                        print("File read went wrong during lastBridge, couldn't convert data to float")
                bridgeMatrix.append(bridgeLine.copy())
            bridgeCube.append(bridgeMatrix.copy())
        bridges.append(bridgeCube.copy())

    return bridges

def saveAI(AI: selfAI, fixedName: str = None):
    fileNameCounter = 0
    file = None
    try:
        os.mkdir("selfAI")
    except FileExistsError:
        pass
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
    for bridge in range(len(AI.bridges) - 2):
        bridgeCounter += 1
        file.write("Bridge between layers: "+ str(bridgeCounter)+ " and "+ str(bridgeCounter + 1)+ "\n")
        for matrix in AI.bridges[bridge]:
            for line in matrix:
                file.write(str(line)+ " ") 
            file.write("\n")

    for last in range(2):
        file.write("Cube: \n")
        for matrix in AI.bridges[-2+last]:
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
        
def writeFile(map: list, log = False, name = ""):
    fileNameCounter = 0
    run = True
    try:
        if log:
            os.mkdir("map/"+name)
        else:
            os.mkdir("map")
    except FileExistsError:
        pass

    while run:
        try:
            if log:
                file = open("map/"+name+"/selfAIMap"+ str(fileNameCounter) +".txt", "xt")
            else:
                file = open("map/selfAIMap"+ str(fileNameCounter) +".txt", "xt")
            run = False
        except:
            fileNameCounter += 1
    for line in map:
        for object in line:
            file.write(object) 
        file.write("\n")   
    file.close()

def trainAI(laps: int, savedAI: str, mode: int = 1):
    
    try: 
        currentAI = loadAI(savedAI)
        train = True
    except: 
        print("No valid AI given")
        train = False
    if not train:
        return
    
    AIList = [] #expanding scope
    
    for times in range(laps):
        AIList = []
        mapList = []
        rewardList = []
        difficulty = 1 if mode == 1 else random.randint(1, 3)  
        baseMap = currentAI.mapStartingPosition((currentAI.networkLayerSize, currentAI.networkLayerSize ))    
        numberOfBestAI = -1
        bestAI = -100 

        for _ in range(100): 
            AIList.append(currentAI.copy())
        
        # seperated from below for the possibility of multiprocessing, currently slower than nottreadhing // i'm probably not doing it right.
        # with Pool(100) as pool:
        #     AIList = pool.map(currentAI.copy, range(100))
        #     AIList = pool.map(mutater, AIList)

        for number, AI in enumerate(AIList):
            AI.mutate()
            AI.input = [difficulty] 
            producedMap = outputToObjects(AI.produceMap((AI.networkLayerSize -1, AI.networkLayerSize -1), baseMap), True)
            if mode == 1:
                reward = rewardV1.calculateReward(producedMap)
            elif mode == 2:
                reward = rewardV2.chooseRewardStructure(producedMap, difficulty)
            rewardList.append(reward)
            mapList.append(producedMap)

            if reward > bestAI:
                bestAI = reward
                numberOfBestAI = number
        if numberOfBestAI != -1:
            currentAI = AIList[numberOfBestAI].copy()
        if (times+1) % 50 == 0: writeFile(mapList[numberOfBestAI], True, savedAI)
        if (times) % 500 == 0: saveAI(currentAI, savedAI)
        progressBar(times, laps)

    saveAI(currentAI, savedAI)

def mutater(AI: selfAI) -> selfAI:
    AI.mutate()
    return AI

def progressBar(laps:int, totalLaps:int):
    if laps != totalLaps-1:
        print("Trained", laps+1, "out of", totalLaps, end="\r")
    else:
        print("Trained", laps+1, "out of", totalLaps)
        print("done")


