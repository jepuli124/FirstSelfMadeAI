from improvedAI import *
from node import * 
import random, os



def run(AI):
    
    pass

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

def saveAI(AI: improvedAI, fixedName: str = None):
    fileNameCounter = 0
    file = None
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

def trainAI(laps: int, savedAI: str):
    
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
        rewardList = []
        mapList = []
        baseMap = 
        numberOfBestAI = -1
        maxSteps = 200
        bestAI = maxSteps + 1 

        for _ in range(100): 
            AIList.append(currentAI.copy())

        for number, AI in enumerate(AIList):
            AI.mutate()
            steps = AI.solveMap(baseMap, maxSteps)
            rewardList.append(steps/maxSteps)

            if steps < bestAI:
                bestAI = steps
                numberOfBestAI = number
        if numberOfBestAI != -1:
            currentAI = AIList[numberOfBestAI].copy()
        progressBar(times, laps)

    saveAI(currentAI, savedAI)

def progressBar(laps:int, totalLaps:int):
    if laps != totalLaps-1:
        print("Trained", laps+1, "out of", totalLaps, end="\r")
    else:
        print("Trained", laps+1, "out of", totalLaps)
        print("done")
