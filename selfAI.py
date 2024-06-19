import random
from node import *

class selfAI():
    def __init__(self):
        self.input = []
        self.layers = [] 
        self.bridges = []   
        self.output = []
        self.networkLayerSize = 0
        self.learnRate = 0.10

    def makeNewRandomNetwork(self, layerSize: list, layerAmount: list):
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


        cube = [] # making last bridge as 3d tensor
        for z in range(layerSize):
            side = []
            for y in range(layerSize): 
                line = []
                for z in range(layerSize): 
                    line.append(random.random())
                side.append(line.copy()) 
            cube.append(side.copy())
        self.bridges[-1] = (cube.copy())
            
        self.networkLayerSize = layerSize
            

    def produceMap(self, mapSize: tuple) -> list:
        if mapSize[0] > self.networkLayerSize or mapSize[1] > self.networkLayerSize:
            print("Too small network\nNetwork size:", str(self.networkLayerSize), "\nAsked map size:", mapSize, "\nMap's size should be at maxium the networks size")
            return None
        
        map = [] #making base for the map. Randomizing start makes output to be unique 
        for y in range(mapSize[1]):
            line = []
            for x in range(mapSize[0]):
                line.append(random.random())
            map.append(line.copy())

        self.output = map.copy()
        self.runNetwork(map, mapSize)

        return self.output
    
    def runNetwork(self, map: list, mapSize: tuple):
        self.input = map   
        self.calculateInputToTier(self.input, self.layers[0])
        for layer in range(len(self.layers)-1):
            self.calculateNextTier(self.layers[layer], self.layers[layer + 1], self.bridges[layer])
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

    def calculateInputToTier(self, previousTier: list, nextTier: list):
        for x in nextTier:
            x.output = 0
            sum = 0
            counter = 0
            for line in previousTier:
                for y in line:
                    sum += y
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
        bridgesLength = len(self.bridges)-2 # 2: because last bridge is a special tensor
        bridgeLength = len(self.bridges[0])-1
        
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.layers[random.randint(0, layersLength)][random.randint(0, layerLength)].bias += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])

        try:
            self.bridges[random.randint(0, bridgesLength)][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
            self.bridges[random.randint(0, bridgesLength)][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
            self.bridges[random.randint(0, bridgesLength)][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        except:
            print(layersLength, layerLength, bridgesLength, bridgeLength)

        self.bridges[-1][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.bridges[-1][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])
        self.bridges[-1][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)][random.randint(0, bridgeLength)] += random.choice([-self.learnRate, -self.learnRate/2, self.learnRate/2, self.learnRate])