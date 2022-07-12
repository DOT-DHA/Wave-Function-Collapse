from Cell import *
from Tiles import *
from graphics import *
import random as R
import time


def checkValid(arr, valid):
    for i in range(len(arr)-1, -1, -1):
        element = arr[i]
        found = False
        for j in range(len(valid)):
            for k in range(len(valid[j])):
                if valid[j][k] == element:
                    found = True
                    break
            if found:
                break
        
        if not found:
            arr.pop(i)

def startOver():
    for i in range(size * size):
        grid[i] = Cell(len(tiles))


if __name__ == "__main__":
    size = 4
    DIM = size * 128
    win = GraphWin("Wave Function Collapse", DIM, DIM)
    win.setBackground("Black")
    tileImages = []
    tiles = []
    grid = []
    display = []

    file = "StarterTiles/"
    for i in range(6):
        tileImages.append(Image(Point(64, 64), file + str(i) + ".png")) #DIM/size*i + DIM/(size*2), 64
    
    tiles.append(Tile(tileImages[0], [0, 0, 0, 0]))
    tiles.append(Tile(tileImages[1], [1, 0, 0, 0]))
    tiles.append(Tile(tileImages[2], [1, 1, 0, 0]))
    tiles.append(Tile(tileImages[3], [1, 0, 1, 0]))
    tiles.append(Tile(tileImages[4], [1, 1, 1, 0]))
    tiles.append(Tile(tileImages[5], [1, 1, 1, 1]))


    #for i in range(6):
    #    for j in range(1, 5):
    #        tiles.append(tiles[i].rotate(j))

    for tile in tiles:
        tile.analyze(tiles)

    for i in range(size*size):
        grid.append(Cell(len(tiles)))
        display.append(False)

    grid[2].options = [1, 3, 5]


    while True:

        for j in range(size):
            for i in range(size):
                cell = grid[i + j * size]
                if cell.collapsed:
                    index = cell.options[0]
                    if display[i + j * size]:
                        continue
                    img = tiles[index].img.clone()
                    imgX = img.getAnchor().getX()
                    imgY = img.getAnchor().getY()
                    img.move(i * 128 + 64 - imgX, j * 128 + 64 - imgY)
                    img.draw(win)
                    display[i + j * size] = True

        #creating copy of array
        gridCopy = list(filter(lambda x : not x.collapsed, grid))

        if len(gridCopy) == 0:
            break

        
        gridCopy = sorted(gridCopy, key = lambda x: len(x.options))

        smallest = len(gridCopy[0].options)

        #random starting tile
        cell = R.choice(list(filter(lambda x: len(x.options) == smallest, gridCopy)))
        cell.collapsed = True
        if len(cell.options) == 0:
            startOver()
            continue
        pick = R.choice(cell.options)

        cell.options = [pick]


        nextGrid = [0] * (size*size)
        for j in range(size):
            for i in range(size):
                index = i + j * size
                if grid[index].collapsed:
                    nextGrid[index] = grid[index]
                else:
                    #Check North
                    options = list(map(lambda x: x, range(len(tiles))))
                    if (j > 0):
                        north = grid[i + (j-1) * size]
                        validOptions = []
                        for option in north.options:
                            valid = tiles[option].south
                            validOptions.append(valid)
                        checkValid(options, validOptions)

                    #Check East
                    if (i > size - 1):
                        east = grid[i + (j-1) * size]
                        validOptions = []
                        for option in east.options:
                            valid = tiles[option].west
                            validOptions.append(valid)
                        checkValid(options, validOptions)

                    #Check South
                    if (j < size - 1):
                        south = grid[i + (j-1) * size]
                        validOptions = []
                        for option in south.options:
                            valid = tiles[option].north
                            validOptions.append(valid)
                        checkValid(options, validOptions)

                    #Check West
                    if (i > 0):
                        west = grid[i + (j-1) * size]
                        validOptions = []
                        for option in west.options:
                            valid = tiles[option].east
                            validOptions.append(valid)
                        checkValid(options, validOptions)

                    nextGrid[index] = Cell(options)

        grid = nextGrid[:]

        time.sleep(.1)

    
    message = Text(Point(DIM/2, DIM/2), "Click to close")
    message.setTextColor("Black")
    message.setSize(18)
    message.draw(win)
    win.getMouse()