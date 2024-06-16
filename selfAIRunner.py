import selfAI

def run(mapSize, AILayerSize, AIlayerAmount):
    newAI = selfAI.selfAI()
    newAI.makeNewRandomNetwork(AILayerSize, AIlayerAmount)
    newMap = newAI.produceMap(mapSize)
    mapAsText = outputToObjects(newMap)
    if mapAsText != None:
        writeFile(mapAsText)
    else:
        run(mapSize, AILayerSize, AIlayerAmount)
    return newAI
    

def loadAI():
    try:
        with open("selfAI") as AI:
            pass
    except:
        print("No saved AI")
        file = open("selfAI/AI.txt","xt")
        file.close()
        return None
    
def saveAI(AI):
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
        file.write("matrix: \n")
        for line in matrix:
            for object in line:
                file.write(str(object)+ " ")
            file.write("\n")

    file.write("Network layer size: "+ str(AI.networkLayerSize))

    file.close() 

def outputToObjects(map):
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
        
def writeFile(map):
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