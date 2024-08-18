import selfAI, improvedAI, mapSolverAI
import selfAIRunner, improvedAIRunner, mapSolverRunner
import rewardMapSolver, rewardV2
import random, os

def trainSelfAI(mapMakerAI: str, mapSolverAI: str, laps: int):
    currentMapAI = None
    currentSolverAI = None
    train = True
    try: 
        currentMapAI = selfAIRunner.loadAI(mapMakerAI)
    except: 
        print("No valid Map AI given")
        train = False
    try: 
        currentSolverAI = mapSolverRunner.loadAI(mapSolverAI)
    except: 
        print("No valid Solver AI given")
        train = False
    if not train:
        return
    
    solverAIList = [] #expanding scope
    mapAIList = []
    rerun = 0 #needs a value before loop
    ogLearnRate = 0.005
    learnRate = ogLearnRate
    for times in range(laps):

        solverAIList = []
        bestMapAIs = []
        
        currentBestSolver = -1
        maxSteps = 15
        bestSteps = maxSteps +3

        bestSolvers = []
        mapAIList = []
        mapList = []
        difficulty = random.randint(1, 3)  
        baseMap = currentMapAI.mapStartingPosition((currentMapAI.networkLayerSize, currentMapAI.networkLayerSize ))    
        numberOfBestAI = -1
        for _ in range(10):
            bestMapAIs.append([-1000, -1, []])

        reward = -1000

        for _ in range(100): 
            solverAI = currentSolverAI.copy()
            solverAI.learnRate = learnRate
            solverAI.mutate()
            solverAIList.append(solverAI)

        for _ in range(100): 
            mapAIList.append(currentMapAI.copy())
        

        for number, AI in enumerate(mapAIList):
            AI.mutate()
            AI.input = [difficulty] 
            producedMap = selfAIRunner.outputToObjects(AI.produceMap((AI.networkLayerSize -1, AI.networkLayerSize -1), baseMap), True)
            mapList.append(producedMap)
            reward = rewardV2.chooseRewardStructure(producedMap, difficulty)
            if reward < bestMapAIs[-1][0]:
                continue
            if reward > bestMapAIs[-1][0]:
                bestMapAIs.append([reward, number, producedMap])
                bestMapAIs.sort(key=lambda list: list[0], reverse=True)
                bestMapAIs.pop()
            
        reward = -1000
        for index, pack in enumerate(bestMapAIs):
            if pack[0] != -100:
                producedMap = pack[2]
                steps, bestSolverAI = mapSolverTime(producedMap, solverAIList, maxSteps)
                bestMapAIs[index][0] -= steps*2
                if bestMapAIs[index][0] > reward:
                    numberOfBestAI = pack[1]
                if bestSteps > steps:
                    bestSteps = steps
                bestSolvers.append(bestSolverAI.copy())



        if numberOfBestAI != -1:
            currentMapAI = mapAIList[numberOfBestAI].copy()
        selfAIRunner.writeFile(mapList[numberOfBestAI], True, mapMakerAI)

        if len(bestSolvers) == 1:
            mapSolverRunner.writeFile(bestSolvers[0], baseMap, True, mapSolverAI)
            currentSolverAI = bestSolvers[0].copy()
            rerun = 0
        else: 
            currentBestSolver = -1
            currentReward = -1000
            for number, solverAI in enumerate(bestSolvers):
                reward = rewardMapSolver.rewardPath(solverAI)
                if reward > currentReward:
                    currentBestSolver = number
                    currentReward = reward 
            if currentBestSolver != -1:
                mapSolverRunner.writeFile(bestSolvers[currentBestSolver], baseMap, True, mapSolverAI)
                currentSolverAI = bestSolvers[currentBestSolver].copy()
            if bestSteps >= maxSteps + 1: # if bad evolution (no success with map) was made, increasing the learnrate to initiate a evolution easier
                learnRate = ogLearnRate + (ogLearnRate/2 * rerun)
                rerun += 1
                if rerun == 50:
                    rerun = 0
            else:
                learnRate = ogLearnRate
                rerun = 0
        #writeFile(bestMapAIs) Easy way to log information for debugging
        if (times+1) % 10 == 0: selfAIRunner.saveAI(currentMapAI, mapMakerAI)
        if (times+1) % 10 == 0: mapSolverRunner.saveAI(currentSolverAI, mapSolverAI)

        mapSolverRunner.progressBar(times, laps)
    selfAIRunner.saveAI(currentMapAI, mapMakerAI)
    mapSolverRunner.saveAI(currentSolverAI, mapSolverAI)



