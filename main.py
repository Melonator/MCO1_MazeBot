# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Graph:
    mazeSize = int
    start = (int, int)
    end = (int, int)
    adjacList = {}

    def __init__(self, mazeTextFile):
        self.createAdjList(mazeTextFile)

    def isWallChar(self, char):
        return char == "#"

    def isStartChar(self, char):
        return char == "S"

    def isGoalChar(self, char):
        return char == "G"

    def isOutOfBounds(self, x, y):
        if x == -1 or y == -1:
            return True
        if x > self.mazeSize - 1 or y > self.mazeSize - 1:
            return True

        return False

    def createAdjList(self, mazeTextFile):
        data = self.fileToStringList(mazeTextFile)
        self.mazeSize = int(data[0][0])
        data.pop(0)
        for x in range(self.mazeSize):
            for y in range(self.mazeSize):
                char = data[x][y]
                if not self.isWallChar(char):
                    if not self.isOutOfBounds(x-1, y):
                        up = data[x-1][y]
                    else:
                        up = " "
                    if not self.isOutOfBounds(x+1, y):
                        down = data[x+1][y]
                    else:
                        down = " "
                    if not self.isOutOfBounds(x, y-1):
                        left = data[x][y-1]
                    else:
                        left = " "
                    if not self.isOutOfBounds(x, y+1):
                        right = data[x][y+1]
                    else:
                        right = " "

                    nodes = [up, down, left, right]

                    nodesCoords = [(x-1,y), (x+1, y),
                                   (x, y-1), (x, y+1)]
                    adjacNodesCoords = []
                    for i in range(len(nodes)):
                        if nodes[i] != " " and self.isWallChar(nodes[i]) is False:
                            adjacNodesCoords.append(nodesCoords[i])

                    self.adjacList[x,y] = adjacNodesCoords
                if(self.isStartChar(char)):
                    self.start = (x, y)
                elif(self.isGoalChar(char)):
                    self.end = (x, y)

    def fileToStringList(self, mazeTextFile):
        file = open(mazeTextFile, "r")
        data = file.read().split("\n")
        file.close()
        return data

    def getNeighbors(self, coord):
        return self.adjacList[coord]

    def heuristic(self, coord1):
        return abs(coord1[0] - self.end[0]) + abs(coord1[1] - self.end[1])

    def aStarSearch(self):
        open = set([self.start])
        closed = set([])

        fCosts = {}
        fCosts[self.start] = 0

        gCosts = {}
        gCosts[self.start] = 0

        #set initial costs
        for neighbor in self.getNeighbors(self.start):
            gCosts[neighbor] = 1

        parents = {}
        parents[self.start] = self.start

        while len(open) > 0:
            n = None

            for node in open:
                if n == None or (fCosts[node] < fCosts[n]):
                    n = node

            if n is None:
                print("No path exists!")
                return None

            if n == self.end:
                optimalPath = []
                print("Goal found!")
                node = self.end
                while node != parents[node]:
                    optimalPath.append(node)
                    node = parents[node]
                optimalPath.append(self.start)
                optimalPath.reverse()
                return optimalPath

            for neighbor in self.getNeighbors(n):
                if neighbor not in open and neighbor not in closed:
                    open.add(neighbor)
                    parents[neighbor] = n
                    gCosts[neighbor] = gCosts[parents[neighbor]] + 1
                    fCosts[neighbor] = gCosts[neighbor] + self.heuristic(neighbor)

                elif neighbor in open:
                    if gCosts[n] < gCosts[neighbor]:
                        fCosts[neighbor] = gCosts[n] + self.heuristic(neighbor)
                        parents[neighbor] = n

                        if neighbor in closed:
                            closed.remove(neighbor)
                            open.add(neighbor)

            open.remove(n)
            closed.add(n)

        print('Path does not exist!')
        return None

if __name__ == '__main__':
    graph = Graph("maze.txt")
    print("Path is {}".format(graph.aStarSearch()))
