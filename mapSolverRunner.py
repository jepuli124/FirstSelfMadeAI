from mapSolverAI import *
from node import * 
import random, os, rewardMapSolver

def mapDecoder(mapName:str) -> list:
    try:
        with open("map/"+mapName+".txt") as mapfile:
            map = mapfile.readlines()
            length = 0
            hight = 0
            returnableMap = []
            for line in map:
                hight += 1
                if len(line) > length:
                    length = len(line)

            for line in range(length):
                xAxis = [None] * hight
                returnableMap.append(xAxis.copy())

            for ynumber, y in enumerate(map):
                for xnumber, x in enumerate(y):
                    returnableMap[xnumber][ynumber] = x
        print(returnableMap)
        return returnableMap
    except:
        print("map not found")
        return False

def run(AI):
    print(AI.solveMap(mapDecoder("test"), 50))
    pass

def makeAI(layerSize: int = 10, layerAmount: int = 2) -> mapSolverAI:
    AI = mapSolverAI()
    AI.makeNewRandomNetwork(layerSize, layerAmount)
    return AI

def loadAI(savedAI:str) -> mapSolverAI:
    loadedAI = mapSolverAI()
    layersData = []
    layerData = []
    bridgesData = []
    bridgeData = []
    bridgecubeData = []
    bridgematrixData = []

    try:
        with open("mapSolverAI/"+savedAI+".txt") as AIFile:
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
        return None

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

def saveAI(AI: mapSolverAI, fixedName: str = None):
    fileNameCounter = 0
    file = None
    try:
        os.mkdir("mapSolverAI")
    except FileExistsError:
        pass
    if fixedName == None:
        run = True
        while run:
            try:
                file = open("mapSolverAI/mapSolverAI"+ str(fileNameCounter) +".txt", "xt")
                run = False
            except:
                fileNameCounter += 1
    else:
        try:
            file = open("mapSolverAI/"+ fixedName +".txt", "wt")
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

def trainAI(laps: int, savedAI: str):
    currentAI = None
    try: 
        currentAI = loadAI(savedAI)
        train = True
    except: 
        print("No valid AI given")
        train = False
    if not train:
        return
    
    AIList = [] #expanding scope
    rerun = 0 #needs a value before loop
    mapList = getMaps()
    print("Amount of loaded training maps:", len(mapList))
    
    for times in range(laps):
        AIList = []
        bestAIs = []
        if rerun == 0: 
            baseMap = random.choice(mapList) 
        
        currentBest = -1
        numberOfBestAI = -1
        maxSteps = 15
        bestAI = maxSteps + 1

        

        for _ in range(100): 
            AIList.append(currentAI.copy())
        if len(AIList) == 0:
            print("no AI copies\n")

        for number, AI in enumerate(AIList):
            AI.mutate()
            steps = AI.solveMap(baseMap, maxSteps)

            if steps < bestAI and steps != 0:
                bestAI = steps
                numberOfBestAI = number
                bestAIs = [number]
                if steps <= 3:
                    break
            elif steps == bestAI and steps != 0:
                bestAIs.append(number)

        if len(bestAIs) == 1:
            #if (times+1) % 10 == 0: writeFile(currentAI, baseMap, True, savedAI) # if logs are less necessary
            writeFile(AIList[numberOfBestAI], baseMap, True, savedAI)
            currentAI = AIList[numberOfBestAI].copy()
            rerun = 0
        else: 
            currentBest = -1
            currentReward = -1000
            for x in bestAIs:
                reward = rewardMapSolver.rewardPath(AIList[x])
                if reward > currentReward:
                    currentBest = x
                    currentReward = reward 
            if currentBest != -1:
                writeFile(AIList[currentBest], baseMap, True, savedAI)
                currentAI = AIList[currentBest].copy()
        
            if bestAI == maxSteps + 1: # if bad evolution (no success with map) was made, increasing the learnrate to initiate a evolution easier
                currentAI.learnRate = 0.05 + (0.025 * rerun)
                rerun += 1
                if rerun == 50:
                    rerun = 0
            else:
                currentAI.learnRate = 0.05
                rerun = 0
        
        if (times+1) % 100 == 0: saveAI(currentAI, savedAI)
        progressBar(times, laps)

    saveAI(currentAI, savedAI)

def progressBar(laps:int, totalLaps:int):
    if laps != totalLaps-1:
        print("Trained", laps+1, "out of", totalLaps, end="\r")
    else:
        print("Trained", laps+1, "out of", totalLaps)
        print("done")


def getMaps() -> list:
    listOfMaps = []
    nameOfMaps = os.listdir("mapSolverTrainMaps/")
    for name in nameOfMaps:
        try:
            with open("mapSolverTrainMaps/"+name) as mapfile:
                map = mapfile.readlines()
                processedMap = []
                for y in map:
                    lineOfMap = []
                    for x in y:
                        lineOfMap.append(x)
                    lineOfMap.pop() #deletes the line change marker 
                    processedMap.append(lineOfMap.copy())
                listOfMaps.append(processedMap)
        except:
            print("map not found")

    return listOfMaps

def writeFile(AI: mapSolverAI, map: list, log = False, name = ""):
    fileNameCounter = 0
    run = True
    try:
        if log:
            os.mkdir("mapSolverLogs/"+name)
        else:
            os.mkdir("mapSolverLogs")
    except FileExistsError:
        pass

    while run:
        try:
            if log:
                file = open("mapSolverLogs/"+name+"/mapSolverLog"+ str(fileNameCounter) +".txt", "at")
            else:
                file = open("mapSolverLogs/mapSolverLog"+ str(fileNameCounter) +".txt", "at")
            run = False
        except:
            fileNameCounter += 1
        file.write(str(AI.steps))
        file.write(str(" "))
        file.write(str(AI.currentLocation))
        file.write(str(" "))
        file.write(str(AI.endLocation))
        file.write(str(" "))
        file.write(str(AI.path))
        file.write(str(" "))
        file.write(str(AI.learnRate))
        file.write(str(" "))
        file.write(str(AI.generation))
        file.write(str(" "))
        file.write("\n")   
    file.close()