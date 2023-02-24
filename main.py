
import os
import time
import style


class Graph:
    mazeSize = int
    start = (int, int)
    end = (int, int)
    adjacList = {}
    explored = {}

    def __init__(self, mazeTextFile):
        self.createAdjList(mazeTextFile)

    # Utility method
    def isWallChar(self, char):
        return char == "#"

    # Utility method
    def isStartChar(self, char):
        return char == "S"

    # Utility method
    def isGoalChar(self, char):
        return char == "G"

    # Utility method
    def isOutOfBounds(self, x, y):
        if x == -1 or y == -1:
            return True
        if x > self.mazeSize - 1 or y > self.mazeSize - 1:
            return True

        return False

    # Utility method
    def fileToStringList(self, mazeTextFile):
        file = open(mazeTextFile, "r")
        data = file.read().split("\n")
        file.close()
        return data

    # Create adjacency list from text file
    def createAdjList(self, mazeTextFile):
        self.data = self.fileToStringList(mazeTextFile)
        self.mazeSize = int(self.data[0])
        self.data.pop(0)
        for x in range(self.mazeSize):
            for y in range(self.mazeSize):
                char = self.data[x][y]
                # Get traversible locations if node is not a wall
                if not self.isWallChar(char):
                    if not self.isOutOfBounds(x-1, y):
                        up = self.data[x-1][y]
                    else:
                        up = " "
                    if not self.isOutOfBounds(x+1, y):
                        down = self.data[x+1][y]
                    else:
                        down = " "
                    if not self.isOutOfBounds(x, y-1):
                        left = self.data[x][y-1]
                    else:
                        left = " "
                    if not self.isOutOfBounds(x, y+1):
                        right = self.data[x][y+1]
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

                # Set start if node encountered is start
                if(self.isStartChar(char)):
                    self.start = (x, y)
                # Set end if node encountered is end
                elif(self.isGoalChar(char)):
                    self.end = (x, y)

    # Utility method
    def getNeighbors(self, coord):
        return self.adjacList[coord]

    # Utility method
    def heuristic(self, coord1):
        return abs(coord1[0] - self.end[0]) + abs(coord1[1] - self.end[1])

    # Returns the most optimal path
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

            # Get lowest cost node in open
            for node in open:
                if n == None or (fCosts[node] < fCosts[n]):
                    n = node



            # Explored
            self.explored[(n[0], n[1])] = (n[0], n[1])

            # Call draw path function
            self.draw()

            if n is None:
                print("No path exists!")
                return None

            # Return optimal path via traversing parent map if end is reached
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




            # Get all neighbors of chosen node
            for neighbor in self.getNeighbors(n):
                # A new node is encountered, calculate f cost and set the parent
                if neighbor not in open and neighbor not in closed:
                    open.add(neighbor)
                    parents[neighbor] = n
                    gCosts[neighbor] = gCosts[parents[neighbor]] + 1
                    fCosts[neighbor] = gCosts[neighbor] + self.heuristic(neighbor)

                # Existing node in open encountered
                elif neighbor in open:
                    # Check if g cost of current is less than the neighbor encountered
                    # This means its cheaper to get there, recalculate the f cost and set a new parent
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

    def draw(self):

        time.sleep(.5)
        os.system('cls' if os.name == 'nt' else 'clear')

        for row in range(self.mazeSize):
            for column in range(self.mazeSize):
                if (row, column) in self.explored and (row, column) != self.start and (row, column) != self.end:
                    print("o", end=" ")
                else:
                    print(self.data[row][column], end=" ")
            print()


# 1. Instantiate graph object
# 2. Set constructor as the name of the file
# 3. Call object.aStarSearch() to return the most optimal path
def main():
    graph = Graph("maze.txt")
    path = graph.aStarSearch()
    pathDisplay = []

    # Display optimal path
    for coord in path:
        pathDisplay.append(coord)
        time.sleep(.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in range(graph.mazeSize):
            for column in range(graph.mazeSize):
                if (row, column) in pathDisplay and (row, column) != graph.start and (row, column) != graph.end:
                    print("%", end=" ")
                elif (row, column) in graph.explored and (row, column) != graph.start and (row, column) != graph.end:
                    print("o", end=" ")
                else:
                    print(graph.data[row][column], end=" ")
            print()

    print()
    print("Length is {}".format(len(path)))

if __name__ == '__main__':
    main()