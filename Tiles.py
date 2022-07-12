

class Tile:
    def __init__(self, img, edges):
        self.img = img
        self.edges = edges

        self.north = []
        self.east = []
        self.south = []
        self.west = []


    def analyze(self, tiles):

        for i in range(len(tiles)):
            tile = tiles[i]
            if tile.edges[2] == self.edges[0]:
                self.north.append(i)

            if tile.edges[3] == self.edges[1]:
                self.east.append(i)

            if tile.edges[0] == self.edges[2]:
                self.south.append(i)

            if tile.edges[1] == self.edges[3]:
                self.west.append(i)
