# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mazeGen
import math
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import csv

class Graph:
    mazeSize = int
    start = (int, int)
    end = (int, int)
    adjacList = {}
    statesExplored = 0

    def __init__(self, mazeList):
        self.createAdjList(mazeList)

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

    # Create adjacency list from text file
    def createAdjList(self, mazeList):
        self.mazeSize = len(mazeList)
        for x in range(self.mazeSize):
            for y in range(self.mazeSize):
                char = mazeList[x][y]
                # Get traversible locations if node is not a wall
                if not self.isWallChar(char):
                    if not self.isOutOfBounds(x-1, y):
                        up = mazeList[x-1][y]
                    else:
                        up = " "
                    if not self.isOutOfBounds(x+1, y):
                        down = mazeList[x+1][y]
                    else:
                        down = " "
                    if not self.isOutOfBounds(x, y-1):
                        left = mazeList[x][y-1]
                    else:
                        left = " "
                    if not self.isOutOfBounds(x, y+1):
                        right = mazeList[x][y+1]
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
                elif fCosts[node] == fCosts[n]:
                    if self.heuristic(node) < self.heuristic(n):
                        n = node
            self.statesExplored += 1

            if n is None:
                print("No path exists!")
                return None

            # Return optimal path via traversing parent map if end is reached
            if n == self.end:
                optimalPath = []
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
# 1. Instantiate graph object
# 2. Set constructor as the name of the file
# 3. Call object.aStarSearch() to return the most optimal path

def initStartEnd(maze):
    for column in range(len(maze)):
        if maze[0][column] == '.':
            maze[0][column] = 'S'
        if maze[len(maze) - 1][column] == '.':
            maze[len(maze) - 1][column] = 'G'

def main():
    sumTime = 0
    sumStates = 0
    averageStates = 0
    averageTime = 0
    x = []
    y = []
    testCases = [[0 for x in range(60)] for y in range(50)]

    for n in range(5, 65):
        mg = mazeGen.mazeGenerator()
        mg.mazeSize = n
        x.append(n)
        for i in range(50):
            maze = mg.generateMaze()
            initStartEnd(maze)
            graph = Graph(maze)
            start = timer()
            path = graph.aStarSearch()
            end = timer()
            total = end - start
            testCases[i][n-5] = total
            sumTime += total
            sumStates += graph.statesExplored
            print("time is {}".format(total))
            maze.clear()
        averageTime = sumTime / 50
        averageStates = sumStates / 50
        y.append(averageTime)
        sumTime = 0
        sumStates = 0
        print("Average time for size {} is {}".format(n, averageTime))
        print("Average states explored for size {} is {}".format(n, math.floor(averageStates)))

    plt.plot(x, y, color='g', label="Runtime")

    plt.xticks(rotation=25)
    plt.xlabel('Maze size')
    plt.ylabel('Time')
    plt.title('Average Runtime of A*', fontsize=20)
    plt.grid()
    plt.legend()
    plt.show()

    with open('runtimes.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(testCases)



if __name__ == '__main__':
    main()