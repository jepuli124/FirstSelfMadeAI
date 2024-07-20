from mapSolverAI import *
from node import * 

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
    bridgetesseractData = []
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
                        if len(bridgeData) >= 1:
                            bridgesData.append(bridgeData.copy())
                        bridgeData = []
                        state = 1 

                    if line[0].upper() == "M": #Matrix of a bridge
                        if len(bridgematrixData) >= 1:
                            bridgecubeData.append(bridgematrixData.copy())
                        bridgematrixData = []
                    if line[0].upper() == "C": #Cube of a bridge
                        if len(bridgecubeData) >= 1:
                            bridgetesseractData.append(bridgecubeData.copy())
                        bridgecubeData = []
                    if line[0].upper() == "T": #Tesseract of a bridge
                        if len(bridgetesseractData) >= 1:
                            bridgeData.append(bridgetesseractData.copy())
                        bridgetesseractData = []
                    
                    if line[0].upper() == "N": #Network 
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
                    print("File read went wrong during layers, couldn't convert data to float")
            layerMatrix.append(layerLine.copy())
        layers.append(layerMatrix.copy())
    return layers


def makeBridges(data: list) -> list:
    bridges = []
    for cube in data:
        bridgeCube = []
        for matrix in cube:
            bridgeMatrix = []
            for line in matrix:
                bridge = []
                for cellOfData in line:
                    try:
                        bridge.append((float(cellOfData)))
                    except:
                        print("File read went wrong during bridges, couldn't convert data to float")
                bridgeMatrix.append(bridge.copy())
            bridgeCube.append(bridgeMatrix.copy())
        bridges.append(bridgeCube.copy())
    return bridges

def saveAI(AI: mapSolverAI, fixedName: str = None):
    fileNameCounter = 0
    file = None
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
        tesseractCounter = 0
        for tesseract in bridge:
            tesseractCounter += 1
            file.write("Tesseract "+ str(tesseractCounter)+ "\n")
            cubeCounter = 0
            for cube in tesseract:
                cubeCounter += 1
                file.write("Cube "+ str(cubeCounter)+ "\n")
                for matrix in cube:
                    for line in matrix:
                        file.write(str(line)+ " ") 
                    file.write("\n")

    file.write("Network layer size: "+ str(AI.networkLayerSize))

    file.close() 


AI = loadAI("mapSolverAI1")
print(AI)
saveAI(AI, "mapSolverAI1 copy")