import random
from node import *

class mapSolverAI():
    def __init__(self):
        self.steps = 0
        self.layers = [] 
        self.bridges = []   
        self.output = [0, 0, 0, 0, 0]  #these repesent actions, 0 = left, 1 = up, 2 = right, 3 = Down, 4 = do nothing
        self.path = []
        self.networkLayerSize = 0

    def makeNewRandomNetwork(self, layerSize: int, layerAmount: int):
        for _ in range(layerAmount):
            layer = []
            bridge = []
            for z in range(layerSize):
                layerLine = []
                bridgeCube = []
                for y in range(layerSize):
                    layerLine.append(node(random.random()/8))
                    bridgeMatrix = []
                    for x in range(layerSize): # bridge to each other node in the next tier
                        bridgeLine = []
                        for fourthDimension in range(layerSize): #Legendary fifth for loop in row
                            bridgeLine.append(random.random()/4)
                        bridgeMatrix.append(bridgeLine.copy())
                    bridgeCube.append(bridgeMatrix.copy())
                layer.append(layerLine.copy())
                bridge.append(bridgeCube.copy())
            self.layers.append(layer.copy())
            self.bridges.append(bridge)
        self.networkLayerSize = layerSize
    
    def decide(self, input: list):

        self.calculateInputToTier(input, self.layers[0])
        for layer in range(len(self.layers)-1):
            self.calculateNextTier(self.layers[layer], self.layers[layer + 1], self.bridges[layer])
        self.calculateOutput(self.layers[-1], self.bridges[-1])
    
    def calculateInputToTier(self, previousTier: list, nextTier: list):
        for yNext in nextTier:
            for xNext in yNext:
                xNext.output = 0
                sum = 0
                counter = 0
                for y in previousTier:
                    for x in y:
                        sum += x
                        counter += 1
                sum /= counter
                if sum >= xNext.bias:
                    xNext.output = sum - xNext.bias

    def calculateNextTier(self, previousTier: list, nextTier: list, layerBridge: list):
        for yLocationNext, yNext in enumerate(nextTier):
            for xLocationNext, xNext in enumerate(yNext):
                xNext.output = 0
                sum = 0
                counter = 0
                for yLocation, y in enumerate(previousTier):
                    for xLocation, x in enumerate(y):
                        sum += (layerBridge[yLocationNext][xLocationNext][yLocation][xLocation] * x.output) 
                        counter += 1
                sum /= counter
                if sum >= xNext.bias:
                    xNext.output = sum - xNext.bias

    def calculateOutput(self, previousTier: list, layerBridge: list):
        for xLocationNext, xNext in enumerate(self.output):
            sum = 0
            counter = 0
            for yLocation, y in enumerate(previousTier):
                for xLocation, x in enumerate(y):
                    sum += (layerBridge[0][xLocationNext][yLocation][xLocation] * x.output) 
                    counter += 1
            sum /= counter
            self.output[xLocationNext] = sum 

    def solveMap(self, map: list, maxSteps: int) -> int:
        startLocation = (-1, -1) # marked as y, x
        currentLocation = [-1, -1]
        endLocation = (-1, -1)
        numericalMap = []

        for ylocation, y in enumerate(map):
            numericalMapLine = []
            for xlocation, x in enumerate(y):
                if x == "s":
                    startLocation = (ylocation, xlocation)
                    currentLocation = [ylocation, xlocation]
                    numericalMapLine.append(1) # Startpoint, currently not necessary
                elif x == "e":
                    endLocation = (ylocation, xlocation)
                    numericalMapLine.append(2) #End point
                elif x == "b":
                    numericalMapLine.append(3)  #Block
                elif x == "t":
                    numericalMapLine.append(4) #Triangle
                elif x == " ":
                    numericalMapLine.append(0) #empty
            if len(numericalMapLine) >= 1:
                numericalMap.append(numericalMapLine.copy())
        if startLocation == (-1, -1) or endLocation == (-1, -1):
            return maxSteps+1 # in case of training 
        
        numericalMap[currentLocation[0]][currentLocation[1]] = 7 #player
        solid = ['b', 't']

        while currentLocation != endLocation and self.steps <= maxSteps:
            
            print(currentLocation)
            self.decide(numericalMap)
            try:
                match self.output.index(max(self.output)):
                    case 0: # "left"
                        if map[currentLocation[0]][currentLocation[1]-1] not in solid and currentLocation[1]-1 >= 0:
                            numericalMap[currentLocation[0]][currentLocation[1]] = 0
                            currentLocation[1] += -1
                            numericalMap[currentLocation[0]][currentLocation[1]] = 7
                    case 1: # "up"
                        if map[currentLocation[0]-1][currentLocation[1]] not in solid and currentLocation[0]-1 >= 0:
                            numericalMap[currentLocation[0]][currentLocation[1]] = 0
                            currentLocation[0] += -1
                            numericalMap[currentLocation[0]][currentLocation[1]] = 7
                    case 2: # "right"
                        if map[currentLocation[0]][currentLocation[1]+1] not in solid and currentLocation[1]+1 < len(map[0]):
                            numericalMap[currentLocation[0]][currentLocation[1]] = 0
                            currentLocation[1] += 1
                            numericalMap[currentLocation[0]][currentLocation[1]] = 7
                    case 3: # "down"
                        if map[currentLocation[0]+1][currentLocation[1]] not in solid and currentLocation[0]+1 < len(map):
                            numericalMap[currentLocation[0]][currentLocation[1]] = 0
                            currentLocation[0] += 1
                            numericalMap[currentLocation[0]][currentLocation[1]] = 7
                    case 4: # "nothing"
                        pass
                    case _: # "nothing"
                        pass
            except IndexError: # AI is trying to get out of bounds
                pass
            self.steps += 1

        return self.steps
    