def trainImprovedAI(mapMakerAI: improvedAI, mapSolverAI: mapSolverAI, laps: int):
    currentMapAI = None
    currentSolverAI = None
    train = True
    try: 
        currentMapAI = improvedAIRunner.loadAI(mapMakerAI)
    except: 
        print("No valid Map AI given")
        train = False
    try: 
        currentSolverAI = mapSolverRunner.loadAI(mapSolverAI)
    except: 
        print("No valid Solver AI given")
        train = False
    if not train:
        return
    
    solverAIList = [] #expanding scope
    mapAIList = []
    rerun = 0 #needs a value before loop
    ogLearnRate = 0.005
    learnRate = ogLearnRate
    for times in range(laps):

        solverAIList = []
        bestMapAIs = []
        
        currentBestSolver = -1
        maxSteps = 15
        bestSteps = maxSteps +3

        bestSolvers = []
        mapAIList = []
        mapList = []
        difficulty = random.randint(1, 3)  
        baseMap = currentMapAI.mapStartingPosition((currentMapAI.networkLayerSize, currentMapAI.networkLayerSize ))    
        numberOfBestAI = -1
        for _ in range(10):
            bestMapAIs.append([-1000, -1, []])

        reward = -1000

        for _ in range(100): 
            solverAI = currentSolverAI.copy()
            solverAI.learnRate = learnRate
            solverAI.mutate()
            solverAIList.append(solverAI)

        for _ in range(100): 
            mapAIList.append(currentMapAI.copy())
        

        for number, AI in enumerate(mapAIList):
            AI.mutate()
            AI.input = [difficulty] 
            producedMap = improvedAIRunner.outputToObjects(AI.produceMap((AI.networkLayerSize -1, AI.networkLayerSize -1), baseMap), True)
            mapList.append(producedMap)
            reward = rewardV2.chooseRewardStructure(producedMap, difficulty)
            if reward < bestMapAIs[-1][0]:
                continue
            if reward > bestMapAIs[-1][0]:
                bestMapAIs.append([reward, number, producedMap])
                bestMapAIs.sort(key=lambda list: list[0], reverse=True)
                bestMapAIs.pop()
            
        reward = -1000
        for index, pack in enumerate(bestMapAIs):
            if pack[0] != -100:
                producedMap = pack[2]
                steps, bestSolverAI = mapSolverTime(producedMap, solverAIList, maxSteps)
                bestMapAIs[index][0] -= steps*2
                if bestMapAIs[index][0] > reward:
                    numberOfBestAI = pack[1]
                if bestSteps > steps:
                    bestSteps = steps
                bestSolvers.append(bestSolverAI.copy())



        if numberOfBestAI != -1:
            currentMapAI = mapAIList[numberOfBestAI].copy()
        improvedAIRunner.writeFile(mapList[numberOfBestAI], True, mapMakerAI)

        if len(bestSolvers) == 1:
            mapSolverRunner.writeFile(bestSolvers[0], baseMap, True, mapSolverAI)
            currentSolverAI = bestSolvers[0].copy()
            rerun = 0
        else: 
            currentBestSolver = -1
            currentReward = -1000
            for number, solverAI in enumerate(bestSolvers):
                reward = rewardMapSolver.rewardPath(solverAI)
                if reward > currentReward:
                    currentBestSolver = number
                    currentReward = reward 
            if currentBestSolver != -1:
                mapSolverRunner.writeFile(bestSolvers[currentBestSolver], baseMap, True, mapSolverAI)
                currentSolverAI = bestSolvers[currentBestSolver].copy()
            if bestSteps >= maxSteps + 1: # if bad evolution (no success with map) was made, increasing the learnrate to initiate a evolution easier
                learnRate = ogLearnRate + (ogLearnRate/2 * rerun)
                rerun += 1
                if rerun == 50:
                    rerun = 0
            else:
                learnRate = ogLearnRate
                rerun = 0
        #writeFile(bestMapAIs) Easy way to log information for debugging
        if (times+1) % 10 == 0: improvedAIRunner.saveAI(currentMapAI, mapMakerAI)
        if (times+1) % 10 == 0: mapSolverRunner.saveAI(currentSolverAI, mapSolverAI)

        mapSolverRunner.progressBar(times, laps)
    improvedAIRunner.saveAI(currentMapAI, mapMakerAI)
    mapSolverRunner.saveAI(currentSolverAI, mapSolverAI)

def mapSolverTime(map: list, solverList: list, maxSteps: int) -> list:
    bestSolverAIs = []
    currentBest = -1
    numberOfBestAI = -1
    bestAI = maxSteps + 3

    numericalMap, startLocation, currentLocation, endLocation = solverList[0].defineNumericalMap(map)
    for number, AI in enumerate(solverList):
        steps = AI.solveMap(map, maxSteps, numericalMap, locationPackage = [startLocation, currentLocation, endLocation])

        if steps < bestAI and steps != 0:
            bestAI = steps
            numberOfBestAI = number
            bestSolverAIs = [number]
        elif steps == bestAI and steps != 0:
            bestSolverAIs.append(number)

    if len(bestSolverAIs) == 1:
        currentAI = solverList[numberOfBestAI].copy()
    else: 
        currentBest = -1
        currentReward = -1000
        for x in bestSolverAIs:
            reward = rewardMapSolver.rewardPath(solverList[x])
            if reward > currentReward:
                currentBest = x
                currentReward = reward 
        #if currentBest != -1: #forcing to return a solver AI, otherwise program breaks and this scenario is so rare it shouldn't make difference 
        currentAI = solverList[currentBest].copy() 

        
    return bestAI, currentAI


def writeFile(information: list):
    try:
        os.mkdir("adversarialLogs")
    except FileExistsError:
        pass

    try:
        file = open("adversarialLogs/log.txt", "at")
        for pack in information:
            file.write(str(pack[0]))
            file.write(str(" "))
            file.write(str(id(pack[0])))
            file.write(str(" "))
            file.write(str(pack[1]))
            file.write(str(" "))
            file.write(str(id(pack[1])))
            file.write(str(" "))
            file.write(str(pack[2]))
            file.write(str(" "))
            file.write(str(id(pack[2])))
            file.write(str(" "))
            file.write("\n") 
        file.write(str(" "))
        file.write("\n")   
        file.close()
    except:
        pass
    