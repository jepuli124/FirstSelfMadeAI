import random
from node import *

class selfAI():
    def __init__(self):
        self.input = []
        self.layers = [] 
        self.bridges = []   
        self.output = []
        self.networkLayerSize = 0
        self.learnRate = 0.05

    def copy(self, *_): # returns selfAI type object.
        copiedAI = selfAI()

        for z in range(len(self.layers)):
            layer = []
            bridge = []
            for y in range(self.networkLayerSize):
                layer.append(self.layers[z][y].copy())
                bridge.append(self.bridges[z][y].copy())
            copiedAI.layers.append(layer.copy())
            copiedAI.bridges.append(bridge.copy())

        for tensor in range(2):
            cube = [] # making last bridge as 3d tensor
            for z in range(len(self.bridges[-2+tensor])):
                side = []
                for y in range(len(self.bridges[-2+tensor])): 
                    line = []
                    for x in range(len(self.bridges[-2+tensor])): 
                        line.append(self.bridges[-2+tensor][z][x][y])
                    side.append(line.copy()) 
                cube.append(side.copy())
            copiedAI.bridges.append(cube.copy())

        copiedAI.networkLayerSize = self.networkLayerSize
        
        return copiedAI


    def makeNewRandomNetwork(self, layerSize: int, layerAmount: int):
        for _ in range(layerAmount):
            layer = []
            bridge = []
            for y in range(layerSize):
                layer.append(node(random.random()/2))
                bridgeLine = []
                for x in range(layerSize): # bridge to each other node in the next tier
                    bridgeLine.append(random.random()*2)
                bridge.append(bridgeLine.copy())
            self.layers.append(layer.copy())
            self.bridges.append(bridge)

        for _ in range(2):
            cube = [] # making last bridge as 3d tensor
            for z in range(layerSize+1):
                side = []
                for y in range(layerSize+1): 
                    line = []
                    for x in range(layerSize+1): 
                        line.append(random.random())
                    side.append(line.copy()) 
                cube.append(side.copy())
            self.bridges.append(cube.copy())
            
        self.networkLayerSize = layerSize
            

    def produceMap(self, mapSize: tuple, map: list = None) -> list:
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
        self.calculateInputToTier(map.copy(), self.layers[0], self.bridges[-2])
        for layer in range(len(self.layers)-1):
            self.calculateNextTier(self.layers[layer], self.layers[layer + 1], self.bridges[layer+1])
        self.calculateLastTierToOutput(self.layers[-1], self.output, self.bridges[-1], mapSize)


    def calculateNextTier(self, previousTier: list, nextTier: list, layerBridge: list):
        for xLocation, x in enumerate(nextTier):
            x.output = 0
            sum = 0
            counter = 0
            for yLocation, y in enumerate(previousTier):
                sum += (layerBridge[yLocation][xLocation] * y.output) 
                counter += 1
            sum /= counter
            if sum >= x.bias:
                x.output = sum - x.bias

    def calculateInputToTier(self, previousTier: list, nextTier: list, layerBridge: list):
        previousTier.append(self.input)
        for xLocation, x in enumerate(nextTier):
            x.output = 0
            sum = 0
            counter = 0
            for yLocation, y in enumerate(previousTier):
                for zLocation, z in enumerate(y):
                    sum += (layerBridge[xLocation][yLocation][zLocation]* z) 
                    counter += 1
            sum /= counter
            if sum >= x.bias:
                x.output = 1

    def calculateLastTierToOutput(self, previousTier: list, output: list, layerBridge: list, mapSize: tuple):
        for yOutput in range(mapSize[1]):
            for xOutput in range(mapSize[0]):
                sum = 0
                counter = 0
                for yLocation, y in enumerate(previousTier):
                    sum += (layerBridge[yLocation][yOutput][xOutput] * y.output) 
                    counter += 1
                sum /= counter
                output[yOutput][xOutput] = sum

    def mutate(self):

        layersLength = len(self.layers)-1
        layerLength = len(self.layers[0])-1
        bridgesLength = len(self.bridges)-3 # 2: because last two bridges are special tensors
        bridgeLength = len(self.bridges[0])-1
        
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgesLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        self.bridges[randomizisedBridge1][randomizisedBridge2][randomizisedBridge3] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgeLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        self.bridges[-random.randint(1, 2)][randomizisedBridge1][randomizisedBridge2][randomizisedBridge3] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgeLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        self.bridges[-random.randint(1, 2)][randomizisedBridge1][randomizisedBridge2][randomizisedBridge3] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        randomizisedBridge1 = random.randint(0, bridgeLength)
        randomizisedBridge2 = random.randint(0, bridgeLength)
        randomizisedBridge3 = random.randint(0, bridgeLength)
        self.bridges[-random.randint(1, 2)][randomizisedBridge1][randomizisedBridge2][randomizisedBridge3] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])




