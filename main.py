import AIrandom, selfAIRunner, AITorch
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
            pass
    return listOfNumbers

def mainLoop():
    main = True
    while main:

        print("\n1) Run AI\n2) Play Game\n3) Exit")
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
                        userInput = input("Do you want to use saved AI? ")
                        if "y" in userInput.lower():
                            listOfAIs = os.listdir("selfAI/")
                            print("\nAvailable AIs: ")
                            for AIFromList in listOfAIs:
                                print(AIFromList)
                            selectedAI = input("Which AI (without '.txt')? ")
                            selfAIRunner.run(mapSize, savedAI = selectedAI)
                        else:
                            userInput = input("Do you want to configure the new AI? ")
                            AISize = (10, 5)
                            if "y" in userInput.lower():
                                userInput = input("How many nodes per layer and how many layers? ")
                                AISize = numberParser(userInput)
                            newAI = selfAIRunner.run(mapSize, AISize[0], AISize[1])

                            userInput = input("Do you want to save the new AI? ")
                            if "y" in userInput.lower():
                                selfAIRunner.saveAI(newAI)
                    case "3":
                        AITorch.run(mapSize)

            case "2":
                listOfMaps = os.listdir("map/")
                print("\nAvailable maps: ")
                for map in listOfMaps:
                    print(map)

                userInput = input("Which map (without '.txt')? ")
                game.start()
                game.gameLoop(userInput)
                game.end()

            case "3":
                main = False  

mainLoop()
