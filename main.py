import AIrandom, AISelf, AITorch
import enviroment
import game
import os



def numberParser(mapSize):
    x, y, state = 0, 0, 0
    for character in mapSize:
        try:
            number = int(character)
            if state % 2 == 0:
                state += 1
            if state == 1:
                x = x * 10 + number
            if state == 3:
                y = y * 10 + number
        except:
            if state % 2 == 1:
                state += 1
            pass
    return (x,y)

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
                        AISelf.run(mapSize)
                    case "3":
                        AITorch.run(mapSize)

            case "2":
                listOfMaps = os.listdir("map/")
                print("\nAvailable maps: ")
                for map in listOfMaps:
                    print(map)

                userInput = input("Which map? ")
                game.start()
                game.gameLoop(userInput)
                game.end()

            case "3":
                main = False  

mainLoop()
