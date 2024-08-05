from improvedAI import *
from node import * 
import rewardV1, rewardV2, os




def run(mapSize:tuple,  savedAI:str = None, AI:improvedAI = None, repeats:int = 0, mode: int = 1) -> None:
    
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
                run(mapSize, savedAI=savedAI, repeats= repeats+1, mode=mode) 
            return None
        if repeats > 100:
            return None
        run(mapSize, AI = AI, savedAI=savedAI, repeats= repeats+1, mode=mode)
    return None

def makeAI(layerSize: int = 10, layerAmount: int = 2) -> improvedAI:
    AI = improvedAI()
    AI.makeNewRandomNetwork(layerSize, layerAmount)
    return AI

def loadAI(savedAI:str) -> improvedAI:
    loadedAI = improvedAI()
    layersData = []
    layerData = []
    bridgesData = []
    bridgeData = []
    bridgecubeData = []
    bridgematrixData = []
    noAI = False
    try:
        with open("improvedAI/"+savedAI+".txt") as AIFile:
            data = AIFile.readlines()
            state = 0
            datacheck = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
            for line in data:
                if line[0] in datacheck:
                    splitedData = line.split(" ")
                    splitedData.pop()  # removes \n line marker
                    match state:
                        case 0:
                            layerData.append(splitedData)
                        case 1:
                            bridgematrixData.append(splitedData)      
                else:
                    if line[0].upper() == "L": #layers
                        if len(layerData) >= 1:
                            layersData.append(layerData.copy())
                        layerData = []
                        state = 0 
                    if line[0].upper() == "B": #Bridges
                        if len(layerData) >= 1:
                            layersData.append(layerData.copy())
                        layerData = []
                        if len(bridgematrixData) >= 1:
                            bridgecubeData.append(bridgematrixData.copy())
                        bridgematrixData = []
                        if len(bridgecubeData) >= 1:
                            bridgeData.append(bridgecubeData.copy())
                        bridgecubeData = []
                        if len(bridgeData) >= 1:
                            bridgesData.append(bridgeData.copy())
                        bridgeData = []
                        
                        state = 1 

                    if line[0].upper() == "M": #Matrix of a bridge
                        if len(bridgematrixData) >= 1:
                            bridgecubeData.append(bridgematrixData.copy())
                        bridgematrixData = []
                    if line[0].upper() == "C": #Cube of a bridge
                        if len(bridgematrixData) >= 1:
                            bridgecubeData.append(bridgematrixData.copy())
                        bridgematrixData = []
                        if len(bridgecubeData) >= 1:
                            bridgeData.append(bridgecubeData.copy())
                        bridgecubeData = []
                    
                    if line[0].upper() == "N": #Network 
                        if len(bridgematrixData) >= 1:
                            bridgecubeData.append(bridgematrixData.copy())
                        bridgematrixData = []
                        if len(bridgecubeData) >= 1:
                            bridgeData.append(bridgecubeData.copy())
                        bridgecubeData = []
                        if len(bridgeData) >= 1:
                            bridgesData.append(bridgeData.copy())
                        bridgeData = []
                        splitedData = line.split(" ")
                        loadedAI.networkLayerSize = int(splitedData[-1])

    except FileNotFoundError:
        print("No saved AI")
        noAI = True
    if noAI: return 

    loadedAI.layers = makeLayers(layersData)
    loadedAI.bridges = makeBridges(bridgesData)

    return loadedAI


def makeLayers(data: list) -> list:
    layers = []
    for matrix in data:
        layerMatrix = []
        for line in matrix:
            layerLine = []
            for cellOfData in line:
                try:
                    layerLine.append(node(float(cellOfData)))
                except:
                    print("File read went wrong during layers, couldn't convert data to float: ", cellOfData)
            layerMatrix.append(layerLine.copy())
        layers.append(layerMatrix.copy())
    return layers


def makeBridges(data: list) -> list:
    bridges = []
    for tesseract in data:
        bridgeTesseract = []
        for cube in tesseract:
            bridgeCube = []
            for matrix in cube:
                bridgeMatrix = []
                for line in matrix:
                    bridge = []
                    for cellOfData in line:
                        try:
                            bridge.append((float(cellOfData)))
                        except:
                            print("File read went wrong during bridges, couldn't convert data to float: ", cellOfData)
                    bridgeMatrix.append(bridge.copy())
                bridgeCube.append(bridgeMatrix.copy())
            bridgeTesseract.append(bridgeCube.copy())
        bridges.append(bridgeTesseract.copy())
    return bridges

def saveAI(AI: improvedAI, fixedName: str = None):
    fileNameCounter = 0
    file = None
    try:
        os.mkdir("improvedAI")
    except FileExistsError:
        pass
    if fixedName == None:
        run = True
        while run:
            try:
                file = open("improvedAI/improvedAI"+ str(fileNameCounter) +".txt", "xt")
                run = False
            except:
                fileNameCounter += 1
    else:
        try:
            file = open("improvedAI/"+ fixedName +".txt", "wt")
        except:
            print("Couldn't open file")
            return None

    file.write("Layers: \n")
    layerCounter = 0
    for layer in AI.layers:
        layerCounter += 1
        file.write("Layer "+ str(layerCounter)+ "\n")
        for line in layer:
            for object in line:
                file.write(str(object.bias)+ " ") 
            file.write("\n")   
    
    file.write("Bridges: \n")
    bridgeCounter = 0
    for bridge in AI.bridges:
        bridgeCounter += 1
        file.write("Bridge "+ str(bridgeCounter)+ "\n")
        cubeCounter = 0
        for cube in bridge:
            cubeCounter += 1
            file.write("Cube "+ str(cubeCounter)+ "\n")
            matrixCounter = 0
            for matrix in cube:
                matrixCounter += 1
                file.write("Matrix "+ str(matrixCounter)+ "\n")
                for line in matrix:
                    for object in line:
                        file.write(str(object)+ " ") 
                    file.write("\n")

    file.write("Network layer size: "+ str(AI.networkLayerSize))

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

def progressBar(laps:int, totalLaps:int):
    if laps != totalLaps-1:
        print("Trained", laps+1, "out of", totalLaps, end="\r")
    else:
        print("Trained", laps+1, "out of", totalLaps)
        print("done")

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
                file = open("map/"+name+"/improvedAIMap"+ str(fileNameCounter) +".txt", "xt")
            else:
                file = open("map/improvedAIMap"+ str(fileNameCounter) +".txt", "xt")
            run = False
        except:
            fileNameCounter += 1
    for line in map:
        for object in line:
            file.write(object) 
        file.write("\n")   
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