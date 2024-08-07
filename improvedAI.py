import random
from node import *

class improvedAI():
    def __init__(self):
        self.input = []
        self.layers = [] 
        self.bridges = []   
        self.output = []
        self.networkLayerSize = 0
        self.learnRate = 0.04

    def copy(self, *_): #returns improvedAI object 
        copiedAI = improvedAI()

        for z in range(len(self.layers)):
            layerMatrix = []
            for y in range(self.networkLayerSize):
                layerLine = []
                for x in range(self.networkLayerSize):
                    layerLine.append(self.layers[z][y][x].copy())
                layerMatrix.append(layerLine.copy())
            copiedAI.layers.append(layerMatrix.copy())

        for z in range(len(self.bridges)):
            bridgeCube = []
            for y in range(len(self.bridges[0])):
                bridgeMatrix = []
                for x in range(len(self.bridges[0][0])):
                    bridgeLine = []
                    for fourth in range(len(self.bridges[0][0][0])):
                        bridgeLine.append(self.bridges[z][y][x][fourth].copy())
                    bridgeMatrix.append(bridgeLine.copy())
                bridgeCube.append(bridgeMatrix.copy())
            copiedAI.bridges.append(bridgeCube.copy())

        copiedAI.networkLayerSize = self.networkLayerSize
        
        return copiedAI


    def makeNewRandomNetwork(self, layerSize: int, layerAmount: int):
        for _ in range(layerAmount):
            layer = []
            for z in range(layerSize):
                layerLine = []
                for y in range(layerSize):
                    layerLine.append(node(random.random()/8))
                layer.append(layerLine.copy())
            self.layers.append(layer.copy())
        
        for _ in range(layerAmount+1):
            bridge = []
            for z in range(layerSize+1):
                bridgeCube = []
                for y in range(layerSize+1):
                    bridgeMatrix = []
                    for x in range(layerSize+1): # bridge to each other node in the next tier
                        bridgeLine = []
                        for fourthDimension in range(layerSize+1): #Legendary fifth for loop in row
                            bridgeLine.append(random.random()/4)
                        bridgeMatrix.append(bridgeLine.copy())
                    bridgeCube.append(bridgeMatrix.copy())
                bridge.append(bridgeCube.copy())
            self.bridges.append(bridge)

        self.networkLayerSize = layerSize
            

    def produceMap(self, mapSize: tuple, map: list = None, difficulty: int = 1) -> list:
        self.input = [difficulty]
        if mapSize[0] > self.networkLayerSize or mapSize[1] > self.networkLayerSize:
            print("Too small network\nNetwork size:", str(self.networkLayerSize), "\nAsked map size:", mapSize, "\nMap's size should be at maxium the networks size")
            return None
        
        if map == None:
            map = self.mapStartingPosition(mapSize)

        self.output = []
        for line in map: # this is to make deep copy of the map
            self.output.append(line.copy())

        self.runNetwork(map, mapSize)

        return self.output
    
    def mapStartingPosition(self, mapSize: tuple) -> list: #making base for the map. Randomizing start makes output to be unique 
        map = []
        for y in range(mapSize[1]):
            line = []
            for x in range(mapSize[0]):
                line.append(random.random())
            map.append(line.copy())
        return map
    
    def runNetwork(self, map: list, mapSize: tuple):   
        self.calculateInputToTier(map.copy(), self.layers[0], self.bridges[0])
        for layer in range(len(self.layers)-1):
            self.calculateNextTier(self.layers[layer], self.layers[layer + 1], self.bridges[layer+1])
        self.calculateOutput(mapSize)


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

    def calculateInputToTier(self, previousTier: list, nextTier: list, layerBridge: list):
        previousTier.append(self.input)
        for yLocationNext, yNext in enumerate(nextTier):
            for xLocationNext, xNext in enumerate(yNext):
                xNext.output = 0
                sum = 0
                counter = 0
                for yLocation, y in enumerate(previousTier):
                    for xLocation, x in enumerate(y):
                        sum += (layerBridge[yLocationNext][xLocationNext][yLocation][xLocation] * x) 
                        counter += 1
                sum /= counter
                if sum >= xNext.bias:
                    xNext.output = sum - xNext.bias
    
    def calculateOutput(self, mapSize):
        self.output = []
        for y in range(mapSize[0]):
            line = []
            for x in range(mapSize[1]):
                line.append(self.layers[-1][y][x].bias)
            self.output.append(line)


    def mutate(self):
        layersLength = len(self.layers)-1
        layerLength = len(self.layers[0][0])-1
        bridgesLength = len(self.bridges)-1
        bridgeLength = len(self.bridges[0])-1

        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])


        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        randomizisedBridge4 = random.randint(0, bridgeLength)
        randomizisedBridge5 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3][randomizisedBridge4][randomizisedBridge5] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        randomizisedBridge4 = random.randint(0, bridgeLength)
        randomizisedBridge5 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3][randomizisedBridge4][randomizisedBridge5] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        randomizisedBridge4 = random.randint(0, bridgeLength)
        randomizisedBridge5 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3][randomizisedBridge4][randomizisedBridge5] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        randomizisedBridge4 = random.randint(0, bridgeLength)
        randomizisedBridge5 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3][randomizisedBridge4][randomizisedBridge5] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        randomizisedBridge4 = random.randint(0, bridgeLength)
        randomizisedBridge5 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3][randomizisedBridge4][randomizisedBridge5] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        randomizisedBridge4 = random.randint(0, bridgeLength)
        randomizisedBridge5 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3][randomizisedBridge4][randomizisedBridge5] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

