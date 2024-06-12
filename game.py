import pygame




def mapDecoder(map):
    returnableMap = [["air"] * map.size[y]] * map.size[x]

    for xnumber, x in enumerate(map):
        for ynumber, y in enumerate(x):
            match y:
                case "b":
                    returnableMap[xnumber][ynumber] = "block"
                case "g":
                    returnableMap[xnumber][ynumber] = "g"
                case "s":
                    returnableMap[xnumber][ynumber] = "s"
                case _:
                    pass

def gameLoop():
    while True:
        pass



