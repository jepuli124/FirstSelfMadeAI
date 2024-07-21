import AIrandom, selfAIRunner, mapSolverRunner
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

        print("\n1) Run AI\n2) Play Game\n3) Make an AI\n4) Train AI\n5) Exit")
        userInput = input("What shall we do? ")

        match userInput:
            case "1":
                print("\n1) Random AI\n2) Self Made AI \n3) Torch AI")
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
                        selfAIRunner.run(mapSize, savedAI = selectedAI)

                            
                    case "3":
                        pass
                        #AITorch.run(mapSize)

            case "2":
                listOfMaps = os.listdir("map/")
                print("\nAvailable maps: ")
                listOfMaps.sort()
                for map in listOfMaps:
                    print(map)

                userInput = input("Which map (without '.txt')? ")
                game.start()
                game.gameLoop(userInput)
                game.end()
            case "3":
                userInput = input("Which type of AI? 1) MapMaker v1 (selfAI), 2) MapSolverAI ")
                match userInput:
                    case "1":
                        userInput = input("Do you want to configure the new AI? ")
                        AISize = (10, 5)
                        if "y" in userInput.lower():
                            userInput = input("How many nodes per layer and how many layers? ")
                            AISize = numberParser(userInput)
                        newAI = selfAIRunner.makeAI(AISize[0], AISize[1])
                        selfAIRunner.saveAI(newAI)
                    case "2":
                        userInput = input("Do you want to configure the new AI? ")
                        AISize = (10, 2)
                        if "y" in userInput.lower():
                            userInput = input("How many nodes per layer and how many layers? ")
                            AISize = numberParser(userInput)
                        newAI = mapSolverRunner.makeAI(AISize[0], AISize[1])
                        mapSolverRunner.saveAI(newAI)

            case "4":
                userInput = input("Which type of AI? 1) MapMaker v1 (selfAI), 2) MapSolverAI ")
                match userInput:
                    case "1":
                        listOfAIs = os.listdir("selfAI/")
                    case "2":
                        listOfAIs = os.listdir("mapSolverAI/")
                print("\nAvailable AIs: ")
                listOfAIs.sort()
                for AIFromList in listOfAIs:
                    print(AIFromList)
                selectedAI = input("Which AI (without '.txt')? ")
                lapsStr = input("How much would you like to train this AI? ")
                laps = numberParser(lapsStr)
                print("Starting training\n")
                match userInput:
                    case "1":
                        selfAIRunner.trainAI(laps[0], selectedAI)
                    case "2":
                        mapSolverRunner.trainAI(laps[0], selectedAI)

            case "5":
                main = False  

mainLoop()

print("Kiitos ohjelman käytöstä")
