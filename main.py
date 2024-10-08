import AIrandom, selfAIRunner, mapSolverRunner, improvedAIRunner, AdversarialTraining
import game
import os



def numberParser(mapSize: str) -> list:
    listOfNumbers = []
    state = 0
    for character in mapSize:
        try:
            number = int(character)
            if state % 2 == 0:
                state += 1
                listOfNumbers.append(0)
            listOfNumbers[-1] = listOfNumbers[-1]*10 + number
        except:
            if state % 2 == 1:
                state += 1

    return listOfNumbers

def mainLoop():
    main = True
    while main:

        print("\n1) Run AI\n2) Play Game\n3) Make an AI\n4) Train AI\n5) Adversarial training\n6) Exit")
        userInput = input("What shall we do? ")

        match userInput:
            case "1": # run AI !lacks behind due to not beign important!
                print("\n1) Random AI\n2) Self Made AI \n3) Improved AI")
                userInput = input("Which AI? ")
                mapSizeInput = input("How big map would you like? give x and y cordinates:")
                mapSize = numberParser(mapSizeInput)
                match userInput:
                    case "1":
                        AIrandom.run(mapSize)
                    case "2":
                        listOfAIs = os.listdir("selfAI/")
                        print("\nAvailable AIs: ")
                        for AIFromList in listOfAIs:
                            print(AIFromList)
                        selectedAI = input("Which AI (without '.txt')? ")
                        mode = numberParser(input("In which difficulty will the map be? 1) easy, 2) medium, 3) hard "))
                        selfAIRunner.run(mapSize, savedAI = selectedAI, mode = mode[0])

                            
                    case "3":
                        listOfAIs = os.listdir("improvedAI/")
                        print("\nAvailable AIs: ")
                        for AIFromList in listOfAIs:
                            print(AIFromList)
                        selectedAI = input("Which AI (without '.txt')? ")
                        mode = numberParser(input("In which difficulty will the map be? 1) easy, 2) medium, 3) hard "))
                        improvedAIRunner.run(mapSize, savedAI = selectedAI, mode = mode[0])

            case "2": #play game
                listOfMaps = os.listdir("map/")
                print("\nAvailable maps: ")
                listOfMaps.sort()
                for map in listOfMaps:
                    if "txt" in map:
                        print(map)

                userInput = input("Which map (without '.txt')? ")
                game.start()
                game.gameLoop(userInput)
                game.end()
            case "3": #Make AI
                userInput = input("Which type of AI? 1) MapMaker v1 (selfAI), 2) MapSolverAI, 3) improved map AI ")
                match userInput:
                    case "1":
                        userInput = input("Do you want to configure the new AI? (default 10x10 layer, 5 layers) ")
                        AISize = (10, 5)
                        if "y" in userInput.lower():
                            userInput = input("How many nodes per layer and how many layers? ")
                            AISize = numberParser(userInput)
                        newAI = selfAIRunner.makeAI(AISize[0], AISize[1])
                        selfAIRunner.saveAI(newAI)
                    case "2":
                        userInput = input("Do you want to configure the new AI? (default 10x10 layer, 2 layers) ")
                        AISize = (10, 2)
                        if "y" in userInput.lower():
                            userInput = input("How many nodes per layer and how many layers? ")
                            AISize = numberParser(userInput)
                        newAI = mapSolverRunner.makeAI(AISize[0], AISize[1])
                        mapSolverRunner.saveAI(newAI)
                    case "3":
                        userInput = input("Do you want to configure the new AI? (default 10x10 layer, 2 layers) ")
                        AISize = (10, 2)
                        if "y" in userInput.lower():
                            userInput = input("How many nodes per layer and how many layers? ")
                            AISize = numberParser(userInput)
                        newAI = improvedAIRunner.makeAI(AISize[0], AISize[1])
                        improvedAIRunner.saveAI(newAI)

            case "4": # Train AI
                userInput = input("Which type of AI? 1) MapMaker v1 (selfAI), 2) MapSolverAI, 3) improved map AI ")
                match userInput:
                    case "1":
                        listOfAIs = os.listdir("selfAI/")
                    case "2":
                        listOfAIs = os.listdir("mapSolverAI/")
                    case "3":
                        listOfAIs = os.listdir("improvedAI/")
                print("\nAvailable AIs: ")
                listOfAIs.sort()
                for AIFromList in listOfAIs:
                    if "txt" in AIFromList:
                        print(AIFromList)
                selectedAI = input("Which AI (without '.txt')? ")
                lapsStr = input("How much would you like to train this AI? ")
                laps = numberParser(lapsStr)
                match userInput:
                    case "1":
                        mode = numberParser(input("In which mode you want to train the AI? 1) fixed, 2) changing difficulty, 3) with map solver, 4) mixed "))
                        print("Starting training with mode", mode[0],"\n")
                        selfAIRunner.trainAI(laps[0], selectedAI, mode[0])
                    case "2":
                        print("Starting training\n")
                        mapSolverRunner.trainAI(laps[0], selectedAI)
                    case "3":
                        mode = numberParser(input("In which mode you want to train the AI? 1) fixed, 2) changing difficulty, 3) with map solver, 4) mixed "))
                        print("Starting training with mode", mode[0],"\n")
                        improvedAIRunner.trainAI(laps[0], selectedAI, mode[0])
            case "5":
                MapAIType = input("Which type of Map maker AI? 1) MapMaker v1 (selfAI), 2) improved map AI ")
                match MapAIType:
                    case "1":
                        listOfAIs = os.listdir("selfAI/")
                    case "2":
                        listOfAIs = os.listdir("improvedAI/")
                print("\nAvailable AIs: ")
                listOfAIs.sort()
                for AIFromList in listOfAIs:
                    if "txt" in AIFromList:
                        print(AIFromList)
                selectedAI1 = input("Which AI (without '.txt')? ")
                listOfAIs = os.listdir("mapSolverAI/")
                print("\nAvailable mapSolver AIs: ")
                listOfAIs.sort()
                for AIFromList in listOfAIs:
                    if "txt" in AIFromList:
                        print(AIFromList)
                selectedAI2 = input("Which AI (without '.txt')? ")
                lapsStr = input("How much would you like to train this AI? ")
                laps = numberParser(lapsStr)
                match MapAIType:
                    case "1":
                        AdversarialTraining.trainSelfAI(selectedAI1, selectedAI2, laps[0])
                    case "2":
                        AdversarialTraining.trainImprovedAI(selectedAI1, selectedAI2, laps[0])

            case "6": #end the program
                main = False  

mainLoop()

print("Kiitos ohjelman käytöstä")
