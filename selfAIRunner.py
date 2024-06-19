from selfAI import *
from node import * 

def run(mapSize:tuple, AILayerSize:int = None, AIlayerAmount:int = None, savedAI:str = None, AI:selfAI = None, repeats:int = 0) -> selfAI:
    
    if AI == None:
        if savedAI != None:
            AI = loadAI(savedAI)
        else:
            AI = selfAI()
            AI.makeNewRandomNetwork(AILayerSize, AIlayerAmount)
    newMap = AI.produceMap(mapSize)
    if newMap == None: return None
    mapAsText = outputToObjects(newMap)
    if mapAsText != None:
        writeFile(mapAsText)
    else:
        print("map failed, retrying")
        if repeats > 10:
            if savedAI == None:
                run(mapSize, AILayerSize, AIlayerAmount, savedAI=savedAI, repeats= repeats + 1) 
            return None
        if repeats > 100:
            return None
        run(mapSize, AILayerSize, AIlayerAmount, AI = AI, savedAI=savedAI, repeats= repeats+1)
    if savedAI == None:
        return AI
    return None
    

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

def saveAI(AI: selfAI):
    fileNameCounter = 0
    run = True
    while run:
        try:
            file = open("selfAI/selfAI"+ str(fileNameCounter) +".txt", "xt")
            run = False
        except:
            fileNameCounter += 1

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

def outputToObjects(map: list) -> list:
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
    if twoRandomValues[0] < 0.21:
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
